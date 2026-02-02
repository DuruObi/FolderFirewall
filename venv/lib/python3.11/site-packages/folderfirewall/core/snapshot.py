# backend/core/snapshot.py
import os
import json
import hashlib

SNAPSHOT_DIR = os.path.expanduser("~/FolderFirewall/snapshots")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

def snapshot_folder(folder_path, session_id):
    snapshot = {}
    for root, _, files in os.walk(folder_path):
        for f in files:
            path = os.path.join(root, f)
            with open(path, "rb") as file:
                snapshot[path] = hashlib.sha256(file.read()).hexdigest()
    snapshot_file = os.path.join(SNAPSHOT_DIR, f"{session_id}.json")
    with open(snapshot_file, "w") as f:
        json.dump(snapshot, f, indent=2)
    return snapshot_file

def compare_snapshot(session_id, folder_path):
    snapshot_file = os.path.join(SNAPSHOT_DIR, f"{session_id}.json")
    if not os.path.exists(snapshot_file):
        return []

    with open(snapshot_file, "r") as f:
        old_snapshot = json.load(f)

    changes = []
    for root, _, files in os.walk(folder_path):
        for f in files:
            path = os.path.join(root, f)
            with open(path, "rb") as file:
                h = hashlib.sha256(file.read()).hexdigest()
            if path not in old_snapshot or old_snapshot[path] != h:
                changes.append(path)
    return changes
