// src/pages/LoginPage.jsx
import React, { useState } from 'react';
import '../styles/login.css';
import { FaUser, FaLock } from 'react-icons/fa';
import ForgotPasswordModal from '../components/ForgotPasswordModal';

function LoginPage({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username === 'admin' && password === 'admin') {
      onLoginSuccess();
    } else {
      alert('Usuário ou senha inválidos.');
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
                type="password"
                id="password"
                placeholder="SENHA"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="form-options">
              <label htmlFor="remember" className="remember-me">
                <input type="checkbox" id="remember" /> Lembrar
              </label>
              <button
                type="button" // Impede que o botão envie o formulário
                onClick={() => setIsModalOpen(true)}
                style={{ background: 'none', border: 'none', color: 'var(--text-light)', cursor: 'pointer', padding: 0, textDecoration: 'underline' }}
              >
                Esqueci a senha
              </button>
            </div>
            <button type="submit" className="login-button">
              Entrar
            </button>
          </form>
        </section>
      </main>

      <ForgotPasswordModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </React.Fragment>
  );
}

export default LoginPage;