// src/pages/UserProfilePage.jsx
import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import Toast from '../components/Toast';
import '../styles/profile.css';

const UserProfilePage = ({ onLogout, onNavigateToHome, onNavigateToPage, onNavigateToProfile, userInfo, onUpdateUserInfo }) => {
  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    telefone: '',
    cargo: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [errors, setErrors] = useState({});
  const [toast, setToast] = useState({ isVisible: false, message: '', type: 'error' });

  // Carrega os dados do usuário quando o componente é montado
  useEffect(() => {
    const loadUserData = async () => {
      try {
        const token = localStorage.getItem('authToken');
        if (!token) {
          console.warn('UserProfilePage - Token não encontrado');
          return;
        }
        
        console.log('UserProfilePage - Buscando dados via /api/Usuarios/meu-perfil');
        const response = await fetch(`http://localhost:5000/api/Usuarios/meu-perfil`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Accept': 'application/json'
          }
        });
        
        console.log('UserProfilePage - Resposta da API:', response.status, response.statusText);
        
        if (response.ok) {
          const userData = await response.json();
          console.log('UserProfilePage - Dados do perfil carregados:', userData);
          
          // Atualiza o formData com os dados recebidos
          const newFormData = {
            nome: userData.nome || userData.Nome || '',
            email: userData.email || userData.Email || '',
            telefone: userData.telefone || userData.Telefone || '',
            cargo: userData.cargo || userData.Cargo || ''
          };
          
          setFormData(newFormData);
          
          // Atualiza o userInfo no App se houver callback
          if (onUpdateUserInfo) {
            const updatedUserInfo = {
              id: userData.id || userData.Id,
              nome: newFormData.nome,
              email: newFormData.email,
              telefone: newFormData.telefone,
              cargo: newFormData.cargo,
              permissao: userData.permissao || userData.Permissao || userInfo?.permissao
            };
            console.log('UserProfilePage - Atualizando userInfo no App:', updatedUserInfo);
            onUpdateUserInfo(updatedUserInfo);
          }
        } else {
          const errorData = await response.json().catch(() => ({}));
          console.warn('UserProfilePage - Erro ao buscar dados do perfil:', response.status, errorData);
          
          // Se falhar, tenta usar os dados do userInfo se existirem
          if (userInfo && (userInfo.nome || userInfo.email)) {
            setFormData({
              nome: userInfo.nome || '',
              email: userInfo.email || '',
              telefone: userInfo.telefone || '',
              cargo: userInfo.cargo || ''
            });
          }
        }
      } catch (error) {
        console.error('UserProfilePage - Erro ao carregar dados do perfil:', error);
        
        // Se falhar, tenta usar os dados do userInfo se existirem
        if (userInfo && (userInfo.nome || userInfo.email)) {
          setFormData({
            nome: userInfo.nome || '',
            email: userInfo.email || '',
            telefone: userInfo.telefone || '',
            cargo: userInfo.cargo || ''
          });
        }
      }
    };
    
    loadUserData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Executa apenas uma vez ao montar o componente

  // Validação em tempo real
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
        
      case 'telefone':
        if (value && !/^[\d\s\-\(\)\+]+$/.test(value)) {
          newErrors.telefone = 'Telefone deve conter apenas números e símbolos válidos';
        } else {
          delete newErrors.telefone;
        }
        break;
        
      case 'cargo':
        if (!value.trim()) {
          newErrors.cargo = 'Cargo é obrigatório';
        } else {
          delete newErrors.cargo;
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
    
    // Validação em tempo real apenas quando estiver editando
    if (isEditing) {
      validateField(name, value);
    }
  };

  const showToast = (message, type = 'error') => {
    setToast({ isVisible: true, message, type });
  };

  const hideToast = () => {
    setToast({ isVisible: false, message: '', type: 'error' });
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    // Restaura os dados originais
    if (userInfo) {
      setFormData({
        nome: userInfo.nome || '',
        email: userInfo.email || '',
        telefone: userInfo.telefone || '',
        cargo: userInfo.cargo || ''
      });
    }
    setIsEditing(false);
    setErrors({});
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    // Validação final antes do envio
    const hasErrors = Object.keys(errors).length > 0;
    const hasEmptyRequiredFields = !formData.nome.trim() || !formData.email.trim() || !formData.cargo.trim();
    
    if (hasErrors || hasEmptyRequiredFields) {
      showToast('Por favor, corrija os erros antes de salvar.', 'error');
      return;
    }
    
    setIsLoading(true);

    try {
      const token = localStorage.getItem('authToken');

      if (!token) {
        showToast('Token de autenticação não encontrado.', 'error');
        setIsLoading(false);
        return;
      }

      console.log('UserProfilePage - Atualizando perfil via /api/Usuarios/meu-perfil');
      const response = await fetch(`http://localhost:5000/api/Usuarios/meu-perfil`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          nome: formData.nome,
          email: formData.email,
          telefone: formData.telefone,
          cargo: formData.cargo
        }),
      });

      const data = await response.json().catch(() => ({}));

      if (response.ok) {
        showToast('Perfil atualizado com sucesso!', 'success');
        setIsEditing(false);
        // Atualiza as informações do usuário no App
        if (onUpdateUserInfo) {
          onUpdateUserInfo({
            ...userInfo,
            ...formData
          });
        }
      } else {
        showToast(data.message || 'Erro ao atualizar perfil.', 'error');
      }
    } catch (error) {
      console.error('Erro ao atualizar perfil:', error);
      showToast('Erro de conexão. Tente novamente.', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const userName = userInfo?.nome || formData.nome || 'Usuário';
  const firstName = userName?.split(' ')[0] || 'Usuário';
  
  // Debug: verificar dados
  console.log('UserProfilePage - userInfo:', userInfo);
  console.log('UserProfilePage - formData:', formData);
  console.log('UserProfilePage - userName:', userName);

  return (
    <div className="profile-layout">
      <Header onLogout={onLogout} userName={userName} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
      <Sidebar currentPage="profile" onNavigate={onNavigateToPage} />
      <main className="profile-main-content">
        <button 
          className="back-button" 
          onClick={onNavigateToHome}
          aria-label="Voltar para página inicial"
        >
          ← Voltar
        </button>
        <div className="profile-header">
          <h2>MEU PERFIL</h2>
        </div>

        <div className="profile-card">
          <div className="profile-avatar-section">
            <div className="profile-avatar">
              <span>{firstName.charAt(0).toUpperCase()}</span>
            </div>
            <h3 className="profile-name">{formData.nome || userInfo?.nome || 'Usuário'}</h3>
            <p className="profile-role">{formData.cargo || userInfo?.cargo || 'Cargo não informado'}</p>
          </div>

          <form className="profile-form" onSubmit={handleSubmit} noValidate>
            <div className={`form-group ${errors.nome ? 'error' : ''}`}>
              <label htmlFor="nome">Nome Completo *</label>
              <input 
                type="text" 
                id="nome" 
                name="nome" 
                value={formData.nome}
                onChange={handleInputChange}
                placeholder="Digite seu nome completo"
                disabled={!isEditing}
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
                disabled={!isEditing}
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
              <input 
                type="text" 
                id="cargo" 
                name="cargo" 
                value={formData.cargo}
                onChange={handleInputChange}
                placeholder="Ex: Administrador, Gestor, Técnico"
                disabled={!isEditing}
                required 
                aria-describedby={errors.cargo ? 'cargo-error' : undefined}
              />
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
                disabled={!isEditing}
                aria-describedby={errors.telefone ? 'telefone-error' : undefined}
              />
              {errors.telefone && (
                <span id="telefone-error" className="error-message" role="alert">
                  {errors.telefone}
                </span>
              )}
            </div>

            <div className="profile-actions">
              {!isEditing ? (
                <button 
                  type="button" 
                  className="edit-button" 
                  onClick={handleEdit}
                >
                  EDITAR PERFIL
                </button>
              ) : (
                <div className="action-buttons">
                  <button 
                    type="button" 
                    className="cancel-button" 
                    onClick={handleCancel}
                    disabled={isLoading}
                  >
                    CANCELAR
                  </button>
                  <button 
                    type="submit" 
                    className="save-button" 
                    disabled={isLoading || Object.keys(errors).length > 0}
                  >
                    {isLoading ? (
                      <span className="loading-indicator">
                        <span className="loading-spinner"></span>
                        SALVANDO...
                      </span>
                    ) : (
                      'SALVAR ALTERAÇÕES'
                    )}
                  </button>
                </div>
              )}
            </div>
          </form>
        </div>
      </main>
      
      <Toast
        isVisible={toast.isVisible}
        message={toast.message}
        type={toast.type}
        onClose={hideToast}
      />
    </div>
  );
};

export default UserProfilePage;

