# backend/core/sandbox.py
import docker
import os

class DockerSandbox:
    def __init__(self):
        self.client = docker.from_env()

    def start(self, folder_path):
        folder_path = os.path.abspath(folder_path)  # MUST be absolute path
        container = self.client.containers.run(
            "python:3.11-slim",
            command="sleep infinity",
            volumes={folder_path: {"bind": "/sandbox", "mode": "rw"}},
            network_mode="none",
            detach=True
        )
        return container.id

    def stop(self, container_id):
        container = self.client.containers.get(container_id)
        container.stop()
        container.remove()
