// src/components/Header.jsx
import React, { useState } from 'react';
// Importando os ícones
import { FaUserCircle, FaCog, FaChevronDown, FaWaveSquare } from 'react-icons/fa';
import DropdownMenu from './DropdownMenu';
import ConfirmLogoutModal from './ConfirmLogoutModal';

function Header({ onLogout, userName, userInfo, onNavigateToProfile }) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [showLogoutModal, setShowLogoutModal] = useState(false);

  // Usa o nome completo do userInfo diretamente (já normalizado no App.jsx)
  const displayName = userInfo?.nome || userName || 'Usuário';

  const handleUserIconClick = () => {
    if (onNavigateToProfile) {
      onNavigateToProfile();
    }
  };

  const handleProfileClick = () => {
    setIsDropdownOpen(false);
    if (onNavigateToProfile) {
      onNavigateToProfile();
    }
  };

  return (
    <header className="home-header">
      <div className="header-left">
        <span className="header-title">HELPWAVE</span>
      </div>
      <div className="header-user-info">
        <FaUserCircle 
          className="user-icon" 
          onClick={handleUserIconClick}
          style={{ cursor: onNavigateToProfile ? 'pointer' : 'default' }}
        />
        <span>BEM-VINDO(A), {displayName}</span>
        {/* Quadrado agrupando engrenagem e seta */}
        <div className="settings-dropdown-square">
          <FaCog 
            className="settings-icon" 
            style={{ pointerEvents: 'none', opacity: 0.7 }}
          />
          <FaChevronDown 
            className="dropdown-arrow" 
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            style={{ cursor: 'pointer' }}
          />
          {isDropdownOpen && (
            <DropdownMenu 
              onLogout={() => { setIsDropdownOpen(false); setShowLogoutModal(true); }}
              onNavigateToProfile={handleProfileClick}
            />
          )}
        </div>
      </div>
      {/* Modal de confirmação de logout */}
      <ConfirmLogoutModal 
        isOpen={showLogoutModal}
        onConfirm={() => { setShowLogoutModal(false); if (onLogout) onLogout(); }}
        onCancel={() => setShowLogoutModal(false)}
      />
    </header>
  );
}

export default Header;