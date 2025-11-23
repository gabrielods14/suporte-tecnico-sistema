// src/pages/UsersReportPage.jsx
import React, { useState, useEffect } from 'react';
import '../styles/users-report.css';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import { FaSearch, FaUsers } from 'react-icons/fa';
import { userService } from '../utils/api';

function mapPermissaoToLabel(p) {
  const n = Number(p);
  if (n === 1) return 'Colaborador';
  if (n === 2) return 'Suporte Técnico';
  if (n === 3) return 'Administrador';
  return 'Desconhecido';
}

function UsersReportPage({ onLogout, onNavigateToHome, onNavigateToPage, currentPage, userInfo, onNavigateToProfile, onViewUser }) {
  const [users, setUsers] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    loadUsers();
  }, []);

  useEffect(() => {
    applyFilter();
  }, [users, search]);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const res = await userService.getUsers();
      console.log('UsersReportPage - Resposta da API:', res);
      
      // A API pode retornar diferentes formatos
      let list = [];
      if (Array.isArray(res)) {
        list = res;
      } else if (res && Array.isArray(res.items)) {
        list = res.items;
      } else if (res && Array.isArray(res.users)) {
        list = res.users;
      } else if (res && Array.isArray(res.usuarios)) {
        // Formato retornado pela API HelpWave
        list = res.usuarios;
      } else if (res && Array.isArray(res.data)) {
        list = res.data;
      } else if (res && typeof res === 'object' && Object.keys(res).length > 0) {
        // Tentar interpretar como retorno paginado com 'total' e 'lista'
        list = res.lista || res.list || [];
      }

      console.log('UsersReportPage - Lista extraída:', list);

      // Normalizar campos básicos
      const mapped = list.map(u => ({
        id: u.id || u.Id || u.userId || u.user_id,
        nome: u.nome || u.Nome || u.name || u.email || 'Usuário',
        email: u.email || u.Email || u.username || '',
        cargo: u.cargo || u.Cargo || '',
        permissao: u.permissao || u.Permissao || u.role || 1
      }));

      console.log('UsersReportPage - Dados mapeados:', mapped);
      setUsers(mapped);
    } catch (error) {
      console.error('Erro ao carregar usuários:', error);
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  const applyFilter = () => {
    const q = search.trim().toLowerCase();
    if (!q) {
      setFiltered(users);
      return;
    }
    const f = users.filter(u => {
      return String(u.id).includes(q) || (u.nome || '').toLowerCase().includes(q) || (u.email || '').toLowerCase().includes(q);
    });
    setFiltered(f);
  };

  const handleRowClick = (user) => {
    if (onViewUser) {
      onViewUser(user.id);
      return;
    }
    // fallback: navigate to page and set selectedUserId in parent handled via onNavigateToPage
    if (onNavigateToPage) {
      // store selected id in localStorage for the detail page to pick up if parent doesn't manage state
      localStorage.setItem('selectedUserId', user.id);
      onNavigateToPage('user-activity');
    }
  };

  if (loading) {
    return (
      <div className="users-report-page">
        <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} userInfo={userInfo} />
        <Header onLogout={onLogout} userName={userInfo?.nome || 'Usuário'} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
        <main className="users-report-main">
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Carregando usuários...</p>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="users-report-page">
      <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} userInfo={userInfo} />
      <Header onLogout={onLogout} userName={userInfo?.nome} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />

      <main className="users-report-main">
        <button 
          className="back-button" 
          onClick={onNavigateToHome}
          aria-label="Voltar para página inicial"
        >
          ← Voltar
        </button>
        
        <div className="page-header">
          <h1>RELATÓRIO DE USUÁRIOS</h1>
        </div>

        <div className="filters-section">
          <div className="search-box">
            <FaSearch className="search-icon" />
            <input 
              type="text"
              placeholder="Buscar por id, nome ou e-mail" 
              value={search} 
              onChange={(e) => setSearch(e.target.value)} 
            />
          </div>
        </div>

        <div className="table-section">
          <table className="users-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>NOME</th>
                <th>E-MAIL</th>
                <th>CARGO</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan="4">Nenhum usuário encontrado</td>
                </tr>
              ) : (
                filtered.map(u => (
                  <tr key={u.id} onClick={() => handleRowClick(u)} style={{ cursor: 'pointer' }}>
                    <td>{String(u.id)}</td>
                    <td>{u.nome}</td>
                    <td>{u.email}</td>
                    <td>{u.cargo || mapPermissaoToLabel(u.permissao)}</td>
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

export default UsersReportPage;
