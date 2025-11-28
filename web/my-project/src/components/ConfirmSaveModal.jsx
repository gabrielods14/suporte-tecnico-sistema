import React from 'react';
import '../styles/modal.css';

function ConfirmSaveModal({ isOpen, title = 'Confirmar alterações', message = 'Deseja realmente salvar as alterações do perfil?', onConfirm, onCancel }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content confirm-modal" role="dialog" aria-modal="true" aria-labelledby="confirm-save-title">
        <div className="modal-header">
          <h3 id="confirm-save-title">{title}</h3>
        </div>
        <div className="modal-body">
          <p>{message}</p>
        </div>
        <div className="modal-footer">
          <button className="modal-button modal-button-cancel" onClick={onCancel}>Cancelar</button>
          <button className="modal-button modal-button-confirm" onClick={onConfirm}>Confirmar</button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmSaveModal;
