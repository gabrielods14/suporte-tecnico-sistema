// src/components/Footer.jsx
import React from 'react';
import '../styles/footer.css';

function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="app-footer">
      <div className="footer-content">
        <p className="footer-tagline">HelpWave — Simplificando o seu suporte.</p>
        <p className="footer-copyright">© {currentYear} HelpWave. Todos os direitos reservados.</p>
      </div>
    </footer>
  );
}

export default Footer;





