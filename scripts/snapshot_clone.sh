#!/usr/bin/env bash
# scripts/snapshot_clone.sh
# Usage: snapshot_clone.sh /path/to/clone [passphrase]
set -e
CLONE_PATH="$1"
PASSPHRASE="$2"
ROOT="$(pwd)"
SNAP_DIR="$ROOT/snapshots"
mkdir -p "$SNAP_DIR"

if [ -z "$CLONE_PATH" ]; then
  echo "Usage: $0 /path/to/clone [passphrase]"
  exit 1
fi

CLONE_NAME="$(basename "$CLONE_PATH")"
TS="$(date +%Y%m%d-%H%M%S)"
TAR_NAME="${CLONE_NAME}-${TS}.tar.gz"
TAR_PATH="$SNAP_DIR/$TAR_NAME"

echo "Creating tarball $TAR_PATH ..."
tar -czf "$TAR_PATH" -C "$(dirname "$CLONE_PATH")" "$CLONE_NAME"

if [ -n "$PASSPHRASE" ]; then
  ENC_PATH="$TAR_PATH.enc"
  echo "Encrypting snapshot with AES-256 (openssl). Output: $ENC_PATH"
  # -pbkdf2 for better key derivation
  openssl enc -aes-256-cbc -pbkdf2 -salt -in "$TAR_PATH" -out "$ENC_PATH" -pass pass:"$PASSPHRASE"
  rm -f "$TAR_PATH"
  echo "Encrypted snapshot saved to $ENC_PATH"
else
  echo "Snapshot saved (not encrypted) to $TAR_PATH"
fi
