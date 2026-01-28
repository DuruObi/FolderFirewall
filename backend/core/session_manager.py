# backend/core/session_manager.py
import uuid
import json
import os
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
        return session_id

    def stop_session(self, session_id):
        session = self.sessions.get(session_id)
        if not session:
            raise Exception(f"Session {session_id} not found")

        self.sandbox.stop(session["container"])
        session["status"] = "stopped"
        self._save()
        return session

    def list_sessions(self):
        return self.sessions
