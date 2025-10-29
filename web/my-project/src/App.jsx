// src/App.jsx
import React, { useState } from 'react';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import RegisterEmployeePage from './pages/RegisterEmployeePage';
import NewTicketPage from './pages/NewTicketPage';
import PendingTicketsPage from './pages/PendingTicketsPage';
import TicketDetailPage from './pages/TicketDetailPage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentPage, setCurrentPage] = useState('home');
  const [userInfo, setUserInfo] = useState(null);
  const [selectedTicketId, setSelectedTicketId] = useState(null);

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

  const navigateToPage = (pageId) => {
    setCurrentPage(pageId);
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

  const navigateToTicketDetail = (ticketId) => {
    setSelectedTicketId(ticketId);
    setCurrentPage('ticket-detail');
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
          onNavigateToPage={navigateToPage}
          currentPage={currentPage}
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
          onNavigateToPage={navigateToPage}
          userInfo={userInfo}
        />
      )}
      {currentPage === 'pending-tickets' && (
        <PendingTicketsPage 
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          onNavigateToPage={navigateToPage}
          currentPage={currentPage}
          userInfo={userInfo}
          onNavigateToTicketDetail={navigateToTicketDetail}
        />
      )}
      {currentPage === 'ticket-detail' && (
        <TicketDetailPage 
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          onNavigateToPage={navigateToPage}
          userInfo={userInfo}
          ticketId={selectedTicketId}
        />
      )}
    </React.Fragment>
  );
}

export default App;