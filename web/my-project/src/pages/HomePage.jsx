// src/pages/HomePage.jsx
import React from 'react';
import '../styles/home.css';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
// Importando os ícones para os cards
import { FaEdit, FaClipboardList, FaCheckCircle, FaChartBar, FaUserPlus } from 'react-icons/fa';
//import { MdOutlineSupportAgent } from "react-icons/md"; // Exemplo de outro pacote de ícones

function HomePage({ onLogout }) {
  return (
    <div className="home-page-layout">
      <Header onLogout={onLogout} /> {/* Adicionado ao grid area 'header' */}
      <Sidebar /> {/* Adicionado ao grid area 'sidebar' */}

      <main className="home-main-content">
        <h2 className="main-welcome">BEM VINDO (A)</h2>

        <section className="dashboard-cards">
          <article className="card">
            {/* Ícone substituído */}
            <FaEdit className="card-icon" />
            <span>NOVO CHAMADO</span>
          </article>
          <article className="card">
            {/* Ícone substituído */}
            <FaClipboardList className="card-icon" />
            <span>CHAMADOS EM ANDAMENTO</span>
          </article>
          <article className="card">
            {/* Ícone substituído */}
            <FaCheckCircle className="card-icon" />
            <span>CHAMADOS CONCLUÍDOS</span>
          </article>
          <article className="card">
            {/* Ícone substituído */}
            <FaChartBar className="card-icon" />
            <span>RELATÓRIOS</span>
          </article>
          <article className="card">
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