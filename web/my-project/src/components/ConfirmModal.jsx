// src/components/ConfirmModal.jsx
import React from 'react';
import '../styles/modal.css';

function ConfirmModal({ isOpen, title, message, onConfirm, onCancel, confirmText = 'Confirmar', cancelText = 'Cancelar', isDangerous = false, isLoading = false }) {
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
          <button className="modal-button modal-button-cancel" onClick={onCancel} disabled={isLoading}>
            {cancelText}
          </button>
          <button className={`modal-button ${isDangerous ? 'modal-button-danger' : 'modal-button-confirm'}`} onClick={onConfirm} disabled={isLoading}>
            {isLoading ? (
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span className="loading-spinner" style={{ width: '14px', height: '14px', border: '2px solid rgba(255, 255, 255, 0.3)', borderTop: '2px solid white', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></span>
                {confirmText === 'Salvar' ? 'Salvando...' : confirmText === 'Excluir' ? 'Excluindo...' : 'Processando...'}
              </span>
            ) : (
              confirmText
            )}
          </button>
        </footer>
      </div>
    </div>
  );
}

export default ConfirmModal;
