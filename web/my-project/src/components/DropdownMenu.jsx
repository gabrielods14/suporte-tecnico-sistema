// src/components/DropdownMenu.jsx
import React from 'react';
import '../styles/dropdown.css';
import { FaSignOutAlt } from 'react-icons/fa'; // Ícone para o logout

function DropdownMenu({ onLogout }) {
  return (
    <div className="dropdown-menu">
      <ul>
        <li className="dropdown-item" onClick={onLogout}>
          <FaSignOutAlt className="item-icon" />
          <span>Logout</span>
        </li>
        {/* Você poderia adicionar mais itens aqui no futuro, como "Perfil", "Configurações", etc. */}
      </ul>
    </div>
  );
}

export default DropdownMenu;