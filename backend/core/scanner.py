import hashlib
import shutil
import time
from plugins.loader import load_plugins
import os
from core.audit import log_event

folder = "./untrusted_folder"
for root, _, files in os.walk(folder):
    for f in files:
        scan_file(os.path.join(root, f))

QUARANTINE_DIR = os.path.expanduser("~/FolderFirewall/quarantine")
os.makedirs(QUARANTINE_DIR, exist_ok=True)

SUSPICIOUS_EXTENSIONS = {".sh", ".exe", ".bat", ".ps1", ".pyc"}

def list_quarantine():
    """Return list of quarantined files"""
    try:
        return os.listdir(QUARANTINE_DIR)
    except FileNotFoundError:
        return []

def restore_quarantine(file_name, restore_path):
    src = os.path.join(QUARANTINE_DIR, file_name)
    dst = os.path.join(os.path.abspath(restore_path), file_name)

    if not os.path.exists(src):
        raise FileNotFoundError(f"{file_name} not found in quarantine")

    shutil.move(src, dst)


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def scan_folder(folder_path):
    """
    Scan a folder for suspicious files.
    Returns a dict with scan results.
    """
    results = {
        "scanned_at": time.time(),
        "folder": os.path.abspath(folder_path),
        "quarantined": [],
        "hashes": {}
    }

    for root, _, files in os.walk(folder_path):
        for name in files:
            file_path = os.path.join(root, name)
            ext = os.path.splitext(name)[1].lower()

            try:
                results["hashes"][file_path] = file_hash(file_path)
            except Exception:
                continue

            if ext in SUSPICIOUS_EXTENSIONS:
                quarantine_path = os.path.join(
                    QUARANTINE_DIR,
                    f"{int(time.time())}_{name}"
                )
                shutil.move(file_path, quarantine_path)
                results["quarantined"].append(quarantine_path)

    return results

def run_plugins(file_path):
    findings = []
    for plugin in load_plugins():
        result = plugin.scan(file_path)
        if result:
            findings.append(result)
    return findings

def scan_file(file_path):
    findings = run_plugins(file_path)
    for result in findings:
        print(f"[{result['plugin']}] {result['issue']} -> {file_path}")
    return findings

def scan_file(file_path):
    findings = run_plugins(file_path)
    if findings:
        for result in findings:
            log_event("scan_alert", {
                "file": file_path,
                "plugin": result["plugin"],
                "issue": result["issue"]
            })
            print(f"[{result['plugin']}] {result['issue']} -> {file_path}")
    return findings

def quarantine_file(file_path):
    # Move file to quarantine...
    log_event("quarantine_file", {"file": file_path})
