# backend/app.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from core.session_manager import SessionManager

app = FastAPI()
manager = SessionManager()

@app.post("/session/start")
def start_session():
    session_id, info = manager.start_session()
    return JSONResponse({"session_id": session_id, "info": info})

@app.post("/session/stop/{session_id}")
def stop_session(session_id: str):
    success = manager.stop_session(session_id)
    if success:
        return {"status": "stopped", "session_id": session_id}
    return JSONResponse({"error": "session not found"}, status_code=404)

@app.get("/session/list")
def list_sessions():
    sessions = manager.list_sessions()
    return {"sessions": sessions}
