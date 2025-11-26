// src/components/LoadingScreen.jsx
import React from 'react';
import '../styles/loading-screen.css';

function LoadingScreen({ message = 'Aguarde...' }) {
  return (
    <div className="loading-screen">
      <div className="loading-screen-content">
        <div className="loading-spinner-large"></div>
        <p className="loading-message">{message}</p>
      </div>
    </div>
  );
}

export default LoadingScreen;

