#!/usr/bin/env python3

# folderfirewall/cli.py

from rich.console import Console
from folderfirewall.daemon import run_daemon
from folderfirewall.core.alerts import watch_audit_log
import sys
from pathlib import Path
import typer
from folderfirewall.core.session_manager import SessionManager
from folderfirewall.core.scanner import scan_folder, list_quarantine, restore_quarantine
from folderfirewall.core.sandbox import DockerSandbox

app = typer.Typer()
manager = SessionManager()

@app.command()
def sandbox(folder: str):
    """Start a sandbox session"""
    session_id = manager.start_session(folder)
    print(f"Sandbox started, session ID: {session_id}")

@app.command()
def sessions():
    """List active sessions"""
    active = manager.list_sessions()
    if not active:
        print("No active sessions")
    else:
        for s in active:
            print(f"- {s}")

@app.command()
def daemon(session_id: str, folder: str):
    """Start folder monitoring"""
    manager.run_daemon(session_id, folder)

@app.command()
def list_quarantine_cmd():
    """List quarantined files"""
    files = list_quarantine()
    for f in files:
        print(f"- {f}")

@app.command()
def restore(file_name: str, restore_path: str):
    """Restore a quarantined file"""
    restore_quarantine(file_name, restore_path)
    print(f"Restored {file_name} to {restore_path}")

@app.command()
def stop(session_id: str):
    """Stop a sandbox session"""
    session = manager.stop_session(session_id)
    print(f"Stopped session {session_id}")

if __name__ == "__main__":
    app()

