#!/usr/bin/env bash
<<<<<<< HEAD
# scripts/snapshot_secure.sh
# Usage: snapshot_secure.sh /path/to/clone <output-name> [passphrase]
set -euo pipefail

CLONE_PATH="${1:-}"
OUTNAME="${2:-}"
PASSPHRASE="${3:-}"

if [ -z "$CLONE_PATH" ]; then
  echo "Usage: $0 /path/to/clone <outbase> [passphrase]"
  exit 2
fi

ROOT="$(pwd)"
SNAP_DIR="$ROOT/snapshots"
mkdir -p "$SNAP_DIR"

if [ -z "$OUTNAME" ]; then
  OUTNAME="$(basename "$CLONE_PATH")-$(date +%Y%m%d-%H%M%S)"
fi

TAR_PATH="${SNAP_DIR}/${OUTNAME}.tar.gz"
ENC_PATH="${SNAP_DIR}/${OUTNAME}.tar.gz.enc"

echo "[+] Creating tarball: $TAR_PATH"
tar -czf "$TAR_PATH" -C "$(dirname "$CLONE_PATH")" "$(basename "$CLONE_PATH")"

=======
set -euo pipefail
CLONE_PATH="${1:-}"
OUTNAME="${2:-}"
PASSPHRASE="${3:-}"
if [ -z "$CLONE_PATH" ]; then
  echo "Usage: $0 /path/to/clone <outbase> [passphrase]"; exit 2
fi
ROOT="$(pwd)"; SNAP_DIR="$ROOT/snapshots"; mkdir -p "$SNAP_DIR"
if [ -z "$OUTNAME" ]; then OUTNAME="$(basename "$CLONE_PATH")-$(date +%Y%m%d-%H%M%S)"; fi
TAR_PATH="${SNAP_DIR}/${OUTNAME}.tar.gz"; ENC_PATH="${SNAP_DIR}/${OUTNAME}.tar.gz.enc"
echo "[+] Creating tarball: $TAR_PATH"
tar -czf "$TAR_PATH" -C "$(dirname "$CLONE_PATH")" "$(basename "$CLONE_PATH")"
>>>>>>> e58de9e (Implement CI workflow, secure snapshot functionality, and encrypted loop creation scripts)
if [ -n "$PASSPHRASE" ]; then
  echo "[+] Encrypting snapshot to: $ENC_PATH"
  python3 backend/secure_snapshot.py encrypt "$TAR_PATH" "$ENC_PATH" "$PASSPHRASE"
  rm -f "$TAR_PATH"
  echo "[+] Encrypted snapshot created: $ENC_PATH"
else
  echo "[+] No passphrase provided; leaving unencrypted tar: $TAR_PATH"
fi
