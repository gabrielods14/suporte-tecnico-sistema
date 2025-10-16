// src/pages/RegisterEmployeePage.jsx

import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import Toast from '../components/Toast';
import '../styles/register.css';

const RegisterEmployeePage = ({ onLogout, onNavigateToHome, userInfo }) => {
  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    cargo: '',
    senha: '',
    telefone: '',
    permissao: 1
  });
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [toast, setToast] = useState({ isVisible: false, message: '', type: 'error' });

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
                                 !formData.cargo.trim() || !formData.senha.trim();
    
    if (hasErrors || hasEmptyRequiredFields) {
      showToast('Por favor, corrija os erros antes de continuar.', 'error');
      return;
    }
    
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        showToast('Funcionário cadastrado com sucesso!', 'success');
        // Limpa o formulário
        setFormData({
          nome: '',
          email: '',
          cargo: '',
          senha: '',
          telefone: '',
          permissao: 1
        });
        setErrors({});
      } else {
        showToast(data.message || 'Erro ao cadastrar funcionário.', 'error');
      }
    } catch (error) {
      console.error('Erro no cadastro:', error);
      showToast('Erro de conexão. Tente novamente.', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="register-layout">
      <Header onLogout={onLogout} userName={userInfo?.nome} />
      <Sidebar />
      <main className="register-main-content">
        <button 
          className="back-button" 
          onClick={onNavigateToHome}
          aria-label="Voltar para página inicial"
        >
          ← Voltar
        </button>
        <div className="register-header">
          <h2>CADASTRO DE FUNCIONÁRIO</h2>
        </div>
        <form className="register-form" onSubmit={handleSubmit} noValidate>
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
              placeholder="exemplo@empresa.com"
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
              placeholder="Ex: Desenvolvedor, Analista"
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
            <input 
              type="password" 
              id="senha" 
              name="senha" 
              value={formData.senha}
              onChange={handleInputChange}
              placeholder="Mínimo 6 caracteres"
              required 
              aria-describedby={errors.senha ? 'senha-error' : undefined}
            />
            {errors.senha && (
              <span id="senha-error" className="error-message" role="alert">
                {errors.senha}
              </span>
            )}
          </div>

          <button 
            type="submit" 
            className="submit-button" 
            disabled={isLoading || Object.keys(errors).length > 0}
            aria-describedby="submit-help"
          >
            {isLoading ? (
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

export default RegisterEmployeePage;