/**
 * Hook personalizado para gerenciar autenticação
 */
import { useState, useEffect, useCallback } from 'react';
import { authService } from '../utils/api';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  /**
   * Verifica se há um usuário autenticado na inicialização
   */
  useEffect(() => {
    const checkAuth = async () => {
      try {
        setIsLoading(true);
        
        if (authService.isAuthenticated()) {
          const userInfo = authService.getUserInfo();
          if (userInfo) {
            setUser(userInfo);
            setIsAuthenticated(true);
          } else {
            // Token inválido
            await authService.logout();
          }
        }
      } catch (error) {
        console.error('Erro ao verificar autenticação:', error);
        await authService.logout();
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  /**
   * Faz login do usuário
   */
  const login = useCallback(async (email, password) => {
    try {
      setIsLoading(true);
      
      const response = await authService.login(email, password);
      
      if (response.token) {
        localStorage.setItem('authToken', response.token);
      }
      
      setUser(response.user || { nome: 'Usuário', email });
      setIsAuthenticated(true);
      
      return { success: true, user: response.user };
    } catch (error) {
      console.error('Erro no login:', error);
      return { 
        success: false, 
        error: error.message || 'Erro ao fazer login' 
      };
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Faz logout do usuário
   */
  const logout = useCallback(async () => {
    try {
      await authService.logout();
      setUser(null);
      setIsAuthenticated(false);
      return { success: true };
    } catch (error) {
      console.error('Erro no logout:', error);
      return { 
        success: false, 
        error: error.message || 'Erro ao fazer logout' 
      };
    }
  }, []);

  /**
   * Atualiza informações do usuário
   */
  const updateUser = useCallback((userData) => {
    setUser(prevUser => ({
      ...prevUser,
      ...userData
    }));
  }, []);

  /**
   * Verifica se o usuário tem uma permissão específica
   */
  const hasPermission = useCallback((permission) => {
    if (!user) return false;
    
    // Implementar lógica de permissões baseada no nível do usuário
    const userLevel = user.permissao || 1;
    
    switch (permission) {
      case 'admin':
        return userLevel === 1;
      case 'manager':
        return userLevel <= 2;
      case 'user':
        return userLevel <= 3;
      default:
        return false;
    }
  }, [user]);

  return {
    user,
    isLoading,
    isAuthenticated,
    login,
    logout,
    updateUser,
    hasPermission
  };
};

