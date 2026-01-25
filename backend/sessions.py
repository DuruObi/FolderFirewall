import uuid
from datetime import datetime

SESSIONS = {}

def start_session():
    session_id = str(uuid.uuid4())
    session = {
        "id": session_id,
        "status": "running",
        "created_at": datetime.utcnow().isoformat(),
        "stopped_at": None,
        "sandbox": None
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
