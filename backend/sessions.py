import uuid
from datetime import datetime

SESSIONS = {}

def start_session():
    session_id = str(uuid.uuid4())

    session = {
        "id": session_id,
        "status": "running",
        "created_at": datetime.utcnow().isoformat(),
        "sandbox": None
    }

    SESSIONS[session_id] = session
    return session
