# backend/core/session_manager.py
import uuid
import json
import os
from core.hashes import snapshot_folder
from core.audit import log_event
from backend.sandbox.docker_sandbox import DockerSandbox

SESSIONS_FILE = os.path.expanduser("~/FolderFirewall/sessions.json")

class SessionManager:
    def __init__(self):
        self.sandbox = DockerSandbox()
        self.sessions = self._load()

    def _load(self):
        if os.path.exists(SESSIONS_FILE):
            with open(SESSIONS_FILE, "r") as f:
                return json.load(f)
        return {}

    def _save(self):
        os.makedirs(os.path.dirname(SESSIONS_FILE), exist_ok=True)
        with open(SESSIONS_FILE, "w") as f:
            json.dump(self.sessions, f, indent=2)

    def start_session(self, folder_path):
        session_id = uuid.uuid4().hex[:8]
        container_id = self.sandbox.start(folder_path)

        self.sessions[session_id] = {
            "id": session_id,
            "folder": os.path.abspath(folder_path),
            "container": container_id,
            "status": "running"
        }
        self._save()
# backend/core/session_manager.py
import uuid
import json
import os
from core.audit import log_event
from backend.sandbox.docker_sandbox import DockerSandbox

SESSIONS_FILE = os.path.expanduser("~/FolderFirewall/sessions.json")


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

    def start_session(self, folder_path):
        """Start a new Docker sandbox session for a folder"""
        folder_abs = os.path.abspath(folder_path)
        session_id = uuid.uuid4().hex[:8]
        container_id = self.sandbox.start(folder_abs)

        self.sessions[session_id] = {
            "id": session_id,
            "folder": folder_abs,
            "container": container_id,
            "status": "running"
        }

        self._save()
        log_event("start_session", {"session_id": session_id, "folder": folder_abs})
        return session_id

    def stop_session(self, session_id):
        """Stop a running sandbox session"""
        session = self.sessions.get(session_id)
        if not session:
            raise Exception(f"Session {session_id} not found")

        self.sandbox.stop(session["container"])
        session["status"] = "stopped"

        self._save()
        log_event("stop_session", {"session_id": session_id})
        return session

    def list_sessions(self):
        """Return all sessions"""
        return self.sessions

    def get_session(self, session_id):
        """Retrieve a single session"""
        session = self.sessions.get(session_id)
        if not session:
            raise Exception(f"Session {session_id} not found")
        return session

class SessionManager:
    ...
    def start_session(self, folder_path: str):
        session_id = uuid.uuid4().hex[:8]
        container_id = self.sandbox.start(folder_path)
        
        # Take initial hash snapshot
        file_hashes = snapshot_folder(folder_path)
        log_event("session_start_hashes", {"session_id": session_id, "hashes": file_hashes})
        
        self.sessions[session_id] = {
            "id": session_id,
            "folder": folder_path,
            "container": container_id,
            "status": "running",
            "hashes": file_hashes,
        }
        return session_id

    def stop_session(self, session_id: str):
        session = self.sessions.get(session_id)
        if not session:
            raise Exception("Session not found")
        
        # Take final hash snapshot and compare
        final_hashes = snapshot_folder(session["folder"])
        for path, h in final_hashes.items():
            old_hash = session["hashes"].get(path)
            if old_hash != h:
                log_event("file_modified", {"session_id": session_id, "file": path})
        
        self.sandbox.stop(session["container"])
        session["status"] = "stopped"
        return session
