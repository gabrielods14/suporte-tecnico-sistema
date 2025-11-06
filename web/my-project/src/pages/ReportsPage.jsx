// src/pages/ReportsPage.jsx
import React, { useState, useEffect } from 'react';
import '../styles/reports.css';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import { FaServer, FaDatabase, FaRobot, FaUsers, FaCheckCircle, FaClock, FaSpinner } from 'react-icons/fa';
import { ticketService, getUserDisplayName } from '../utils/api';

function ReportsPage({ onLogout, onNavigateToHome, onNavigateToPage, currentPage, userInfo, onNavigateToProfile }) {
  const [loading, setLoading] = useState(true);
  const [reports, setReports] = useState({
    totalUsuarios: 0,
    totalChamados: 0,
    chamadosResolvidos: 0,
    chamadosEmAndamento: 0,
    usuariosPorNivel: {
      colaboradores: 0,
      suporteTecnico: 0,
      administradores: 0
    },
    apiStatus: {
      database: { status: 'checking', responseTime: null },
      ai: { status: 'not-implemented', responseTime: null }
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
      
      // Calcular estatísticas
      const totalChamados = tickets.length;
      const chamadosResolvidos = tickets.filter(t => t.status === 4 || t.status === 5).length;
      const chamadosEmAndamento = tickets.filter(t => t.status === 1 || t.status === 2 || t.status === 3).length;
      
      // Simular dados de usuários (será substituído quando houver endpoint)
      const totalUsuarios = 0;
      const usuariosPorNivel = {
        colaboradores: 0,
        suporteTecnico: 0,
        administradores: 0
      };
      
      // Verificar status da API de banco de dados
      const databaseStatus = await checkApiStatus();
      
      setReports({
        totalUsuarios,
        totalChamados,
        chamadosResolvidos,
        chamadosEmAndamento,
        usuariosPorNivel,
        apiStatus: {
          database: databaseStatus,
          ai: { status: 'not-implemented', responseTime: null }
        }
      });
    } catch (error) {
      console.error('Erro ao carregar relatórios:', error);
    } finally {
      setLoading(false);
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
    return (
      <div className="reports-page">
        <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} />
        <Header onLogout={onLogout} userName={getUserDisplayName(userInfo)} onNavigateToProfile={onNavigateToProfile} />
        <main className="reports-main">
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Carregando relatórios...</p>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="reports-page">
      <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} />
      <Header onLogout={onLogout} userName={userInfo?.nome} />
      
      <main className="reports-main">
        <div className="page-header">
          <h1>RELATÓRIOS DO SISTEMA</h1>
        </div>

        {/* Cards de Estatísticas Gerais */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon users">
              <FaUsers />
            </div>
            <div className="stat-content">
              <h3>{reports.totalUsuarios}</h3>
              <p>Usuários Cadastrados</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon tickets">
              <FaCheckCircle />
            </div>
            <div className="stat-content">
              <h3>{reports.totalChamados}</h3>
              <p>Total de Chamados</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon resolved">
              <FaCheckCircle />
            </div>
            <div className="stat-content">
              <h3>{reports.chamadosResolvidos}</h3>
              <p>Chamados Resolvidos</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon in-progress">
              <FaClock />
            </div>
            <div className="stat-content">
              <h3>{reports.chamadosEmAndamento}</h3>
              <p>Em Andamento</p>
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
                <span>{reports.chamadosEmAndamento} ({calculatePercentage(reports.chamadosEmAndamento, reports.totalChamados)}%)</span>
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
                <h3>API de IA</h3>
                <div className="api-status">
                  {getStatusIcon(reports.apiStatus.ai.status)}
                  <span style={{ color: getStatusColor(reports.apiStatus.ai.status) }}>
                    {getStatusText(reports.apiStatus.ai.status)}
                  </span>
                </div>
                <p className="response-time">
                  Implementação Futura
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default ReportsPage;
