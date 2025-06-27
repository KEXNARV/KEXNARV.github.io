const DEFAULT_EMAIL = 'kex@example.com';
const DEFAULT_PASSWORD = 'JouleNW2027';

async function ensureDefaultUser() {
  try {
    await firebase.auth().createUserWithEmailAndPassword(DEFAULT_EMAIL, DEFAULT_PASSWORD);
    console.log('Default user created');
  } catch (error) {
    if (error.code !== 'auth/email-already-in-use') {
      console.error('Error creating default user:', error);
    }
  }
}

ensureDefaultUser();

async function firebaseSignIn(email, password) {
  try {
    const credential = await firebase.auth().signInWithEmailAndPassword(email, password);
    const user = credential.user;
    const role = user.email === DEFAULT_EMAIL ? 'root' : 'usuarios';
    localStorage.setItem('authenticated', 'true');
    localStorage.setItem('currentUser', JSON.stringify({ username: user.email, role }));
    window.location.href = 'index.html';
  } catch (error) {
    console.error('Firebase login error:', error);
    alert('Credenciales incorrectas');
  }
}
