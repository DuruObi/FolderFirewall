import time
import os
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from backend.core.session_manager import SessionManager
from backend.core.scanner import scan_folder

console = Console()
manager = SessionManager()

class AutoSecurityHandler(FileSystemEventHandler):
    def __init__(self, session_id, folder):
        super().__init__()
        self.session_id = session_id
        self.folder = folder

    def _audit_changes(self):
        changes = scan_folder(self.folder, auto_block=True)
        for c in changes:
            console.print(f"[red]⚠ Quarantined suspicious file:[/] {c}")

    def on_created(self, event):
        if not event.is_directory:
            console.print(f"[yellow]New file detected:[/] {event.src_path}")
            self._audit_changes()

    def on_modified(self, event):
        if not event.is_directory:
            console.print(f"[yellow]Modified file:[/] {event.src_path}")
            self._audit_changes()

    def on_deleted(self, event):
        if not event.is_directory:
            console.print(f"[red]Deleted file:[/] {event.src_path}")
            self._audit_changes()

def run_daemon(session_id, folder_path, interval=5):
    print(f"🛡 Monitoring session {session_id}")

    while True:
        results = scan_folder(folder_path)

        if results["quarantined"]:
            print("⚠ Suspicious files quarantined:")
            for f in results["quarantined"]:
                print(" -", f)

        time.sleep(interval)
