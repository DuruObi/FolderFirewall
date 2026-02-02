import subprocess

class DockerSandbox:
    def start(self, session_id):
        cmd = [
            "docker", "run", "-d",
            "--rm",
            "--name", f"ff_{session_id}",
            "--cpus", "1",
            "--memory", "512m",
            "--security-opt", "no-new-privileges",
            "folderfirewall-sandbox"
        ]
        result = subprocess.check_output(cmd)
        return result.decode().strip()

    def stop(self, container_id):
        subprocess.call(["docker", "stop", container_id])

    def snapshot(self, container_id):
        subprocess.call([
            "docker", "commit",
            container_id,
            f"snapshot_{container_id}"
        ])
