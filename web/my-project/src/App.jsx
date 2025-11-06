// src/App.jsx
import React, { useState, useEffect } from 'react';
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
import { authService } from './utils/api';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentPage, setCurrentPage] = useState('home');
  const [userInfo, setUserInfo] = useState(null);
  const [selectedTicketId, setSelectedTicketId] = useState(null);
  const [previousPage, setPreviousPage] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Verifica autenticação ao carregar a aplicação
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('authToken');
        console.log('App - Verificando autenticação, token existe:', !!token);
        
        if (token) {
          // Verifica se o token é válido e obtém informações do usuário
          const userInfoFromToken = authService.getUserInfo();
          console.log('App - userInfoFromToken:', userInfoFromToken);
          
          if (userInfoFromToken) {
            const userId = userInfoFromToken.sub || userInfoFromToken.id;
            console.log('App - userId extraído:', userId);
            
            // Busca informações completas do usuário da API
            try {
              const response = await fetch(`http://localhost:5000/usuarios/${userId}`, {
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              });
              
              console.log('App - Resposta da API de usuário:', response.status, response.statusText);
              
              if (response.ok) {
                const userData = await response.json();
                console.log('App - userData recebido:', userData);
                setUserInfo(userData);
                setIsLoggedIn(true);
              } else {
                // Token inválido, limpa o localStorage
                console.warn('App - Token inválido ou usuário não encontrado');
                localStorage.removeItem('authToken');
                setIsLoggedIn(false);
              }
            } catch (error) {
              console.error('App - Erro ao buscar usuário da API:', error);
              // Se não conseguir buscar da API, usa dados do token
              console.log('App - Usando dados do token como fallback');
              setUserInfo(userInfoFromToken);
              setIsLoggedIn(true);
            }
          } else {
            // Token inválido
            console.warn('App - Token inválido (não foi possível decodificar)');
            localStorage.removeItem('authToken');
            setIsLoggedIn(false);
          }
        } else {
          console.log('App - Nenhum token encontrado');
          setIsLoggedIn(false);
        }
      } catch (error) {
        console.error('App - Erro ao verificar autenticação:', error);
        localStorage.removeItem('authToken');
        setIsLoggedIn(false);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const handleLoginSuccess = async (userData) => {
    setIsLoggedIn(true);
    setCurrentPage('home');
    
    // Se userData não tiver nome completo, busca da API
    if (!userData?.nome || !userData?.id) {
      try {
        const token = localStorage.getItem('authToken');
        const userId = userData?.id;
        
        if (token && userId) {
          const response = await fetch(`http://localhost:5000/usuarios/${userId}`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          
          if (response.ok) {
            const fullUserData = await response.json();
            console.log('App - handleLoginSuccess - Dados completos:', fullUserData);
            setUserInfo(fullUserData);
            return;
          }
        }
      } catch (error) {
        console.error('App - Erro ao buscar dados completos após login:', error);
      }
    }
    
    console.log('App - handleLoginSuccess - userData:', userData);
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

  // Mostra loading enquanto verifica autenticação
  if (isLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        fontSize: '18px'
      }}>
        Carregando...
      </div>
    );
  }

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