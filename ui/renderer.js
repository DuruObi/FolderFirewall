// ui/renderer.js

const startBtn = document.getElementById('startBtn');
const sessionsTable = document.getElementById('sessionsTable');

async function refreshSessions() {
  const data = await window.api.listSessions();
  sessionsTable.innerHTML = '';
  data.sessions.forEach(s => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${s.id}</td>
      <td>${s.status}</td>
      <td>${s.sandbox || ''}</td>
      <td>
        ${s.status === 'running' ? `<button onclick="stopSession('${s.id}')">Stop</button>` : ''}
      </td>
    `;
    sessionsTable.appendChild(row);
  });
}

async function startSession() {
  await window.api.startSession();
  refreshSessions();
}

async function stopSession(id) {
  await window.api.stopSession(id);
  refreshSessions();
}

startBtn.addEventListener('click', startSession);
refreshSessions();
setInterval(refreshSessions, 3000); // auto-refresh every 3s
