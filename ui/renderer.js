<<<<<<< HEAD
...paste renderer.js content...
=======
// ui/renderer.js
const folder = document.getElementById('folder');
const app = document.getElementById('app');
const output = document.getElementById('output');
const manage = document.getElementById('manage');
const back = document.getElementById('back');
const clonesSelect = document.getElementById('clones-select');

folder.addEventListener('click', () => {
  folder.classList.add('hidden');
  app.classList.remove('hidden');
});

document.getElementById('btn-start').addEventListener('click', async () => {
  output.textContent = 'Creating clone...';
  const res = await window.ffapi.startClone();
  if (res.ok) {
    output.textContent = `Clone created: ${res.clone} at ${res.path}`;
  } else {
    output.textContent = `Error: ${res.error}`;
  }
});

document.getElementById('btn-manage').addEventListener('click', async () => {
  manage.classList.remove('hidden');
  back.classList.remove('hidden');
  // populate clones
  const r = await window.ffapi.listClones();
  if (r.ok) {
    clonesSelect.innerHTML = '';
    if (r.clones.length === 0) {
      clonesSelect.innerHTML = '<option value="">(no clones found)</option>';
    } else {
      r.clones.forEach(c => {
        const o = document.createElement('option');
        o.value = c;
        o.text = c;
        clonesSelect.appendChild(o);
      });
    }
  } else {
    output.textContent = 'Error listing clones: ' + r.error;
  }
});

document.getElementById('btn-list').addEventListener('click', async () => {
  output.textContent = 'Listing clones...';
  const r = await window.ffapi.listClones();
  if (r.ok) output.textContent = r.clones.join('\n') || '(no clones)';
  else output.textContent = 'Error: ' + r.error;
});

document.getElementById('btn-snapshot').addEventListener('click', async () => {
  const name = clonesSelect.value;
  if (!name) return (output.textContent = 'No clone selected');
  const pass = document.getElementById('pass').value || '';
  output.textContent = 'Creating snapshot...';
  const r = await window.ffapi.snapshotClone(name, pass);
  if (r.ok) output.textContent = 'Snapshot success:\n' + r.out;
  else output.textContent = 'Snapshot failed: ' + JSON.stringify(r);
});

back.addEventListener('click', () => {
  manage.classList.add('hidden');
  back.classList.add('hidden');
  app.classList.remove('hidden');
});
>>>>>>> origin/main
