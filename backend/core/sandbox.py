# backend/core/sandbox.py
import os
import docker
from pathlib import Path

class DockerSandbox:
    def __init__(self):
        self.client = docker.from_env()

    def start(self, folder_path: str):
        folder_path = str(Path(folder_path).resolve())  # Absolute path
        container = self.client.containers.run(
            "python:3.11-slim",
            command="sleep infinity",
            volumes={folder_path: {"bind": "/sandbox", "mode": "rw"}},
            network_mode="none",  # 🔐 disable all networking
            detach=True,
        )
        return container.id

    def stop(self, container_id: str):
        container = self.client.containers.get(container_id)
        container.stop()
        container.remove()
