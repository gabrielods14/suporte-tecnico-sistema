// src/components/Header.jsx
import React, { useState } from 'react';
// Importando os ícones
import { FaUserCircle, FaCog, FaChevronDown } from 'react-icons/fa';
import DropdownMenu from './DropdownMenu';

function Header({ onLogout }) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  return (
    <header className="home-header">
      <div className="header-user-info">
        <FaUserCircle className="user-icon" />
        <span>BEM-VINDO(A) XXXXXX</span>
        <div className="dropdown-container">
          <FaCog 
            className="settings-icon" 
            onClick={() => setIsDropdownOpen(!isDropdownOpen)} // Alterna o estado
          />
          {isDropdownOpen && <DropdownMenu onLogout={onLogout} />}
        </div>

        <FaChevronDown className="dropdown-arrow" /> {/* Seta para dropdown */}
      </div>
    </header>
  );
}

export default Header;