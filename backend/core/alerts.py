# backend/core/alerts.py
import time
import json
from pathlib import Path
from core.audit import AUDIT_LOG

# Simple set to track already alerted hashes
seen_hashes = set()

def watch_audit_log(poll_interval=1):
    """Continuously watch the audit log and print alerts for risky events"""
    log_path = Path(AUDIT_LOG)
    print("[yellow]Starting alert watcher...[/yellow]")
    
    while True:
        if not log_path.exists():
            time.sleep(poll_interval)
            continue
        
        with log_path.open() as f:
            for line in f:
                event = json.loads(line)
                if event["hash"] in seen_hashes:
                    continue  # Already alerted
                
                # Check for risky actions
                if event["action"] in ("scan_alert", "quarantine_file"):
                    print(f"[red][ALERT][/red] {event['timestamp']} - {event['action']}: {event['details']}")
                
                seen_hashes.add(event["hash"])
        
        time.sleep(poll_interval)
