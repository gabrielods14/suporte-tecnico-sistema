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
      
      const isColaborador = userInfo?.permissao === 1;
      const filters = {};
      
      if (isColaborador) {
        let userId = userInfo?.id;
        if (!userId) {
          try {
            const token = localStorage.getItem('authToken');
            if (token) {
              const payload = JSON.parse(atob(token.split('.')[1]));
              userId = payload?.sub || payload?.id;
            }
          } catch (e) {
            console.error('Erro ao decodificar token:', e);
          }
        }
        
        if (userId) {
          filters.solicitanteId = Number(userId);
        }
      }
      
      try {
        const apiTickets = await ticketService.getTickets(filters);
        if (apiTickets && apiTickets.length > 0) {
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
          
          let filteredTickets = apiTickets.filter(item => {
            const status = item.status;
            return status === 1 || status === 2 || status === 4;
          });
          
          if (isColaborador) {
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
              filteredTickets = filteredTickets.filter(item => {
                const solicitanteId = item.solicitanteId || item.SolicitanteId;
                return Number(solicitanteId) === userId;
              });
            }
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
          return;
        }
      } catch (apiError) {
        console.error('Erro ao carregar chamados da API:', apiError);
      }
      
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
        <Header onLogout={onLogout} userName={userInfo?.nome || 'Usuário'} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
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
      <Header onLogout={onLogout} userName={userInfo?.nome} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
      
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
