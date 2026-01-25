import uuid
from datetime import datetime

# In-memory session store (MVP)
SESSIONS = {}

def start_session():
    session_id = str(uuid.uuid4())

    session = {
        "id": session_id,
        "status": "running",
        "created_at": datetime.utcnow().isoformat(),
        "sandbox": None  # Docker container id later
    }

    SESSIONS[session_id] = session
    return session
