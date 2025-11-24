// src/App.jsx
import React, { useState, useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import RegisterEmployeePage from './pages/RegisterEmployeePage';
import NewTicketPage from './pages/NewTicketPage';
import PendingTicketsPage from './pages/PendingTicketsPage';
import CompletedTicketsPage from './pages/CompletedTicketsPage';
import MyTicketsPage from './pages/MyTicketsPage';
import ReportsPage from './pages/ReportsPage';
import UsersReportPage from './pages/UsersReportPage';
import UserActivityPage from './pages/UserActivityPage';
import TicketDetailPage from './pages/TicketDetailPage';
import UserProfilePage from './pages/UserProfilePage';
import FAQPage from './pages/FAQPage';
import ContactPage from './pages/ContactPage';
import { authService } from './utils/api';

/**
 * Normaliza os dados do usuário para garantir que sempre temos um nome completo
 * @param {Object} userData - Dados do usuário retornados da API
 * @param {Object} tokenPayload - Payload decodificado do JWT
 * @param {string} email - Email do usuário
 * @returns {Object} Dados do usuário normalizados
 */
const normalizeUserData = (userData, tokenPayload = null, email = '') => {
  // Tenta obter nome de várias fontes
  let nome = userData?.nome || userData?.Nome || userData?.name || userData?.Name || '';
  
  // Se não encontrou, tenta do token
  if (!nome && tokenPayload) {
    nome = tokenPayload?.nome || tokenPayload?.Nome || tokenPayload?.name || tokenPayload?.Name || 
           tokenPayload?.unique_name || tokenPayload?.preferred_username || tokenPayload?.upn || '';
  }
  
  // Se ainda não tem nome, tenta usar o email
  if (!nome && email) {
    nome = email.split('@')[0];
  }
  
  return {
    id: userData?.id || userData?.Id || tokenPayload?.sub || tokenPayload?.userId || tokenPayload?.id,
    nome: nome.trim() || 'Usuário',
    email: userData?.email || userData?.Email || email || '',
    telefone: userData?.telefone || userData?.Telefone || '',
    cargo: userData?.cargo || userData?.Cargo || '',
    permissao: userData?.permissao !== undefined ? userData.permissao : 
               (userData?.Permissao !== undefined ? userData.Permissao : tokenPayload?.role || 1)
  };
};

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
            const userId = userInfoFromToken.sub || userInfoFromToken.id || userInfoFromToken.userId || userInfoFromToken.user_id;
            console.log('App - userInfoFromToken completo:', userInfoFromToken);
            console.log('App - userId extraído:', userId);
            
            // Busca informações completas do usuário usando endpoint /meu-perfil
            try {
              console.log('App - checkAuth - Buscando dados do perfil via /api/Usuarios/meu-perfil');
              const response = await fetch(`http://localhost:5000/api/Usuarios/meu-perfil`, {
                headers: {
                  'Authorization': `Bearer ${token}`,
                  'Accept': 'application/json'
                }
              });
              
              console.log('App - Resposta da API de perfil:', response.status, response.statusText);
              
              if (response.ok) {
                const userData = await response.json();
                console.log('App - Dados do perfil recebido:', userData);
                
                // Normaliza os dados usando a função auxiliar
                const normalizedData = normalizeUserData(userData, userInfoFromToken, userInfoFromToken?.email);
                console.log('App - Dados normalizados:', normalizedData);
                setUserInfo(normalizedData);
                setIsLoggedIn(true);
              } else {
                // Token inválido, limpa o localStorage
                console.warn('App - Token inválido ou usuário não encontrado');
                localStorage.removeItem('authToken');
                setIsLoggedIn(false);
              }
            } catch (error) {
              console.error('App - Erro ao buscar perfil da API:', error);
              // Se não conseguir buscar da API, usa dados do token normalizados
              console.log('App - Usando dados do token como fallback');
              const normalizedData = normalizeUserData({}, userInfoFromToken, userInfoFromToken?.email);
              setUserInfo(normalizedData);
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
    console.log('App - handleLoginSuccess - userData inicial:', userData);
    
    // Sempre tenta buscar dados completos da API após login usando /meu-perfil
    try {
      const token = localStorage.getItem('authToken');
      
      if (token) {
        console.log('App - handleLoginSuccess - Buscando dados via /api/Usuarios/meu-perfil');
        const response = await fetch(`http://localhost:5000/api/Usuarios/meu-perfil`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Accept': 'application/json'
          }
        });
        
        if (response.ok) {
          const fullUserData = await response.json();
          console.log('App - handleLoginSuccess - Dados do perfil recebidos:', fullUserData);
          
          // Normaliza os dados usando a função auxiliar
          const tokenPayload = authService.getUserInfo();
          const normalizedData = normalizeUserData(fullUserData, tokenPayload, userData?.email);
          console.log('App - handleLoginSuccess - Dados normalizados:', normalizedData);
          setUserInfo(normalizedData);
          return;
        } else {
          console.warn('App - handleLoginSuccess - Erro ao buscar perfil:', response.status);
        }
      }
    } catch (error) {
      console.error('App - Erro ao buscar perfil após login:', error);
    }
    
    // Fallback: usa os dados recebidos do login normalizados
    console.log('App - handleLoginSuccess - Usando dados do login:', userData);
    const normalizedData = normalizeUserData(userData, {}, userData?.email);
    setUserInfo(normalizedData);
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
        fontSize: '18px',
        color: '#000000'
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
      {currentPage === 'my-tickets' && (
        <MyTicketsPage 
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
        <UsersReportPage
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          onNavigateToPage={navigateToPage}
          currentPage={currentPage}
          userInfo={userInfo}
          onNavigateToProfile={navigateToProfile}
          onViewUser={(id) => { setSelectedTicketId(null); setPreviousPage('reports'); setCurrentPage('user-activity'); localStorage.setItem('selectedUserId', id); }}
        />
      )}
      {currentPage === 'dashboard' && (
        <ReportsPage 
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          onNavigateToPage={navigateToPage}
          currentPage={'dashboard'}
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
      {currentPage === 'user-activity' && (
        <UserActivityPage
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          onNavigateToPage={navigateToPage}
          currentPage={currentPage}
          userInfo={userInfo}
          onNavigateToProfile={navigateToProfile}
          userId={Number(localStorage.getItem('selectedUserId'))}
          onBack={() => setCurrentPage('reports')}
        />
      )}
      {currentPage === 'profile' && (
        <UserProfilePage 
          onLogout={handleLogout}
          onNavigateToHome={navigateToHome}
          onNavigateToPage={navigateToPage}
          onNavigateToProfile={navigateToProfile}
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