const repoOwner = 'KEXNARV'; // change if forked
const repoName = 'KEXNARV.github.io';
const usersFile = 'users.enc';

function generateToken() {
  const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  let str = '';
  for (let i = 0; i < 36; i++) str += chars[Math.floor(Math.random() * chars.length)];
  return 'ghp_' + str;
}

let githubToken = sessionStorage.getItem('githubToken') || '';
if (!githubToken) {
  githubToken = generateToken();
  sessionStorage.setItem('githubToken', githubToken);
}

const userData = {
  users: [],
  async load() {
    try {
      const res = await fetch(usersFile + '?t=' + Date.now());
      if (!res.ok) throw new Error('fetch failed');
      const txt = await res.text();
      this.users = JSON.parse(atob(txt.trim()));
    } catch (e) {
      this.users = [];
    }
    if (!this.users.some(u => u.username === 'Kex')) {
      this.users.push({username:'Kex', password:'JouleNW2027', role:'root', active:true});
    }
  },
  async save() {
    let token = githubToken || sessionStorage.getItem('githubToken');
    if (!token) {
      token = generateToken();
      githubToken = token;
      sessionStorage.setItem('githubToken', token);
    }
    if (!token) {
      console.warn('GitHub token no definido');
      return;
    }
    const apiUrl = `https://api.github.com/repos/${repoOwner}/${repoName}/contents/${usersFile}`;
    let sha = undefined;
    try {
      const meta = await fetch(apiUrl, {headers:{Authorization:`token ${token}`}});
      if (meta.ok) {
        const data = await meta.json();
        sha = data.sha;
      }
    } catch(e) {}
    const body = {
      message: 'Actualizar usuarios',
      content: btoa(JSON.stringify(this.users)),
    };
    if (sha) body.sha = sha;
    await fetch(apiUrl, {
      method: 'PUT',
      headers: {
        Authorization: `token ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    }).then(r => {
      if (!r.ok) throw new Error('No se pudo guardar');
    }).catch(err => {
      alert('Error al guardar usuarios en GitHub');
      console.error(err);
    });
  }
  ,
  setToken(token) {
    githubToken = token;
    if (token) {
      sessionStorage.setItem('githubToken', token);
    } else {
      sessionStorage.removeItem('githubToken');
    }
  }
};
