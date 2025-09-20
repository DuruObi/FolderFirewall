#!/bin/bash
# scripts/upgrade_pip.sh
# Upgrade pip to the latest version inside Codespace or local environment

echo "🔄 Upgrading pip to the latest version..."
python3 -m pip install --upgrade pip

echo "✅ Pip upgrade complete!"
pip --version
