const repoOwner = 'KEXNARV'; // change if forked
const repoName = 'KEXNARV.github.io';
const usersFile = 'users.enc';

<<<<<<< HEAD
=======
const githubToken = '';

>>>>>>> codex/modificar-inicio-de-sesión-para-compatibilidad-con-github-pa
const userData = {
  users: [],
  async load() {
    try {
      const res = await fetch(usersFile + '?t=' + Date.now());
      if (!res.ok) throw new Error('fetch failed');
      const txt = await res.text();
      this.users = JSON.parse(atob(txt.trim()));
    } catch (e) {
      this.users = [{username:'Kex', password:'JouleNW2027', role:'root', active:true}];
    }
  },
  async save() {
<<<<<<< HEAD
    const token = localStorage.getItem('githubToken');
    if (!token) {
      alert('GitHub token no definido');
=======
    const token = githubToken;
    if (!token) {
      console.warn('GitHub token no definido');
>>>>>>> codex/modificar-inicio-de-sesión-para-compatibilidad-con-github-pa
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
};
