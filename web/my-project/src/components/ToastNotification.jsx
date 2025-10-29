/**
 * Componente de Toast Notification melhorado
 */
import React, { useState, useEffect } from 'react';
import { FaCheckCircle, FaExclamationTriangle, FaInfoCircle, FaTimes, FaTimesCircle } from 'react-icons/fa';

const ToastNotification = ({ 
  isVisible, 
  message, 
  type = 'info', 
  duration = 5000, 
  onClose,
  position = 'top-right'
}) => {
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    if (isVisible) {
      setIsAnimating(true);
      
      const timer = setTimeout(() => {
        handleClose();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [isVisible, duration]);

  const handleClose = () => {
    setIsAnimating(false);
    setTimeout(() => {
      if (onClose) onClose();
    }, 300); // Aguarda a animação de saída
  };

  const getToastConfig = () => {
    switch (type) {
      case 'success':
        return {
          icon: FaCheckCircle,
          bgColor: 'bg-green-500',
          textColor: 'text-white',
          iconColor: 'text-green-100'
        };
      case 'error':
        return {
          icon: FaTimesCircle,
          bgColor: 'bg-red-500',
          textColor: 'text-white',
          iconColor: 'text-red-100'
        };
      case 'warning':
        return {
          icon: FaExclamationTriangle,
          bgColor: 'bg-yellow-500',
          textColor: 'text-white',
          iconColor: 'text-yellow-100'
        };
      case 'info':
      default:
        return {
          icon: FaInfoCircle,
          bgColor: 'bg-blue-500',
          textColor: 'text-white',
          iconColor: 'text-blue-100'
        };
    }
  };

  const getPositionClasses = () => {
    switch (position) {
      case 'top-left':
        return 'top-4 left-4';
      case 'top-center':
        return 'top-4 left-1/2 transform -translate-x-1/2';
      case 'top-right':
        return 'top-4 right-4';
      case 'bottom-left':
        return 'bottom-4 left-4';
      case 'bottom-center':
        return 'bottom-4 left-1/2 transform -translate-x-1/2';
      case 'bottom-right':
        return 'bottom-4 right-4';
      default:
        return 'top-4 right-4';
    }
  };

  if (!isVisible) return null;

  const config = getToastConfig();
  const IconComponent = config.icon;

  return (
    <div 
      className={`
        fixed ${getPositionClasses()} z-50
        ${isAnimating ? 'animate-slide-in' : 'animate-slide-out'}
        ${config.bgColor} ${config.textColor}
        rounded-lg shadow-lg p-4 min-w-80 max-w-md
        flex items-center gap-3
        transition-all duration-300 ease-in-out
      `}
    >
      <IconComponent className={`${config.iconColor} text-xl flex-shrink-0`} />
      
      <div className="flex-1">
        <p className="font-medium text-sm leading-relaxed">
          {message}
        </p>
      </div>
      
      <button
        onClick={handleClose}
        className={`
          ${config.iconColor} hover:text-white
          transition-colors duration-200
          flex-shrink-0 p-1 rounded-full
          hover:bg-black hover:bg-opacity-20
        `}
        aria-label="Fechar notificação"
      >
        <FaTimes className="text-sm" />
      </button>
    </div>
  );
};

export default ToastNotification;

