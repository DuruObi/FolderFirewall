#!/usr/bin/env python3
"""
FolderFirewall prototype CLI (backend/app.py)

- Creates a "clone" folder under ./clones/
- Optionally copies a source folder into the clone (disabled by default)
- Opens a shell with working dir = clone (so everything you do stays inside clone)
- On shell exit: prompt Save / Discard / Snapshot (encrypted tar.gz)
"""
import os
import sys
import time
import shutil
import subprocess
from pathlib import Path

ROOT = Path.cwd()
CLONES_DIR = ROOT / "clones"
SAMPLE_SCRIPT = ROOT / "scripts" / "create_sample_files.sh"
SNAPSHOT_SCRIPT = ROOT / "scripts" / "snapshot_clone.sh"


def ensure_dirs():
    CLONES_DIR.mkdir(exist_ok=True)


def show_menu():
    print("\n=== FolderFirewall (Prototype) ===")
    print("1) Start a secure cloned environment (prototype)")
    print("2) List clones")
    print("3) Remove a clone")
    print("4) Exit")


def iso_timestamp():
    return time.strftime("%Y%m%d-%H%M%S")


def start_clone():
    ensure_dirs()
    clone_id = f"clone-{iso_timestamp()}"
    clone_path = CLONES_DIR / clone_id
    clone_path.mkdir(parents=True, exist_ok=False)
    print(f"\n[+] Created clone: {clone_path}")

    # Optionally: copy a source folder into the clone.
    # For prototype we create sample files if a helper exists
    if SAMPLE_SCRIPT.exists():
        try:
            subprocess.run([str(SAMPLE_SCRIPT), str(clone_path)], check=True)
            print("    Sample files created in clone.")
        except Exception as e:
            print("    Warning: sample file creation failed:", e)
    else:
        # Create a small sample file so it's not empty
        (clone_path / "README_IN_CLONE.txt").write_text(
            "This is a FolderFirewall prototype clone.\nAll changes made here only affect this folder.\n"
        )

    print("\n[i] Opening a shell inside the cloned environment.")
    shell = os.environ.get("SHELL", "/bin/bash")
    # Set an env var so child shell can know it's inside a clone
    env = os.environ.copy()
    env["FOLDERFIREWALL_CLONE"] = str(clone_path)

    try:
        # Launch an interactive shell with cwd=clone_path
        subprocess.call([shell], cwd=str(clone_path), env=env)
    except KeyboardInterrupt:
        print("\n[!] Shell interrupted.")

    # After shell exits
    post_clone_menu(clone_path)


def list_clones():
    ensure_dirs()
    clones = sorted(CLONES_DIR.iterdir(), reverse=True)
    if not clones:
        print("\n[!] No clones found.")
        return
    print("\nExisting clones:")
    for c in clones:
        size = get_size_readable(c)
        print(f" - {c.name}\t{size}")


def remove_clone():
    list_clones()
    name = input("\nEnter clone name to remove (e.g. clone-20250101-123000): ").strip()
    if not name:
        print("No name provided. Cancel.")
        return
    target = CLONES_DIR / name
    if not target.exists():
        print("Clone not found:", target)
        return
    confirm = input(f"Confirm DELETE {target} ? This permanently removes files. (yes/no): ").strip().lower()
    if confirm == "yes":
        shutil.rmtree(target)
        print("Removed", target)
    else:
        print("Cancelled.")


def post_clone_menu(clone_path: Path):
    print("\nSession ended for clone:", clone_path.name)
    while True:
        print("\nWhat would you like to do with this clone?")
        print("1) Save (keep as-is)")
        print("2) Discard (delete clone)")
        print("3) Snapshot (export encrypted archive)")
        print("4) Back to main menu (do nothing)")

        choice = input("Choose (1-4): ").strip()
        if choice == "1":
            print("Clone saved:", clone_path)
            break
        elif choice == "2":
            confirm = input("Are you sure you want to permanently delete this clone? (yes/no): ").strip().lower()
            if confirm == "yes":
                shutil.rmtree(clone_path)
                print("Clone deleted.")
            else:
                print("Cancelled deletion.")
            break
        elif choice == "3":
            # call snapshot helper
            if SNAPSHOT_SCRIPT.exists():
                passphrase = input("Enter a passphrase to encrypt the snapshot (leave empty for no encryption): ")
                try:
                    subprocess.run([str(SNAPSHOT_SCRIPT), str(clone_path), passphrase], check=True)
                    print("Snapshot created.")
                except Exception as e:
                    print("Snapshot failed:", e)
            else:
                print("Snapshot script not found. Cannot snapshot.")
            break
        elif choice == "4":
            print("Returning to main menu.")
            break
        else:
            print("Invalid choice.")


def get_size_readable(path: Path):
    total = 0
    for p in path.rglob('*'):
        if p.is_file():
            try:
                total += p.stat().st_size
            except Exception:
                pass
    # human readable
    for unit in ['B', 'KB', 'MB', 'GB']:
        if total < 1024:
            return f"{total:.1f}{unit}"
        total /= 1024.0
    return f"{total:.1f}TB"


def main():
    ensure_dirs()
    while True:
        show_menu()
        choice = input("\nEnter choice: ").strip()
        if choice == "1":
            start_clone()
        elif choice == "2":
            list_clones()
        elif choice == "3":
            remove_clone()
        elif choice == "4":
            print("Bye — keep building!")
            sys.exit(0)
        else:
            print("Invalid choice — try again.")


if __name__ == "__main__":
    main()
