// src/pages/NewTicketPage.jsx

import React, { useState } from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import Toast from '../components/Toast';
import ConfirmModal from '../components/ConfirmModal';
import '../styles/newticket.css';
import { ticketService } from '../utils/api';

const NewTicketPage = ({ onLogout, onNavigateToHome, onNavigateToPage, userInfo, onNavigateToProfile }) => {
  const [formData, setFormData] = useState({
    tipoChamado: '',
    titulo: '',
    descricao: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [toast, setToast] = useState({ isVisible: false, message: '', type: 'error' });
  const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);

  // Opções para o dropdown de tipo de chamado
  const tiposChamado = [
    { value: '', label: 'Selecione o tipo de chamado' },
    { value: 'Suporte', label: 'Suporte' },
    { value: 'Manutenção', label: 'Manutenção' },
    { value: 'Instalação', label: 'Instalação' },
    { value: 'Consultoria', label: 'Consultoria' },
    { value: 'Emergência', label: 'Emergência' }
  ];

  // Validação em tempo real - Heurística de Nielsen: Prevenção de Erros
  const validateField = (name, value) => {
    const newErrors = { ...errors };
    
    switch (name) {
      case 'tipoChamado':
        if (!value.trim()) {
          newErrors.tipoChamado = 'Tipo de chamado é obrigatório';
        } else {
          delete newErrors.tipoChamado;
        }
        break;
        
      case 'titulo':
        if (!value.trim()) {
          newErrors.titulo = 'Título é obrigatório';
        } else if (value.trim().length < 5) {
          newErrors.titulo = 'Título deve ter pelo menos 5 caracteres';
        } else if (value.trim().length > 100) {
          newErrors.titulo = 'Título deve ter no máximo 100 caracteres';
        } else {
          delete newErrors.titulo;
        }
        break;
        
      case 'descricao':
        if (!value.trim()) {
          newErrors.descricao = 'Descrição é obrigatória';
        } else if (value.trim().length < 10) {
          newErrors.descricao = 'Descrição deve ter pelo menos 10 caracteres';
        } else if (value.trim().length > 1000) {
          newErrors.descricao = 'Descrição deve ter no máximo 1000 caracteres';
        } else {
          delete newErrors.descricao;
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

  const handleSubmit = (event) => {
    event.preventDefault();
    
    // Validação final antes do envio - Heurística de Nielsen: Prevenção de Erros
    const hasErrors = Object.keys(errors).length > 0;
    const hasEmptyRequiredFields = !formData.tipoChamado.trim() || 
                                 !formData.titulo.trim() || 
                                 !formData.descricao.trim();
    
    if (hasErrors || hasEmptyRequiredFields) {
      showToast('Por favor, preencha todos os campos obrigatórios corretamente.', 'error');
      return;
    }
    
    // Abre o modal de confirmação
    setIsConfirmModalOpen(true);
  };

  const handleConfirmSubmit = async () => {
    setIsConfirmModalOpen(false);
    setIsLoading(true);

    try {
      const solicitanteId = (userInfo?.id && Number(userInfo.id)) || (() => {
        try {
          const token = localStorage.getItem('authToken');
          if (!token) return undefined;
          const payload = JSON.parse(atob(token.split('.')[1]));
          return payload?.sub ? Number(payload.sub) : undefined;
        } catch {
          return undefined;
        }
      })();

      const payload = {
        tipo: formData.tipoChamado,
        titulo: formData.titulo,
        descricao: formData.descricao,
        prioridade: 2, // Média
        solicitanteId: solicitanteId
      };

      const data = await ticketService.createTicket(payload);

      if (data) {
        showToast('Chamado criado com sucesso!', 'success');
        
        // Limpa o formulário
        setFormData({
          tipoChamado: '',
          titulo: '',
          descricao: ''
        });
        setErrors({});
        
        // Navega para a página de chamados em andamento após 1.5s
        setTimeout(() => {
          if (onNavigateToPage) {
            onNavigateToPage('pending-tickets');
          }
        }, 1500);
        
      }
      
    } catch (error) {
      console.error('Erro ao criar chamado:', error);
      showToast('Erro de conexão. Verifique se o servidor está rodando.', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="newticket-layout">
      <Header onLogout={onLogout} userName={userInfo?.nome || 'Usuário'} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
      <Sidebar currentPage="newticket" onNavigate={onNavigateToPage} userInfo={userInfo} />
      <main className="newticket-main-content">
        <button 
          className="back-button" 
          onClick={onNavigateToHome}
          aria-label="Voltar para página inicial"
        >
          ← Voltar
        </button>
        <div className="newticket-header">
          <h1>NOVO CHAMADO</h1>
        </div>
        
        <form className="newticket-form" onSubmit={handleSubmit} noValidate>
          {/* Campo Tipo de Chamado */}
          <div className={`form-group ${errors.tipoChamado ? 'error' : ''}`}>
            <label htmlFor="tipoChamado">TIPO DE CHAMADO *</label>
            <div className="select-container">
              <select 
                id="tipoChamado" 
                name="tipoChamado" 
                value={formData.tipoChamado}
                onChange={handleInputChange}
                required 
                aria-describedby={errors.tipoChamado ? 'tipoChamado-error' : undefined}
              >
                {tiposChamado.map((tipo) => (
                  <option key={tipo.value} value={tipo.value}>
                    {tipo.label}
                  </option>
                ))}
              </select>
              <div className="select-arrow">▼</div>
            </div>
            {errors.tipoChamado && (
              <span id="tipoChamado-error" className="error-message" role="alert">
                {errors.tipoChamado}
              </span>
            )}
          </div>
          
          {/* Campo Título */}
          <div className={`form-group ${errors.titulo ? 'error' : ''}`}>
            <label htmlFor="titulo">TÍTULO DO CHAMADO *</label>
            <input 
              type="text" 
              id="titulo" 
              name="titulo" 
              value={formData.titulo}
              onChange={handleInputChange}
              placeholder="Digite um título descritivo para o chamado"
              required 
              maxLength="100"
              aria-describedby={errors.titulo ? 'titulo-error' : undefined}
            />
            <div className="character-count">
              {formData.titulo.length}/100 caracteres
            </div>
            {errors.titulo && (
              <span id="titulo-error" className="error-message" role="alert">
                {errors.titulo}
              </span>
            )}
          </div>
          
          {/* Campo Descrição */}
          <div className={`form-group ${errors.descricao ? 'error' : ''}`}>
            <label htmlFor="descricao">DESCRIÇÃO *</label>
            <textarea 
              id="descricao" 
              name="descricao" 
              value={formData.descricao}
              onChange={handleInputChange}
              placeholder="Descreva detalhadamente o problema ou solicitação"
              required 
              maxLength="1000"
              rows="8"
              aria-describedby={errors.descricao ? 'descricao-error' : undefined}
            />
            <div className="character-count">
              {formData.descricao.length}/1000 caracteres
            </div>
            {errors.descricao && (
              <span id="descricao-error" className="error-message" role="alert">
                {errors.descricao}
              </span>
            )}
          </div>

          {/* Botão de Envio */}
          <button 
            type="submit" 
            className="submit-button" 
            disabled={isLoading || Object.keys(errors).length > 0}
            aria-describedby="submit-help"
          >
            {isLoading ? (
              <span className="loading-indicator">
                <span className="loading-spinner"></span>
                ENVIANDO...
              </span>
            ) : (
              'ENVIAR'
            )}
          </button>
          
          <div id="submit-help" className="form-help">
            * Campos obrigatórios
          </div>
        </form>
      </main>
      
      <Toast
        isVisible={toast.isVisible}
        message={toast.message}
        type={toast.type}
        onClose={hideToast}
      />
      
      <ConfirmModal
        isOpen={isConfirmModalOpen}
        title="CONFIRMAR CHAMADO"
        message={`Tem certeza que deseja enviar o chamado com o título "${formData.titulo}"?`}
        confirmText="Confirmar"
        cancelText="Cancelar"
        onConfirm={handleConfirmSubmit}
        onCancel={() => setIsConfirmModalOpen(false)}
      />
    </div>
  );
};

export default NewTicketPage;
