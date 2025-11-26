// src/components/DropdownMenu.jsx
import React from 'react';
import '../styles/dropdown.css';
import { FaSignOutAlt, FaUser } from 'react-icons/fa'; // Ícones para logout e perfil

function DropdownMenu({ onLogout, onNavigateToProfile }) {
  return (
    <div className="dropdown-menu">
      <ul>
        {onNavigateToProfile && (
          <li className="dropdown-item" onClick={onNavigateToProfile}>
            <FaUser className="item-icon" />
            <span>Perfil</span>
          </li>
        )}
        <li className="dropdown-item" onClick={onLogout}>
          <FaSignOutAlt className="item-icon" />
          <span>Logout</span>
        </li>
      </ul>
    </div>
  );
}

export default DropdownMenu;