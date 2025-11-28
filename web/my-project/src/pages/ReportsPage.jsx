// src/pages/ReportsPage.jsx
import React, { useState, useEffect } from 'react';
import '../styles/reports.css';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import Footer from '../components/Footer';
import LoadingScreen from '../components/LoadingScreen';
import { FaServer, FaDatabase, FaRobot, FaUsers, FaCheckCircle, FaClock, FaSpinner, FaExclamationTriangle, FaInfoCircle, FaChartLine, FaCalendarAlt, FaLightbulb, FaTrophy, FaTag } from 'react-icons/fa';
import { ticketService, userService } from '../utils/api';

function DashboardPage({ onLogout, onNavigateToHome, onNavigateToPage, currentPage, userInfo, onNavigateToProfile }) {
  const [loading, setLoading] = useState(true);
  const [reports, setReports] = useState({
    totalUsuarios: 0,
    totalChamados: 0,
    chamadosResolvidos: 0,
    chamadosEmAndamento: 0,
    chamadosAbertos: 0,
    chamadosAbertosHoje: 0,
    chamadosResolvidosHoje: 0,
    chamadosResolvidosSemana: 0,
    chamadosPorPrioridade: {
      alta: 0,
      media: 0,
      baixa: 0
    },
    chamadosPorTipo: {},
    tempoMedioResolucao: 0,
    taxaResolucao: 0,
    usuariosPorNivel: {
      colaboradores: 0,
      suporteTecnico: 0,
      administradores: 0
    },
    apiStatus: {
      database: { status: 'checking', responseTime: null },
      ai: { status: 'checking', responseTime: null, modelo: null, sugestaoGerada: false }
    },
    sistemaInfo: {
      versao: '1.0.0',
      ultimaAtualizacao: new Date().toLocaleDateString('pt-BR'),
      nome: 'HelpWave - Sistema de Suporte Técnico'
    }
  });

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      setLoading(true);
      
      // Buscar todos os chamados da API
      const tickets = await ticketService.getTickets();
      
      console.log('Dashboard - Total de chamados recebidos:', tickets.length);
      console.log('Dashboard - Exemplo de chamado:', tickets[0]);
      
      // Calcular estatísticas dos chamados
      const totalChamados = tickets.length;
      
      // Normalizar status (pode vir como número ou string)
      const chamadosResolvidos = tickets.filter(t => {
        const status = Number(t.status || t.Status || 0);
        return status === 3;
      }).length;
      
      const chamadosEmAndamento = tickets.filter(t => {
        const status = Number(t.status || t.Status || 0);
        return status === 2;
      }).length;
      
      const chamadosAbertos = tickets.filter(t => {
        const status = Number(t.status || t.Status || 0);
        return status === 1;
      }).length;
      
      console.log('Dashboard - Estatísticas calculadas:', {
        totalChamados,
        chamadosResolvidos,
        chamadosEmAndamento,
        chamadosAbertos
      });
      
      // Data atual para cálculos
      const hoje = new Date();
      hoje.setHours(0, 0, 0, 0);
      const umaSemanaAtras = new Date(hoje);
      umaSemanaAtras.setDate(umaSemanaAtras.getDate() - 7);
      
      // Chamados abertos hoje
      const chamadosAbertosHoje = tickets.filter(t => {
        if (Number(t.status) !== 1) return false;
        if (!t.dataAbertura) return false;
        try {
          const dataAbertura = new Date(t.dataAbertura);
          dataAbertura.setHours(0, 0, 0, 0);
          return dataAbertura.getTime() === hoje.getTime();
        } catch {
          return false;
        }
      }).length;
      
      // Chamados resolvidos hoje
      const chamadosResolvidosHoje = tickets.filter(t => {
        if (Number(t.status) !== 3 || !t.dataFechamento) return false;
        try {
          const dataFechamento = new Date(t.dataFechamento);
          dataFechamento.setHours(0, 0, 0, 0);
          return dataFechamento.getTime() === hoje.getTime();
        } catch {
          return false;
        }
      }).length;
      
      // Chamados resolvidos na última semana
      const chamadosResolvidosSemana = tickets.filter(t => {
        if (Number(t.status) !== 3 || !t.dataFechamento) return false;
        try {
          const dataFechamento = new Date(t.dataFechamento);
          return dataFechamento >= umaSemanaAtras;
        } catch {
          return false;
        }
      }).length;
      
      // Chamados por prioridade
      const chamadosPorPrioridade = {
        alta: tickets.filter(t => Number(t.prioridade || t.Prioridade) === 3).length,
        media: tickets.filter(t => Number(t.prioridade || t.Prioridade) === 2).length,
        baixa: tickets.filter(t => Number(t.prioridade || t.Prioridade) === 1).length
      };
      
      // Chamados por tipo
      const chamadosPorTipo = {};
      tickets.forEach(t => {
        const tipo = t.tipo || t.Tipo || 'Outros';
        chamadosPorTipo[tipo] = (chamadosPorTipo[tipo] || 0) + 1;
      });
      
      // Calcular tempo médio de resolução (em horas)
      const chamadosComTempo = tickets.filter(t => 
        Number(t.status) === 3 && t.dataAbertura && t.dataFechamento
      );
      
      let tempoMedioResolucao = 0;
      if (chamadosComTempo.length > 0) {
        const temposTotal = chamadosComTempo.reduce((acc, t) => {
          try {
            const abertura = new Date(t.dataAbertura);
            const fechamento = new Date(t.dataFechamento);
            const diffHoras = (fechamento - abertura) / (1000 * 60 * 60);
            return acc + (isNaN(diffHoras) ? 0 : diffHoras);
          } catch {
            return acc;
          }
        }, 0);
        tempoMedioResolucao = Math.round(temposTotal / chamadosComTempo.length);
      }
      
      // Taxa de resolução (porcentagem)
      const taxaResolucao = totalChamados > 0 
        ? Math.round((chamadosResolvidos / totalChamados) * 100) 
        : 0;
      
      // Buscar dados de usuários com estatísticas
      let totalUsuarios = 0;
      let usuariosPorNivel = {
        colaboradores: 0,
        suporteTecnico: 0,
        administradores: 0
      };
      
      try {
        const usuariosData = await userService.getUsers();
        
        // A API pode retornar um array diretamente ou um objeto
        let usuariosArray = [];
        if (Array.isArray(usuariosData)) {
          usuariosArray = usuariosData;
        } else if (usuariosData?.usuarios && Array.isArray(usuariosData.usuarios)) {
          usuariosArray = usuariosData.usuarios;
        } else if (usuariosData?.items && Array.isArray(usuariosData.items)) {
          usuariosArray = usuariosData.items;
        } else if (usuariosData?.users && Array.isArray(usuariosData.users)) {
          usuariosArray = usuariosData.users;
        }
        
        totalUsuarios = usuariosArray.length;
        
        // Contar usuários por nível de permissão
            usuariosPorNivel = {
          colaboradores: usuariosArray.filter(u => (u.permissao || u.Permissao) === 1).length,
          suporteTecnico: usuariosArray.filter(u => (u.permissao || u.Permissao) === 2).length,
          administradores: usuariosArray.filter(u => (u.permissao || u.Permissao) === 3).length
        };
          
          console.log('Dados de usuários carregados:', { totalUsuarios, usuariosPorNivel });
      } catch (error) {
        console.warn('Erro ao buscar usuários:', error);
        // Continuar mesmo se falhar ao buscar usuários
      }
      
      // Verificar status da API de banco de dados e IA
      const databaseStatus = await checkDatabaseApiStatus();
      const iaStatus = await checkIaApiStatus();
      
      setReports({
        totalUsuarios,
        totalChamados,
        chamadosResolvidos,
        chamadosEmAndamento,
        chamadosAbertos,
        chamadosAbertosHoje,
        chamadosResolvidosHoje,
        chamadosResolvidosSemana,
        chamadosPorPrioridade,
        chamadosPorTipo,
        tempoMedioResolucao,
        taxaResolucao,
        usuariosPorNivel,
        apiStatus: {
          database: databaseStatus,
          ai: iaStatus
        },
        sistemaInfo: {
          versao: '1.0.0',
          ultimaAtualizacao: new Date().toLocaleDateString('pt-BR'),
          nome: 'HelpWave - Sistema de Suporte Técnico'
        }
      });
    } catch (error) {
      console.error('Erro ao carregar relatórios:', error);
    } finally {
      setLoading(false);
    }
  };

  const checkDatabaseApiStatus = async () => {
    try {
      const startTime = performance.now();
      await ticketService.getTickets();
      const endTime = performance.now();
      const responseTime = Math.round(endTime - startTime);
      
      return {
        status: 'online',
        responseTime: responseTime < 1000 ? responseTime : Math.round(responseTime / 1000)
      };
    } catch (error) {
      return {
        status: 'offline',
        responseTime: null
      };
    }
  };

  const checkIaApiStatus = async () => {
    try {
      const startTime = performance.now();
      
      // Usa a URL completa do backend Flask
      const response = await fetch('http://localhost:5000/api/gemini/sugerir-resposta', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          titulo: 'Teste de Status',
          descricao: 'Teste de verificação de status da API de IA'
        })
      });
      
      const endTime = performance.now();
      const responseTime = Math.round(endTime - startTime);
      
      if (response.ok) {
        const data = await response.json().catch(() => ({}));
        return {
          status: 'online',
          responseTime: responseTime < 1000 ? responseTime : Math.round(responseTime / 1000),
          modelo: 'Gemini 2.0 Flash',
          sugestaoGerada: !!data.sugestao
        };
      } else {
        const errorData = await response.json().catch(() => ({}));
        return {
          status: 'offline',
          responseTime: null,
          erro: errorData.erro || 'Erro ao conectar com a API'
        };
      }
    } catch (error) {
      console.warn('Erro ao verificar status da IA:', error);
      return {
        status: 'offline',
        responseTime: null,
        erro: error.message || 'Erro de conexão'
      };
    }
  };

  const checkApiStatus = async () => {
    try {
      const startTime = performance.now();
      await ticketService.getTickets();
      const endTime = performance.now();
      const responseTime = Math.round(endTime - startTime);
      
      return {
        status: 'online',
        responseTime: responseTime < 1000 ? responseTime : Math.round(responseTime / 1000)
      };
    } catch (error) {
      return {
        status: 'offline',
        responseTime: null
      };
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'online':
        return <FaCheckCircle className="status-icon online" />;
      case 'offline':
        return <FaClock className="status-icon offline" />;
      case 'checking':
        return <FaSpinner className="status-icon checking" />;
      case 'not-implemented':
        return <FaRobot className="status-icon not-implemented" />;
      default:
        return null;
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'online':
        return 'Online';
      case 'offline':
        return 'Offline';
      case 'checking':
        return 'Verificando...';
      case 'not-implemented':
        return 'Não Implementado';
      default:
        return 'Desconhecido';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'online':
        return '#28a745';
      case 'offline':
        return '#dc3545';
      case 'checking':
        return '#ffc107';
      case 'not-implemented':
        return '#6c757d';
      default:
        return '#6c757d';
    }
  };

  const calculatePercentage = (value, total) => {
    if (total === 0) return 0;
    return Math.round((value / total) * 100);
  };

  if (loading) {
    return <LoadingScreen message="Aguarde..." />;
  }

  return (
    <div className="reports-page">
      <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} userInfo={userInfo} />
      <Header onLogout={onLogout} userName={userInfo?.nome} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
      
      <main className="reports-main">
        <button 
          className="back-button" 
          onClick={onNavigateToHome}
          aria-label="Voltar para página inicial"
        >
          ← Voltar
        </button>
        
        <div className="page-header">
          <h1>DASHBOARD</h1>
        </div>

        {/* Cards de Estatísticas Gerais */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-header">
            <div className="stat-icon users">
              <FaUsers />
            </div>
            <div className="stat-content">
              <h3>{reports.totalUsuarios}</h3>
              <p>Usuários Cadastrados</p>
              </div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-header">
            <div className="stat-icon tickets">
              <FaCheckCircle />
            </div>
            <div className="stat-content">
              <h3>{reports.totalChamados}</h3>
              <p>Total de Chamados</p>
              </div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-header">
            <div className="stat-icon resolved">
              <FaCheckCircle />
            </div>
            <div className="stat-content">
              <h3>{reports.chamadosResolvidos}</h3>
              <p>Chamados Resolvidos</p>
              </div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-header">
            <div className="stat-icon in-progress">
              <FaClock />
            </div>
            <div className="stat-content">
              <h3>{reports.chamadosEmAndamento}</h3>
              <p>Em Andamento</p>
              </div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-header">
              <div className="stat-icon tickets">
                <FaCalendarAlt />
              </div>
              <div className="stat-content">
                <h3>{reports.chamadosAbertosHoje}</h3>
                <p>Abertos Hoje</p>
              </div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-header">
              <div className="stat-icon resolved">
                <FaCheckCircle />
              </div>
              <div className="stat-content">
                <h3>{reports.chamadosResolvidosHoje}</h3>
                <p>Resolvidos Hoje</p>
              </div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-header">
              <div className="stat-icon resolved">
                <FaChartLine />
              </div>
              <div className="stat-content">
                <h3>{reports.taxaResolucao}%</h3>
                <p>Taxa de Resolução</p>
              </div>
            </div>
          </div>
        </div>

        {/* Seção de Usuários por Nível */}
        <div className="section-card">
          <h2>USUÁRIOS POR NÍVEL DE ACESSO</h2>
          <div className="users-breakdown">
            <div className="user-level-item">
              <div className="level-indicator colaborador"></div>
              <div className="level-content">
                <span className="level-name">Colaboradores</span>
                <span className="level-count">{reports.usuariosPorNivel.colaboradores}</span>
              </div>
            </div>
            <div className="user-level-item">
              <div className="level-indicator suporte"></div>
              <div className="level-content">
                <span className="level-name">Suporte Técnico</span>
                <span className="level-count">{reports.usuariosPorNivel.suporteTecnico}</span>
              </div>
            </div>
            <div className="user-level-item">
              <div className="level-indicator admin"></div>
              <div className="level-content">
                <span className="level-name">Administradores</span>
                <span className="level-count">{reports.usuariosPorNivel.administradores}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Seção de Status das Chamados */}
        <div className="section-card">
          <h2>ESTATÍSTICAS DE CHAMADOS</h2>
          <div className="tickets-stats">
            <div className="ticket-stat-item">
              <div className="stat-bar">
                <div 
                  className="stat-bar-fill resolved"
                  style={{ width: `${calculatePercentage(reports.chamadosResolvidos, reports.totalChamados)}%` }}
                ></div>
              </div>
              <div className="stat-info">
                <span>Resolvidos</span>
                <span>{reports.chamadosResolvidos} ({calculatePercentage(reports.chamadosResolvidos, reports.totalChamados)}%)</span>
              </div>
            </div>
            
            <div className="ticket-stat-item">
              <div className="stat-bar">
                <div 
                  className="stat-bar-fill in-progress"
                  style={{ width: `${calculatePercentage(reports.chamadosEmAndamento, reports.totalChamados)}%` }}
                ></div>
              </div>
              <div className="stat-info">
                <span>Em Andamento</span>
                <span>{reports.chamadosEmAndamento} de {reports.totalChamados} ({calculatePercentage(reports.chamadosEmAndamento, reports.totalChamados)}%)</span>
              </div>
            </div>
            
            <div className="ticket-stat-item">
              <div className="stat-bar">
                <div 
                  className="stat-bar-fill open"
                  style={{ width: `${calculatePercentage(reports.chamadosAbertos, reports.totalChamados)}%` }}
                ></div>
              </div>
              <div className="stat-info">
                <span>Abertos</span>
                <span>{reports.chamadosAbertos} de {reports.totalChamados} ({calculatePercentage(reports.chamadosAbertos, reports.totalChamados)}%)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Seção de Chamados por Prioridade */}
        <div className="section-card">
          <h2>CHAMADOS POR PRIORIDADE</h2>
          <div className="priority-breakdown">
            <div className="priority-item">
              <div className="priority-indicator alta">
                <FaExclamationTriangle />
              </div>
              <div className="priority-content">
                <span className="priority-name">Alta Prioridade</span>
                <span className="priority-count">{reports.chamadosPorPrioridade.alta}</span>
                <span className="priority-percentage">
                  {reports.totalChamados > 0 
                    ? Math.round((reports.chamadosPorPrioridade.alta / reports.totalChamados) * 100) 
                    : 0}%
                </span>
              </div>
            </div>
            <div className="priority-item">
              <div className="priority-indicator media">
                <FaClock />
              </div>
              <div className="priority-content">
                <span className="priority-name">Média Prioridade</span>
                <span className="priority-count">{reports.chamadosPorPrioridade.media}</span>
                <span className="priority-percentage">
                  {reports.totalChamados > 0 
                    ? Math.round((reports.chamadosPorPrioridade.media / reports.totalChamados) * 100) 
                    : 0}%
                </span>
              </div>
            </div>
            <div className="priority-item">
              <div className="priority-indicator baixa">
                <FaInfoCircle />
              </div>
              <div className="priority-content">
                <span className="priority-name">Baixa Prioridade</span>
                <span className="priority-count">{reports.chamadosPorPrioridade.baixa}</span>
                <span className="priority-percentage">
                  {reports.totalChamados > 0 
                    ? Math.round((reports.chamadosPorPrioridade.baixa / reports.totalChamados) * 100) 
                    : 0}%
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Seção de Chamados por Tipo */}
        {Object.keys(reports.chamadosPorTipo).length > 0 && (
          <div className="section-card">
            <h2>CHAMADOS POR TIPO</h2>
            <div className="type-breakdown">
              {Object.entries(reports.chamadosPorTipo)
                .sort((a, b) => b[1] - a[1])
                .map(([tipo, quantidade]) => (
                  <div key={tipo} className="type-item">
                    <div className="type-icon">
                      <FaTag />
                    </div>
                    <div className="type-content">
                      <span className="type-name">{tipo}</span>
                      <span className="type-count">{quantidade}</span>
                    </div>
                    <div className="type-bar">
                      <div 
                        className="type-bar-fill"
                        style={{ 
                          width: `${reports.totalChamados > 0 
                            ? (quantidade / reports.totalChamados) * 100 
                            : 0}%` 
                        }}
                      ></div>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        )}

        {/* Seção de Métricas de Performance */}
        <div className="section-card">
          <h2>MÉTRICAS DE PERFORMANCE</h2>
          <div className="performance-grid">
            <div className="performance-item">
              <div className="performance-icon">
                <FaClock />
              </div>
              <div className="performance-content">
                <h4>Tempo Médio de Resolução</h4>
                <p className="performance-value">
                  {reports.tempoMedioResolucao > 0 
                    ? `${reports.tempoMedioResolucao}h` 
                    : 'N/A'}
                </p>
                <span className="performance-label">Baseado em chamados resolvidos</span>
              </div>
            </div>
            <div className="performance-item">
              <div className="performance-icon">
                <FaCheckCircle />
              </div>
              <div className="performance-content">
                <h4>Resolvidos na Semana</h4>
                <p className="performance-value">{reports.chamadosResolvidosSemana}</p>
                <span className="performance-label">Últimos 7 dias</span>
              </div>
            </div>
            <div className="performance-item">
              <div className="performance-icon">
                <FaChartLine />
              </div>
              <div className="performance-content">
                <h4>Taxa de Resolução</h4>
                <p className="performance-value">{reports.taxaResolucao}%</p>
                <span className="performance-label">
                  {reports.chamadosResolvidos} de {reports.totalChamados} chamados
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Seção de Status das APIs */}
        <div className="section-card">
          <h2>STATUS DOS SERVIÇOS</h2>
          <div className="api-status-grid">
            <div className="api-status-card">
              <div className="api-icon">
                <FaDatabase />
              </div>
              <div className="api-info">
                <h3>API Banco de Dados</h3>
                <div className="api-status">
                  {getStatusIcon(reports.apiStatus.database.status)}
                  <span style={{ color: getStatusColor(reports.apiStatus.database.status) }}>
                    {getStatusText(reports.apiStatus.database.status)}
                  </span>
                </div>
                {reports.apiStatus.database.responseTime !== null && (
                  <p className="response-time">
                    Tempo de Resposta: {reports.apiStatus.database.responseTime}ms
                  </p>
                )}
              </div>
            </div>

            <div className="api-status-card">
              <div className="api-icon">
                <FaRobot />
              </div>
              <div className="api-info">
                <h3>API de Inteligência Artificial</h3>
                <div className="api-status">
                  {getStatusIcon(reports.apiStatus.ai.status)}
                  <span style={{ color: getStatusColor(reports.apiStatus.ai.status) }}>
                    {getStatusText(reports.apiStatus.ai.status)}
                  </span>
                </div>
                {reports.apiStatus.ai.status === 'online' && (
                  <>
                    {reports.apiStatus.ai.responseTime !== null && (
                <p className="response-time">
                        Tempo de Resposta: {reports.apiStatus.ai.responseTime}ms
                      </p>
                    )}
                    {reports.apiStatus.ai.modelo && (
                      <p className="api-model" style={{ fontSize: '0.875rem', color: '#6c757d', marginTop: '0.5rem' }}>
                        Modelo: {reports.apiStatus.ai.modelo}
                      </p>
                    )}
                    {reports.apiStatus.ai.sugestaoGerada && (
                      <p className="api-feature" style={{ fontSize: '0.875rem', color: '#28a745', marginTop: '0.25rem' }}>
                        ✓ Sugestões automáticas ativas
                      </p>
                    )}
                  </>
                )}
                {reports.apiStatus.ai.status === 'offline' && reports.apiStatus.ai.erro && (
                  <p className="api-error" style={{ fontSize: '0.875rem', color: '#dc3545', marginTop: '0.5rem' }}>
                    {reports.apiStatus.ai.erro}
                  </p>
                )}
                {reports.apiStatus.ai.status === 'checking' && (
                  <p className="response-time" style={{ fontSize: '0.875rem', color: '#6c757d' }}>
                    Verificando conexão...
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Seção de Informações do Sistema */}
        <div className="section-card">
          <h2>INFORMAÇÕES DO SISTEMA</h2>
          <div className="system-info-grid">
            <div className="system-info-item">
              <div className="system-info-icon">
                <FaServer />
              </div>
              <div className="system-info-content">
                <h4>{reports.sistemaInfo.nome}</h4>
                <p>Versão {reports.sistemaInfo.versao}</p>
                <span className="system-info-label">
                  Última atualização: {reports.sistemaInfo.ultimaAtualizacao}
                </span>
              </div>
            </div>
            <div className="system-info-item">
              <div className="system-info-icon">
                <FaRobot />
              </div>
              <div className="system-info-content">
                <h4>Inteligência Artificial</h4>
                <p>Gemini 2.0 Flash</p>
                <span className="system-info-label">
                  Sugestões automáticas de soluções
                </span>
              </div>
            </div>
            <div className="system-info-item">
              <div className="system-info-icon">
                <FaUsers />
              </div>
              <div className="system-info-content">
                <h4>Equipe Ativa</h4>
                <p>{reports.usuariosPorNivel.suporteTecnico + reports.usuariosPorNivel.administradores} técnicos</p>
                <span className="system-info-label">
                  {reports.usuariosPorNivel.suporteTecnico} suporte + {reports.usuariosPorNivel.administradores} admin
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Seção de Dicas e Informações Úteis */}
        <div className="section-card tips-card">
          <h2>
            <FaLightbulb style={{ marginRight: '0.5rem' }} />
            DICAS E INFORMAÇÕES ÚTEIS
          </h2>
          <div className="tips-grid">
            <div className="tip-item">
              <FaInfoCircle className="tip-icon" />
              <div className="tip-content">
                <h4>Atendimento Prioritário</h4>
                <p>Chamados de alta prioridade devem ser atendidos em até 24 horas. Verifique regularmente a fila de chamados.</p>
              </div>
            </div>
            <div className="tip-item">
              <FaRobot className="tip-icon" />
              <div className="tip-content">
                <h4>Assistente de IA</h4>
                <p>Use o botão "Gerar Sugestão com IA" ao atender chamados para obter sugestões automáticas de soluções.</p>
              </div>
            </div>
            <div className="tip-item">
              <FaChartLine className="tip-icon" />
              <div className="tip-content">
                <h4>Métricas de Performance</h4>
                <p>Acompanhe sua taxa de resolução e tempo médio de atendimento para melhorar a eficiência do suporte.</p>
              </div>
            </div>
            <div className="tip-item">
              <FaCheckCircle className="tip-icon" />
              <div className="tip-content">
                <h4>Documentação Completa</h4>
                <p>Sempre preencha a solução de forma detalhada. Isso ajuda outros técnicos e melhora a base de conhecimento.</p>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default DashboardPage;
