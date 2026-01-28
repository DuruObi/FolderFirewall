#!/usr/bin/env python3

# backend/cli.py

import typer
from rich.console import Console
from backend.core.scanner import list_quarantine, restore_quarantine
from backend.daemon import run_daemon
from backend.core.session_manager import SessionManager
from backend.core.scanner import scan_folder
from backend.sandbox.docker_sandbox import DockerSandbox

console = Console()
app = typer.Typer()
manager = SessionManager()

@app.command()
def sandbox(folder: str):
    """Start a sandbox session"""
    session_id = manager.start_session(folder)
    console.print(f"[green]Sandbox started[/] ID: {session_id}")

@app.command()
def sessions():
    """List all sessions"""
    all_sessions = manager.list_sessions()
    if not all_sessions:
        console.print("No active sessions")
        return
    for s in all_sessions.values():
        console.print(f"{s['id']}: {s['status']} - {s['folder']}")

@app.command()
def stop(session_id: str):
    """Stop a session"""
    manager.stop_session(session_id)
    console.print(f"[red]Stopped session[/] {session_id}")

@app.command()
def save(session_id: str):
    """Save session snapshot"""
    manager.save_session(session_id)
    console.print(f"[green]Snapshot saved[/] {session_id}")

@app.command()
def daemon(session_id: str, folder: str):
    """Start the monitoring daemon"""
    run_daemon(session_id, folder)

@app.command()
def list_quarantine_cmd():
    """List quarantined files"""
    files = list_quarantine()
    if not files:
        console.print("No quarantined files")
    else:
        for f in files:
            console.print(f"[red]{f}[/]")

@app.command()
def restore(file_name: str, restore_path: str):
    """Restore a quarantined file"""
    try:
        restore_quarantine(file_name, restore_path)
        console.print(f"[green]Restored[/] {file_name}")
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/]")

if __name__ == "__main__":
    app()
