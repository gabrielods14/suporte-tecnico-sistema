// src/pages/PendingTicketsPage.jsx
import React, { useState, useEffect } from 'react';
import '../styles/pending-tickets.css';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import { FaClipboardList, FaSearch, FaFilter } from 'react-icons/fa';
import { ticketService } from '../utils/api';

function PendingTicketsPage({ onLogout, onNavigateToHome, onNavigateToPage, currentPage, userInfo, onNavigateToTicketDetail, onNavigateToProfile }) {
  const handleTicketClick = (ticketId) => {
    if (onNavigateToTicketDetail) {
      onNavigateToTicketDetail(ticketId, 'pending-tickets');
    }
  };
  const [tickets, setTickets] = useState([]);
  const [filteredTickets, setFilteredTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('codigo'); // codigo, titulo, prioridade, dataLimite
  const [sortOrder, setSortOrder] = useState('asc'); // asc, desc

  

  useEffect(() => {
    loadTickets();
  }, [userInfo?.id, userInfo?.permissao]);

  useEffect(() => {
    applyFiltersAndSort();
  }, [tickets, searchTerm, sortBy, sortOrder]);

  const loadTickets = async () => {
    try {
      setLoading(true);
      
      // Debug: verificar informações do usuário
      console.log('=== DEBUG PendingTicketsPage ===');
      console.log('userInfo completo:', userInfo);
      console.log('userInfo.id:', userInfo?.id);
      console.log('userInfo.permissao:', userInfo?.permissao);
      
      // Determinar se é usuário comum (permissão 1) que deve ver apenas seus chamados
      // Técnicos (2) e Admins (3) veem todos os chamados
      const isColaborador = userInfo?.permissao === 1;
      const filters = {};
      
      // Apenas colaboradores devem ter seus chamados filtrados
      // Técnicos e Admins veem todos os chamados (sem filtro)
      if (isColaborador) {
        // Tentar obter o ID do userInfo ou do token como fallback
        let userId = userInfo?.id;
        if (!userId) {
          // Tentar obter do token JWT como fallback
          try {
            const token = localStorage.getItem('authToken');
            if (token) {
              const payload = JSON.parse(atob(token.split('.')[1]));
              userId = payload?.sub || payload?.id;
              console.log('⚠️ userInfo.id não encontrado, usando ID do token:', userId);
            }
          } catch (e) {
            console.error('Erro ao decodificar token:', e);
          }
        }
        
        if (userId) {
          filters.solicitanteId = Number(userId);
          console.log('✅ Filtrando chamados para colaborador ID:', filters.solicitanteId);
        } else {
          console.error('❌ ERRO: Não foi possível obter o ID do usuário para filtrar chamados!');
          console.error('userInfo completo:', userInfo);
          console.error('Token disponível:', !!localStorage.getItem('authToken'));
        }
      } else if (!isColaborador) {
        console.log('✅ Usuário é técnico/admin (permissão:', userInfo?.permissao, ') - mostrando todos os chamados');
      }
      
      // Tentar carregar da API real primeiro
      try {
        console.log('Buscando chamados com filtros:', filters);
        const apiTickets = await ticketService.getTickets(filters);
        console.log('Chamados recebidos da API:', apiTickets?.length || 0, 'chamados');
        if (apiTickets && apiTickets.length > 0) {
          console.log('Primeiro chamado (exemplo):', apiTickets[0]);
          const mapPriority = (p) => {
            if (typeof p === 'number') {
              return p === 3 ? 'ALTA' : p === 2 ? 'MÉDIA' : 'BAIXA';
            }
            const val = (p || '').toString().toLowerCase();
            if (val.includes('alta')) return 'ALTA';
            if (val.includes('medi')) return 'MÉDIA';
            if (val.includes('baix')) return 'BAIXA';
            return 'MÉDIA';
          };
          // Filtrar chamados com status: Aberto (1), Em Andamento (2) ou Resolvido (4)
          // Colaboradores precisam ver seus chamados abertos também!
          let filteredTickets = apiTickets.filter(item => {
            const status = item.status;
            // Status válidos: 1 (Aberto), 2 (Em Andamento), 4 (Resolvido)
            const isValidStatus = status === 1 || status === 2 || status === 4;
            if (!isValidStatus) {
              console.log(`Chamado ${item.id} com status ${status} foi filtrado (não está aberto/em andamento/resolvido)`);
            }
            return isValidStatus;
          });
          console.log(`Chamados após filtro de status (1, 2 ou 4): ${filteredTickets.length}`);
          
          // IMPORTANTE: Se for colaborador (permissão 1), garantir que só vê seus próprios chamados
          // Este é um filtro de segurança adicional no frontend (o backend já filtra, mas garantimos aqui também)
          // Técnicos (permissão 2) e Admins (permissão 3) veem TODOS os chamados
          if (isColaborador) {
            // Obter userId (do userInfo ou do token como fallback)
            let userId = userInfo?.id;
            if (!userId) {
              try {
                const token = localStorage.getItem('authToken');
                if (token) {
                  const payload = JSON.parse(atob(token.split('.')[1]));
                  userId = payload?.sub || payload?.id;
                }
              } catch (e) {
                console.error('Erro ao obter userId do token:', e);
              }
            }
            
            if (userId) {
              userId = Number(userId);
              const beforeFilter = filteredTickets.length;
              filteredTickets = filteredTickets.filter(item => {
                // A API pode retornar SolicitanteId (C#) ou solicitanteId (JSON)
                const solicitanteId = item.solicitanteId || item.SolicitanteId;
                const solicitanteIdNum = Number(solicitanteId);
                const match = solicitanteIdNum === userId;
                if (!match) {
                  console.log(`❌ Chamado ${item.id} não pertence ao usuário ${userId} (solicitanteId: ${solicitanteId})`);
                } else {
                  console.log(`✅ Chamado ${item.id} pertence ao usuário ${userId} (status: ${item.status})`);
                }
                return match;
              });
              console.log(`✅ Colaborador ID ${userId}: ${beforeFilter} → ${filteredTickets.length} chamados após filtro por solicitanteId`);
              if (filteredTickets.length === 0 && beforeFilter > 0) {
                console.warn(`⚠️ ATENÇÃO: ${beforeFilter} chamados foram filtrados por solicitanteId. Verifique se o ID está correto: ${userId}`);
                console.warn('Primeiro chamado exemplo:', apiTickets[0]);
              }
            } else {
              console.error('❌ ERRO: Não foi possível obter userId para filtrar chamados!');
            }
          } else {
            // Técnicos e Admins veem TODOS os chamados
            console.log(`✅ Técnico/Admin vê todos os ${filteredTickets.length} chamados`);
          }
        
        const mapped = filteredTickets
          .map(item => {
            const abertura = item.dataAbertura ? new Date(item.dataAbertura) : new Date();
            const limite = new Date(abertura);
            limite.setDate(limite.getDate() + 7);
            return {
              id: item.id,
              codigo: String(item.id).padStart(6, '0'),
              titulo: item.titulo || '',
              prioridade: mapPriority(item.prioridade),
              dataLimite: limite.toISOString(),
              status: item.status || 'ABERTO'
            };
          });
          setTickets(mapped);
          console.log(`✅ Total de ${mapped.length} chamados exibidos na lista`);
          return;
        } else {
          console.log('⚠️ Nenhum chamado retornado da API ou array vazio');
          console.log('Isso pode significar:');
          console.log('1. Não há chamados no banco de dados');
          console.log('2. Os chamados não pertencem a este usuário (se for colaborador)');
          console.log('3. Os chamados não têm status 1, 2 ou 4');
          console.log('userInfo atual:', userInfo);
        }
      } catch (apiError) {
        console.error('❌ Erro ao carregar chamados da API:', apiError);
        console.error('Detalhes do erro:', apiError.message);
      }
      
      // Se a API falhar, usar array vazio
      console.log('⚠️ Definindo lista de chamados como vazia');
      setTickets([]);
    } catch (error) {
      console.error('Erro ao carregar tickets:', error);
      setTickets([]);
    } finally {
      setLoading(false);
    }
  };

  const applyFiltersAndSort = () => {
    let filtered = [...tickets];

    // Aplicar filtro de busca
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      filtered = filtered.filter(ticket => 
        ticket.titulo.toLowerCase().includes(searchLower) ||
        ticket.codigo.toLowerCase().includes(searchLower)
      );
    }

    // Aplicar ordenação
    filtered.sort((a, b) => {
      let aValue, bValue;

      switch (sortBy) {
        case 'codigo':
          aValue = parseInt(a.codigo);
          bValue = parseInt(b.codigo);
          break;
        case 'titulo':
          aValue = a.titulo.toLowerCase();
          bValue = b.titulo.toLowerCase();
          break;
        case 'prioridade':
          const priorityOrder = { 'ALTA': 1, 'MÉDIA': 2, 'BAIXA': 3 };
          aValue = priorityOrder[a.prioridade] || 4;
          bValue = priorityOrder[b.prioridade] || 4;
          break;
        case 'dataLimite':
          aValue = new Date(a.dataLimite);
          bValue = new Date(b.dataLimite);
          break;
        default:
          return 0;
      }

      if (aValue < bValue) return sortOrder === 'asc' ? -1 : 1;
      if (aValue > bValue) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });

    setFilteredTickets(filtered);
  };

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('asc');
    }
  };

  const calculateDaysToExpire = (dataLimite) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const limitDate = new Date(dataLimite);
    limitDate.setHours(0, 0, 0, 0);
    const diffTime = limitDate.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) {
      return `Vencido há ${Math.abs(diffDays)} dias`;
    } else if (diffDays === 0) {
      return 'Vence hoje';
    } else {
      return `Faltam ${diffDays} dias`;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'ALTA': return '#dc3545';
      case 'MÉDIA': return '#ffc107';
      case 'BAIXA': return '#28a745';
      default: return '#6c757d';
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
  };

  if (loading) {
    return (
      <div className="pending-tickets-page">
        <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} />
        <Header onLogout={onLogout} userName={userInfo?.nome} onNavigateToProfile={onNavigateToProfile} />
        <main className="pending-tickets-main">
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Carregando chamados...</p>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="pending-tickets-page">
      <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} />
      <Header onLogout={onLogout} userName={userInfo?.nome} />
      
      <main className="pending-tickets-main">
        {/* Header da página */}
        <div className="page-header">
          <h1>CHAMADOS EM ANDAMENTO</h1>
        </div>

        {/* Filtros */}
        <div className="filters-section">
          <div className="search-box">
            <FaSearch className="search-icon" />
            <input
              type="text"
              placeholder="Buscar por código ou título..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="sort-options">
            <label>
              <FaFilter className="filter-icon" />
              Ordenar por:
            </label>
            <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
              <option value="codigo">Código</option>
              <option value="titulo">Título</option>
              <option value="prioridade">Prioridade</option>
              <option value="dataLimite">Data Limite</option>
            </select>
            <select value={sortOrder} onChange={(e) => setSortOrder(e.target.value)}>
              <option value="asc">Crescente</option>
              <option value="desc">Decrescente</option>
            </select>
          </div>
        </div>

        {/* Tabela de chamados */}
        <div className="table-section">
          <table className="tickets-table">
            <thead>
              <tr>
                <th onClick={() => handleSort('codigo')} className="sortable">
                  CÓDIGO {sortBy === 'codigo' && (sortOrder === 'asc' ? '▲' : '▼')}
                </th>
                <th onClick={() => handleSort('titulo')} className="sortable">
                  TÍTULO {sortBy === 'titulo' && (sortOrder === 'asc' ? '▲' : '▼')}
                </th>
                <th onClick={() => handleSort('prioridade')} className="sortable">
                  PRIORIDADE {sortBy === 'prioridade' && (sortOrder === 'asc' ? '▲' : '▼')}
                </th>
                <th onClick={() => handleSort('dataLimite')} className="sortable">
                  DATA LIMITE {sortBy === 'dataLimite' && (sortOrder === 'asc' ? '▲' : '▼')}
                </th>
                <th>DIAS P/ VENCER</th>
              </tr>
            </thead>
            <tbody>
              {filteredTickets.length === 0 ? (
                <tr>
                  <td colSpan="5" className="no-data">
                    <p>Nenhum chamado encontrado</p>
                  </td>
                </tr>
              ) : (
                filteredTickets.map((ticket) => {
                  const daysToExpire = calculateDaysToExpire(ticket.dataLimite);
                  const isOverdue = daysToExpire.includes('Vencido');
                  
                  return (
                    <tr key={ticket.id} onClick={() => handleTicketClick(ticket.id)} style={{ cursor: 'pointer' }}>
                      <td className="code-cell">{ticket.codigo}</td>
                      <td className="title-cell">{ticket.titulo}</td>
                      <td>
                        <span 
                          className="priority-badge"
                          style={{ backgroundColor: getPriorityColor(ticket.prioridade) }}
                        >
                          {ticket.prioridade}
                        </span>
                      </td>
                      <td className="date-cell">{formatDate(ticket.dataLimite)}</td>
                      <td className={`days-cell ${isOverdue ? 'overdue' : ''}`}>
                        {daysToExpire}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}

export default PendingTicketsPage;
