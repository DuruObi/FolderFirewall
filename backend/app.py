from fastapi import FastAPI
from core.session_manager import SessionManager

app = FastAPI()
manager = SessionManager()

@app.post("/session/start")
def start_session():
    return manager.start_session()

@app.post("/session/stop/{session_id}")
def stop_session(session_id: str):
    return manager.stop_session(session_id)

@app.post("/session/save/{session_id}")
def save_session(session_id: str):
    return manager.save_session(session_id)

@app.get("/session/list")
def list_sessions():
    return manager.list_sessions()
# (paste the full app.py content here exactly as above)
