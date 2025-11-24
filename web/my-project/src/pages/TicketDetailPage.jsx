// src/pages/TicketDetailPage.jsx
import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import Toast from '../components/Toast';
import ConfirmModal from '../components/ConfirmModal';
import { ticketService, aiService } from '../utils/api';
import '../styles/ticket-detail.css';

const TicketDetailPage = ({ onLogout, onNavigateToHome, onNavigateToPage, userInfo, ticketId, previousPage, onNavigateToProfile }) => {
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  // REMOVED: Priority dropdown states
  const [solution, setSolution] = useState('');
  const [toast, setToast] = useState({ isVisible: false, message: '', type: 'error' });
  const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);

  useEffect(() => {
    if (ticketId) {
      loadTicket();
    }
  }, [ticketId]);

  const loadTicket = async () => {
    try {
      setLoading(true);
      const ticketData = await ticketService.getTicket(ticketId);
      setTicket(ticketData);
      setSolution(''); // Limpa o campo de solução ao carregar um novo chamado
      
      // Se o chamado está em status "Aberto" (1) e o usuário é um técnico, muda para "Em Atendimento" (2)
      if (ticketData.status === 1 && (userInfo?.permissao === 2 || userInfo?.permissao === 3)) {
        try {
          await ticketService.updateTicket(ticketId, { status: 2 });
          // Atualiza o estado local com o novo status
          setTicket(prevTicket => ({ ...prevTicket, status: 2 }));
          console.log('Chamado atualizado para "Em Atendimento"');
        } catch (error) {
          console.error('Erro ao atualizar status do chamado:', error);
          // Não mostra erro ao usuário, pois o chamado já foi carregado
        }
      }
    } catch (error) {
      console.error('Erro ao carregar chamado:', error);
      showToast('Erro ao carregar detalhes do chamado.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const showToast = (message, type = 'error') => {
    setToast({ isVisible: true, message, type });
  };

  const hideToast = () => {
    setToast({ isVisible: false, message: '', type: 'error' });
  };

  // Estados para sugestão de IA
  const [sugestao, setSugestao] = useState('');
  const [carregandoSugestao, setCarregandoSugestao] = useState(false);

  /**
   * Gera uma sugestão de resposta usando a IA (Gemini)
   */
  const handleGerarSugestao = async () => {
    if (!ticket || !ticket.descricao) {
      showToast('Não é possível gerar sugestão sem a descrição do problema.', 'error');
      return;
    }

    try {
      setCarregandoSugestao(true);
      
      const response = await aiService.gerarSugestao(
        ticket.titulo || '',
        ticket.descricao
      );

      if (response.sugestao) {
        setSugestao(response.sugestao);
        showToast('Sugestão gerada com sucesso! Clique em "Usar Sugestão" para aplicá-la.', 'success');
      } else {
        showToast('Não foi possível gerar uma sugestão. Tente novamente.', 'error');
      }
    } catch (error) {
      console.error('Erro ao gerar sugestão:', error);
      const errorMessage = error.data?.erro || error.message || 'Erro ao gerar sugestão. Verifique se a API do Gemini está configurada.';
      showToast(errorMessage, 'error');
    } finally {
      setCarregandoSugestao(false);
    }
  };

  /**
   * Usa a sugestão gerada no campo de solução
   */
  const handleUsarSugestao = () => {
    if (sugestao) {
      setSolution(sugestao);
      showToast('Sugestão aplicada ao campo de solução.', 'success');
    }
  };

  const handleSolutionChange = (e) => {
    setSolution(e.target.value);
  };

  const handleSendSolution = () => {
    if (!solution.trim()) {
      showToast('Por favor, descreva a solução antes de enviar.', 'error');
      return;
    }

    // Abre o modal de confirmação
    setIsConfirmModalOpen(true);
  };

  const handleConfirmSolution = async () => {
    setIsConfirmModalOpen(false);
    
    try {
      setSaving(true);
      
      // Atualiza o chamado com a solução E muda o status para "Fechado" (3)
      const updateData = {
        solucao: solution,
        status: 3, // Fechado
        // Define o técnico responsável apenas se ainda não estiver definido
        tecnicoResponsavelId: ticket.tecnicoResponsavelId || (userInfo?.id ? Number(userInfo.id) : null),
        // Define a data de fechamento como agora
        dataFechamento: new Date().toISOString()
      };

      await ticketService.updateTicket(ticketId, updateData);
      
      showToast('Solução enviada e chamado fechado com sucesso!', 'success');
      
      // Aguarda um pouco para a toast ser exibida e depois navega
      setTimeout(() => {
        if (onNavigateToPage) {
          onNavigateToPage('completed-tickets');
        }
      }, 1500);

    } catch (error) {
      console.error('Erro ao enviar solução:', error);
      showToast('Erro ao enviar solução. Tente novamente.', 'error');
    } finally {
      setSaving(false);
    }
  };

  // REMOVED: Priority dropdown options

  const getPriorityColor = (priority) => {
    if (typeof priority === 'number') {
      switch (priority) {
        case 3: return '#dc3545'; // Alta
        case 2: return '#ffc107'; // Média
        case 1: return '#28a745'; // Baixa
        default: return '#6c757d';
      }
    }
    return '#6c757d';
  };

  const getPriorityText = (priority) => {
      // REMOVED: Priority change handlers
    if (typeof priority === 'number') {
      switch (priority) {
        case 3: return 'ALTA';
        case 2: return 'MÉDIA';
        case 1: return 'BAIXA';
        default: return 'N/A';
      }
    }
    return priority || 'N/A';
  };

  const getStatusText = (status) => {
    if (typeof status === 'number') {
      switch (status) {
        case 1: return 'ABERTO';
        case 2: return 'EM ATENDIMENTO';
        case 3: return 'AGUARDANDO USUÁRIO';
        case 4: return 'RESOLVIDO';
        case 5: return 'FECHADO';
        default: return 'N/A';
      }
    }
    return status || 'N/A';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR');
  };

  if (loading) {
    return (
      <div className="ticket-detail-layout">
        <Sidebar currentPage={previousPage || 'pending-tickets'} onNavigate={onNavigateToPage} userInfo={userInfo} />
        <Header onLogout={onLogout} userName={userInfo?.nome || 'Usuário'} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
        <main className="ticket-detail-main">
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Carregando...</p>
          </div>
        </main>
      </div>
    );
  }

  if (!ticket) {
    return (
      <div className="ticket-detail-layout">
        <Sidebar currentPage={previousPage || 'pending-tickets'} onNavigate={onNavigateToPage} userInfo={userInfo} />
        <Header onLogout={onLogout} userName={userInfo?.nome || 'Usuário'} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
        <main className="ticket-detail-main">
          <div className="error-container">
            <p>Chamado não encontrado.</p>
            <button onClick={() => {
              const pageToReturn = previousPage || 'pending-tickets';
              onNavigateToPage(pageToReturn);
            }}>
              Voltar para lista
            </button>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="ticket-detail-layout">
      <Sidebar currentPage="pending-tickets" onNavigate={onNavigateToPage} userInfo={userInfo} />
      <Header onLogout={onLogout} userName={userInfo?.nome} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
      
      <main className="ticket-detail-main">
        <button 
          className="back-button" 
          onClick={() => {
            // Determina a página de retorno baseado no status do chamado ou previousPage
            // Se o chamado está concluído (status 5) ou se veio de completed-tickets, volta para completed-tickets
            // Caso contrário, volta para pending-tickets
            let pageToReturn = previousPage;
            
            // Se não houver previousPage, tenta determinar pelo status do chamado
            if (!pageToReturn && ticket) {
              const isConcluido = ticket.status === 5; // Status 5 = Fechado
              pageToReturn = isConcluido ? 'completed-tickets' : 'pending-tickets';
            } else {
              // Se houver previousPage, usa ela (pode ser completed-tickets ou pending-tickets)
              pageToReturn = pageToReturn || 'pending-tickets';
            }
            
            console.log('Voltando para:', pageToReturn, '(status do chamado:', ticket?.status, ')');
            onNavigateToPage(pageToReturn);
          }}
          aria-label="Voltar para lista"
        >
          ← Voltar
        </button>
        
        <div className="ticket-detail-header">
          <h1>DETALHES DO CHAMADO #{String(ticket.id).padStart(6, '0')}</h1>
        </div>

        <div className="ticket-detail-content">
          {/* Informações do chamado */}
          <div className="ticket-info-section">
            <h2>Informações do Chamado</h2>
            
            <div className="info-grid">
              <div className="info-item">
                <label>Título:</label>
                <span>{ticket.titulo}</span>
              </div>
              
              <div className="info-item">
                <label>Tipo:</label>
                <span>{ticket.tipo}</span>
              </div>
              
              <div className="info-item">
                <label>Prioridade:</label>
                <span 
                  className="priority-badge"
                  style={{ backgroundColor: getPriorityColor(ticket.prioridade) }}
                >
                  {getPriorityText(ticket.prioridade)}
                </span>
              </div>
              
              <div className="info-item">
                <label>Status:</label>
                <span className="status-badge">
                  {getStatusText(ticket.status)}
                </span>
              </div>
              
              <div className="info-item">
                <label>Data de Abertura:</label>
                <span>{formatDate(ticket.dataAbertura)}</span>
              </div>
              
              <div className="info-item">
                <label>Data de Fechamento:</label>
                <span>{formatDate(ticket.dataFechamento)}</span>
              </div>
            </div>
          </div>

          {/* Informações do solicitante */}
          <div className="solicitante-info-section">
            <h2>Informações do Solicitante</h2>
            
            <div className="info-grid">
              <div className="info-item">
                <label>Nome:</label>
                <span>{ticket.solicitante?.nome || 'N/A'}</span>
              </div>
              
              <div className="info-item">
                <label>Email:</label>
                <span>{ticket.solicitante?.email || 'N/A'}</span>
              </div>
              
              <div className="info-item">
                <label>Cargo:</label>
                <span>{ticket.solicitante?.cargo || 'N/A'}</span>
              </div>
              
              <div className="info-item">
                <label>Telefone:</label>
                <span>{ticket.solicitante?.telefone || 'N/A'}</span>
              </div>
            </div>
          </div>

          {/* Técnico responsável */}
          {ticket.tecnicoResponsavel && (
            <div className="tecnico-info-section">
              <h2>Técnico Responsável</h2>
              
              <div className="info-grid">
                <div className="info-item">
                  <label>Nome:</label>
                  <span>{ticket.tecnicoResponsavel.nome}</span>
                </div>
                
                <div className="info-item">
                  <label>Email:</label>
                  <span>{ticket.tecnicoResponsavel.email}</span>
                </div>
              </div>
            </div>
          )}

          {/* Descrição original do problema */}
          <div className="problem-description-section">
            <h2>Descrição do Problema</h2>
            <div className="description-box">
              {ticket.descricao}
            </div>
          </div>

          {/* Solução (se já foi registrada) */}
          {ticket.solucao && (
            <div className="solution-display-section">
              <h2>Solução Sugerida pelo Técnico</h2>
              <div className="description-box" style={{ backgroundColor: '#e8f5e9' }}>
                {ticket.solucao}
              </div>
            </div>
          )}

          {/* Campo de solução (apenas para técnicos) e apenas se o chamado não está fechado */}
          {(userInfo?.permissao === 2 || userInfo?.permissao === 3) && ticket?.status !== 3 && (
            <div className="solution-section">
              <div className="solution-header">
                <h2>Registrar Solução</h2>
                <button 
                  onClick={handleGerarSugestao}
                  disabled={carregandoSugestao}
                  className="ai-suggestion-button"
                  title="Gerar sugestão de resposta usando IA"
                >
                  {carregandoSugestao ? (
                    <>
                      <span className="loading-spinner-small"></span>
                      Gerando Sugestão...
                    </>
                  ) : (
                    <>
                      🤖 Gerar Sugestão com IA
                    </>
                  )}
                </button>
              </div>

              {/* Exibir sugestão gerada (se houver) */}
              {sugestao && (
                <div className="ai-suggestion-box">
                  <div className="ai-suggestion-header">
                    <span className="ai-label">💡 Sugestão gerada pela IA:</span>
                    <div className="ai-suggestion-actions">
                      <button 
                        onClick={handleUsarSugestao}
                        className="use-suggestion-button"
                        title="Usar esta sugestão no campo de solução"
                      >
                        Usar Sugestão
                      </button>
                      <button 
                        onClick={() => setSugestao('')}
                        className="close-suggestion-button"
                        title="Fechar sugestão"
                      >
                        ✕
                      </button>
                    </div>
                  </div>
                  <div className="ai-suggestion-content">
                    {sugestao}
                  </div>
                </div>
              )}

              <textarea
                value={solution}
                onChange={handleSolutionChange}
                placeholder="Descreva aqui a solução sugerida para o problema. Use o botão acima para gerar uma sugestão com IA..."
                className="solution-textarea"
                rows="8"
              />
              
              <div className="solution-actions">
                <button 
                  onClick={handleSendSolution}
                  disabled={saving || !solution.trim()}
                  className="conclude-button"
                >
                  {saving ? 'Enviando...' : 'Enviar Solução'}
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
      
      <Toast
        isVisible={toast.isVisible}
        message={toast.message}
        type={toast.type}
        onClose={hideToast}
      />
      
      <ConfirmModal
        isOpen={isConfirmModalOpen}
        title="CONFIRMAR ENVIO DA SOLUÇÃO"
        message={`Tem certeza que deseja enviar esta solução e fechar o chamado?\n\nO chamado será marcado como "Fechado" e o usuário receberá a solução sugerida.`}
        confirmText="Confirmar"
        cancelText="Cancelar"
        onConfirm={handleConfirmSolution}
        onCancel={() => setIsConfirmModalOpen(false)}
      />
    </div>
  );
};

export default TicketDetailPage;
