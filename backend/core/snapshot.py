# backend/core/snapshot.py
import os
import hashlib
import json

SNAPSHOT_FOLDER = os.path.expanduser("~/FolderFirewall/snapshots")
os.makedirs(SNAPSHOT_FOLDER, exist_ok=True)

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def snapshot_folder(folder_path, session_id):
    snapshot = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            snapshot[full_path] = hash_file(full_path)
    snapshot_file = os.path.join(SNAPSHOT_FOLDER, f"{session_id}.json")
    with open(snapshot_file, "w") as f:
        json.dump(snapshot, f, indent=2)
    return snapshot_file

def compare_snapshot(session_id, folder_path):
    snapshot_file = os.path.join(SNAPSHOT_FOLDER, f"{session_id}.json")
    if not os.path.exists(snapshot_file):
        return None
    with open(snapshot_file) as f:
        old_snapshot = json.load(f)

    changes = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            h = hashlib.sha256(open(full_path, "rb").read()).hexdigest()
            if full_path not in old_snapshot:
                changes.append(f"New file: {full_path}")
            elif old_snapshot[full_path] != h:
                changes.append(f"Modified file: {full_path}")

    for f in old_snapshot:
        if not os.path.exists(f):
            changes.append(f"Deleted file: {f}")

    return changes
