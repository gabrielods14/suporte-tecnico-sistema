// src/components/ForgotPasswordModal.jsx
import React from 'react';
import '../styles/modal.css';

function ForgotPasswordModal({ isOpen, onClose }) {
  // Se não estiver aberto, não renderiza nada.
  if (!isOpen) {
    return null;
  }

  return (
    // O overlay que cobre a tela
    <div className="modal-overlay" onClick={onClose}>
      {/* Impede que o clique dentro do modal feche o mesmo */}
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <header className="modal-header">
          <h2>RECUPERAR SENHA</h2>
        </header>
        <main className="modal-body">
          <p>Para recuperar a sua senha envie mensagem para o seu gestor.</p>
        </main>
        <footer className="modal-footer">
          <button className="modal-button" onClick={onClose}>
            OK
          </button>
        </footer>
      </div>
    </div>
  );
}

export default ForgotPasswordModal;