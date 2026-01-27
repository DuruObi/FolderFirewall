import time
import os
import hashlib
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from core.session_manager import SessionManager
from core.scanner import scan_folder, restore_quarantine, list_quarantine
from core.snapshot import snapshot_folder, compare_snapshot

console = Console()
manager = SessionManager()
QUARANTINE_FOLDER = os.path.expanduser("~/FolderFirewall/quarantine")
os.makedirs(QUARANTINE_FOLDER, exist_ok=True)

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

class AutoSecurityHandler(FileSystemEventHandler):
    def __init__(self, session_id, folder):
        super().__init__()
        self.session_id = session_id
        self.folder = folder
        self.snapshot_file = snapshot_folder(folder, session_id)
        console.print(f"[green]Snapshot saved[/] {self.snapshot_file}")

    def on_created(self, event):
        if not event.is_directory:
            console.print(f"[red]⚠ New file detected:[/] {event.src_path}")
            findings = scan_folder(event.src_path, auto_block=True)
            if findings:
                console.print(f"[red]⚠ Suspicious file quarantined:[/] {findings[0]}")
            self._audit_changes()

    def on_modified(self, event):
        if not event.is_directory:
            console.print(f"[yellow]⚠ File modified:[/] {event.src_path}")
            self._audit_changes()

    def on_deleted(self, event):
        if not event.is_directory:
            console.print(f"[red]⚠ File deleted:[/] {event.src_path}")
            self._audit_changes()

    def _audit_changes(self):
        changes = compare_snapshot(self.session_id, self.folder)
        if changes:
            console.print(f"[red]⚠ ALERT! Suspicious changes detected in session {self.session_id}:[/]")
            for c in changes:
                console.print(f" - {c}")

def run_daemon(session_id, folder):
    event_handler = AutoSecurityHandler(session_id, folder)
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=True)
    observer.start()
    console.print(f"[green]Daemon started[/] Monitoring folder: {folder} (Session ID: {session_id})")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        console.print("[red]Daemon stopped[/]")
    observer.join()
