const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('ffapi', {
  startClone: () => ipcRenderer.invoke('backend:start-clone'),
  listClones: () => ipcRenderer.invoke('backend:list-clones'),
  snapshotClone: (name, pass) => ipcRenderer.invoke('backend:snapshot-clone', name, pass)
});
