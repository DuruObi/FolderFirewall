# backend/core/session_manager.py
from sandbox.docker_sandbox import DockerSandbox
import uuid

class SessionManager:
    def __init__(self):
        self.sessions = {}  # {session_id: {"container_id": ..., "status": ...}}
        self.sandbox = DockerSandbox()

    def start_session(self):
        session_id = str(uuid.uuid4())
        container_id, container_name = self.sandbox.start_container()
        self.sessions[session_id] = {
            "container_id": container_id,
            "container_name": container_name,
            "status": "running"
        }
        return session_id, self.sessions[session_id]

    def stop_session(self, session_id):
        session = self.sessions.get(session_id)
        if not session:
            return False
        self.sandbox.stop_container(session["container_id"])
        session["status"] = "stopped"
        return True

    def list_sessions(self):
        return [
            {
                "id": sid,
                "status": info["status"],
                "sandbox": info["container_name"]
            }
            for sid, info in self.sessions.items()
        ]
