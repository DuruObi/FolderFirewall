from fastapi import FastAPI
import sessions

app = FastAPI(title="FolderFirewall API")

@app.post("/session/start")
def start():
    session = sessions.start_session()
    return {
        "message": "Session started",
        "session": session
    }
