import uuid
from datetime import datetime
import docker

SESSIONS = {}

client = docker.from_env()

def start_session():
    session_id = str(uuid.uuid4())
    # Start lightweight Alpine container
    container = client.containers.run(
        "alpine:latest",
        "sleep 3600",   # keep alive for demo
        detach=True,
        tty=True
    )

    session = {
        "id": session_id,
        "status": "running",
        "created_at": datetime.utcnow().isoformat(),
        "stopped_at": None,
        "sandbox": container.id
    }
    SESSIONS[session_id] = session
    return session

def stop_session(session_id: str):
    session = SESSIONS.get(session_id)
    if not session:
        return None
    # Stop Docker container
    if session.get("sandbox"):
        try:
            container = client.containers.get(session["sandbox"])
            container.stop()
            container.remove()
        except Exception as e:
            print(f"Error stopping container: {e}")

    session["status"] = "stopped"
    session["stopped_at"] = datetime.utcnow().isoformat()
    return session

def list_sessions():
    return list(SESSIONS.values())
