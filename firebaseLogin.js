async function firebaseSignIn(email, password) {
  try {
    const credential = await firebase.auth().signInWithEmailAndPassword(email, password);
    const user = credential.user;
    localStorage.setItem('authenticated', 'true');
    localStorage.setItem('currentUser', JSON.stringify({ username: user.email }));
    window.location.href = 'index.html';
  } catch (error) {
    console.error('Firebase login error:', error);
    alert('Credenciales incorrectas');
  }
}
