import json
import os
from core.audit import log_event
import uuid
from sandbox.docker_sandbox import DockerSandbox

SESSION_FILE = os.path.expanduser("~/FolderFirewall/sessions.json")

class SessionManager:
    def __init__(self):
        self.sandbox = DockerSandbox()
        self.sessions = self._load_sessions()

    def _load_sessions(self):
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE) as f:
                return json.load(f)
        return {}

    def _save_sessions(self):
        with open(SESSION_FILE, "w") as f:
            json.dump(self.sessions, f, indent=2)

    def start_session(self, path):
        sid, container_id = self.sandbox.run(path)
        self.sessions[sid] = {
            "id": sid,
            "status": "running",
            "container": container_id,
            "folder": path
        }
        self._save_sessions()
        return self.sessions[sid]

    def stop_session(self, session_id):
        session = self.sessions.get(session_id)
        if not session:
            raise Exception(f"Session {session_id} not found")
        self.sandbox.stop(session["container"])
        session["status"] = "stopped"
        self._save_sessions()
        return session

    def list_sessions(self):
        return list(self.sessions.values())

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.sandbox = DockerSandbox()

    def start_session(self, folder_path):
        session_id = uuid.uuid4().hex[:8]
        container_id = self.sandbox.start(folder_path)

        self.sessions[session_id] = {
            "id": session_id,
            "folder": folder_path,
            "container": container_id,
            "status": "running"
        }

        # log audit event
        log_event("start_session", {"session_id": session_id, "folder": folder_path})
        return session_id

    def stop_session(self, session_id):
        session = self.sessions.get(session_id)
        if not session:
            raise Exception("Session not found")
        self.sandbox.stop(session["container"])
        session["status"] = "stopped"

        # log audit event
        log_event("stop_session", {"session_id": session_id})
        return session
