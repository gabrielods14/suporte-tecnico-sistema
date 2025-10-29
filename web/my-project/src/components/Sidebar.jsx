// src/components/Sidebar.jsx
import React from 'react';
// Importando os ícones
import { 
  FaHome, 
  FaQuestionCircle, 
  FaEnvelopeOpenText, 
  FaClipboardList, 
  FaPlus, 
  FaCheckCircle, 
  FaChartBar,
  FaPhone
} from 'react-icons/fa';

function Sidebar({ currentPage, onNavigate }) {
  const handleMenuClick = (itemId) => {
    if (onNavigate) {
      onNavigate(itemId);
    }
  };

  return (
    <aside className="home-sidebar">
      <div className="sidebar-logo">LOGO</div>
      <nav className="sidebar-nav">
        <ul>
          <li>
            <a href="#" onClick={(e) => { e.preventDefault(); handleMenuClick('home'); }}>
              <FaHome className="nav-icon" /> HOME
            </a>
          </li>
          <li>
            <a href="#" className={currentPage === 'pending-tickets' ? 'active' : ''} onClick={(e) => { e.preventDefault(); handleMenuClick('pending-tickets'); }}>
              <FaClipboardList className="nav-icon" /> CHAMADO
            </a>
          </li>
          <li>
            <a href="#" className={currentPage === 'reports' ? 'active' : ''} onClick={(e) => { e.preventDefault(); handleMenuClick('reports'); }}>
              <FaChartBar className="nav-icon" /> RELATÓRIOS
            </a>
          </li>
          <li>
            <a href="#" className={currentPage === 'faq' ? 'active' : ''} onClick={(e) => { e.preventDefault(); handleMenuClick('faq'); }}>
              <FaQuestionCircle className="nav-icon" /> FQA
            </a>
          </li>
          <li>
            <a href="#" className={currentPage === 'contact' ? 'active' : ''} onClick={(e) => { e.preventDefault(); handleMenuClick('contact'); }}>
              <FaPhone className="nav-icon" /> CONTATO
            </a>
          </li>
        </ul>
      </nav>
    </aside>
  );
}

export default Sidebar;