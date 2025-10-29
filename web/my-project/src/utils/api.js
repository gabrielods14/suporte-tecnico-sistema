/**
 * Utilitários para integração com a API
 */

const API_BASE_URL = 'http://localhost:5000';

/**
 * Classe para gerenciar requisições à API
 */
class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  /**
   * Obtém o token de autenticação do localStorage
   */
  getAuthToken() {
    return localStorage.getItem('authToken');
  }

  /**
   * Configura headers com autenticação
   */
  getHeaders(includeAuth = true) {
    const headers = { ...this.defaultHeaders };
    
    if (includeAuth) {
      const token = this.getAuthToken();
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
    }
    
    return headers;
  }

  /**
   * Faz uma requisição GET
   */
  async get(endpoint, includeAuth = true) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        method: 'GET',
        headers: this.getHeaders(includeAuth),
      });

      return await this.handleResponse(response);
    } catch (error) {
      console.error('Erro na requisição GET:', error);
      throw this.handleError(error);
    }
  }

  /**
   * Faz uma requisição POST
   */
  async post(endpoint, data, includeAuth = true) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        method: 'POST',
        headers: this.getHeaders(includeAuth),
        body: JSON.stringify(data),
      });

      return await this.handleResponse(response);
    } catch (error) {
      console.error('Erro na requisição POST:', error);
      throw this.handleError(error);
    }
  }

  /**
   * Faz uma requisição PUT
   */
  async put(endpoint, data, includeAuth = true) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        method: 'PUT',
        headers: this.getHeaders(includeAuth),
        body: JSON.stringify(data),
      });

      return await this.handleResponse(response);
    } catch (error) {
      console.error('Erro na requisição PUT:', error);
      throw this.handleError(error);
    }
  }

  /**
   * Faz uma requisição DELETE
   */
  async delete(endpoint, includeAuth = true) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        method: 'DELETE',
        headers: this.getHeaders(includeAuth),
      });

      return await this.handleResponse(response);
    } catch (error) {
      console.error('Erro na requisição DELETE:', error);
      throw this.handleError(error);
    }
  }

  /**
   * Processa a resposta da API
   */
  async handleResponse(response) {
    let data;
    
    try {
      data = await response.json();
    } catch (error) {
      data = { message: 'Erro interno do servidor.' };
    }

    if (!response.ok) {
      const error = new Error(data.message || 'Erro na requisição');
      error.status = response.status;
      error.data = data;
      throw error;
    }

    return data;
  }

  /**
   * Trata erros de rede e outros erros
   */
  handleError(error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      return new Error('Erro de conexão. Verifique se o servidor está rodando.');
    }
    
    if (error.status === 401) {
      // Token inválido ou expirado
      localStorage.removeItem('authToken');
      window.location.href = '/login';
      return new Error('Sessão expirada. Faça login novamente.');
    }
    
    return error;
  }
}

// Instância global do cliente da API
export const apiClient = new ApiClient();

/**
 * Serviços específicos da API
 */
export const authService = {
  /**
   * Faz login do usuário
   */
  async login(email, password) {
    return await apiClient.post('/login', { email, senha: password }, false);
  },

  /**
   * Faz logout do usuário
   */
  async logout() {
    localStorage.removeItem('authToken');
    return { message: 'Logout realizado com sucesso' };
  },

  /**
   * Verifica se o usuário está autenticado
   */
  isAuthenticated() {
    return !!localStorage.getItem('authToken');
  },

  /**
   * Obtém informações do usuário do token
   */
  getUserInfo() {
    const token = localStorage.getItem('authToken');
    if (!token) return null;
    
    try {
      // Decodifica o token JWT (implementação simples)
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload;
    } catch (error) {
      console.error('Erro ao decodificar token:', error);
      return null;
    }
  }
};

export const userService = {
  /**
   * Registra um novo usuário
   */
  async register(userData) {
    return await apiClient.post('/register', userData, false);
  },

  /**
   * Obtém lista de usuários
   */
  async getUsers() {
    return await apiClient.get('/users');
  },

  /**
   * Atualiza dados do usuário
   */
  async updateUser(userId, userData) {
    return await apiClient.put(`/users/${userId}`, userData);
  },

  /**
   * Remove usuário
   */
  async deleteUser(userId) {
    return await apiClient.delete(`/users/${userId}`);
  }
};

export const ticketService = {
  /**
   * Cria um novo ticket
   */
  async createTicket(ticketData) {
    return await apiClient.post('/tickets', ticketData);
  },

  /**
   * Obtém lista de tickets
   */
  async getTickets() {
    return await apiClient.get('/tickets');
  },

  /**
   * Obtém um ticket específico
   */
  async getTicket(ticketId) {
    return await apiClient.get(`/tickets/${ticketId}`);
  },

  /**
   * Atualiza um ticket
   */
  async updateTicket(ticketId, ticketData) {
    return await apiClient.put(`/tickets/${ticketId}`, ticketData);
  },

  /**
   * Remove um ticket
   */
  async deleteTicket(ticketId) {
    return await apiClient.delete(`/tickets/${ticketId}`);
  }
};

export default apiClient;

