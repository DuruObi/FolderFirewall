#!/usr/bin/env bash
set -euo pipefail
CLONE_NAME="${1:-}"
IMAGE="${2:-docker.io/library/ubuntu:24.04}"
if [ -z "$CLONE_NAME" ]; then
  echo "Usage: $0 <clone-name> [container-image]"
  exit 2
fi
ROOT="$(pwd)"
MOUNT_POINT="/mnt/folderfirewall/${CLONE_NAME}"
if [ ! -d "$MOUNT_POINT" ]; then
  echo "[!] Mount point not found: $MOUNT_POINT"
  exit 3
fi
SECCOMP_PROFILE="$(pwd)/security/seccomp-default.json"
SECCOMP_OPT=""
if [ -f "$SECCOMP_PROFILE" ]; then
  SECCOMP_OPT="--security-opt seccomp=${SECCOMP_PROFILE}"
fi
echo "[+] Starting rootless podman container with clone mounted..."
podman run --rm -it \
  --security-opt no-new-privileges:true \
  ${SECCOMP_OPT} \
  --cap-drop ALL \
  -v "${MOUNT_POINT}":/home/user:Z \
  --network=slirp4netns:allow_host_loopback=false \
  "${IMAGE}" /bin/bash -lc "export FOLDERFIREWALL_CLONE=/home/user; cd /home/user; bash"
echo "[+] Container exited."
