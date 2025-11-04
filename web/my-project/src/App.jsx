// src/App.jsx
import React, { useState } from 'react';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import RegisterEmployeePage from './pages/RegisterEmployeePage';
import NewTicketPage from './pages/NewTicketPage';
import PendingTicketsPage from './pages/PendingTicketsPage';
import CompletedTicketsPage from './pages/CompletedTicketsPage';
import ReportsPage from './pages/ReportsPage';
import TicketDetailPage from './pages/TicketDetailPage';
import UserProfilePage from './pages/UserProfilePage';
import FAQPage from './pages/FAQPage';
import ContactPage from './pages/ContactPage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentPage, setCurrentPage] = useState('home');
  const [userInfo, setUserInfo] = useState(null);
  const [selectedTicketId, setSelectedTicketId] = useState(null);
  const [previousPage, setPreviousPage] = useState(null);

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

  const navigateToTicketDetail = (ticketId, fromPage) => {
    setSelectedTicketId(ticketId);
    setPreviousPage(fromPage || currentPage);
    setCurrentPage('ticket-detail');
  };

  const navigateToProfile = () => {
    setCurrentPage('profile');
  };

  const handleUpdateUserInfo = (updatedUserInfo) => {
    setUserInfo(updatedUserInfo);
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
          onNavigateToProfile={navigateToProfile}
        />
      )}
      {currentPage === 'register' && (
        <RegisterEmployeePage 
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          userInfo={userInfo}
          onNavigateToProfile={navigateToProfile}
        />
      )}
      {currentPage === 'newticket' && (
        <NewTicketPage 
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          onNavigateToPage={navigateToPage}
          userInfo={userInfo}
          onNavigateToProfile={navigateToProfile}
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
          onNavigateToProfile={navigateToProfile}
        />
      )}
      {currentPage === 'completed-tickets' && (
        <CompletedTicketsPage 
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          onNavigateToPage={navigateToPage}
          currentPage={currentPage}
          userInfo={userInfo}
          onNavigateToTicketDetail={navigateToTicketDetail}
          onNavigateToProfile={navigateToProfile}
        />
      )}
      {currentPage === 'reports' && (
        <ReportsPage 
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          onNavigateToPage={navigateToPage}
          currentPage={currentPage}
          userInfo={userInfo}
          onNavigateToProfile={navigateToProfile}
        />
      )}
      {currentPage === 'ticket-detail' && (
        <TicketDetailPage 
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          onNavigateToPage={navigateToPage}
          userInfo={userInfo}
          ticketId={selectedTicketId}
          previousPage={previousPage}
          onNavigateToProfile={navigateToProfile}
        />
      )}
      {currentPage === 'profile' && (
        <UserProfilePage 
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          userInfo={userInfo}
          onUpdateUserInfo={handleUpdateUserInfo}
        />
      )}
      {currentPage === 'faq' && (
        <FAQPage 
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          onNavigateToPage={navigateToPage}
          currentPage={currentPage}
          userInfo={userInfo}
          onNavigateToProfile={navigateToProfile}
        />
      )}
      {currentPage === 'contact' && (
        <ContactPage 
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          onNavigateToPage={navigateToPage}
          currentPage={currentPage}
          userInfo={userInfo}
          onNavigateToProfile={navigateToProfile}
        />
      )}
    </React.Fragment>
  );
}

export default App;