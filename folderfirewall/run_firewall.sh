#!/bin/bash
# Run FolderFirewall CLI + daemon in one command

# Activate venv
source venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Start sandbox session and capture session ID
SESSION_ID=$(python -m cli sandbox ../untrusted_folder | grep -oP '(?<=ID: )\w+')
echo "Started sandbox with session ID: $SESSION_ID"

# Start daemon monitoring
python -m cli daemon $SESSION_ID ../untrusted_folder
