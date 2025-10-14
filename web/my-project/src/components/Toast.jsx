// src/components/Toast.jsx
import React, { useState, useEffect } from 'react';
import '../styles/toast.css';

const Toast = ({ message, type = 'error', isVisible, onClose }) => {
  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(() => {
        onClose();
      }, 4000); // Auto-close após 4 segundos

      return () => clearTimeout(timer);
    }
  }, [isVisible, onClose]);

  if (!isVisible) return null;

  return (
    <div className={`toast toast-${type}`}>
      <div className="toast-content">
        <span className="toast-message">{message}</span>
        <button className="toast-close" onClick={onClose}>
          ×
        </button>
      </div>
    </div>
  );
};

export default Toast;
