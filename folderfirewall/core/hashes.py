# backend/core/hashes.py
import hashlib
from pathlib import Path

def compute_file_hash(file_path: str, algo="sha256") -> str:
    """Compute a hash for a file using SHA256 (default)"""
    file_path = Path(file_path)
    h = hashlib.new(algo)
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def snapshot_folder(folder_path: str, algo="sha256") -> dict:
    """Return a dict of {relative_path: hash} for all files in folder"""
    folder = Path(folder_path)
    hashes = {}
    for file in folder.rglob("*"):
        if file.is_file():
            rel_path = str(file.relative_to(folder))
            hashes[rel_path] = compute_file_hash(file, algo)
    return hashes
