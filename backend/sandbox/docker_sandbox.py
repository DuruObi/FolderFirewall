# backend/sandbox/docker_sandbox.py

import docker
import uuid
import os

class DockerSandbox:
    def __init__(self):
        self.client = docker.from_env()

    def run(self, folder_path: str):
        session_id = str(uuid.uuid4())[:8]
        container = self.client.containers.run(
            "python:3.11-slim",
            command="sleep 3600",
            volumes={os.path.abspath(folder_path): {"bind": "/sandbox", "mode": "ro"}},
            detach=True,
            name=f"ff_{session_id}",
            network_mode="none",
            security_opt=["no-new-privileges"]
        )
        return session_id, container.id

    def stop(self, container_id: str):
        container = self.client.containers.get(container_id)
        container.stop()
        container.remove()
