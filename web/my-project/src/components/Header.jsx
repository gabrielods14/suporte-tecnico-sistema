// src/components/Header.jsx
import React, { useState } from 'react';
// Importando os ícones
import { FaUserCircle, FaCog, FaChevronDown, FaWaveSquare } from 'react-icons/fa';
import DropdownMenu from './DropdownMenu';

function Header({ onLogout, userName = 'Administrador', onNavigateToProfile }) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  // Normaliza o userName para garantir que sempre tenha um valor válido
  const displayName = (() => {
    if (userName && typeof userName === 'string' && userName.trim()) {
      // Se for um nome completo, pega apenas o primeiro nome
      const parts = userName.trim().split(/\s+/);
      return parts[0];
    }
    return 'Usuário';
  })();

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
        <span>BEM-VINDO(A) {displayName.toUpperCase()}</span>
        <div className="dropdown-container">
          <FaCog 
            className="settings-icon" 
            onClick={() => setIsDropdownOpen(!isDropdownOpen)} // Alterna o estado
          />
          {isDropdownOpen && (
            <DropdownMenu 
              onLogout={onLogout} 
              onNavigateToProfile={handleProfileClick}
            />
          )}
        </div>

        <FaChevronDown className="dropdown-arrow" /> {/* Seta para dropdown */}
      </div>
    </header>
  );
}

export default Header;