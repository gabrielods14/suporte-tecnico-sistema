// src/pages/HomePage.jsx
import React from 'react';
import '../styles/home.css';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
// Importando os ícones para os cards
import { FaEdit, FaClipboardList, FaCheckCircle, FaChartBar, FaUserPlus } from 'react-icons/fa';
//import { MdOutlineSupportAgent } from "react-icons/md"; // Exemplo de outro pacote de ícones

function HomePage({ onLogout, onNavigateToRegister, onNavigateToNewTicket, onNavigateToPage, currentPage, userInfo }) {
  const handleCardClick = (cardType) => {
    switch (cardType) {
      case 'new-ticket':
        onNavigateToNewTicket();
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
      <Header onLogout={onLogout} userName={userInfo?.nome} /> {/* Adicionado ao grid area 'header' */}
      <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} /> {/* Adicionado ao grid area 'sidebar' */}

      <main className="home-main-content">
        <h2 className="main-welcome">BEM VINDO (A)</h2>

        <section className="dashboard-cards">
          <article className="card" onClick={() => handleCardClick('new-ticket')}>
            {/* Ícone substituído */}
            <FaEdit className="card-icon" />
            <span>NOVO CHAMADO</span>
          </article>
          <article className="card" onClick={() => handleCardClick('pending-tickets')}>
            {/* Ícone substituído */}
            <FaClipboardList className="card-icon" />
            <span>CHAMADOS EM ANDAMENTO</span>
          </article>
          <article className="card" onClick={() => handleCardClick('completed-tickets')}>
            {/* Ícone substituído */}
            <FaCheckCircle className="card-icon" />
            <span>CHAMADOS CONCLUÍDOS</span>
          </article>
          <article className="card" onClick={() => handleCardClick('reports')}>
            {/* Ícone substituído */}
            <FaChartBar className="card-icon" />
            <span>RELATÓRIOS</span>
          </article>
          <article className="card" onClick={() => handleCardClick('register')}>
            {/* Ícone substituído */}
            <FaUserPlus className="card-icon" />
            <span>CADASTRO DE FUNCIONÁRIO</span>
          </article>
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