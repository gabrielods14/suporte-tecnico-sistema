// src/pages/ContactPage.jsx
import React from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';
import '../styles/contact.css';
import { 
  FaPhone, 
  FaEnvelope, 
  FaHeadset,
  FaClock,
  FaMapMarkerAlt
} from 'react-icons/fa';

function ContactPage({ onLogout, onNavigateToHome, onNavigateToPage, currentPage, userInfo, onNavigateToProfile }) {
  const userName = userInfo?.nome || 'Usuário';

  // Informações de contato do administrador
  const adminContact = {
    email: 'admin2@helpwave.com',
    phone: '(12) 99999-8888',
    horario: 'Segunda a Sexta: 8h às 18h',
    endereco: 'Sistema de Suporte Técnico HelpWave'
  };

  const handleEmailClick = () => {
    window.location.href = `mailto:${adminContact.email}?subject=Contato HelpWave`;
  };

  const handlePhoneClick = () => {
    window.location.href = `tel:${adminContact.phone}`;
  };

  return (
    <div className="contact-layout">
      <Header onLogout={onLogout} userName={userName} userInfo={userInfo} onNavigateToProfile={onNavigateToProfile} />
      <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} userInfo={userInfo} />
      
      <main className="contact-main-content">
        <button 
          className="back-button" 
          onClick={() => onNavigateToPage('home')}
          aria-label="Voltar para página inicial"
        >
          ← Voltar
        </button>
        
        <div className="contact-header">
          <h1>
            <FaHeadset className="contact-title-icon" />
            Entre em Contato
          </h1>
          <p className="contact-subtitle">Entre em contato com o administrador do sistema</p>
        </div>

        <div className="contact-content">
          <div className="contact-intro">
            <p>
              Precisa entrar em contato com o administrador do sistema? Utilize os canais abaixo para suporte, 
              dúvidas ou solicitações. Estamos prontos para ajudar!
            </p>
          </div>

          <div className="contact-cards">
            {/* Card de Email */}
            <div className="contact-card email-card">
              <div className="contact-card-icon">
                <FaEnvelope />
              </div>
              <h3>E-mail</h3>
              <p className="contact-card-description">
                Envie um e-mail para o administrador do sistema
              </p>
              <a 
                href={`mailto:${adminContact.email}?subject=Contato HelpWave`}
                onClick={handleEmailClick}
                className="contact-link email-link"
              >
                {adminContact.email}
              </a>
              <button 
                className="contact-button email-button"
                onClick={handleEmailClick}
              >
                Enviar E-mail
              </button>
            </div>

            {/* Card de Telefone */}
            <div className="contact-card phone-card">
              <div className="contact-card-icon">
                <FaPhone />
              </div>
              <h3>Telefone</h3>
              <p className="contact-card-description">
                Entre em contato por telefone durante o horário comercial
              </p>
              <a 
                href={`tel:${adminContact.phone}`}
                onClick={handlePhoneClick}
                className="contact-link phone-link"
              >
                {adminContact.phone}
              </a>
              <button 
                className="contact-button phone-button"
                onClick={handlePhoneClick}
              >
                Ligar Agora
              </button>
            </div>
          </div>

          {/* Informações Adicionais */}
          <div className="contact-info-section">
            <div className="info-box">
              <FaClock className="info-icon" />
              <div className="info-content">
                <h4>Horário de Atendimento</h4>
                <p>{adminContact.horario}</p>
                <p className="info-note">Respostas por e-mail em até 24 horas úteis</p>
              </div>
            </div>

            <div className="info-box">
              <FaMapMarkerAlt className="info-icon" />
              <div className="info-content">
                <h4>Localização</h4>
                <p>{adminContact.endereco}</p>
                <p className="info-note">Sistema online disponível 24/7</p>
              </div>
            </div>
          </div>

          {/* Informação Adicional */}
          <div className="contact-info-box">
            <p>
              <strong>Observação:</strong> Para questões relacionadas a chamados técnicos, 
              utilize a funcionalidade de criar novo chamado no sistema. O suporte técnico 
              responderá através do próprio sistema de chamados.
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default ContactPage;

