// src/components/ConfirmModal.jsx
import React from 'react';
import '../styles/modal.css';

function ConfirmModal({ isOpen, title, message, onConfirm, onCancel, confirmText = 'Confirmar', cancelText = 'Cancelar', isDangerous = false }) {
  // Se não estiver aberto, não renderiza nada.
  if (!isOpen) {
    return null;
  }

  return (
    // O overlay que cobre a tela
    <div className="modal-overlay" onClick={onCancel}>
      {/* Impede que o clique dentro do modal feche o mesmo */}
      <div className="modal-content confirm-modal" onClick={(e) => e.stopPropagation()}>
        <header className="modal-header">
          <h2>{title}</h2>
        </header>
        <main className="modal-body">
          <p>{message}</p>
        </main>
        <footer className="modal-footer">
          <button className="modal-button modal-button-cancel" onClick={onCancel}>
            {cancelText}
          </button>
          <button className={`modal-button ${isDangerous ? 'modal-button-danger' : 'modal-button-confirm'}`} onClick={onConfirm}>
            {confirmText}
          </button>
        </footer>
      </div>
    </div>
  );
}

export default ConfirmModal;
