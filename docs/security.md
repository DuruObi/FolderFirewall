# FolderFirewall — Security notes & usage
## Overview
This explains the Linux-first secure clone flow: LUKS encrypted image + rootless container + encrypted snapshots.
## Important caveats
- Host kernel compromises limit guarantees.
- LUKS passphrases are entered interactively.
- The seccomp profile is starter-only and must be hardened.
## Quick install
sudo apt update
sudo apt install -y cryptsetup podman tar openssl python3-pip
pip3 install argon2-cffi cryptography keyring

# FolderFirewall — Security notes & usage

## Overview
This document covers the Linux-first secure clone flow implemented by the scripts in this repo.

## How it works (high level)
- `create_encrypted_loop.sh` creates a LUKS2-encrypted loop image and mounts it under `/mnt/folderfirewall/<clone>`.
- `run_clone_podman.sh` starts a rootless Podman container and mounts the encrypted filesystem inside the container.
- `scripts/snapshot_secure.sh` creates a tarball and uses `backend/secure_snapshot.py` (Argon2 + AES-GCM) to encrypt the snapshot.

## Important security caveats
- You must trust the host OS kernel. If the host is compromised (rootkit, malicious hypervisor), these protections are reduced.
- LUKS passphrases are entered interactively; do not expose them to process lists or logs.
- The seccomp profile is a basic starter and must be hardened for production workloads.
- Use TPM-backed sealing for production key management where available.

## Recommended packages to install (Linux)
