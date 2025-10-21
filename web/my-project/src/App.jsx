// src/App.jsx
import React, { useState } from 'react';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import RegisterEmployeePage from './pages/RegisterEmployeePage';
import NewTicketPage from './pages/NewTicketPage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentPage, setCurrentPage] = useState('home');
  const [userInfo, setUserInfo] = useState(null);

  const handleLoginSuccess = (userData) => {
    setIsLoggedIn(true);
    setCurrentPage('home');
    setUserInfo(userData);
  };

  const handleLogout = () => {
    // Limpa o token de autenticação
    localStorage.removeItem('authToken');
    setIsLoggedIn(false);
    setCurrentPage('home');
    setUserInfo(null);
  };

  const navigateToRegister = () => {
    setCurrentPage('register');
  };

  const navigateToNewTicket = () => {
    setCurrentPage('newticket');
  };

  const navigateToHome = () => {
    setCurrentPage('home');
  };

  if (!isLoggedIn) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <React.Fragment>
      {currentPage === 'home' && (
        <HomePage 
          onLogout={handleLogout} 
          onNavigateToRegister={navigateToRegister}
          onNavigateToNewTicket={navigateToNewTicket}
          userInfo={userInfo}
        />
      )}
      {currentPage === 'register' && (
        <RegisterEmployeePage 
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          userInfo={userInfo}
        />
      )}
      {currentPage === 'newticket' && (
        <NewTicketPage 
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          userInfo={userInfo}
        />
      )}
    </React.Fragment>
  );
}

export default App;