// src/pages/RegisterEmployeePage.jsx

import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';
import Toast from '../components/Toast';
import ConfirmModal from '../components/ConfirmModal';
import { FaEye, FaEyeSlash, FaUser, FaTrash, FaEdit } from 'react-icons/fa';
import { userService } from '../utils/api';
import '../styles/register.css';

const RegisterEmployeePage = ({ onLogout, onNavigateToHome, onNavigateToPage, currentPage, userInfo, onNavigateToProfile }) => {
  // Lista de cargos corporativos pré-definidos
  const cargosCorporativos = [
    'Diretor',
    'Gerente',
    'Coordenador',
    'Supervisor',
    'Analista',
    'Analista de TI',
    'Analista de Sistemas',
    'Desenvolvedor',
    'Técnico',
    'Técnico de TI',
    'Suporte Técnico',
    'Especialista',
    'Consultor',
    'Assistente',
    'Assistente Administrativo',
    'Auxiliar',
    'Coordenador de TI',
    'Gerente de TI',
    'Administrador de Sistemas',
    'Analista de Suporte',
    'Analista de Negócios',
    'Product Owner',
    'Scrum Master',
    'Arquiteto de Software',
    'DevOps',
    'DBA',
    'Analista de Segurança',
    'Analista de Qualidade',
    'Analista de Dados',
    'Analista de Infraestrutura',
    'Coordenador de Projetos',
    'Gerente de Projetos',
    'Estagiário',
    'Trainee'
  ];

  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    cargo: '',
    senha: '',
    confirmarSenha: '',
    telefone: '',
    permissao: 1
  });
  const [isLoadingCadastro, setIsLoadingCadastro] = useState(false);
  const [isLoadingEdit, setIsLoadingEdit] = useState(false);
  const [isLoadingDelete, setIsLoadingDelete] = useState(false);
  const [errors, setErrors] = useState({});
  const [toast, setToast] = useState({ isVisible: false, message: '', type: 'error' });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);
  const [isConfirmEditModalOpen, setIsConfirmEditModalOpen] = useState(false);
  const [users, setUsers] = useState([]);
  const [loadingUsers, setLoadingUsers] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [editingUser, setEditingUser] = useState(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [deleteConfirmUser, setDeleteConfirmUser] = useState(null);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [changePassword, setChangePassword] = useState(false);
  const [editPassword, setEditPassword] = useState('');
  const [editConfirmPassword, setEditConfirmPassword] = useState('');
  const [showEditPassword, setShowEditPassword] = useState(false);
  const [showEditConfirmPassword, setShowEditConfirmPassword] = useState(false);
  const [editPasswordErrors, setEditPasswordErrors] = useState({});

  // Validação em tempo real - Heurística de Nielsen: Prevenção de Erros
  const validateField = (name, value) => {
    const newErrors = { ...errors };
    
    switch (name) {
      case 'nome':
        if (!value.trim()) {
          newErrors.nome = 'Nome é obrigatório';
        } else if (value.trim().length < 2) {
          newErrors.nome = 'Nome deve ter pelo menos 2 caracteres';
        } else {
          delete newErrors.nome;
        }
        break;
        
      case 'email':
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!value.trim()) {
          newErrors.email = 'E-mail é obrigatório';
        } else if (!emailRegex.test(value)) {
          newErrors.email = 'E-mail inválido';
        } else {
          delete newErrors.email;
        }
        break;
        
      case 'senha':
        if (!value) {
          newErrors.senha = 'Senha é obrigatória';
        } else if (value.length < 6) {
          newErrors.senha = 'Senha deve ter pelo menos 6 caracteres';
        } else {
          delete newErrors.senha;
        }
        // Validar confirmação de senha se já foi preenchida
        if (formData.confirmarSenha && value !== formData.confirmarSenha) {
          newErrors.confirmarSenha = 'As senhas não conferem';
        } else if (formData.confirmarSenha && value === formData.confirmarSenha) {
          delete newErrors.confirmarSenha;
        }
        break;
        
      case 'confirmarSenha':
        if (!value) {
          newErrors.confirmarSenha = 'Confirmação de senha é obrigatória';
        } else if (value !== formData.senha) {
          newErrors.confirmarSenha = 'As senhas não conferem';
        } else {
          delete newErrors.confirmarSenha;
        }
        break;
        
      case 'cargo':
        if (!value.trim()) {
          newErrors.cargo = 'Cargo é obrigatório';
        } else {
          delete newErrors.cargo;
        }
        break;
        
      case 'telefone':
        if (value && !/^[\d\s\-\(\)\+]+$/.test(value)) {
          newErrors.telefone = 'Telefone deve conter apenas números e símbolos válidos';
        } else {
          delete newErrors.telefone;
        }
        break;
        
      default:
        break;
    }
    
    setErrors(newErrors);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Validação em tempo real
    validateField(name, value);
  };

  const showToast = (message, type = 'error') => {
    setToast({ isVisible: true, message, type });
  };

  const hideToast = () => {
    setToast({ isVisible: false, message: '', type: 'error' });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    // Validação final antes do envio - Heurística de Nielsen: Prevenção de Erros
    const hasErrors = Object.keys(errors).length > 0;
    const hasEmptyRequiredFields = !formData.nome.trim() || !formData.email.trim() || 
                                 !formData.cargo.trim() || !formData.senha.trim() || !formData.confirmarSenha.trim();
    
    if (hasErrors || hasEmptyRequiredFields) {
      showToast('Por favor, corrija os erros antes de continuar.', 'error');
      return;
    }
    
    // Validar se as senhas conferem
    if (formData.senha !== formData.confirmarSenha) {
      showToast('As senhas não conferem.', 'error');
      return;
    }
    
    // Abre o modal de confirmação
    setIsConfirmModalOpen(true);
  };

  const loadUsers = async () => {
    try {
      setLoadingUsers(true);
      const usersData = await userService.getUsers();
      
      // A API pode retornar um objeto com total e lista, ou diretamente um array
      if (usersData && typeof usersData === 'object') {
        if (Array.isArray(usersData)) {
          setUsers(usersData);
        } else if (usersData.usuarios && Array.isArray(usersData.usuarios)) {
          setUsers(usersData.usuarios);
        } else if (usersData.total !== undefined) {
          // Se tiver total mas não tiver lista explícita, pode estar em outro formato
          setUsers([]);
        } else {
          setUsers([]);
        }
      } else {
        setUsers([]);
      }
    } catch (error) {
      console.error('Erro ao carregar usuários:', error);
      showToast('Erro ao carregar lista de usuários.', 'error');
      setUsers([]);
    } finally {
      setLoadingUsers(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleConfirmCadastro = async () => {
    setIsConfirmModalOpen(false);
    setIsLoadingCadastro(true);

    try {
      // Verifica se o email já existe
      try {
        const allUsers = await userService.getUsers();
        let usersArray = [];
        if (Array.isArray(allUsers)) {
          usersArray = allUsers;
        } else if (allUsers?.usuarios && Array.isArray(allUsers.usuarios)) {
          usersArray = allUsers.usuarios;
        } else if (allUsers?.items && Array.isArray(allUsers.items)) {
          usersArray = allUsers.items;
        } else if (allUsers?.users && Array.isArray(allUsers.users)) {
          usersArray = allUsers.users;
        }

        const emailLower = (formData.email || '').trim().toLowerCase();
        const exists = usersArray.some(u => ((u.email || u.Email || '') + '').toLowerCase() === emailLower);
        if (exists) {
          showToast('O e-mail informado já existe. Verifique e tente novamente.', 'error');
          setIsLoadingCadastro(false);
          return;
        }
      } catch (err) {
        // Se falhar na verificação, prossegue e confia na validação do backend
        console.warn('Não foi possível verificar emails existentes, prosseguindo para tentativa de cadastro:', err);
      }

      // Realiza o cadastro via serviço (mantendo as regras de apiClient)
      await userService.register(formData);
      showToast('Funcionário cadastrado com sucesso!', 'success');
      // Limpa o formulário
      setFormData({
        nome: '',
        email: '',
        cargo: '',
        senha: '',
        confirmarSenha: '',
        telefone: '',
        permissao: 1
      });
      setErrors({});
      // Recarrega a lista de usuários
      await loadUsers();
    } catch (error) {
      console.error('Erro no cadastro:', error);
      // Se o backend retornar erro de duplicidade, mostra mensagem adequada
      const msg = error?.data?.message || error?.message || 'Erro ao cadastrar funcionário.';
      if ((error?.data?.message || '').toLowerCase().includes('email') || (msg || '').toLowerCase().includes('email')) {
        showToast('O e-mail informado já existe. Verifique e tente novamente.', 'error');
      } else {
        showToast(msg, 'error');
      }
    } finally {
      setIsLoadingCadastro(false);
    }
  };

  const getPermissionLabel = (permissao) => {
    switch (permissao) {
      case 1: return 'Colaborador';
      case 2: return 'Suporte Técnico';
      case 3: return 'Administrador';
      default: return 'Desconhecido';
    }
  };

  const getPermissionColor = (permissao) => {
    switch (permissao) {
      case 1: return '#4299e1';
      case 2: return '#f6ad55';
      case 3: return '#48bb78';
      default: return '#6c757d';
    }
  };

  const filteredUsers = users.filter(user => {
    if (!searchTerm) return true;
    const search = searchTerm.toLowerCase();
    return (
      (user.nome && user.nome.toLowerCase().includes(search)) ||
      (user.email && user.email.toLowerCase().includes(search)) ||
      (user.cargo && user.cargo.toLowerCase().includes(search))
    );
  });

  const handleEditUser = (user) => {
    setEditingUser({
      id: user.id || user.Id,
      nome: user.nome || user.Nome || '',
      email: user.email || user.Email || '',
      cargo: user.cargo || user.Cargo || '',
      telefone: user.telefone || user.Telefone || '',
      permissao: user.permissao || user.Permissao || 1
    });
    setChangePassword(false);
    setEditPassword('');
    setEditConfirmPassword('');
    setEditPasswordErrors({});
    setIsEditModalOpen(true);
  };

  const handleCloseEditModal = () => {
    setIsEditModalOpen(false);
    setChangePassword(false);
    setEditPassword('');
    setEditConfirmPassword('');
    setEditPasswordErrors({});
    setShowEditPassword(false);
    setShowEditConfirmPassword(false);
  };

  const handleDeleteUser = (user) => {
    setDeleteConfirmUser(user);
    setIsDeleteModalOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (!deleteConfirmUser) return;
    
    setIsDeleteModalOpen(false);
    setIsLoadingDelete(true);

    try {
      const userId = deleteConfirmUser.id || deleteConfirmUser.Id;
      await userService.deleteUser(userId);
      showToast('Usuário excluído com sucesso!', 'success');
      await loadUsers();
    } catch (error) {
      console.error('Erro ao excluir usuário:', error);
      const msg = error?.data?.message || error?.message || 'Erro ao excluir usuário.';
      showToast(msg, 'error');
    } finally {
      setIsLoadingDelete(false);
      setDeleteConfirmUser(null);
    }
  };

  const handleSaveEdit = async () => {
    if (!editingUser) return;

    // Validação básica
    if (!editingUser.nome?.trim() || !editingUser.email?.trim() || !editingUser.cargo?.trim()) {
      showToast('Por favor, preencha todos os campos obrigatórios.', 'error');
      return;
    }

    // Validação de email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(editingUser.email)) {
      showToast('E-mail inválido.', 'error');
      return;
    }

    // Validação de senha se a opção de alterar senha estiver marcada
    if (changePassword) {
      if (!editPassword.trim()) {
        showToast('Por favor, preencha a nova senha.', 'error');
        return;
      }
      if (editPassword.length < 6) {
        showToast('A senha deve ter pelo menos 6 caracteres.', 'error');
        return;
      }
      if (editPassword !== editConfirmPassword) {
        showToast('As senhas não conferem.', 'error');
        return;
      }
    }

    // Abre o modal de confirmação
    setIsConfirmEditModalOpen(true);
  };

  const handleConfirmSaveEdit = async () => {
    if (!editingUser) return;

    setIsConfirmEditModalOpen(false);
    setIsEditModalOpen(false);
    setIsLoadingEdit(true);

    try {
      const userId = editingUser.id;
      const updateData = {
        Nome: editingUser.nome.trim(),
        Email: editingUser.email.trim(),
        Cargo: editingUser.cargo.trim(),
        Telefone: editingUser.telefone?.trim() || null,
        Permissao: editingUser.permissao
      };

      // Adiciona NovaSenha apenas se a opção de alterar senha estiver marcada
      if (changePassword && editPassword.trim()) {
        updateData.NovaSenha = editPassword.trim();
      }

      await userService.updateUser(userId, updateData);
      
      // Mensagem informativa quando a senha foi alterada
      if (changePassword && editPassword.trim()) {
        showToast('Usuário atualizado com sucesso! O usuário precisará trocar a senha no próximo login.', 'success');
      } else {
        showToast('Usuário atualizado com sucesso!', 'success');
      }
      
      await loadUsers();
      setEditingUser(null);
      setChangePassword(false);
      setEditPassword('');
      setEditConfirmPassword('');
      setEditPasswordErrors({});
    } catch (error) {
      console.error('Erro ao atualizar usuário:', error);
      const msg = error?.data?.message || error?.message || 'Erro ao atualizar usuário.';
      showToast(msg, 'error');
      setIsEditModalOpen(true); // Reabre o modal em caso de erro
    } finally {
      setIsLoadingEdit(false);
    }
  };

  return (
    <div className="register-layout">
      <Header onLogout={onLogout} userName={userInfo?.nome || 'Usuário'} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
      <Sidebar currentPage={currentPage || "register"} onNavigate={onNavigateToPage} userInfo={userInfo} />
      <main className="register-main-content">
        <div className="register-page-header">
          <h1>CADASTRO DE FUNCIONÁRIO</h1>
        </div>
        
        <div className="register-content-grid">
          {/* Formulário de Cadastro */}
          <div className="register-form-section">
            <button 
              className="back-button" 
              onClick={onNavigateToHome}
              aria-label="Voltar para página inicial"
            >
              ← Voltar
            </button>
            <div className="register-header">
              <h2>NOVO FUNCIONÁRIO</h2>
            </div>

            <form className="register-form" onSubmit={handleSubmit} noValidate>
          {/* Permissões do usuário */}
          <div className={`form-group`}>
            <label htmlFor="permissao">Permissão *</label>
            <div className="select-container">
              <select
                id="permissao"
                name="permissao"
                value={formData.permissao}
                onChange={(e) => handleInputChange({ target: { name: 'permissao', value: Number(e.target.value) } })}
                required
              >
                <option value={1}>Colaborador</option>
                <option value={2}>Suporte Técnico</option>
                <option value={3}>Administrador</option>
              </select>
              <div className="select-arrow">▼</div>
            </div>
          </div>
          {/* Campos do formulário com validação em tempo real */}
          <div className={`form-group ${errors.nome ? 'error' : ''}`}>
            <label htmlFor="nome">Nome Completo *</label>
            <input 
              type="text" 
              id="nome" 
              name="nome" 
              value={formData.nome}
              onChange={handleInputChange}
              placeholder="Digite o nome completo"
              required 
              aria-describedby={errors.nome ? 'nome-error' : undefined}
            />
            {errors.nome && (
              <span id="nome-error" className="error-message" role="alert">
                {errors.nome}
              </span>
            )}
          </div>
          
          <div className={`form-group ${errors.email ? 'error' : ''}`}>
            <label htmlFor="email">E-mail *</label>
            <input 
              type="email" 
              id="email" 
              name="email" 
              value={formData.email}
              onChange={handleInputChange}
              placeholder="exemplo@helpwave.com"
              required 
              aria-describedby={errors.email ? 'email-error' : undefined}
            />
            {errors.email && (
              <span id="email-error" className="error-message" role="alert">
                {errors.email}
              </span>
            )}
          </div>
          
          <div className={`form-group ${errors.cargo ? 'error' : ''}`}>
            <label htmlFor="cargo">Cargo *</label>
            <div className="select-container">
              <select
                id="cargo"
                name="cargo"
                value={formData.cargo}
                onChange={handleInputChange}
                required
                aria-describedby={errors.cargo ? 'cargo-error' : undefined}
              >
                <option value="">Selecione um cargo</option>
                {cargosCorporativos.map((cargo) => (
                  <option key={cargo} value={cargo}>
                    {cargo}
                  </option>
                ))}
              </select>
              <div className="select-arrow">▼</div>
            </div>
            {errors.cargo && (
              <span id="cargo-error" className="error-message" role="alert">
                {errors.cargo}
              </span>
            )}
          </div>
          
          <div className={`form-group ${errors.telefone ? 'error' : ''}`}>
            <label htmlFor="telefone">Telefone</label>
            <input 
              type="tel" 
              id="telefone" 
              name="telefone" 
              value={formData.telefone}
              onChange={handleInputChange}
              placeholder="(11) 99999-9999"
              aria-describedby={errors.telefone ? 'telefone-error' : undefined}
            />
            {errors.telefone && (
              <span id="telefone-error" className="error-message" role="alert">
                {errors.telefone}
              </span>
            )}
          </div>
          
          <div className={`form-group ${errors.senha ? 'error' : ''}`}>
            <label htmlFor="senha">Senha *</label>
            <div className="password-input-container">
              <input 
                type={showPassword ? 'text' : 'password'}
                id="senha" 
                name="senha" 
                value={formData.senha}
                onChange={handleInputChange}
                placeholder="Mínimo 6 caracteres"
                required 
                aria-describedby={errors.senha ? 'senha-error' : undefined}
              />
              <button
                type="button"
                className="password-toggle-register"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={showPassword ? 'Ocultar senha' : 'Mostrar senha'}
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>
            {errors.senha && (
              <span id="senha-error" className="error-message" role="alert">
                {errors.senha}
              </span>
            )}
          </div>
          
          <div className={`form-group ${errors.confirmarSenha ? 'error' : ''}`}>
            <label htmlFor="confirmarSenha">Confirmar Senha *</label>
            <div className="password-input-container">
              <input 
                type={showConfirmPassword ? 'text' : 'password'}
                id="confirmarSenha" 
                name="confirmarSenha" 
                value={formData.confirmarSenha}
                onChange={handleInputChange}
                placeholder="Repita a senha"
                required 
                aria-describedby={errors.confirmarSenha ? 'confirmarSenha-error' : undefined}
              />
              <button
                type="button"
                className="password-toggle-register"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                aria-label={showConfirmPassword ? 'Ocultar senha' : 'Mostrar senha'}
              >
                {showConfirmPassword ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>
            {errors.confirmarSenha && (
              <span id="confirmarSenha-error" className="error-message" role="alert">
                {errors.confirmarSenha}
              </span>
            )}
          </div>

          <button 
            type="submit" 
            className="submit-button" 
            disabled={isLoadingCadastro || Object.keys(errors).length > 0}
            aria-describedby="submit-help"
          >
            {isLoadingCadastro ? (
              <span className="loading-indicator">
                <span className="loading-spinner"></span>
                CADASTRANDO...
              </span>
            ) : (
              'CADASTRAR'
            )}
          </button>
          
            <div id="submit-help" className="form-help">
              * Campos obrigatórios
            </div>
          </form>
          </div>

          {/* Lista de Usuários */}
          <div className="users-list-section">
            <div className="users-list-header">
              <h2>LISTA DE USUÁRIOS</h2>
              <input
                type="text"
                className="users-search"
                placeholder="Buscar usuário..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>

            {loadingUsers ? (
              <div className="users-loading">
                <div className="loading-spinner"></div>
                <p>Carregando usuários...</p>
              </div>
            ) : (
              <div className="users-list-container">
                {filteredUsers.length === 0 ? (
                  <div className="no-users">
                    <FaUser />
                    <p>Nenhum usuário encontrado</p>
                  </div>
                ) : (
                  <div className="users-table">
                    <div className="users-table-header">
                      <div className="user-col-name">Nome</div>
                      <div className="user-col-email">Email</div>
                      <div className="user-col-cargo">Cargo</div>
                      <div className="user-col-permission">Permissão</div>
                      <div className="user-col-actions">Ações</div>
                    </div>
                    <div className="users-table-body">
                      {filteredUsers.map((user) => (
                        <div key={user.id || user.Id} className="user-row">
                          <div className="user-col-name">
                            <FaUser className="user-icon" />
                            {user.nome || user.Nome || 'N/A'}
                          </div>
                          <div className="user-col-email">{user.email || user.Email || 'N/A'}</div>
                          <div className="user-col-cargo">{user.cargo || user.Cargo || 'N/A'}</div>
                          <div className="user-col-permission">
                            <span 
                              className="permission-badge"
                              style={{ backgroundColor: getPermissionColor(user.permissao || user.Permissao) }}
                            >
                              {getPermissionLabel(user.permissao || user.Permissao)}
                            </span>
                          </div>
                          <div className="user-col-actions">
                            <button
                              className="action-button edit-button"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleEditUser(user);
                              }}
                              aria-label="Editar usuário"
                              title="Editar usuário"
                            >
                              <FaEdit />
                            </button>
                            <button
                              className="action-button delete-button"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleDeleteUser(user);
                              }}
                              aria-label="Excluir usuário"
                              title="Excluir usuário"
                            >
                              <FaTrash />
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
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
        title="CONFIRMAR CADASTRO"
        message={`Tem certeza que deseja cadastrar o funcionário ${formData.nome || ''}?`}
        confirmText="Confirmar"
        cancelText="Cancelar"
        onConfirm={handleConfirmCadastro}
        onCancel={() => setIsConfirmModalOpen(false)}
      />

      {/* Modal de Edição */}
      {isEditModalOpen && editingUser && (
        <div className="modal-overlay" onClick={handleCloseEditModal}>
          <div className="modal-content edit-user-modal" onClick={(e) => e.stopPropagation()}>
            <header className="modal-header">
              <h2>EDITAR USUÁRIO</h2>
            </header>
            <main className="modal-body">
              <div className="form-group">
                <label htmlFor="edit-nome">Nome Completo *</label>
                <input
                  type="text"
                  id="edit-nome"
                  value={editingUser.nome}
                  onChange={(e) => setEditingUser({ ...editingUser, nome: e.target.value })}
                  placeholder="Digite o nome completo"
                />
              </div>
              <div className="form-group">
                <label htmlFor="edit-email">E-mail *</label>
                <input
                  type="email"
                  id="edit-email"
                  value={editingUser.email}
                  onChange={(e) => setEditingUser({ ...editingUser, email: e.target.value })}
                  placeholder="exemplo@helpwave.com"
                />
              </div>
              <div className="form-group">
                <label htmlFor="edit-cargo">Cargo *</label>
                <div className="select-container">
                  <select
                    id="edit-cargo"
                    value={editingUser.cargo}
                    onChange={(e) => setEditingUser({ ...editingUser, cargo: e.target.value })}
                  >
                    <option value="">Selecione um cargo</option>
                    {cargosCorporativos.map((cargo) => (
                      <option key={cargo} value={cargo}>
                        {cargo}
                      </option>
                    ))}
                  </select>
                  <div className="select-arrow">▼</div>
                </div>
              </div>
              <div className="form-group">
                <label htmlFor="edit-telefone">Telefone</label>
                <input
                  type="tel"
                  id="edit-telefone"
                  value={editingUser.telefone}
                  onChange={(e) => setEditingUser({ ...editingUser, telefone: e.target.value })}
                  placeholder="(11) 99999-9999"
                />
              </div>
              <div className="form-group">
                <label htmlFor="edit-permissao">Permissão *</label>
                <div className="select-container">
                  <select
                    id="edit-permissao"
                    value={editingUser.permissao}
                    onChange={(e) => setEditingUser({ ...editingUser, permissao: Number(e.target.value) })}
                  >
                    <option value={1}>Colaborador</option>
                    <option value={2}>Suporte Técnico</option>
                    <option value={3}>Administrador</option>
                  </select>
                  <div className="select-arrow">▼</div>
                </div>
              </div>
              
              {/* Checkbox para alterar senha */}
              <div className="form-group">
                <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                  <input
                    type="checkbox"
                    checked={changePassword}
                    onChange={(e) => {
                      setChangePassword(e.target.checked);
                      if (!e.target.checked) {
                        setEditPassword('');
                        setEditConfirmPassword('');
                        setEditPasswordErrors({});
                      }
                    }}
                    style={{ width: 'auto', cursor: 'pointer' }}
                  />
                  <span>Alterar senha</span>
                </label>
              </div>

              {/* Campos de senha (mostrados apenas se checkbox marcada) */}
              {changePassword && (
                <>
                  <div className={`form-group ${editPasswordErrors.senha ? 'error' : ''}`}>
                    <label htmlFor="edit-senha">Nova Senha *</label>
                    <div className="password-input-container">
                      <input
                        type={showEditPassword ? 'text' : 'password'}
                        id="edit-senha"
                        value={editPassword}
                        onChange={(e) => {
                          setEditPassword(e.target.value);
                          // Validação em tempo real
                          if (e.target.value && e.target.value.length < 6) {
                            setEditPasswordErrors({ ...editPasswordErrors, senha: 'Senha deve ter pelo menos 6 caracteres' });
                          } else {
                            const newErrors = { ...editPasswordErrors };
                            delete newErrors.senha;
                            setEditPasswordErrors(newErrors);
                          }
                          // Verifica se as senhas conferem
                          if (e.target.value !== editConfirmPassword && editConfirmPassword) {
                            setEditPasswordErrors({ ...editPasswordErrors, confirmarSenha: 'As senhas não conferem' });
                          } else if (e.target.value === editConfirmPassword && editConfirmPassword) {
                            const newErrors = { ...editPasswordErrors };
                            delete newErrors.confirmarSenha;
                            setEditPasswordErrors(newErrors);
                          }
                        }}
                        placeholder="Mínimo 6 caracteres"
                      />
                      <button
                        type="button"
                        className="password-toggle-register"
                        onClick={() => setShowEditPassword(!showEditPassword)}
                        aria-label={showEditPassword ? 'Ocultar senha' : 'Mostrar senha'}
                      >
                        {showEditPassword ? <FaEyeSlash /> : <FaEye />}
                      </button>
                    </div>
                    {editPasswordErrors.senha && (
                      <span className="error-message" role="alert">
                        {editPasswordErrors.senha}
                      </span>
                    )}
                  </div>
                  
                  <div className={`form-group ${editPasswordErrors.confirmarSenha ? 'error' : ''}`}>
                    <label htmlFor="edit-confirmar-senha">Confirmar Nova Senha *</label>
                    <div className="password-input-container">
                      <input
                        type={showEditConfirmPassword ? 'text' : 'password'}
                        id="edit-confirmar-senha"
                        value={editConfirmPassword}
                        onChange={(e) => {
                          setEditConfirmPassword(e.target.value);
                          // Validação em tempo real
                          if (e.target.value !== editPassword) {
                            setEditPasswordErrors({ ...editPasswordErrors, confirmarSenha: 'As senhas não conferem' });
                          } else {
                            const newErrors = { ...editPasswordErrors };
                            delete newErrors.confirmarSenha;
                            setEditPasswordErrors(newErrors);
                          }
                        }}
                        placeholder="Repita a senha"
                      />
                      <button
                        type="button"
                        className="password-toggle-register"
                        onClick={() => setShowEditConfirmPassword(!showEditConfirmPassword)}
                        aria-label={showEditConfirmPassword ? 'Ocultar senha' : 'Mostrar senha'}
                      >
                        {showEditConfirmPassword ? <FaEyeSlash /> : <FaEye />}
                      </button>
                    </div>
                    {editPasswordErrors.confirmarSenha && (
                      <span className="error-message" role="alert">
                        {editPasswordErrors.confirmarSenha}
                      </span>
                    )}
                  </div>
                </>
              )}
            </main>
            <footer className="modal-footer">
              <button className="modal-button modal-button-cancel" onClick={handleCloseEditModal} disabled={isLoadingEdit}>
                Cancelar
              </button>
              <button className="modal-button modal-button-confirm" onClick={handleSaveEdit} disabled={isLoadingEdit}>
                {isLoadingEdit ? 'Salvando...' : 'Salvar'}
              </button>
            </footer>
          </div>
        </div>
      )}

      {/* Modal de Confirmação de Edição */}
      <ConfirmModal
        isOpen={isConfirmEditModalOpen}
        title="CONFIRMAR EDIÇÃO"
        message={`Tem certeza que deseja salvar as alterações no usuário ${editingUser?.nome || ''}?`}
        confirmText="Salvar"
        cancelText="Cancelar"
        onConfirm={handleConfirmSaveEdit}
        onCancel={() => setIsConfirmEditModalOpen(false)}
        isLoading={isLoadingEdit}
      />

      {/* Modal de Confirmação de Exclusão */}
      <ConfirmModal
        isOpen={isDeleteModalOpen}
        title="CONFIRMAR EXCLUSÃO"
        message={`Tem certeza que deseja excluir o usuário ${deleteConfirmUser?.nome || deleteConfirmUser?.Nome || ''}? Esta ação não pode ser desfeita.`}
        confirmText="Excluir"
        cancelText="Cancelar"
        isDangerous={true}
        onConfirm={handleConfirmDelete}
        onCancel={() => {
          setIsDeleteModalOpen(false);
          setDeleteConfirmUser(null);
        }}
        isLoading={isLoadingDelete}
      />
      <Footer />
    </div>
  );
};

export default RegisterEmployeePage;