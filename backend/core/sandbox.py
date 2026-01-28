import docker
import os

class DockerSandbox:
    def __init__(self):
        self.client = docker.from_env()

    def start(self, folder_path):
        folder_path = os.path.abspath(folder_path)  # 🔥 FIX

        container = self.client.containers.run(
            "python:3.11-slim",
            command="sleep infinity",
            volumes={
                folder_path: {"bind": "/sandbox", "mode": "rw"}
            },
            detach=True,
            network_mode="none"
        )
        return container.id
