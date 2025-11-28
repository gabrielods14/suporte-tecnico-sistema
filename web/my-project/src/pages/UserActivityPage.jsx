// src/pages/UserActivityPage.jsx
import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import Footer from '../components/Footer';
import LoadingScreen from '../components/LoadingScreen';
import '../styles/user-activity.css';
import { userService, ticketService } from '../utils/api';

function mapStatusLabel(status) {
  const s = Number(status);
  if (s === 1) return 'Aberto';
  if (s === 2) return 'Em Atendimento';
  if (s === 3) return 'Fechado';
  return 'Desconhecido';
}

function mapPermissaoLabel(perm) {
  const p = Number(perm);
  if (p === 1) return 'Colaborador';
  if (p === 2) return 'Suporte Técnico';
  if (p === 3) return 'Administrador';
  return 'Desconhecido';
}

function UserActivityPage({ onLogout, onNavigateToHome, onNavigateToPage, currentPage, userInfo, onNavigateToProfile, userId, onBack }) {
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);
  const [ticketsOpened, setTicketsOpened] = useState([]);
  const [ticketsResolved, setTicketsResolved] = useState([]);
  const [loginCount, setLoginCount] = useState(null);

  useEffect(() => {
    const id = userId || Number(localStorage.getItem('selectedUserId'));
    if (!id) {
      setLoading(false);
      return;
    }
    loadActivity(id);
  }, [userId]);

  const loadActivity = async (id) => {
    try {
      setLoading(true);
      
      // Buscar dados do usuário
      let u;
      try {
        u = await userService.getUser(id);
        console.log('User data loaded:', u);
      } catch (e) {
        console.error('Erro ao buscar usuário individual, tentando fallback:', e);
        // Fallback: obter lista completa e procurar
        try {
          const allData = await userService.getUsers();
          let allUsers = [];
          
          if (Array.isArray(allData)) {
            allUsers = allData;
          } else if (allData?.usuarios && Array.isArray(allData.usuarios)) {
            allUsers = allData.usuarios;
          } else if (allData?.items && Array.isArray(allData.items)) {
            allUsers = allData.items;
          } else if (allData?.users && Array.isArray(allData.users)) {
            allUsers = allData.users;
          }
          
          u = allUsers.find(x => Number(x.id) === Number(id));
          if (u) console.log('User found via fallback:', u);
        } catch (fallbackError) {
          console.error('Fallback também falhou:', fallbackError);
        }
      }
      
      setUser(u || { id, nome: `Usuário ${id}` });

      // Buscar chamados abertos pelo usuário
      let ticketsData = [];
      try {
        const opened = await ticketService.getTickets({ solicitanteId: id });
        ticketsData = Array.isArray(opened) ? opened : [];
        console.log('Tickets opened by user:', ticketsData);
      } catch (e) {
        console.error('Erro ao buscar chamados do usuário:', e);
        
        // Fallback: buscar todos e filtrar
        try {
          const allTickets = await ticketService.getTickets();
          const allList = Array.isArray(allTickets) ? allTickets : [];
          ticketsData = allList.filter(t => Number(t.solicitanteId) === Number(id));
          console.log('Tickets found via fallback:', ticketsData);
        } catch (fallbackError) {
          console.error('Fallback para tickets também falhou:', fallbackError);
        }
      }
      
      setTicketsOpened(ticketsData);

      // Separar resolvidos dos abertos
      const resolvedByUser = ticketsData.filter(t => Number(t.status) === 3);
      const openByUser = ticketsData.filter(t => Number(t.status) !== 3);
      
      // Para técnicos, incluir chamados onde ele é responsável
      if (u && Number(u.permissao) === 2) {
        try {
          const assigned = await ticketService.getTickets();
          const assignedList = Array.isArray(assigned) ? assigned : [];
          const resolvedByTech = assignedList.filter(t => {
            const techId = t.tecnicoResponsavel?.id || t.tecnicoResponsavelId;
            return Number(techId) === Number(id) && Number(t.status) === 3;
          });
          resolvedByUser.push(...resolvedByTech);
        } catch (e) {
          console.error('Erro ao buscar chamados atribuídos ao técnico:', e);
        }
      }
      
      setTicketsOpened(openByUser);
      setTicketsResolved(resolvedByUser);

      // Tentar buscar contagem de logins (endpoint opcional)
      try {
        const resp = await fetch(`http://localhost:5000/api/Usuarios/${id}/logins`, {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` }
        });
        if (resp.ok) {
          const data = await resp.json();
          if (typeof data === 'object' && data.count !== undefined) {
            setLoginCount(data.count);
          } else if (Array.isArray(data)) {
            setLoginCount(data.length);
          }
        }
      } catch (e) {
        console.log('Endpoint de logins não disponível:', e.message);
      }

    } catch (error) {
      console.error('Erro ao carregar atividade do usuário:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (s) => {
    if (!s) return 'N/A';
    try { return new Date(s).toLocaleString('pt-BR'); } catch { return s; }
  };

  const calcOpenTime = (ticket) => {
    try {
      const open = new Date(ticket.dataAbertura || ticket.createdAt || ticket.created_at);
      const close = ticket.dataFechamento ? new Date(ticket.dataFechamento) : new Date();
      const diff = Math.abs(close - open);
      const days = Math.floor(diff / (1000*60*60*24));
      const hours = Math.floor((diff % (1000*60*60*24)) / (1000*60*60));
      return `${days}d ${hours}h`;
    } catch {
      return 'N/A';
    }
  };

  if (loading) {
    return <LoadingScreen message="Aguarde..." />;
  }

  return (
    <div className="user-activity-page">
      <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} userInfo={userInfo} />
      <Header onLogout={onLogout} userName={userInfo?.nome} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />

      <main className="user-activity-main">
        <button 
          className="back-button" 
          onClick={() => { if (onBack) onBack(); else onNavigateToPage('reports'); }}
          aria-label="Voltar para relatórios"
        >
          ← Voltar
        </button>
        
        <div className="page-header">
          <h1>ATIVIDADE DO USUÁRIO</h1>
        </div>

        <div className="user-summary">
          <h2>{user?.nome || `Usuário ${user?.id || ''}`}</h2>
          <p><strong>ID:</strong> {user?.id}</p>
          <p><strong>E-mail:</strong> {user?.email || 'N/A'}</p>
          <p><strong>Cargo:</strong> {user?.cargo || 'N/A'}</p>
          <p><strong>Permissão:</strong> {mapPermissaoLabel(user?.permissao)}</p>
          <p><strong>Logins:</strong> {loginCount === null ? 'N/D' : loginCount}</p>
        </div>

        <div className="section-card">
          <h2>CHAMADOS ABERTOS PELO USUÁRIO ({ticketsOpened.length})</h2>
          <div className="table-section">
            <table className="tickets-table">
              <thead>
                <tr>
                  <th>CÓDIGO</th>
                  <th>TÍTULO</th>
                  <th>STATUS</th>
                  <th>DATA ABERTURA</th>
                  <th>TEMPO ABERTO</th>
                </tr>
              </thead>
              <tbody>
                {ticketsOpened.length === 0 ? (
                  <tr>
                    <td colSpan="5" style={{ textAlign: 'center', padding: '3rem', color: '#999', fontStyle: 'italic' }}>
                      Nenhum chamado aberto encontrado
                    </td>
                  </tr>
                ) : (
                  ticketsOpened.map(t => (
                    <tr key={t.id}>
                      <td className="code-cell">{String(t.id).padStart(6,'0')}</td>
                      <td className="title-cell">{t.titulo}</td>
                      <td>{mapStatusLabel(t.status)}</td>
                      <td className="date-cell">{formatDate(t.dataAbertura || t.createdAt)}</td>
                      <td className="date-cell">{calcOpenTime(t)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        <div className="section-card">
          <h2>CHAMADOS RESOLVIDOS ({ticketsResolved.length})</h2>
          <div className="table-section">
            <table className="tickets-table">
              <thead>
                <tr>
                  <th>CÓDIGO</th>
                  <th>TÍTULO</th>
                  <th>DATA ABERTURA</th>
                  <th>DATA FECHAMENTO</th>
                  <th>TEMPO ABERTO</th>
                </tr>
              </thead>
              <tbody>
                {ticketsResolved.length === 0 ? (
                  <tr>
                    <td colSpan="5" style={{ textAlign: 'center', padding: '3rem', color: '#999', fontStyle: 'italic' }}>
                      Nenhum chamado resolvido encontrado
                    </td>
                  </tr>
                ) : (
                  ticketsResolved.map(t => (
                    <tr key={t.id}>
                      <td className="code-cell">{String(t.id).padStart(6,'0')}</td>
                      <td className="title-cell">{t.titulo}</td>
                      <td className="date-cell">{formatDate(t.dataAbertura)}</td>
                      <td className="date-cell">{formatDate(t.dataFechamento)}</td>
                      <td className="date-cell">{calcOpenTime(t)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

      </main>
      <Footer />
    </div>
  );
}

export default UserActivityPage;
