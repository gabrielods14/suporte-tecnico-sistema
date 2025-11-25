// src/pages/HomePage.jsx
import React from 'react';
import '../styles/home.css';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
// Importando os ícones para os cards
import { FaEdit, FaClipboardList, FaCheckCircle, FaChartBar, FaUserPlus, FaList } from 'react-icons/fa';
//import { MdOutlineSupportAgent } from "react-icons/md"; // Exemplo de outro pacote de ícones

function HomePage({ onLogout, onNavigateToRegister, onNavigateToNewTicket, onNavigateToPage, currentPage, userInfo, onNavigateToProfile }) {
  const permissao = userInfo?.permissao; // 3=Admin, 2=SuporteTecnico, 1=Colaborador
  
  // Debug: verificar dados do usuário
  console.log('HomePage - userInfo:', userInfo);
  console.log('HomePage - permissao:', permissao);
  
  // Usa o nome completo diretamente do userInfo (já normalizado no App.jsx)
  // Formata o nome para exibição (primeira letra maiúscula)
  const formatName = (name) => {
    if (!name || name.trim() === '') return 'Usuário';
    // Se o nome parece ser um email, extrai a parte antes do @
    if (name.includes('@')) {
      const emailPart = name.split('@')[0];
      return emailPart.split(/[._-]/).map(part => 
        part.charAt(0).toUpperCase() + part.slice(1).toLowerCase()
      ).join(' ');
    }
    // Formata o nome normalmente
    return name.split(' ').map(part => 
      part.charAt(0).toUpperCase() + part.slice(1).toLowerCase()
    ).join(' ');
  };
  
  const userName = formatName(userInfo?.nome || 'Usuário');
  const handleCardClick = (cardType) => {
    switch (cardType) {
      case 'new-ticket':
        onNavigateToNewTicket();
        break;
      case 'my-tickets':
        onNavigateToPage('my-tickets');
        break;
      case 'pending-tickets':
        onNavigateToPage('pending-tickets');
        break;
      case 'completed-tickets':
        onNavigateToPage('completed-tickets');
        break;
      case 'reports':
        onNavigateToPage('reports');
        break;
      case 'register':
        onNavigateToRegister();
        break;
      default:
        break;
    }
  };

  return (
    <div className="home-page-layout">
      <Header 
        onLogout={onLogout} 
        userName={userName}
        userInfo={userInfo}
        onNavigateToProfile={onNavigateToProfile}
      /> {/* Adicionado ao grid area 'header' */}
      <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} userInfo={userInfo} /> {/* Adicionado ao grid area 'sidebar' */}

      <main className="home-main-content">
        <h2 className="main-welcome">BEM-VINDO(A), {userName}</h2>

        <section className="dashboard-cards">
          {/* Card "NOVO CHAMADO" - sempre visível para todos */}
          <article className="card" onClick={() => handleCardClick('new-ticket')}>
            <FaEdit className="card-icon" />
            <span>NOVO CHAMADO</span>
          </article>

          {/* Card "MEUS CHAMADOS" - visível para colaboradores (1) */}
          {permissao === 1 && (
            <article className="card" onClick={() => handleCardClick('my-tickets')}>
              <FaList className="card-icon" />
              <span>MEUS CHAMADOS</span>
            </article>
          )}

          {/* Cards para Suporte (2) e Admin (3) */}
          {(permissao === 2 || permissao === 3) && (
            <>
              <article className="card" onClick={() => handleCardClick('pending-tickets')}>
                <FaClipboardList className="card-icon" />
                <span>CHAMADOS EM ANDAMENTO</span>
              </article>

              <article className="card" onClick={() => handleCardClick('completed-tickets')}>
                <FaCheckCircle className="card-icon" />
                <span>CHAMADOS CONCLUÍDOS</span>
              </article>

              <article className="card" onClick={() => handleCardClick('reports')}>
                <FaChartBar className="card-icon" />
                <span>RELATÓRIOS</span>
              </article>
            </>
          )}

          {/* Card para Admin (3) - Cadastro de Funcionário */}
          {permissao === 3 && (
            <article className="card" onClick={() => handleCardClick('register')}>
              <FaUserPlus className="card-icon" />
              <span>CADASTRO DE FUNCIONÁRIO</span>
            </article>
          )}
        </section>

        <footer className="home-footer">
          <p>HelpWave — Simplificando o seu suporte.</p>
          <p>© 2025 HelpWave</p>
        </footer>
      </main>
    </div>
  );
}

export default HomePage;