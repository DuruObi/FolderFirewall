import uuid
from sandbox.docker_engine import DockerSandbox

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.sandbox = DockerSandbox()

    def start_session(self):
        session_id = str(uuid.uuid4())
        container_id = self.sandbox.start(session_id)

        self.sessions[session_id] = {
            "status": "running",
            "container": container_id
        }

        return {"session_id": session_id}

    def stop_session(self, session_id):
        self.sandbox.stop(self.sessions[session_id]["container"])
        self.sessions[session_id]["status"] = "stopped"
        return {"status": "stopped"}

    def save_session(self, session_id):
        self.sandbox.snapshot(self.sessions[session_id]["container"])
        return {"status": "saved"}

    def list_sessions(self):
        return self.sessions
