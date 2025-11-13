import os
import sys
import yaml
import argparse
from pathlib import Path
from ultralytics import YOLO
from collections import Counter, defaultdict
import importlib.util
from pathlib import Path as _Path

# load translator module directly from backend/utils to avoid import path issues
translator_path = _Path(__file__).resolve().parent / 'utils' / 'braille_translator.py'
if translator_path.exists():
    spec = importlib.util.spec_from_file_location('braille_translator', str(translator_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    braille_to_text = getattr(mod, 'braille_to_text')
else:
    # fallback: simple identity translator
    def braille_to_text(labels):
        return ''.join(labels)


def levenshtein_alignment(a, b):
    # returns distance and aligned sequences with '-' for gaps
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    # backtrace
    i, j = n, m
    ra, rb = [], []
    while i > 0 or j > 0:
        if i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ra.append(a[i - 1]); rb.append('-'); i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            ra.append('-'); rb.append(b[j - 1]); j -= 1
        else:
            ra.append(a[i - 1] if i > 0 else '-')
            rb.append(b[j - 1] if j > 0 else '-')
            i -= 1; j -= 1
    return dp[n][m], ''.join(reversed(ra)), ''.join(reversed(rb))


def normalize_text(s):
    # basic normalization for spanish: lowercase and strip
    return s.strip().lower()


def load_data_yaml(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def read_yolo_label_txt(label_path):
    # returns list of (class_index, x,y,w,h)
    items = []
    if not os.path.exists(label_path):
        return items
    with open(label_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            cls = int(parts[0])
            vals = list(map(float, parts[1:5])) if len(parts) >= 5 else [0,0,0,0]
            items.append((cls, *vals))
    return items


def labels_to_sequence(label_items, names):
    # order by y (center) then x
    boxes = []
    for it in label_items:
        cls = it[0]
        x_center = it[1]
        y_center = it[2]
        boxes.append((y_center, x_center, cls))
    boxes.sort(key=lambda t: (t[0], t[1]))
    # return a list of token strings (don't join here so translator can map tokens)
    seq = [names[c] if c < len(names) else str(c) for (_, _, c) in boxes]
    return seq


def group_boxes_to_lines(boxes, line_tol=0.05):
    """
    boxes: list of (cls, x_center, y_center)
    line_tol: normalized y tolerance to cluster centers into the same line
    returns list of lines, each line is list of (cls, x_center, y_center)
    """
    if not boxes:
        return []
    # sort by y then x
    boxes_sorted = sorted(boxes, key=lambda t: (t[2], t[1]))
    lines = []
    # use running mean of y to decide clustering into the same line
    current_line = [boxes_sorted[0]]
    current_mean_y = boxes_sorted[0][2]
    for b in boxes_sorted[1:]:
        by = b[2]
        # if vertical distance from cluster mean small, same line
        if abs(by - current_mean_y) <= line_tol:
            current_line.append(b)
            # update running mean
            current_mean_y = (current_mean_y * (len(current_line) - 1) + by) / len(current_line)
        else:
            lines.append(sorted(current_line, key=lambda t: t[1]))
            current_line = [b]
            current_mean_y = by
    if current_line:
        lines.append(sorted(current_line, key=lambda t: t[1]))
    return lines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', type=str, required=True)
    parser.add_argument('--data', type=str, default='backend/dataset/dataset7/data.yaml')
    parser.add_argument('--images', type=str, default='backend/dataset/dataset7/valid/images')
    parser.add_argument('--labels', type=str, default='backend/dataset/dataset7/valid/labels')
    parser.add_argument('--conf', type=float, default=0.25)
    parser.add_argument('--line_tol', type=float, default=0.05, help='normalized y tolerance for grouping boxes into lines')
    parser.add_argument('--spell', action='store_true', help='apply simple spellchecker postprocess if available')
    parser.add_argument('--csv', type=str, default=None, help='optional CSV path to save per-image tokenized GT and predictions')
    parser.add_argument('--save', type=str, default='runs/eval_translation_report.txt')
    args = parser.parse_args()

    data_cfg = load_data_yaml(args.data)
    names = data_cfg.get('names', None) or []

    model = YOLO(args.checkpoint)

    images_dir = Path(args.images)
    labels_dir = Path(args.labels)
    image_paths = sorted([p for p in images_dir.glob('*') if p.suffix.lower() in ('.jpg', '.jpeg', '.png')])

    total_chars = 0
    total_char_errors = 0
    total_words = 0
    total_word_errors = 0
    confusion = Counter()
    examples = []

    for img_path in image_paths:
        stem = img_path.stem
        gt_label_path = labels_dir / (stem + '.txt')
        gt_items = read_yolo_label_txt(str(gt_label_path))
        gt_tokens = labels_to_sequence(gt_items, names)
        gt_text = braille_to_text(gt_tokens)
        gt_seq_norm = normalize_text(gt_text)

        # predict
        try:
            res = model.predict(source=str(img_path), conf=args.conf, device='cpu')
        except Exception as e:
            print(f"Prediction failed for {img_path}: {e}")
            continue
        # ultralytics returns list of Results; use first
        pred = res[0]
        boxes = pred.boxes
        pred_items = []
        # boxes.cls may be a tensor
        from PIL import Image
        img = Image.open(str(img_path))
        w, h = img.size
        for i in range(len(boxes)):
            try:
                cls = int(boxes.cls[i].item())
            except Exception:
                cls = int(boxes.cls[i])
            xyxy = boxes.xyxy[i].tolist() if hasattr(boxes.xyxy[i], 'tolist') else list(boxes.xyxy[i])
            x1, y1, x2, y2 = xyxy[:4]
            # convert to normalized center coords by dividing by image size
            x_center = ((x1 + x2) / 2) / w
            y_center = ((y1 + y2) / 2) / h
            pred_items.append((cls, x_center, y_center))

        # group into lines and order within lines
        lines = group_boxes_to_lines(pred_items, line_tol=args.line_tol)
        line_texts = []
        pred_tokens_all = []
        for ln in lines:
            seq_tokens = [names[c] if c < len(names) else str(c) for (c, _, _) in ln]
            pred_tokens_all.extend(seq_tokens)
            line_text = braille_to_text(seq_tokens)
            line_texts.append(line_text)
        # join lines with a space to create paragraph-level prediction
        pred_seq = ' '.join(line_texts)
        pred_seq_norm = normalize_text(pred_seq)

        # optional spellcheck / dictionary correction
        if args.spell:
            try:
                from spellchecker import SpellChecker
                spell = SpellChecker(language='es')
                # naive token-level correction
                toks = pred_seq_norm.split()
                corrected = []
                for t in toks:
                    # check words of length >1
                    if len(t) > 1:
                        corr = spell.correction(t) or t
                        corrected.append(corr)
                    else:
                        corrected.append(t)
                pred_seq_norm = ' '.join(corrected)
            except Exception:
                # spellchecker not available or failed -> skip
                pass

        # compute character-level alignment
        dist, aligned_gt, aligned_pred = levenshtein_alignment(list(gt_seq_norm), list(pred_seq_norm))
        total_chars += len(gt_seq_norm)
        total_char_errors += dist

        # word-level: split by whitespace
        gt_words = gt_seq_norm.split()
        pred_words = pred_seq_norm.split()
        # naive word distance: levenshtein on word tokens
        wdist, _, _ = levenshtein_alignment(gt_words, pred_words)
        total_words += max(1, len(gt_words))
        total_word_errors += wdist

        # build confusion pairs from aligned sequences
        for gch, pch in zip(aligned_gt, aligned_pred):
            if gch == '-' or pch == '-':
                continue
            if gch != pch:
                confusion[(gch, pch)] += 1

        # save example with highest char error for reporting
        cer = dist / max(1, len(gt_seq_norm)) if len(gt_seq_norm) > 0 else 0
        examples.append((cer, str(img_path), gt_seq_norm, pred_seq_norm))

        # optionally write CSV rows
        if args.csv:
            import csv
            csv_path = Path(args.csv)
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            # write header if file doesn't exist
            write_header = not csv_path.exists()
            with open(csv_path, 'a', encoding='utf-8', newline='') as cf:
                writer = csv.writer(cf)
                if write_header:
                    writer.writerow(['image', 'gt_tokens', 'pred_tokens', 'gt_text', 'pred_text', 'cer'])
                writer.writerow([str(img_path), ' '.join(gt_tokens), ' '.join(pred_tokens_all), gt_text, pred_seq, f"{cer:.6f}"])

    avg_cer = total_char_errors / max(1, total_chars)
    avg_wer = total_word_errors / max(1, total_words)

    # write report
    outp = []
    outp.append(f"Images evaluated: {len(image_paths)}")
    outp.append(f"Total chars (GT): {total_chars}")
    outp.append(f"Total char errors: {total_char_errors}")
    outp.append(f"CER: {avg_cer:.4f}")
    outp.append(f"WER: {avg_wer:.4f}")
    outp.append("\nTop confusion pairs:")
    for (g,p), c in confusion.most_common(30):
        outp.append(f"  {g} -> {p}: {c}")

    examples_sorted = sorted(examples, key=lambda t: t[0], reverse=True)
    outp.append('\nWorst examples (CER, image, GT, PRED):')
    for cer, img, gt, pred in examples_sorted[:20]:
        outp.append(f"{cer:.3f}\t{img}\tGT:{gt}\tPRED:{pred}")

    os.makedirs(Path(args.save).parent, exist_ok=True)
    with open(args.save, 'w', encoding='utf-8') as f:
        f.write('\n'.join(outp))

    print('\n'.join(outp))


if __name__ == '__main__':
    main()
