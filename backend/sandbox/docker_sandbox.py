# backend/sandbox/docker_sandbox.py
import docker

class DockerSandbox:
    def __init__(self):
        self.client = docker.from_env()

    def start_container(self, image="alpine:latest", command="sleep 3600"):
        """Start a new Docker container for a session."""
        container = self.client.containers.run(
            image,
            command,
            detach=True,
            tty=True
        )
        return container

    def stop_container(self, container_id):
        """Stop and remove a container by its ID."""
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            container.remove()
        except Exception as e:
            print(f"[DockerSandbox] Error stopping container {container_id}: {e}")
