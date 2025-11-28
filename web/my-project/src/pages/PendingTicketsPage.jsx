// src/pages/PendingTicketsPage.jsx
import React, { useState, useEffect } from 'react';
import '../styles/pending-tickets.css';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import Footer from '../components/Footer';
import LoadingScreen from '../components/LoadingScreen';
import Toast from '../components/Toast';
import { FaClipboardList, FaSearch, FaFilter, FaEdit } from 'react-icons/fa';
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
  const [editingPriority, setEditingPriority] = useState(null); // ID do ticket sendo editado
  const [toast, setToast] = useState({ isVisible: false, message: '', type: 'error' });
  const [updatingPriority, setUpdatingPriority] = useState(false);

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

  const handlePriorityChange = async (ticketId, newPriority) => {
    try {
      setUpdatingPriority(true);
      const priorityNumber = priorityTextToNumber(newPriority);
      
      // Envia a prioridade no formato que o backend espera (minúsculo)
      await ticketService.updateTicket(ticketId, {
        prioridade: priorityNumber
      });

      // Atualiza o ticket localmente
      setTickets(prevTickets => 
        prevTickets.map(ticket => 
          ticket.id === ticketId 
            ? { 
                ...ticket, 
                prioridade: newPriority,
                prioridadeNumber: priorityTextToNumber(newPriority)
              }
            : ticket
        )
      );

      // Atualiza também os tickets filtrados
      setFilteredTickets(prevFiltered => 
        prevFiltered.map(ticket => 
          ticket.id === ticketId 
            ? { 
                ...ticket, 
                prioridade: newPriority,
                prioridadeNumber: priorityTextToNumber(newPriority)
              }
            : ticket
        )
      );

      setEditingPriority(null);
      showToast('Prioridade atualizada com sucesso!', 'success');
    } catch (error) {
      console.error('Erro ao atualizar prioridade:', error);
      const errorMessage = error?.data?.message || error?.message || 'Erro ao atualizar prioridade.';
      showToast(errorMessage, 'error');
    } finally {
      setUpdatingPriority(false);
    }
  };

  const showToast = (message, type = 'error') => {
    setToast({ isVisible: true, message, type });
  };

  const hideToast = () => {
    setToast({ isVisible: false, message: '', type: 'error' });
  };

  const handlePriorityClick = (e, ticketId) => {
    e.stopPropagation(); // Previne o clique na linha da tabela
    setEditingPriority(ticketId);
  };

  const handlePrioritySelectChange = (e, ticketId) => {
    e.stopPropagation();
    const newPriority = e.target.value;
    handlePriorityChange(ticketId, newPriority);
  };

  const handlePrioritySelectBlur = (e, ticketId) => {
    // Aguarda um pouco antes de fechar para permitir que o onChange seja processado
    setTimeout(() => {
      if (!updatingPriority) {
        setEditingPriority(null);
      }
    }, 300);
  };

  if (loading) {
    return <LoadingScreen message="Aguarde..." />;
  }

  return (
    <div className="pending-tickets-page">
      <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} userInfo={userInfo} />
      <Header onLogout={onLogout} userName={userInfo?.nome} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
      
      <main className="pending-tickets-main">
        <button 
          className="back-button" 
          onClick={onNavigateToHome}
          aria-label="Voltar para página inicial"
        >
          ← Voltar
        </button>
        
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
                      <td onClick={(e) => e.stopPropagation()}>
                        {editingPriority === ticket.id ? (
                          <div className="priority-edit-container">
                            <select
                              className="priority-select"
                              value={ticket.prioridade || 'MÉDIA'}
                              onChange={(e) => handlePrioritySelectChange(e, ticket.id)}
                              onBlur={(e) => handlePrioritySelectBlur(e, ticket.id)}
                              disabled={updatingPriority}
                              autoFocus
                              onClick={(e) => e.stopPropagation()}
                              onMouseDown={(e) => e.stopPropagation()}
                            >
                              <option value="BAIXA">BAIXA</option>
                              <option value="MÉDIA">MÉDIA</option>
                              <option value="ALTA">ALTA</option>
                            </select>
                          </div>
                        ) : (
                          <div 
                            className="priority-badge-container"
                            onClick={(e) => handlePriorityClick(e, ticket.id)}
                            title="Clique para editar a prioridade"
                          >
                            <span 
                              className="priority-badge priority-badge-editable"
                              style={{ backgroundColor: getPriorityColor(ticket.prioridade) }}
                            >
                              {ticket.prioridade}
                            </span>
                            <FaEdit className="priority-edit-icon" />
                          </div>
                        )}
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
      <Footer />
      
      <Toast
        isVisible={toast.isVisible}
        message={toast.message}
        type={toast.type}
        onClose={hideToast}
      />
    </div>
  );
}

export default PendingTicketsPage;
