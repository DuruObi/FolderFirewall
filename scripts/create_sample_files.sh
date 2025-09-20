#!/usr/bin/env bash
# scripts/create_sample_files.sh
# Create a few demo files inside the clone directory passed as $1

set -e
CLONE_DIR="$1"
if [ -z "$CLONE_DIR" ]; then
  echo "Usage: $0 /path/to/clone"
  exit 1
fi

mkdir -p "$CLONE_DIR/docs"
mkdir -p "$CLONE_DIR/data"
echo "FolderFirewall Prototype Clone" > "$CLONE_DIR/README_IN_CLONE.txt"
echo "Sample note: this is safe to edit inside the clone." > "$CLONE_DIR/docs/note1.txt"
head -c 1024 /dev/urandom > "$CLONE_DIR/data/dummy.bin" || true
chmod -R u+rw "$CLONE_DIR"
echo "Sample files created in $CLONE_DIR"
