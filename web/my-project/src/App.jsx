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
import FirstAccessModal from './components/FirstAccessModal';
import LoadingScreen from './components/LoadingScreen';
import { authService } from './utils/api';

/**
 * Normaliza os dados do usuário para garantir que sempre temos um nome completo
 * @param {Object} userData - Dados do usuário retornados da API
 * @param {Object} tokenPayload - Payload decodificado do JWT
 * @param {string} email - Email do usuário
 * @returns {Object} Dados do usuário normalizados
 */
const normalizeUserData = (userData, tokenPayload = null, email = '') => {
  // Tenta obter nome de várias fontes (prioriza dados da API)
  let nome = userData?.nome || userData?.Nome || userData?.name || userData?.Name || '';
  
  // Se não encontrou, tenta do token
  if (!nome || nome.trim() === '') {
    if (tokenPayload) {
      nome = tokenPayload?.nome || tokenPayload?.Nome || tokenPayload?.name || tokenPayload?.Name || 
             tokenPayload?.unique_name || tokenPayload?.preferred_username || tokenPayload?.upn || '';
    }
  }
  
  // Se ainda não tem nome válido, tenta usar o email (mas só como último recurso)
  if (!nome || nome.trim() === '' || nome === email) {
    const emailToUse = userData?.email || userData?.Email || email || '';
    if (emailToUse && emailToUse.includes('@')) {
      // Extrai o nome do email, mas formata melhor
      const emailParts = emailToUse.split('@')[0].split(/[._-]/);
      nome = emailParts.map(part => part.charAt(0).toUpperCase() + part.slice(1).toLowerCase()).join(' ');
    }
  }
  
  // Garante que o nome não seja vazio
  if (!nome || nome.trim() === '') {
    nome = 'Usuário';
  }
  
  // Extrai PrimeiroAcesso de todas as possíveis variações (prioriza camelCase da API)
  // IMPORTANTE: A API está retornando em camelCase: primeiroAcesso
  const primeiroAcessoValue = userData?.primeiroAcesso !== undefined ? userData.primeiroAcesso :
                              userData?.PrimeiroAcesso !== undefined ? userData.PrimeiroAcesso :
                              userData?.primeiro_acesso !== undefined ? userData.primeiro_acesso :
                              false;
  
  console.log('🔄 normalizeUserData - PrimeiroAcesso extraído:', primeiroAcessoValue, 'Tipo:', typeof primeiroAcessoValue);
  console.log('🔄 normalizeUserData - userData completo:', JSON.stringify(userData, null, 2));
  console.log('🔄 normalizeUserData - Chaves de userData:', Object.keys(userData || {}));
  
  return {
    id: userData?.id || userData?.Id || tokenPayload?.sub || tokenPayload?.userId || tokenPayload?.id,
    nome: nome.trim(),
    email: userData?.email || userData?.Email || email || '',
    telefone: userData?.telefone || userData?.Telefone || '',
    cargo: userData?.cargo || userData?.Cargo || '',
    permissao: userData?.permissao !== undefined ? userData.permissao : 
               (userData?.Permissao !== undefined ? userData.Permissao : 
                (tokenPayload?.role ? (typeof tokenPayload.role === 'number' ? tokenPayload.role : 
                 (tokenPayload.role === 'Administrador' ? 3 : tokenPayload.role === 'SuporteTecnico' ? 2 : 1)) : 1)),
    primeiroAcesso: primeiroAcessoValue
  };
};

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentPage, setCurrentPage] = useState('home');
  const [userInfo, setUserInfo] = useState(null);
  const [selectedTicketId, setSelectedTicketId] = useState(null);
  const [previousPage, setPreviousPage] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showFirstAccessModal, setShowFirstAccessModal] = useState(false);
  
  // Debug: Log quando o estado do modal muda
  useEffect(() => {
    console.log('App - showFirstAccessModal mudou para:', showFirstAccessModal);
  }, [showFirstAccessModal]);

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
                console.log('📥 App - checkAuth - Dados do perfil recebido (RAW):', userData);
                console.log('📥 App - checkAuth - Tipo do objeto:', typeof userData);
                console.log('📥 App - checkAuth - Chaves disponíveis:', Object.keys(userData || {}));
                
                // Verifica PRIMEIRO se o campo existe antes de normalizar
                console.log('🔍 App - checkAuth - Verificando PrimeiroAcesso ANTES da normalização:');
                console.log('   userData?.PrimeiroAcesso:', userData?.PrimeiroAcesso, 'Tipo:', typeof userData?.PrimeiroAcesso);
                console.log('   userData?.primeiroAcesso:', userData?.primeiroAcesso, 'Tipo:', typeof userData?.primeiroAcesso);
                console.log('   userData completo (JSON):', JSON.stringify(userData, null, 2));
                
                // Normaliza os dados usando a função auxiliar
                const normalizedData = normalizeUserData(userData, userInfoFromToken, userData?.email || userInfoFromToken?.email);
                console.log('📦 App - checkAuth - Dados normalizados:', normalizedData);
                console.log('📦 App - checkAuth - normalizedData.primeiroAcesso:', normalizedData?.primeiroAcesso, 'Tipo:', typeof normalizedData?.primeiroAcesso);
                
                setUserInfo(normalizedData);
                setIsLoggedIn(true);
                
                // Verifica se é primeiro acesso (API retorna camelCase: primeiroAcesso)
                // Prioriza o valor BRUTO da API antes da normalização
                // IMPORTANTE: A API está retornando em camelCase, não PascalCase!
                const primeiroAcessoRaw = userData?.primeiroAcesso !== undefined ? userData.primeiroAcesso :
                                          userData?.PrimeiroAcesso !== undefined ? userData.PrimeiroAcesso :
                                          userData?.primeiro_acesso !== undefined ? userData.primeiro_acesso :
                                          normalizedData?.primeiroAcesso !== undefined ? normalizedData.primeiroAcesso :
                                          false;
                
                // Converte para boolean
                const primeiroAcesso = primeiroAcessoRaw === true || 
                                      primeiroAcessoRaw === 'true' || 
                                      primeiroAcessoRaw === 1 ||
                                      primeiroAcessoRaw === '1';
                
                console.log('🔍 App - checkAuth - Verificando PrimeiroAcesso...');
                console.log('   PrimeiroAcesso RAW:', primeiroAcessoRaw, 'Tipo:', typeof primeiroAcessoRaw);
                console.log('   PrimeiroAcesso (convertido):', primeiroAcesso);
                console.log('   Valores verificados:', {
                  'userData?.PrimeiroAcesso': userData?.PrimeiroAcesso,
                  'userData?.primeiroAcesso': userData?.primeiroAcesso,
                  'normalizedData?.primeiroAcesso': normalizedData?.primeiroAcesso,
                  'primeiroAcessoRaw': primeiroAcessoRaw,
                  'primeiroAcesso (final)': primeiroAcesso
                });
                
                if (primeiroAcesso) {
                  console.log('✅✅✅ App - checkAuth - MOSTRANDO MODAL DE PRIMEIRO ACESSO ✅✅✅');
                  // Usa setTimeout para garantir que o estado seja atualizado após o render
                  setTimeout(() => {
                    console.log('✅ App - checkAuth - setShowFirstAccessModal(true) chamado');
                    setShowFirstAccessModal(true);
                  }, 200);
                } else {
                  console.log('❌ App - checkAuth - NÃO é primeiro acesso ou campo não encontrado');
                }
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
          console.log('📥 App - handleLoginSuccess - Dados do perfil recebidos (RAW):', fullUserData);
          console.log('📥 App - handleLoginSuccess - Tipo do objeto:', typeof fullUserData);
          console.log('📥 App - handleLoginSuccess - Chaves disponíveis:', Object.keys(fullUserData || {}));
          
          // Verifica PRIMEIRO se o campo existe antes de normalizar
          console.log('🔍 App - handleLoginSuccess - Verificando PrimeiroAcesso ANTES da normalização:');
          console.log('   fullUserData?.PrimeiroAcesso:', fullUserData?.PrimeiroAcesso, 'Tipo:', typeof fullUserData?.PrimeiroAcesso);
          console.log('   fullUserData?.primeiroAcesso:', fullUserData?.primeiroAcesso, 'Tipo:', typeof fullUserData?.primeiroAcesso);
          console.log('   fullUserData completo (JSON):', JSON.stringify(fullUserData, null, 2));
          
          // Normaliza os dados usando a função auxiliar
          const tokenPayload = authService.getUserInfo();
          const normalizedData = normalizeUserData(fullUserData, tokenPayload, fullUserData?.email || userData?.email);
          console.log('📦 App - handleLoginSuccess - Dados normalizados:', normalizedData);
          console.log('📦 App - handleLoginSuccess - normalizedData.primeiroAcesso:', normalizedData?.primeiroAcesso, 'Tipo:', typeof normalizedData?.primeiroAcesso);
          
          setUserInfo(normalizedData);
          
          // Verifica se é primeiro acesso (verifica tanto nos dados normalizados quanto nos dados brutos)
          // Prioriza o valor BRUTO da API antes da normalização
          // IMPORTANTE: A API está retornando em camelCase, não PascalCase!
          const primeiroAcessoRaw = fullUserData?.primeiroAcesso !== undefined ? fullUserData.primeiroAcesso :
                                    fullUserData?.PrimeiroAcesso !== undefined ? fullUserData.PrimeiroAcesso :
                                    fullUserData?.primeiro_acesso !== undefined ? fullUserData.primeiro_acesso :
                                    normalizedData?.primeiroAcesso !== undefined ? normalizedData.primeiroAcesso :
                                    userData?.primeiroAcesso !== undefined ? userData.primeiroAcesso :
                                    userData?.PrimeiroAcesso !== undefined ? userData.PrimeiroAcesso :
                                    false;
          
          // Converte para boolean se necessário
          const primeiroAcesso = primeiroAcessoRaw === true || 
                                primeiroAcessoRaw === 'true' || 
                                primeiroAcessoRaw === 1 ||
                                primeiroAcessoRaw === '1';
          
          console.log('🔍 App - handleLoginSuccess - Verificando PrimeiroAcesso...');
          console.log('   PrimeiroAcesso RAW:', primeiroAcessoRaw, 'Tipo:', typeof primeiroAcessoRaw);
          console.log('   PrimeiroAcesso (convertido):', primeiroAcesso);
          console.log('   Valores verificados:', {
            'fullUserData?.PrimeiroAcesso': fullUserData?.PrimeiroAcesso,
            'fullUserData?.primeiroAcesso': fullUserData?.primeiroAcesso,
            'normalizedData?.primeiroAcesso': normalizedData?.primeiroAcesso,
            'userData?.PrimeiroAcesso': userData?.PrimeiroAcesso,
            'userData?.primeiroAcesso': userData?.primeiroAcesso,
            'primeiroAcessoRaw': primeiroAcessoRaw,
            'primeiroAcesso (final)': primeiroAcesso
          });
          
          if (primeiroAcesso) {
            console.log('✅✅✅ App - handleLoginSuccess - MOSTRANDO MODAL DE PRIMEIRO ACESSO ✅✅✅');
            setTimeout(() => {
              console.log('✅ App - handleLoginSuccess - setShowFirstAccessModal(true) chamado');
              setShowFirstAccessModal(true);
            }, 200);
          } else {
            console.log('❌ App - handleLoginSuccess - NÃO é primeiro acesso ou campo não encontrado');
          }
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
    console.log('App - handleLoginSuccess - Dados normalizados (fallback):', normalizedData);
    setUserInfo(normalizedData);
    
    // Verifica se é primeiro acesso no fallback também
    // IMPORTANTE: A API está retornando em camelCase: primeiroAcesso
    const primeiroAcessoRaw = userData?.primeiroAcesso !== undefined ? userData.primeiroAcesso :
                              userData?.PrimeiroAcesso !== undefined ? userData.PrimeiroAcesso :
                              userData?.primeiro_acesso !== undefined ? userData.primeiro_acesso :
                              normalizedData?.primeiroAcesso !== undefined ? normalizedData.primeiroAcesso :
                              false;
    
    const primeiroAcesso = primeiroAcessoRaw === true || 
                          primeiroAcessoRaw === 'true' || 
                          primeiroAcessoRaw === 1 ||
                          primeiroAcessoRaw === '1';
    
    console.log('App - handleLoginSuccess - PrimeiroAcesso RAW (fallback):', primeiroAcessoRaw, 'Tipo:', typeof primeiroAcessoRaw);
    console.log('App - handleLoginSuccess - PrimeiroAcesso (convertido - fallback):', primeiroAcesso);
    console.log('App - handleLoginSuccess - userData completo (fallback):', JSON.stringify(userData, null, 2));
    console.log('App - handleLoginSuccess - normalizedData (fallback):', normalizedData);
    
    if (primeiroAcesso) {
      console.log('App - handleLoginSuccess - ✅ MOSTRANDO MODAL DE PRIMEIRO ACESSO (fallback)');
      setShowFirstAccessModal(true);
    } else {
      console.log('App - handleLoginSuccess - ❌ NÃO é primeiro acesso ou campo não encontrado (fallback)');
    }
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

  const handleFirstAccessSuccess = async () => {
    // Recarrega os dados do usuário após alterar a senha
    try {
      const token = localStorage.getItem('authToken');
      if (token) {
        const response = await fetch(`http://localhost:5000/api/Usuarios/meu-perfil`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Accept': 'application/json'
          }
        });
        
        if (response.ok) {
          const userData = await response.json();
          const tokenPayload = authService.getUserInfo();
          const normalizedData = normalizeUserData(userData, tokenPayload, userData?.email);
          setUserInfo(normalizedData);
        }
      }
    } catch (error) {
      console.error('Erro ao recarregar dados do usuário:', error);
    }
    
    setShowFirstAccessModal(false);
  };

  // Mostra loading enquanto verifica autenticação
  if (isLoading) {
    return <LoadingScreen message="Carregando..." />;
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
          onNavigateToPage={navigateToPage}
          currentPage={currentPage}
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

      {/* Modal de Primeiro Acesso */}
      {console.log('App - Render - showFirstAccessModal:', showFirstAccessModal, 'Tipo:', typeof showFirstAccessModal)}
      <FirstAccessModal
        isOpen={showFirstAccessModal}
        onSuccess={handleFirstAccessSuccess}
      />
    </React.Fragment>
  );
}

export default App;