# folderfirewall/core/session_manager.py
import uuid
import json
import os
import hashlib
from folderfirewall.core.audit import log_event
from folderfirewall.sandbox.docker_sandbox import DockerSandbox

# File to store sessions
SESSIONS_FILE = os.path.expanduser("~/FolderFirewall/sessions.json")


def snapshot_folder(folder_path):
    """
    Generate SHA256 hashes for all files in a folder recursively.
    Returns a dict: {relative_path: hash}
    """
    folder_path = os.path.abspath(folder_path)
    hashes = {}
    for root, _, files in os.walk(folder_path):
        for f in files:
            file_path = os.path.join(root, f)
            rel_path = os.path.relpath(file_path, folder_path)
            try:
                with open(file_path, "rb") as file_obj:
                    file_hash = hashlib.sha256(file_obj.read()).hexdigest()
                hashes[rel_path] = file_hash
            except Exception as e:
                log_event("hash_error", {"file": rel_path, "error": str(e)})
    return hashes


class SessionManager:
    def __init__(self):
        self.sandbox = DockerSandbox()
        self.sessions = self._load()

    def _load(self):
        """Load sessions from disk"""
        if os.path.exists(SESSIONS_FILE):
            with open(SESSIONS_FILE, "r") as f:
                return json.load(f)
        return {}

    def _save(self):
        """Save sessions to disk"""
        os.makedirs(os.path.dirname(SESSIONS_FILE), exist_ok=True)
        with open(SESSIONS_FILE, "w") as f:
            json.dump(self.sessions, f, indent=2)

    def start_session(self, folder_path: str):
        """
        Start a new Docker sandbox session for a folder,
        take initial file hash snapshot.
        """
        folder_abs = os.path.abspath(folder_path)
        session_id = uuid.uuid4().hex[:8]

        # Start Docker sandbox
        container_id = self.sandbox.start(folder_abs)

        # Take initial snapshot
        file_hashes = snapshot_folder(folder_abs)
        log_event("session_start_hashes", {"session_id": session_id, "hashes": file_hashes})

        self.sessions[session_id] = {
            "id": session_id,
            "folder": folder_abs,
            "container": container_id,
            "status": "running",
            "hashes": file_hashes,
        }

        self._save()
        log_event("start_session", {"session_id": session_id})
        return session_id

    def stop_session(self, session_id: str):
        """
        Stop a running sandbox session and detect file changes.
        """
        session = self.sessions.get(session_id)
        if not session:
            raise Exception(f"Session {session_id} not found")

        # Take final snapshot and compare
        final_hashes = snapshot_folder(session["folder"])
        for path, new_hash in final_hashes.items():
            old_hash = session["hashes"].get(path)
            if old_hash != new_hash:
                log_event("file_modified", {"session_id": session_id, "file": path})

        # Stop Docker sandbox
        self.sandbox.stop(session["container"])
        session["status"] = "stopped"

        self._save()
        log_event("stop_session", {"session_id": session_id})
        return session

    def list_sessions(self):
        """Return all active sessions"""
        return self.sessions

    def get_session(self, session_id: str):
        """Retrieve a single session"""
        session = self.sessions.get(session_id)
        if not session:
            raise Exception(f"Session {session_id} not found")
        return session
