import os
import shutil

DANGEROUS_EXTENSIONS = {".exe", ".bat", ".sh", ".ps1", ".js"}
QUARANTINE_FOLDER = os.path.expanduser("~/FolderFirewall/quarantine")
os.makedirs(QUARANTINE_FOLDER, exist_ok=True)

def scan_folder(path: str, auto_block: bool = True):
    findings = []
    for root, _, files in os.walk(path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            full_path = os.path.join(root, file)
            if ext in DANGEROUS_EXTENSIONS:
                findings.append(full_path)
                if auto_block:
                    shutil.move(full_path, os.path.join(QUARANTINE_FOLDER, file))
    return findings

def list_quarantine():
    return os.listdir(QUARANTINE_FOLDER)

def restore_quarantine(file_name: str, restore_path: str):
    src = os.path.join(QUARANTINE_FOLDER, file_name)
    dst = os.path.join(restore_path, file_name)
    if os.path.exists(src):
        shutil.move(src, dst)
        return dst
    else:
        raise Exception(f"{file_name} not found in quarantine")
