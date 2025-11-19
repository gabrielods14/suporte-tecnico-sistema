// src/components/Header.jsx
import React, { useState } from 'react';
// Importando os ícones
import { FaUserCircle, FaCog, FaChevronDown, FaWaveSquare } from 'react-icons/fa';
import DropdownMenu from './DropdownMenu';

function Header({ onLogout, userName, userInfo, onNavigateToProfile }) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

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