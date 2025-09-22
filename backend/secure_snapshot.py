#!/usr/bin/env python3
# backend/secure_snapshot.py
# Usage: python3 secure_snapshot.py <input.tar.gz> <output.enc> <passphrase>
# Output format: salt(16) || nonce(12) || ciphertext

import sys
import os
from pathlib import Path
from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets

def derive_key(passphrase: bytes, salt: bytes) -> bytes:
    # Argon2id parameters — tune for your environment
    return hash_secret_raw(
        secret=passphrase,
        salt=salt,
        time_cost=2,
        memory_cost=1 << 16,  # 64 MB
        parallelism=1,
        hash_len=32,
        type=Type.ID
    )

def encrypt_file(in_path: Path, out_path: Path, passphrase: str):
    salt = secrets.token_bytes(16)
    key = derive_key(passphrase.encode("utf-8"), salt)
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(12)

    # read input file (for large files you should stream; this is prototype)
    with open(in_path, "rb") as f:
        plaintext = f.read()

    ct = aesgcm.encrypt(nonce, plaintext, None)

    with open(out_path, "wb") as f:
        f.write(salt)
        f.write(nonce)
        f.write(ct)

    print(f"Encrypted {in_path} -> {out_path} (salt+nonce prepended)")

def decrypt_file(enc_path: Path, out_path: Path, passphrase: str):
    with open(enc_path, "rb") as f:
        salt = f.read(16)
        nonce = f.read(12)
        ct = f.read()

    key = derive_key(passphrase.encode("utf-8"), salt)
    aesgcm = AESGCM(key)
    pt = aesgcm.decrypt(nonce, ct, None)
    with open(out_path, "wb") as f:
        f.write(pt)
    print(f"Decrypted {enc_path} -> {out_path}")

def usage():
    print("Usage:")
    print("  secure_snapshot.py encrypt <in.tar.gz> <out.enc> <passphrase>")
    print("  secure_snapshot.py decrypt <in.enc> <out.tar.gz> <passphrase>")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        usage()
        sys.exit(2)
    cmd = sys.argv[1]
    in_p = Path(sys.argv[2])
    out_p = Path(sys.argv[3])
    pwd = sys.argv[4]
    if cmd == "encrypt":
        encrypt_file(in_p, out_p, pwd)
    elif cmd == "decrypt":
        decrypt_file(in_p, out_p, pwd)
    else:
        usage()
        sys.exit(2)
