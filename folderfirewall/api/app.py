from fastapi import FastAPI, HTTPException
import sessions

app = FastAPI(title="FolderFirewall API")

@app.post("/session/start")
def start():
    session = sessions.start_session()
    return {"message": "Session started", "session": session}

@app.post("/session/stop/{session_id}")
def stop(session_id: str):
    session = sessions.stop_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session stopped", "session": session}

@app.get("/session/list")
def get_sessions():
    return {"sessions": sessions.list_sessions()}
