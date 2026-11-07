const form = document.querySelector('#new-task');
const list = document.querySelector('#tasks');
const status = document.querySelector('#status');
async function request(path, options = {}) {
  const response = await fetch(path, {headers: {'Content-Type': 'application/json'}, ...options});
  if (!response.ok) throw new Error(`API ${response.status}：${await response.text()}`);
  return response.status === 204 ? null : response.json();
}
async function perform(action) {
  status.textContent = '処理しています…';
  try { await action(); await refresh(); status.textContent = ''; }
  catch (error) { status.textContent = `エラー：${error.message}`; }
}
async function refresh() {
  const tasks = await request('/api/tasks');
  list.replaceChildren();
  for (const task of tasks) {
    const item = document.createElement('li');
    const title = document.createElement('span');
    title.textContent = task.title; title.className = task.completed ? 'done' : '';
    const description = document.createElement('small'); description.textContent = task.description;
    const toggle = document.createElement('input'); toggle.type = 'checkbox'; toggle.checked = task.completed;
    toggle.setAttribute('aria-label', `完了：${task.title}`);
    toggle.onchange = () => perform(() => request(`/api/tasks/${task.id}`, {method: 'PATCH', body: JSON.stringify({completed: toggle.checked})}));
    const edit = document.createElement('button'); edit.textContent = '編集';
    edit.onclick = () => {
      const value = prompt('新しいタスク名', task.title);
      if (value === null) return;
      const detail = prompt('新しい説明', task.description);
      if (detail !== null) perform(() => request(`/api/tasks/${task.id}`, {method: 'PATCH', body: JSON.stringify({title: value, description: detail})}));
    };
    const remove = document.createElement('button'); remove.textContent = '削除';
    remove.onclick = () => perform(() => request(`/api/tasks/${task.id}`, {method: 'DELETE'}));
    item.append(toggle, title, description, edit, remove); list.append(item);
  }
}
form.onsubmit = event => {
  event.preventDefault(); const data = Object.fromEntries(new FormData(form));
  perform(async () => { await request('/api/tasks', {method: 'POST', body: JSON.stringify(data)}); form.reset(); });
};
perform(async () => {});
