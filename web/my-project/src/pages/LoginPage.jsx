// src/pages/LoginPage.jsx
import React, { useState } from 'react';
import '../styles/login.css';
import { FaUser, FaLock, FaEye, FaEyeSlash } from 'react-icons/fa';
import ForgotPasswordModal from '../components/ForgotPasswordModal';
import Toast from '../components/Toast';

function LoginPage({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [toast, setToast] = useState({ isVisible: false, message: '', type: 'error' });
  const [showAdminCredentials, setShowAdminCredentials] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const showToast = (message, type = 'error') => {
    setToast({ isVisible: true, message, type });
  };

  const hideToast = () => {
    setToast({ isVisible: false, message: '', type: 'error' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: username,
          senha: password
        }),
      });

      let data;
      try {
        data = await response.json();
      } catch (jsonError) {
        // Se não conseguir fazer parse do JSON, usa mensagem padrão
        data = { message: 'Erro interno do servidor.' };
      }

      if (response.ok) {
        // Salva o token no localStorage se a API retornar um
        if (data.token) {
          localStorage.setItem('authToken', data.token);
        }
        // Passa os dados do usuário para o App
        onLoginSuccess(data.user || { nome: 'Usuário', email: username });
      } else {
        // Trata diferentes tipos de erro
        let errorMessage = 'Usuário ou senha incorretos.';
        
        if (data.message) {
          // Se a API retornou uma mensagem específica, usa ela
          errorMessage = data.message;
        } else if (response.status === 404) {
          errorMessage = 'Usuário ou senha incorretos.';
        } else if (response.status === 401) {
          errorMessage = 'Usuário ou senha incorretos.';
        } else if (response.status === 400) {
          errorMessage = 'Dados inválidos. Verifique email e senha.';
        } else if (response.status >= 500) {
          errorMessage = 'Erro interno do servidor. Tente novamente mais tarde.';
        }
        
        showToast(errorMessage, 'error');
      }
    } catch (error) {
      console.error('Erro no login:', error);
      showToast('Erro de conexão. Verifique se o servidor está rodando.', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    // React.Fragment é usado para agrupar múltiplos elementos sem adicionar um nó extra ao DOM
    <React.Fragment>
      <main className="login-page">
        <section className="login-hero">
          <span>HelpWave - Simplificando o seu suporte.</span>
        </section>

        <section className="login-container">
          <form className="login-form" onSubmit={handleSubmit}>
            <h1>Login</h1>
            <div className="form-group">
              <FaUser className="input-icon" />
              <input
                type="text"
                id="username"
                placeholder="USUÁRIO"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <FaLock className="input-icon" />
              <input
                className="password-input"
                type={showPassword ? 'text' : 'password'}
                id="password"
                placeholder="SENHA"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={showPassword ? 'Ocultar senha' : 'Mostrar senha'}
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>
            <div className="form-options">
              <label htmlFor="remember" className="remember-me">
                <input type="checkbox" id="remember" /> Lembrar
              </label>
              <button
                type="button" // Impede que o botão envie o formulário
                onClick={() => setIsModalOpen(true)}
                style={{ background: 'none', border: 'none', color: '#333333', cursor: 'pointer', padding: 0, textDecoration: 'underline', fontWeight: '500' }}
              >
                Esqueci a senha
              </button>
            </div>
            <button type="submit" className="login-button" disabled={isLoading}>
              {isLoading ? 'Entrando...' : 'Entrar'}
            </button>
            
            <div style={{ marginTop: '20px', textAlign: 'center' }}>
              <button 
                type="button"
                onClick={() => setShowAdminCredentials(!showAdminCredentials)}
                style={{
                  background: 'none',
                  border: 'none',
                  color: '#FFFFFF',
                  cursor: 'pointer',
                  textDecoration: 'underline',
                  fontSize: '0.9rem',
                  fontWeight: '500',
                  textShadow: '0 1px 2px rgba(0, 0, 0, 0.3)'
                }}
              >
                {showAdminCredentials ? 'Ocultar' : 'Mostrar'} credenciais de teste
              </button>
              
              {showAdminCredentials && (
                <div className="credentials-info">
                  <p><strong>Usuário:</strong> admin@helpwave.com</p>
                  <p><strong>Senha:</strong> admin123</p>
                  <p>
                    Use estas credenciais para fazer o primeiro login
                  </p>
                </div>
              )}
            </div>
          </form>
        </section>
      </main>

      <ForgotPasswordModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />

      <Toast
        isVisible={toast.isVisible}
        message={toast.message}
        type={toast.type}
        onClose={hideToast}
      />
    </React.Fragment>
  );
}

export default LoginPage;