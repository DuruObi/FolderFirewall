import uuid
from datetime import datetime

# In-memory session store
SESSIONS = {}

def start_session():
    session_id = str(uuid.uuid4())
    session = {
        "id": session_id,
        "status": "running",
        "created_at": datetime.utcnow().isoformat(),
        "stopped_at": None,
        "sandbox": None  # placeholder for Docker container
    }
    SESSIONS[session_id] = session
    return session

def stop_session(session_id: str):
    session = SESSIONS.get(session_id)
    if not session:
        return None
    session["status"] = "stopped"
    session["stopped_at"] = datetime.utcnow().isoformat()
    return session

def list_sessions():
    return list(SESSIONS.values())
