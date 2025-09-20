#!/usr/bin/env bash
# scripts/snapshot_clone.sh
# Usage: snapshot_clone.sh /path/to/clone [passphrase]
# If passphrase is omitted or empty, the script creates a plain tar.gz snapshot.
# If passphrase is given, it encrypts the tar.gz using openssl AES-256-CBC (with pbkdf2 if available).
set -euo pipefail

CLONE_PATH="${1:-}"
PASSPHRASE="${2:-}"
ROOT="$(pwd)"
SNAP_DIR="$ROOT/snapshots"

# helper to print errors
err() { printf "%s\n" "$*" >&2; }

if [ -z "$CLONE_PATH" ]; then
  err "Usage: $0 /path/to/clone [passphrase]"
  exit 2
fi

if [ ! -d "$CLONE_PATH" ]; then
  err "Error: clone path not found or not a directory: $CLONE_PATH"
  exit 3
fi

# Check for required tools
if ! command -v tar >/dev/null 2>&1; then
  err "Error: 'tar' is required but not found in PATH."
  exit 4
fi

# create snapshots dir
mkdir -p "$SNAP_DIR"

CLONE_NAME="$(basename "$CLONE_PATH")"
TS="$(date +%Y%m%d-%H%M%S)"
TAR_NAME="${CLONE_NAME}-${TS}.tar.gz"
TAR_PATH="$SNAP_DIR/$TAR_NAME"

printf "\n[+] Creating tarball: %s\n" "$TAR_PATH"
# create tar.gz (use -C to ensure tar contains only the clone folder)
tar -czf "$TAR_PATH" -C "$(dirname "$CLONE_PATH")" "$CLONE_NAME"

# If passphrase provided => encrypt
if [ -n "$PASSPHRASE" ]; then
  # ensure openssl exists
  if ! command -v openssl >/dev/null 2>&1; then
    err "Error: 'openssl' is required to encrypt snapshot but not found."
    err "You can install openssl (e.g. apt install openssl) or omit the passphrase to keep unencrypted tar."
    exit 5
  fi

  ENC_PATH="${TAR_PATH}.enc"
  printf "[+] Encrypting snapshot to: %s\n" "$ENC_PATH"

  # Use -pbkdf2 if available (modern openssl). We'll attempt with pbkdf2 and fall back if it fails.
  # Provide passphrase via stdin to avoid showing it in process listings.
  if openssl enc -aes-256-cbc -pbkdf2 -salt -in "$TAR_PATH" -out "$ENC_PATH" -pass stdin <<<"$PASSPHRASE"; then
    rm -f "$TAR_PATH"
    printf "[+] Encrypted snapshot saved to: %s\n" "$ENC_PATH"
    printf "[!] Note: To decrypt: openssl enc -d -aes-256-cbc -pbkdf2 -in '%s' -out '%s' -pass stdin\n" "$ENC_PATH" "${ENC_PATH%.tar.gz.enc}.tar.gz"
  else
    # fallback: try without -pbkdf2 (older openssl)
    if openssl enc -aes-256-cbc -salt -in "$TAR_PATH" -out "$ENC_PATH" -pass stdin <<<"$PASSPHRASE"; then
      rm -f "$TAR_PATH"
      printf "[+] Encrypted snapshot saved to: %s (without pbkdf2)\n" "$ENC_PATH"
      printf "[!] Note: To decrypt: openssl enc -d -aes-256-cbc -in '%s' -out '%s' -pass stdin\n" "$ENC_PATH" "${ENC_PATH%.tar.gz.enc}.tar.gz"
    else
      err "Encryption failed. Leaving unencrypted tar at: $TAR_PATH"
      exit 6
    fi
  fi
else
  printf "[+] Snapshot saved (NOT encrypted): %s\n" "$TAR_PATH"
fi

exit 0
