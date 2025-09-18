// src/App.jsx
import React, { useState } from 'react';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    // Apenas definimos o estado de login como falso
    setIsLoggedIn(false); 
    // Em uma aplicação real, você também limparia tokens de autenticação, etc.
  };

  return (
    <React.Fragment>
      {isLoggedIn ? (
        <HomePage onLogout={handleLogout} />
      ) : (
        <LoginPage onLoginSuccess={handleLoginSuccess} />
      )}
    </React.Fragment>
  );
}

export default App;