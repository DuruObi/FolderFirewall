# backend/core/session_manager.py
import os
import json
from sandbox.docker_sandbox import DockerSandbox
from core.snapshot import snapshot_folder, compare_snapshot

SESSION_FILE = os.path.expanduser("~/FolderFirewall/sessions.json")
os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)

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
        snapshot_folder(path, sid)
        self._save_sessions()
        return self.sessions[sid]

    def stop_session(self, session_id):
        session = self.sessions.get(session_id)
        if not session:
            raise Exception(f"Session {session_id} not found")
        # Auto-audit on stop
        changes = compare_snapshot(session_id, session["folder"])
        if changes:
            print(f"[ALERT] Suspicious changes detected during session {session_id}:")
            for c in changes:
                print(f" - {c}")
        self.sandbox.stop(session["container"])
        session["status"] = "stopped"
        self._save_sessions()
        return session

    def list_sessions(self):
        return list(self.sessions.values())
