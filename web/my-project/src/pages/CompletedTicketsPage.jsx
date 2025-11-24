// src/pages/CompletedTicketsPage.jsx
import React, { useState, useEffect } from 'react';
import '../styles/completed-tickets.css';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import { FaCheckCircle, FaSearch, FaFilter } from 'react-icons/fa';
import { ticketService } from '../utils/api';

function CompletedTicketsPage({ onLogout, onNavigateToHome, onNavigateToPage, currentPage, userInfo, onNavigateToTicketDetail, onNavigateToProfile }) {
  const [tickets, setTickets] = useState([]);
  const [filteredTickets, setFilteredTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('dataFechamento'); // codigo, titulo, prioridade, dataFechamento
  const [sortOrder, setSortOrder] = useState('desc'); // asc, desc

  const handleTicketClick = (ticketId) => {
    if (onNavigateToTicketDetail) {
      onNavigateToTicketDetail(ticketId, 'completed-tickets');
    }
  };

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
      const filters = {
        status: 3
      };
      
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
        
        let filteredTickets = apiTickets.filter(item => item.status === 3);
        
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
          .map(item => ({
            id: item.id,
            codigo: String(item.id).padStart(6, '0'),
            titulo: item.titulo || '',
            prioridade: mapPriority(item.prioridade),
            dataFechamento: item.dataFechamento || item.dataAbertura,
            status: item.status,
            tecnico: item.tecnicoResponsavel?.nome || 'N/A'
          }));
        
        setTickets(mapped);
        return;
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
        case 'dataFechamento':
          aValue = new Date(a.dataFechamento);
          bValue = new Date(b.dataFechamento);
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
      setSortOrder('desc');
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

  const getStatusText = (status) => {
    switch (status) {
      case 3: return 'FECHADO';
      case 4: return 'RESOLVIDO';
      case 5: return 'CONCLUÍDO';
      default: return 'N/A';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 3: return '#6c757d';
      case 4: return '#28a745';
      case 5: return '#6c757d';
      default: return '#6c757d';
    }
  };

  if (loading) {
    return (
      <div className="completed-tickets-page">
        <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} userInfo={userInfo} />
        <Header onLogout={onLogout} userName={userInfo?.nome || 'Usuário'} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
        <main className="completed-tickets-main">
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Carregando...</p>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="completed-tickets-page">
      <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} userInfo={userInfo} />
      <Header onLogout={onLogout} userName={userInfo?.nome} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
      
      <main className="completed-tickets-main">
        <button 
          className="back-button" 
          onClick={onNavigateToHome}
          aria-label="Voltar para página inicial"
        >
          ← Voltar
        </button>
        
        {/* Header da página */}
        <div className="page-header">
          <h1>CHAMADOS CONCLUÍDOS</h1>
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
              <option value="dataFechamento">Data de Fechamento</option>
            </select>
            <select value={sortOrder} onChange={(e) => setSortOrder(e.target.value)}>
              <option value="desc">Mais Recente</option>
              <option value="asc">Mais Antigo</option>
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
                <th>STATUS</th>
                <th>TÉCNICO</th>
                <th onClick={() => handleSort('dataFechamento')} className="sortable">
                  DATA FECHAMENTO {sortBy === 'dataFechamento' && (sortOrder === 'asc' ? '▲' : '▼')}
                </th>
              </tr>
            </thead>
            <tbody>
              {filteredTickets.length === 0 ? (
                <tr>
                  <td colSpan="6" className="no-data">
                    <p>Nenhum chamado concluído encontrado</p>
                  </td>
                </tr>
              ) : (
                filteredTickets.map((ticket) => (
                  <tr 
                    key={ticket.id} 
                    onClick={() => handleTicketClick(ticket.id)} 
                    style={{ cursor: 'pointer' }}
                  >
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
                    <td>
                      <span 
                        className="status-badge"
                        style={{ backgroundColor: getStatusColor(ticket.status) }}
                      >
                        {getStatusText(ticket.status)}
                      </span>
                    </td>
                    <td className="tecnico-cell">{ticket.tecnico}</td>
                    <td className="date-cell">{formatDate(ticket.dataFechamento)}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}

export default CompletedTicketsPage;

