#!/usr/bin/env python3

# backend/cli.py

import typer
from rich.console import Console
from core.session_manager import SessionManager
from core.scanner import scan_folder, list_quarantine, restore_quarantine
from core.snapshot import compare_snapshot

app = typer.Typer()
console = Console()
manager = SessionManager()

@app.command()
def scan(path: str):
    console.print(f"[bold cyan]Scanning:[/] {path}")
    findings = scan_folder(path)
    if not findings:
        console.print("[green]✔ No suspicious files found[/]")
    else:
        console.print("[red]⚠ Suspicious files quarantined![/]")
        for f in findings:
            console.print(f" - {f}")

@app.command()
def sandbox(path: str):
    session = manager.start_session(path)
    console.print(f"[green]Sandbox started[/] ID: {session['id']}")

@app.command()
def audit(session_id: str, path: str):
    changes = compare_snapshot(session_id, path)
    if not changes:
        console.print("[green]✔ No changes detected[/]")
    else:
        console.print("[red]⚠ ALERT! Suspicious changes detected![/]")
        for c in changes:
            console.print(f" - {c}")

@app.command()
def sessions():
    s_list = manager.list_sessions()
    if not s_list:
        console.print("[yellow]No active sessions[/]")
        return
    for s in s_list:
        console.print(f"[cyan]{s['id']}[/] | {s['status']} | {s['container']}")

@app.command()
def stop(session_id: str):
    session = manager.stop_session(session_id)
    console.print(f"[red]Stopped session[/] {session_id}")

@app.command()
def quarantine_list():
    files = list_quarantine()
    if not files:
        console.print("[green]Quarantine empty[/]")
        return
    console.print("[red]Quarantined files:[/]")
    for f in files:
        console.print(f" - {f}")

@app.command()
def quarantine_restore(file_name: str, restore_path: str):
    restored = restore_quarantine(file_name, restore_path)
    console.print(f"[green]Restored:[/] {restored}")

@app.command()
def daemon(session_id: str, folder: str):
    """Run a fully autonomous folder firewall daemon"""
    from backend.daemon import run_daemon
    run_daemon(session_id, folder)

if __name__ == "__main__":
    app()
