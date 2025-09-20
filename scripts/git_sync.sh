#!/usr/bin/env bash
git fetch origin
git pull --rebase origin main || { echo "Rebase failed — resolve conflicts and run: git rebase --continue"; exit 1; }
git push origin main --force-with-lease
