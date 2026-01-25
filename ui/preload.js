// ui/preload.js
const { contextBridge } = require('electron');

const API_URL = 'http://127.0.0.1:8000';

contextBridge.exposeInMainWorld('api', {
  startSession: async () => {
    const res = await fetch(`${API_URL}/session/start`, { method: 'POST' });
    return res.json();
  },
  stopSession: async (id) => {
    const res = await fetch(`${API_URL}/session/stop/${id}`, { method: 'POST' });
    return res.json();
  },
  listSessions: async () => {
    const res = await fetch(`${API_URL}/session/list`);
    return res.json();
  },
});
