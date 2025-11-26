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
  FaTachometerAlt,
  FaPhone,
  FaList
} from 'react-icons/fa';

function Sidebar({ currentPage, onNavigate, userInfo }) {
  const handleMenuClick = (itemId) => {
    if (onNavigate) {
      onNavigate(itemId);
    }
  };

  const isColaborador = userInfo?.permissao === 1;
  const isSuporteTecnico = userInfo?.permissao === 2;
  const isAdmin = userInfo?.permissao === 3;

  return (
    <aside className="home-sidebar">
      <div className="sidebar-logo">
        {/* Renderiza logo se existir em /public/logo.png, senão exibe texto */}
        <img
          src="\logo.png"
          alt="HelpWave"
          className="sidebar-logo-img"
          onError={(e) => { e.target.style.display = 'none'; }}
          onLoad={(e) => { const txt = e.target.nextElementSibling; if (txt) txt.style.display = 'none'; }}
        />
        <span className="sidebar-logo-text">HELPWAVE</span>
      </div>
      <nav className="sidebar-nav">
        <ul>
          <li>
            <a href="#" onClick={(e) => { e.preventDefault(); handleMenuClick('home'); }}>
              <FaHome className="nav-icon" /> HOME
            </a>
          </li>
          
          {/* Colaborador: só vê "Meus Chamados" */}
          {isColaborador && (
            <li>
              <a href="#" className={currentPage === 'my-tickets' ? 'active' : ''} onClick={(e) => { e.preventDefault(); handleMenuClick('my-tickets'); }}>
                <FaList className="nav-icon" /> MEUS CHAMADOS
              </a>
            </li>
          )}
          
          {/* Técnico/Admin: vê Chamado, Concluídos, Relatórios */}
          {(isSuporteTecnico || isAdmin) && (
            <>
              <li>
                <a href="#" className={currentPage === 'pending-tickets' ? 'active' : ''} onClick={(e) => { e.preventDefault(); handleMenuClick('pending-tickets'); }}>
                  <FaClipboardList className="nav-icon" /> CHAMADOS
                </a>
              </li>
              <li>
                <a href="#" className={currentPage === 'completed-tickets' ? 'active' : ''} onClick={(e) => { e.preventDefault(); handleMenuClick('completed-tickets'); }}>
                  <FaCheckCircle className="nav-icon" /> CONCLUÍDOS
                </a>
              </li>
              {/* Dashboard - apenas admin */}
              {isAdmin && (
                <li>
                  <a href="#" className={currentPage === 'dashboard' ? 'active' : ''} onClick={(e) => { e.preventDefault(); handleMenuClick('dashboard'); }}>
                    <FaTachometerAlt className="nav-icon" /> DASHBOARD
                  </a>
                </li>
              )}
              <li>
                <a href="#" className={currentPage === 'reports' ? 'active' : ''} onClick={(e) => { e.preventDefault(); handleMenuClick('reports'); }}>
                  <FaChartBar className="nav-icon" /> RELATÓRIOS
                </a>
              </li>
            </>
          )}
          
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