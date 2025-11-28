// src/components/FirstAccessModal.jsx
import React, { useState } from 'react';
import ConfirmModal from './ConfirmModal';
import Toast from './Toast';
import { FaEye, FaEyeSlash, FaLock } from 'react-icons/fa';
import { userService } from '../utils/api';
import '../styles/first-access-modal.css';

function FirstAccessModal({ isOpen, onSuccess }) {
  console.log('FirstAccessModal - isOpen:', isOpen);
  const [senhaAtual, setSenhaAtual] = useState('');
  const [novaSenha, setNovaSenha] = useState('');
  const [confirmarSenha, setConfirmarSenha] = useState('');
  const [showSenhaAtual, setShowSenhaAtual] = useState(false);
  const [showNovaSenha, setShowNovaSenha] = useState(false);
  const [showConfirmarSenha, setShowConfirmarSenha] = useState(false);
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);
  const [toast, setToast] = useState({ isVisible: false, message: '', type: 'error' });

  const showToast = (message, type = 'error') => {
    setToast({ isVisible: true, message, type });
  };

  const hideToast = () => {
    setToast({ isVisible: false, message: '', type: 'error' });
  };

  const validateField = (name, value) => {
    const newErrors = { ...errors };

    switch (name) {
      case 'senhaAtual':
        if (!value.trim()) {
          newErrors.senhaAtual = 'Senha atual é obrigatória';
        } else {
          delete newErrors.senhaAtual;
        }
        break;

      case 'novaSenha':
        if (!value.trim()) {
          newErrors.novaSenha = 'Nova senha é obrigatória';
        } else if (value.length < 6) {
          newErrors.novaSenha = 'A senha deve ter pelo menos 6 caracteres';
        } else {
          delete newErrors.novaSenha;
        }
        // Verifica se as senhas conferem
        if (value !== confirmarSenha && confirmarSenha) {
          newErrors.confirmarSenha = 'As senhas não conferem';
        } else if (value === confirmarSenha && confirmarSenha) {
          delete newErrors.confirmarSenha;
        }
        break;

      case 'confirmarSenha':
        if (!value.trim()) {
          newErrors.confirmarSenha = 'Confirmação de senha é obrigatória';
        } else if (value !== novaSenha) {
          newErrors.confirmarSenha = 'As senhas não conferem';
        } else {
          delete newErrors.confirmarSenha;
        }
        break;

      default:
        break;
    }

    setErrors(newErrors);
  };

  const handleInputChange = (name, value) => {
    switch (name) {
      case 'senhaAtual':
        setSenhaAtual(value);
        validateField('senhaAtual', value);
        break;
      case 'novaSenha':
        setNovaSenha(value);
        validateField('novaSenha', value);
        break;
      case 'confirmarSenha':
        setConfirmarSenha(value);
        validateField('confirmarSenha', value);
        break;
      default:
        break;
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validação final
    const hasErrors = Object.keys(errors).length > 0;
    const hasEmptyFields = !senhaAtual.trim() || !novaSenha.trim() || !confirmarSenha.trim();

    if (hasErrors || hasEmptyFields) {
      // Valida todos os campos
      validateField('senhaAtual', senhaAtual);
      validateField('novaSenha', novaSenha);
      validateField('confirmarSenha', confirmarSenha);
      showToast('Por favor, preencha todos os campos corretamente.', 'error');
      return;
    }

    if (novaSenha !== confirmarSenha) {
      showToast('As senhas não conferem.', 'error');
      return;
    }

    if (novaSenha.length < 6) {
      showToast('A senha deve ter pelo menos 6 caracteres.', 'error');
      return;
    }

    // Abre modal de confirmação
    setIsConfirmModalOpen(true);
  };

  const handleConfirmChangePassword = async () => {
    setIsConfirmModalOpen(false);
    setIsLoading(true);

    try {
      await userService.alterarSenha(senhaAtual, novaSenha);
      showToast('Senha alterada com sucesso!', 'success');
      
      // Limpa os campos
      setSenhaAtual('');
      setNovaSenha('');
      setConfirmarSenha('');
      setErrors({});
      
      // Chama callback de sucesso após um pequeno delay para mostrar o toast
      setTimeout(() => {
        if (onSuccess) {
          onSuccess();
        }
      }, 1500);
    } catch (error) {
      console.error('Erro ao alterar senha:', error);
      const msg = error?.data?.message || error?.message || 'Erro ao alterar senha.';
      showToast(msg, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  console.log('FirstAccessModal - Render - isOpen:', isOpen);
  
  if (!isOpen) {
    console.log('FirstAccessModal - Não renderizando (isOpen = false)');
    return null;
  }
  
  console.log('FirstAccessModal - Renderizando modal');

  console.log('FirstAccessModal - Renderizando JSX, isOpen:', isOpen);
  
  return (
    <div className="first-access-overlay" onClick={(e) => e.stopPropagation()} style={{ display: isOpen ? 'flex' : 'none' }}>
      <div className="first-access-modal" onClick={(e) => e.stopPropagation()}>
        <header className="first-access-header">
          <FaLock className="first-access-icon" />
          <h2>PRIMEIRO ACESSO</h2>
          <p className="first-access-subtitle">Por favor, redefina sua senha para continuar</p>
        </header>

        <main className="first-access-body">
          <form onSubmit={handleSubmit} className="first-access-form">
            <div className={`form-group ${errors.senhaAtual ? 'error' : ''}`}>
              <label htmlFor="senhaAtual">Senha Atual *</label>
              <div className="password-input-container">
                <input
                  type={showSenhaAtual ? 'text' : 'password'}
                  id="senhaAtual"
                  value={senhaAtual}
                  onChange={(e) => handleInputChange('senhaAtual', e.target.value)}
                  placeholder="Digite sua senha atual"
                  required
                  disabled={isLoading}
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowSenhaAtual(!showSenhaAtual)}
                  aria-label={showSenhaAtual ? 'Ocultar senha' : 'Mostrar senha'}
                >
                  {showSenhaAtual ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
              {errors.senhaAtual && (
                <span className="error-message" role="alert">
                  {errors.senhaAtual}
                </span>
              )}
            </div>

            <div className={`form-group ${errors.novaSenha ? 'error' : ''}`}>
              <label htmlFor="novaSenha">Nova Senha *</label>
              <div className="password-input-container">
                <input
                  type={showNovaSenha ? 'text' : 'password'}
                  id="novaSenha"
                  value={novaSenha}
                  onChange={(e) => handleInputChange('novaSenha', e.target.value)}
                  placeholder="Mínimo 6 caracteres"
                  required
                  disabled={isLoading}
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowNovaSenha(!showNovaSenha)}
                  aria-label={showNovaSenha ? 'Ocultar senha' : 'Mostrar senha'}
                >
                  {showNovaSenha ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
              {errors.novaSenha && (
                <span className="error-message" role="alert">
                  {errors.novaSenha}
                </span>
              )}
            </div>

            <div className={`form-group ${errors.confirmarSenha ? 'error' : ''}`}>
              <label htmlFor="confirmarSenha">Confirmar Nova Senha *</label>
              <div className="password-input-container">
                <input
                  type={showConfirmarSenha ? 'text' : 'password'}
                  id="confirmarSenha"
                  value={confirmarSenha}
                  onChange={(e) => handleInputChange('confirmarSenha', e.target.value)}
                  placeholder="Repita a nova senha"
                  required
                  disabled={isLoading}
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowConfirmarSenha(!showConfirmarSenha)}
                  aria-label={showConfirmarSenha ? 'Ocultar senha' : 'Mostrar senha'}
                >
                  {showConfirmarSenha ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
              {errors.confirmarSenha && (
                <span className="error-message" role="alert">
                  {errors.confirmarSenha}
                </span>
              )}
            </div>

            <button
              type="submit"
              className="first-access-submit-button"
              disabled={isLoading || Object.keys(errors).length > 0}
            >
              {isLoading ? (
                <span className="loading-indicator">
                  <span className="loading-spinner"></span>
                  Alterando...
                </span>
              ) : (
                'Alterar Senha'
              )}
            </button>
          </form>
        </main>
      </div>

      <ConfirmModal
        isOpen={isConfirmModalOpen}
        title="CONFIRMAR ALTERAÇÃO DE SENHA"
        message="Tem certeza que é a senha escolhida? Você usará ela por agora."
        confirmText="Confirmar"
        cancelText="Cancelar"
        onConfirm={handleConfirmChangePassword}
        onCancel={() => setIsConfirmModalOpen(false)}
        isLoading={isLoading}
      />

      <Toast
        isVisible={toast.isVisible}
        message={toast.message}
        type={toast.type}
        onClose={hideToast}
      />
    </div>
  );
}

export default FirstAccessModal;

