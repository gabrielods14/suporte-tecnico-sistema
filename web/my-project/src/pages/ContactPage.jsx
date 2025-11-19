// src/pages/ContactPage.jsx
import React from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import '../styles/contact.css';
import { 
  FaPhone, 
  FaEnvelope, 
  FaHeadset
} from 'react-icons/fa';

function ContactPage({ onLogout, onNavigateToHome, onNavigateToPage, currentPage, userInfo, onNavigateToProfile }) {
  const userName = userInfo?.nome || 'Usuário';

  // Informações de contato do administrador
  const adminContact = {
    email: 'admin@helpwave.com',
    phone: '(11) 98765-4321'
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
      <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} />
      
      <main className="contact-main-content">
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
              dúvidas ou solicitações.
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
                Envie um e-mail para o administrador
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
                Entre em contato por telefone
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

          {/* Informação Adicional */}
          <div className="contact-info-box">
            <p>
              <strong>Observação:</strong> Para questões relacionadas a chamados técnicos, 
              utilize a funcionalidade de criar novo chamado no sistema.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default ContactPage;

