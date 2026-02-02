# backend/core/audit.py
import os
import json
import hashlib
from datetime import datetime

AUDIT_LOG = os.path.join(os.path.dirname(__file__), "../logs/audit.jsonl")

def hash_event(event: dict) -> str:
    """Generate SHA256 hash of the event JSON string"""
    event_str = json.dumps(event, sort_keys=True)
    return hashlib.sha256(event_str.encode()).hexdigest()

def log_event(action: str, details: dict):
    """Append an event to audit log with timestamp & hash"""
    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "details": details
    }
    event["hash"] = hash_event(event)
    
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(event) + "\n")

def read_audit_log():
    """Read all audit events"""
    if not os.path.exists(AUDIT_LOG):
        return []
    with open(AUDIT_LOG) as f:
        return [json.loads(line) for line in f]
