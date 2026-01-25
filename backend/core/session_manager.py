# backend/core/session_manager.py
import uuid
from datetime import datetime
from sandbox.docker_sandbox import DockerSandbox

class SessionManager:
    def __init__(self):
        self.sessions = {}  # in-memory store
        self.sandbox = DockerSandbox()

    def start_session(self):
        session_id = str(uuid.uuid4())
        container = self.sandbox.start_container()

        session = {
            "id": session_id,
            "status": "running",
            "created_at": datetime.utcnow().isoformat(),
            "stopped_at": None,
            "sandbox": container.id
        }

        self.sessions[session_id] = session
        return session

    def stop_session(self, session_id):
        session = self.sessions.get(session_id)
        if not session:
            return None

        if session.get("sandbox"):
            self.sandbox.stop_container(session["sandbox"])

        session["status"] = "stopped"
        session["stopped_at"] = datetime.utcnow().isoformat()
        return session

    def list_sessions(self):
        return list(self.sessions.values())
