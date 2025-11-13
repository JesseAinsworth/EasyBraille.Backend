# backend/utils/braille_translator.py

# Diccionario Braille → Letras
braille_dict = {
    "⠁": "a", "⠃": "b", "⠉": "c", "⠙": "d", "⠑": "e",
    "⠋": "f", "⠛": "g", "⠓": "h", "⠊": "i", "⠚": "j",
    "⠅": "k", "⠇": "l", "⠍": "m", "⠝": "n", "⠕": "o",
    "⠏": "p", "⠟": "q", "⠗": "r", "⠎": "s", "⠞": "t",
    "⠥": "u", "⠧": "v", "⠺": "w", "⠭": "x", "⠽": "y",
    "⠵": "z",
    " ": " "
}

def braille_to_text(labels):
    """
    Convierte etiquetas detectadas por YOLO (símbolos Braille) a texto plano.
    :param labels: lista de caracteres Braille (ej: ["⠁", "⠃", "⠉"])
    :return: string con texto traducido
    """
    texto = ""
    for label in labels:
        if label in braille_dict:
            texto += braille_dict[label]
        else:
            texto += "?"  # Símbolo desconocido
    return texto
