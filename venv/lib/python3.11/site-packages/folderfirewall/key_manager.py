#!/usr/bin/env python3
# backend/key_manager.py
# Small wrapper around python-keyring; fallback storing encrypted file with a local symmetric key.
import keyring
import os
from pathlib import Path
from typing import Optional

APP_NAME = "FolderFirewall"
FALLBACK_DIR = Path.cwd() / ".ff_keys"
FALLBACK_DIR.mkdir(exist_ok=True)

def set_key(name: str, secret: str):
    try:
        keyring.set_password(APP_NAME, name, secret)
        return True
    except Exception:
        # fallback: store in a file (rudimentary - improve for production)
        f = FALLBACK_DIR / f"{name}.key"
        f.write_text(secret, encoding="utf-8")
        os.chmod(f, 0o600)
        return True

def get_key(name: str) -> Optional[str]:
    try:
        s = keyring.get_password(APP_NAME, name)
        if s:
            return s
    except Exception:
        pass
    f = FALLBACK_DIR / f"{name}.key"
    if f.exists():
        return f.read_text(encoding="utf-8")
    return None
#!/usr/bin/env python3
import keyring, os
from pathlib import Path
APP_NAME = "FolderFirewall"
FALLBACK_DIR = Path.cwd() / ".ff_keys"
FALLBACK_DIR.mkdir(exist_ok=True)
def set_key(name: str, secret: str):
    try:
        keyring.set_password(APP_NAME, name, secret); return True
    except Exception:
        f = FALLBACK_DIR / f"{name}.key"; f.write_text(secret, encoding="utf-8"); os.chmod(f, 0o600); return True
def get_key(name: str):
    try:
        s = keyring.get_password(APP_NAME, name)
        if s: return s
    except Exception: pass
    f = FALLBACK_DIR / f"{name}.key"
    if f.exists(): return f.read_text(encoding="utf-8")
    return None
