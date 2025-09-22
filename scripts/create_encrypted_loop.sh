#!/usr/bin/env bash
set -euo pipefail
CLONE_NAME="${1:-}"
SIZE_MB="${2:-1024}"
if [ -z "$CLONE_NAME" ]; then
  echo "Usage: $0 <clone-name> <size-MB>"
  exit 2
fi
ROOT="$(pwd)"
CLONES_DIR="$ROOT/clones"
IMG_PATH="$CLONES_DIR/${CLONE_NAME}.img"
MAPPER_NAME="ff_${CLONE_NAME}"
MOUNT_POINT="/mnt/folderfirewall/${CLONE_NAME}"
echo "[+] Creating clones dir if missing: $CLONES_DIR"
mkdir -p "$CLONES_DIR"
if [ -f "$IMG_PATH" ]; then
  echo "[!] Image already exists: $IMG_PATH"
  exit 3
fi
echo "[+] Creating sparse file of ${SIZE_MB}MB: $IMG_PATH"
truncate -s "${SIZE_MB}M" "$IMG_PATH"
echo "[!] Now formatting LUKS container. You will be prompted for a passphrase (twice)."
sudo cryptsetup luksFormat --type luks2 "$IMG_PATH"
echo "[+] Opening LUKS container as /dev/mapper/$MAPPER_NAME"
sudo cryptsetup luksOpen "$IMG_PATH" "$MAPPER_NAME"
echo "[+] Creating filesystem on /dev/mapper/$MAPPER_NAME"
sudo mkfs.ext4 -F "/dev/mapper/$MAPPER_NAME"
echo "[+] Creating mount point: $MOUNT_POINT"
sudo mkdir -p "$MOUNT_POINT"
sudo chown "$(id -u):$(id -g)" "$MOUNT_POINT"
echo "[+] Mounting filesystem"
sudo mount "/dev/mapper/$MAPPER_NAME" "$MOUNT_POINT"
sudo chown "$(id -u):$(id -g)" "$MOUNT_POINT"
chmod 700 "$MOUNT_POINT"
echo "[+] Successfully created and mounted encrypted clone at: $MOUNT_POINT"
echo "    image: $IMG_PATH"
echo "To close the mapper: sudo umount $MOUNT_POINT && sudo cryptsetup luksClose $MAPPER_NAME"
