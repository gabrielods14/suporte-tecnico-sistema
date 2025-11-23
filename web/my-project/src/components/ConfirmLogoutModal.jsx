// src/components/ConfirmLogoutModal.jsx
import React from 'react';
import '../styles/confirm-logout-modal.css';

function ConfirmLogoutModal({ isOpen, onConfirm, onCancel }) {
  if (!isOpen) return null;
  return (
    <div className="confirm-logout-modal-overlay">
      <div className="confirm-logout-modal">
        <h3>Confirmar Logout</h3>
        <p>Tem certeza que deseja sair?</p>
        <div className="modal-actions">
          <button className="btn-confirm" onClick={onConfirm}>Sim</button>
          <button className="btn-cancel" onClick={onCancel}>Cancelar</button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmLogoutModal;
