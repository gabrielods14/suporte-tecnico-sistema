// src/components/Sidebar.jsx
import React from 'react';
// Importando os ícones
import { FaHome, FaQuestionCircle, FaEnvelopeOpenText } from 'react-icons/fa';

// Para ícones, você pode usar uma biblioteca como react-icons
// Ex: import { FaHome, FaQuestionCircle, FaEnvelopeOpenText, FaBars } from 'react-icons/fa';
// Para este exemplo, vou usar texto ou emojis para simular os ícones.

function Sidebar() {
  return (
    <aside className="home-sidebar">
      <div className="sidebar-logo">LOGO</div>
      <nav className="sidebar-nav">
        <ul>
          <li>
            {/* Ícone substituído */}
            <a href="#" className="active">
              <FaHome className="nav-icon" /> HOME
            </a>
          </li>
          <li>
            {/* Ícone substituído */}
            <a href="#">
              <FaQuestionCircle className="nav-icon" /> FQA
            </a>
          </li>
          <li>
            {/* Ícone substituído */}
            <a href="#">
              <FaEnvelopeOpenText className="nav-icon" /> CONTATO
            </a>
          </li>
        </ul>
      </nav>
    </aside>
  );
}

export default Sidebar;