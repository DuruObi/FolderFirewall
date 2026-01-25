from fastapi import FastAPI, HTTPException
import sessions              # in-memory + Docker session wrapper
from core.session_manager import SessionManager
from sandbox.docker_sandbox import DockerSandbox

app = FastAPI(title="FolderFirewall API")

# Initialize Docker session manager
session_manager = SessionManager()

@app.post("/session/start")
def start():
    session = session_manager.start_session()
    return {"message": "Session started", "session": session}

@app.post("/session/stop/{session_id}")
def stop(session_id: str):
    session = session_manager.stop_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session stopped", "session": session}

@app.get("/session/list")
def get_sessions():
    return {"sessions": session_manager.list_sessions()}
