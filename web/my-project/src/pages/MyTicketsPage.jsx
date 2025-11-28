// src/pages/MyTicketsPage.jsx
import React, { useState, useEffect } from 'react';
import '../styles/my-tickets.css';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import Footer from '../components/Footer';
import LoadingScreen from '../components/LoadingScreen';
import { FaSearch, FaFilter, FaSyncAlt } from 'react-icons/fa';
import { ticketService } from '../utils/api';

function MyTicketsPage({ onLogout, onNavigateToHome, onNavigateToPage, currentPage, userInfo, onNavigateToTicketDetail, onNavigateToProfile }) {
  const [tickets, setTickets] = useState([]);
  const [filteredTickets, setFilteredTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('dataAbertura'); // codigo, titulo, prioridade, dataAbertura, status
  const [sortOrder, setSortOrder] = useState('desc'); // asc, desc
  // Removido: edição de prioridade - usuários apenas visualizam, não editam

  // Funções centralizadas para mapeamento de prioridade
  const mapPriority = (p) => {
    // Se for null ou undefined, retorna default
    if (p === null || p === undefined) {
      return 'MÉDIA';
    }
    
    // Se for número, mapeia diretamente
    if (typeof p === 'number') {
      if (p === 3 || p === '3') return 'ALTA';
      if (p === 2 || p === '2') return 'MÉDIA';
      if (p === 1 || p === '1') return 'BAIXA';
      return 'MÉDIA'; // default
    }
    
    // Se for string, tenta parsear
    if (typeof p === 'string') {
      const normalized = p.trim().toLowerCase();
      
      // Tenta parsear como número primeiro
      const numValue = parseInt(normalized, 10);
      if (!isNaN(numValue) && numValue >= 1 && numValue <= 3) {
        return mapPriority(numValue);
      }
      
      // Mapeia por texto (verifica vários formatos possíveis)
      if (normalized === 'alta' || normalized === '3' || normalized.includes('alta')) return 'ALTA';
      if (normalized === 'média' || normalized === 'media' || normalized === '2' || normalized.includes('medi')) return 'MÉDIA';
      if (normalized === 'baixa' || normalized === '1' || normalized.includes('baix')) return 'BAIXA';
      
      // Verifica enum do C# (PrioridadeChamado.Alta, etc)
      if (normalized.includes('prioridadechamado.alta') || normalized.includes('alta')) return 'ALTA';
      if (normalized.includes('prioridadechamado.media') || normalized.includes('prioridadechamado.média')) return 'MÉDIA';
      if (normalized.includes('prioridadechamado.baixa')) return 'BAIXA';
    }
    
    // Default para MÉDIA se não conseguir identificar
    return 'MÉDIA';
  };

  // Função para converter texto de prioridade para número do backend
  const priorityTextToNumber = (priorityText) => {
    if (typeof priorityText === 'number') {
      return priorityText;
    }
    const normalized = String(priorityText || '').trim().toUpperCase();
    switch (normalized) {
      case 'ALTA':
      case '3':
        return 3;
      case 'MÉDIA':
      case 'MEDIA':
      case '2':
        return 2;
      case 'BAIXA':
      case '1':
        return 1;
      default:
        return 2; // Default para MÉDIA
    }
  };

  // Função para converter número do backend para texto de prioridade
  const priorityNumberToText = (priorityNumber) => {
    const num = typeof priorityNumber === 'number' ? priorityNumber : parseInt(priorityNumber, 10);
    switch (num) {
      case 3: return 'ALTA';
      case 2: return 'MÉDIA';
      case 1: return 'BAIXA';
      default: return 'MÉDIA';
    }
  };

  const handleTicketClick = (ticketId) => {
    if (onNavigateToTicketDetail) {
      onNavigateToTicketDetail(ticketId, 'my-tickets');
    }
  };

  // Recarrega os tickets sempre que a página for acessada ou o userInfo mudar
  useEffect(() => {
    if (currentPage === 'my-tickets' && userInfo?.id) {
      loadTickets();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userInfo?.id, currentPage]);

  useEffect(() => {
    applyFiltersAndSort();
  }, [tickets, searchTerm, sortBy, sortOrder]);

  const loadTickets = async () => {
    try {
      setLoading(true);
      
      // Obter ID do usuário
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
      
      if (!userId) {
        setTickets([]);
        setLoading(false);
        return;
      }

      // Buscar todos os chamados do usuário (solicitante)
      const filters = {
        solicitanteId: Number(userId)
      };
      
      const apiTickets = await ticketService.getTickets(filters);
      
      if (apiTickets && apiTickets.length > 0) {

        const mapStatus = (s) => {
          if (typeof s === 'number') {
            switch (s) {
              case 1: return 'ABERTO';
              case 2: return 'EM ATENDIMENTO';
              case 3: return 'FECHADO';
              default: return 'DESCONHECIDO';
            }
          }
          return 'DESCONHECIDO';
        };
        
        const mapped = apiTickets
          .map(item => {
            // Mapeia a prioridade de diferentes formatos possíveis
            const prioridadeValue = item.prioridade !== undefined ? item.prioridade : 
                                  item.Prioridade !== undefined ? item.Prioridade : 
                                  2; // Default para MÉDIA
            const prioridadeText = mapPriority(prioridadeValue);
            const prioridadeNum = typeof prioridadeValue === 'number' 
              ? prioridadeValue 
              : priorityTextToNumber(prioridadeText);
            
            return {
              id: item.id,
              codigo: String(item.id).padStart(6, '0'),
              titulo: item.titulo || '',
              prioridade: prioridadeText,
              prioridadeNumber: prioridadeNum,
              status: item.status,
              statusText: mapStatus(item.status),
              dataAbertura: item.dataAbertura,
              dataFechamento: item.dataFechamento,
              tecnico: item.tecnicoResponsavel?.nome || 'N/A'
            };
          });
        
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
        case 'status':
          const statusOrder = { 'ABERTO': 1, 'EM ATENDIMENTO': 2, 'FECHADO': 3 };
          aValue = statusOrder[a.statusText] || 4;
          bValue = statusOrder[b.statusText] || 4;
          break;
        case 'dataAbertura':
          aValue = new Date(a.dataAbertura);
          bValue = new Date(b.dataAbertura);
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

  const getStatusColor = (status) => {
    switch (status) {
      case 1: return '#007bff'; // Aberto - azul
      case 2: return '#ffc107'; // Em Atendimento - amarelo
      case 3: return '#6c757d'; // Fechado - cinza
      default: return '#6c757d';
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
  };

  // Removido: funções de edição de prioridade - apenas visualização nesta página

  if (loading) {
    return <LoadingScreen message="Aguarde..." />;
  }

  return (
    <div className="my-tickets-page">
      <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} userInfo={userInfo} />
      <Header onLogout={onLogout} userName={userInfo?.nome} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
      
      <main className="my-tickets-main">
        <button 
          className="back-button" 
          onClick={onNavigateToHome}
          aria-label="Voltar para página inicial"
        >
          ← Voltar
        </button>
        
        {/* Header da página */}
        <div className="page-header">
          <h1>MEUS CHAMADOS</h1>
          <button 
            className="refresh-button"
            onClick={() => loadTickets()}
            title="Atualizar lista de chamados"
            aria-label="Atualizar lista de chamados"
          >
            <FaSyncAlt /> Atualizar
          </button>
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
              <option value="dataAbertura">Data Limite</option>
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
                <th onClick={() => handleSort('dataAbertura')} className="sortable">
                  DATA LIMITE {sortBy === 'dataAbertura' && (sortOrder === 'asc' ? '▲' : '▼')}
                </th>
                <th>STATUS</th>
                <th>TÉCNICO RESPONSÁVEL</th>
              </tr>
            </thead>
            <tbody>
              {filteredTickets.length === 0 ? (
                <tr>
                  <td colSpan="6" className="no-data">
                    <p>Nenhum chamado encontrado</p>
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
                    <td className="date-cell">{formatDate(ticket.dataAbertura)}</td>
                    <td>
                      <span 
                        className="status-badge"
                        style={{ backgroundColor: getStatusColor(ticket.status) }}
                      >
                        {ticket.statusText}
                      </span>
                    </td>
                    <td className="tecnico-cell">{ticket.tecnico}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default MyTicketsPage;
