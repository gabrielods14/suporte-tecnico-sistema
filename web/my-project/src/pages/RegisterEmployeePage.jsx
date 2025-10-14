// src/pages/RegisterEmployeePage.jsx

import React, { useState } from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import '../styles/register.css'; // O arquivo de CSS para essa página

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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
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
        alert('Funcionário cadastrado com sucesso!');
        // Limpa o formulário
        setFormData({
          nome: '',
          email: '',
          cargo: '',
          senha: '',
          telefone: '',
          permissao: 1
        });
      } else {
        alert(data.message || 'Erro ao cadastrar funcionário.');
      }
    } catch (error) {
      console.error('Erro no cadastro:', error);
      alert('Erro de conexão. Tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="register-layout">
      <Header onLogout={onLogout} userName={userInfo?.nome} />
      <Sidebar />
      <main className="register-main-content">
        <div className="register-header">
          <button 
            className="back-button" 
            onClick={onNavigateToHome}
            style={{
              background: 'var(--primary-color)',
              color: 'white',
              border: 'none',
              padding: '10px 20px',
              borderRadius: '5px',
              cursor: 'pointer',
              marginBottom: '20px'
            }}
          >
            ← Voltar
          </button>
          <h2>CADASTRO DE FUNCIONÁRIO</h2>
        </div>
        <form className="register-form" onSubmit={handleSubmit}>
          {/* Campos do formulário */}
          <div className="form-group">
            <label htmlFor="nome">Nome Completo</label>
            <input 
              type="text" 
              id="nome" 
              name="nome" 
              value={formData.nome}
              onChange={handleInputChange}
              required 
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">E-mail</label>
            <input 
              type="email" 
              id="email" 
              name="email" 
              value={formData.email}
              onChange={handleInputChange}
              required 
            />
          </div>
          <div className="form-group">
            <label htmlFor="cargo">Cargo</label>
            <input 
              type="text" 
              id="cargo" 
              name="cargo" 
              value={formData.cargo}
              onChange={handleInputChange}
              required 
            />
          </div>
          <div className="form-group">
            <label htmlFor="telefone">Telefone</label>
            <input 
              type="tel" 
              id="telefone" 
              name="telefone" 
              value={formData.telefone}
              onChange={handleInputChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="senha">Senha</label>
            <input 
              type="password" 
              id="senha" 
              name="senha" 
              value={formData.senha}
              onChange={handleInputChange}
              required 
            />
          </div>

          <button type="submit" className="submit-button" disabled={isLoading}>
            {isLoading ? 'CADASTRANDO...' : 'CADASTRAR'}
          </button>
        </form>
      </main>
    </div>
  );
};

export default RegisterEmployeePage;