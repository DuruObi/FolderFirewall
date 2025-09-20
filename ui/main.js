<<<<<<< HEAD
...paste main.js content from above...
=======
// ui/main.js — Electron main process
const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

function createWindow() {
  const win = new BrowserWindow({
    width: 880,
    height: 620,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    },
    icon: path.join(__dirname, 'folder_icon.png')
  });

  win.loadFile(path.join(__dirname, 'index.html'));
  // win.webContents.openDevTools(); // uncomment for debugging
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

// Helper to run backend commands
function runBackend(args, onData, onClose, onError) {
  // Use python3 from PATH
  const py = spawn('python3', [path.join(process.cwd(), 'backend', 'app.py'), ...args], { cwd: process.cwd() });

  py.stdout.on('data', (d) => onData && onData(d.toString()));
  py.stderr.on('data', (d) => onData && onData(d.toString()));
  py.on('close', (code) => onClose && onClose(code));
  py.on('error', (err) => onError && onError(err));
  return py;
}

// IPC handlers from renderer
ipcMain.handle('backend:start-clone', async (evt) => {
  // We'll run backend/app.py in an ephemeral mode: start clone then exit.
  // The backend CLI as written opens an interactive shell; to avoid that here we will
  // invoke it with a trick: run python and simulate choosing "1" then exit.
  // Simpler: call the create sample files script directly and create a clone folder name.
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const cloneId = `ui-clone-${timestamp}`;
  const clonePath = path.join(process.cwd(), 'clones', cloneId);
  try {
    const fs = require('fs');
    fs.mkdirSync(clonePath, { recursive: true });
    // Create a small indicator file
    fs.writeFileSync(path.join(clonePath, 'README_IN_CLONE.txt'),
      `Created from Electron UI at ${new Date().toISOString()}\n`);
    return { ok: true, clone: cloneId, path: clonePath };
  } catch (err) {
    return { ok: false, error: err.message };
  }
});

ipcMain.handle('backend:list-clones', async () => {
  const fs = require('fs');
  const dir = path.join(process.cwd(), 'clones');
  try {
    if (!fs.existsSync(dir)) return { ok: true, clones: [] };
    const items = fs.readdirSync(dir, { withFileTypes: true })
      .filter(d => d.isDirectory())
      .map(d => d.name)
      .sort()
      .reverse();
    return { ok: true, clones: items };
  } catch (err) {
    return { ok: false, error: err.message };
  }
});

ipcMain.handle('backend:snapshot-clone', async (evt, cloneName, passphrase) => {
  const scripts = path.join(process.cwd(), 'scripts', 'snapshot_clone.sh');
  const clonePath = path.join(process.cwd(), 'clones', cloneName);
  if (!require('fs').existsSync(scripts)) {
    return { ok: false, error: 'snapshot script not found' };
  }
  return new Promise((resolve) => {
    const py = spawn(scripts, [clonePath, passphrase || ''], { cwd: process.cwd(), shell: true });
    let out = '';
    py.stdout.on('data', d => out += d.toString());
    py.stderr.on('data', d => out += d.toString());
    py.on('close', (code) => {
      if (code === 0) resolve({ ok: true, out });
      else resolve({ ok: false, code, out });
    });
  });
});
>>>>>>> origin/main
