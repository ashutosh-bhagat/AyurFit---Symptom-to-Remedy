"""
One-time script to upload the AyurFit backend to HuggingFace Spaces.
Run: python upload_to_hf.py
"""
from huggingface_hub import HfApi
import os

# ── Config ────────────────────────────────────────────────────────────────────
HF_TOKEN   = "YOUR_HF_WRITE_TOKEN_HERE"  # Never commit real tokens!
REPO_ID    = "ashutoshbhagat/ayurfit"   # your Space repo ID
REPO_TYPE  = "space"

# Files/folders to upload (relative to backend/)
INCLUDE = [
    "main.py",
    "requirements.txt",
    "Dockerfile",
    ".dockerignore",
    "dataset",
    "model",
]

# ── Upload ────────────────────────────────────────────────────────────────────
api = HfApi(token=HF_TOKEN)

print(f"\nUploading to: https://huggingface.co/spaces/{REPO_ID}")
print("This may take a few minutes for model/dataset files...\n")

api.upload_folder(
    folder_path=".",           # current dir = backend/
    repo_id=REPO_ID,
    repo_type=REPO_TYPE,
    ignore_patterns=[          # skip dev/cache files
        ".git*",
        "__pycache__",
        "*.pyc",
        "*.ipynb",
        ".ipynb_checkpoints",
        ".venv",
        "upload_to_hf.py",     # don't upload this script itself
        ".gitattributes",
    ],
    token=HF_TOKEN,
)

print("\n✅ Upload complete!")
print(f"   View your Space: https://huggingface.co/spaces/{REPO_ID}")
print(f"   API docs (once running): https://ashutoshbhagat-ayurfit.hf.space/docs")
