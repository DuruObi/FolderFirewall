#!/bin/bash
# Run FolderFirewall CLI + daemon in one command

# 1. Activate venv
source venv/bin/activate

# 2. Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend

# 3. Start sandbox session
SESSION_ID=$(python backend/cli.py sandbox ../untrusted_folder | grep -oP '(?<=ID: )\w+')
echo "Started sandbox with session ID: $SESSION_ID"

# 4. Start daemon monitoring
python backend/cli.py daemon $SESSION_ID ../untrusted_folder
