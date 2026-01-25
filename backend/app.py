from fastapi import FastAPI
from sessions import start_session

app = FastAPI(title="FolderFirewall API")

@app.post("/session/start")
def start():
    session = start_session()
    return {
        "message": "Session started",
        "session": session
    }
