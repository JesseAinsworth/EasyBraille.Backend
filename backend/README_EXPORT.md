# Exporting the backend code to a new repository

This file contains example commands to export the `backend/` folder into a standalone repository (`EasyBraille-Backend`) while avoiding large model files in history.

Basic subtree export (keeps history for that folder):

```powershell
# Create a branch with only backend/ history
git subtree split -P backend -b export-backend
# Create a new empty repo on GitHub and add as remote
git remote add backend-remote https://github.com/JesseAinsworth/EasyBraille-Backend.git
# Push the subtree branch to the new remote's main branch
git push backend-remote export-backend:main
```

If the history contains large model files (.pt), use git-filter-repo to remove them before publishing. Example (review docs first):

```powershell
pip install git-filter-repo
# WARNING: This rewrites history. Back up your repo or work on a clone.
git clone --mirror <path-to-local-repo> repo-mirror.git
cd repo-mirror.git
# Remove large model paths from history (adjust paths as needed)
git filter-repo --invert-paths --paths models/best.pt
# Push the cleaned mirror to new remote
git remote add cleaned https://github.com/JesseAinsworth/EasyBraille-Backend.git
git push cleaned --all
```

Security note: Do not push model weights to public repos. Use S3 or private registries for heavy artifacts.
