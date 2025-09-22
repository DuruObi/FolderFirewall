cat > tests/test_scripts.py <<'PYEOF'
# tests/test_scripts.py
import subprocess
import sys
import shutil
from pathlib import Path

def run_cmd(cmd, cwd=None, env=None):
    """Run a command and return CompletedProcess; raise on error."""
    res = subprocess.run(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n\nSTDOUT:\n{res.stdout}\n\nSTDERR:\n{res.stderr}")
    return res

def test_create_sample_files(tmp_path):
    """
    Test that scripts/create_sample_files.sh creates expected files and directories
    when passed a target directory (tmp_path/clone-test).
    This test invokes the script via 'bash' to avoid exec format issues on CI.
    """
    repo_root = Path.cwd()
    script = repo_root / "scripts" / "create_sample_files.sh"
    assert script.exists(), f"{script} not found in repo"

    target = tmp_path / "clone-test"
    # Call the script using 'bash' to avoid exec/permission problems on CI
    run_cmd(["bash", str(script), str(target)])

    # Check expected structure and files
    assert (target / "README_IN_CLONE.txt").exists(), "README_IN_CLONE.txt missing"
    assert (target / "docs" / "note1.txt").exists(), "docs/note1.txt missing"
    assert (target / "data" / "dummy.bin").exists(), "data/dummy.bin missing"
    assert (target / "data" / "dummy.bin").stat().st_size > 0

def test_snapshot_unencrypted_and_encrypted(tmp_path):
    """
    Test that scripts/snapshot_clone.sh creates an unencrypted tar.gz snapshot
    and an encrypted .enc snapshot when a passphrase is supplied.
    """
    repo_root = Path.cwd()
    snapshot_script = repo_root / "scripts" / "snapshot_clone.sh"
    sample_script = repo_root / "scripts" / "create_sample_files.sh"
    assert snapshot_script.exists(), f"{snapshot_script} not found"
    assert sample_script.exists(), f"{sample_script} not found"

    # Create a fake clone using the sample script
    clone_dir = tmp_path / "clone-to-snapshot"
    run_cmd(["bash", str(sample_script), str(clone_dir)])

    # Run snapshot without passphrase (should create snapshots/*.tar.gz)
    run_cmd(["bash", str(snapshot_script), str(clone_dir)])
    snapshots_dir = repo_root / "snapshots"
    found_tar = list(snapshots_dir.glob(f"{clone_dir.name}-*.tar.gz"))
    assert found_tar, f"No unencrypted snapshot found in {snapshots_dir}"
    for f in found_tar:
        try:
            f.unlink()
        except Exception:
            pass

    # Run snapshot with passphrase (should create .tar.gz.enc)
    passphrase = "test-pass-1234"
    run_cmd(["bash", str(snapshot_script), str(clone_dir), passphrase])

    found_enc = list(snapshots_dir.glob(f"{clone_dir.name}-*.tar.gz.enc"))
    assert found_enc, f"No encrypted snapshot found in {snapshots_dir}"
    for f in found_enc:
        try:
            f.unlink()
        except Exception:
            pass
PYEOF
