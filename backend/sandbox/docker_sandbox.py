# backend/sandbox/docker_sandbox.py
import docker
import uuid

class DockerSandbox:
    def __init__(self):
        self.client = docker.from_env()
        self.containers = {}

    def start_container(self, image="ubuntu:22.04"):
        container_name = f"sandbox-{uuid.uuid4().hex[:8]}"
        container = self.client.containers.run(
            image,
            name=container_name,
            detach=True,
            tty=True,
            stdin_open=True,
            command="/bin/bash",
        )
        self.containers[container.id] = container
        return container.id, container_name

    def stop_container(self, container_id):
        container = self.containers.get(container_id)
        if container:
            container.stop()
            container.remove()
            del self.containers[container_id]
            return True
        return False

    def list_containers(self):
        return [
            {
                "id": cid,
                "name": cont.name,
                "status": cont.status,
            }
            for cid, cont in self.containers.items()
        ]
