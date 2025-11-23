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
 * Utilitários para manipulação de dados do usuário
 */

/**
 * Extrai o primeiro nome do usuário de forma segura
 * @param {Object} userInfo - Objeto com informações do usuário
 * @returns {string} Primeiro nome do usuário ou 'Usuário' como fallback
 */
export const getUserDisplayName = (userInfo) => {
  const capitalizeWords = (s) => {
    return s.split(/\s+/).map(p => p.charAt(0).toUpperCase() + p.slice(1).toLowerCase()).join(' ');
  };

  // Se o objeto userInfo tem nome completo, retorna primeiro + último nome
  if (userInfo?.nome && typeof userInfo.nome === 'string' && userInfo.nome.trim()) {
    const parts = userInfo.nome.trim().split(/\s+/);
    if (parts.length >= 2) {
      return capitalizeWords(`${parts[0]} ${parts[parts.length - 1]}`);
    }
    return capitalizeWords(parts[0]);
  }

  // Se não, tenta extrair do token (claims comuns)
  try {
    const token = localStorage.getItem('authToken');
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const nomeFromToken = payload.nome || payload.Nome || payload.name || payload.Name || payload.unique_name || payload.preferred_username || payload.upn || payload.email;
      if (nomeFromToken && typeof nomeFromToken === 'string' && nomeFromToken.trim()) {
        const parts = nomeFromToken.trim().split(/\s+/);
        if (parts.length >= 2) {
          return capitalizeWords(`${parts[0]} ${parts[parts.length - 1]}`);
        }
        // se for apenas um identificador (ex: email), tenta extrair prefixo antes do @
        if (nomeFromToken.includes('@')) {
          const prefix = nomeFromToken.split('@')[0];
          const prefixParts = prefix.split(/[._-]+/);
          return capitalizeWords(prefixParts[0]);
        }
        return capitalizeWords(nomeFromToken);
      }
    }
  } catch (e) {
    console.error('getUserDisplayName - erro ao extrair do token:', e);
  }

  // Fallback: se houver email em userInfo, usa prefixo
  if (userInfo?.email && typeof userInfo.email === 'string') {
    const prefix = userInfo.email.split('@')[0];
    const prefixParts = prefix.split(/[._-]+/);
    return capitalizeWords(prefixParts[0]);
  }

  return 'Usuário';
};

/**
 * Obtém o nome completo do usuário de forma segura, verificando múltiplas fontes
 * @param {Object} userInfo - Objeto com informações do usuário
 * @returns {string} Nome completo do usuário ou 'Usuário' como fallback
 */
export const getUserFullName = (userInfo) => {
  // Primeiro tenta obter do userInfo passado
  if (userInfo) {
    const nome = userInfo.nome || userInfo.Nome || userInfo.name || userInfo.Name;
    if (nome && typeof nome === 'string' && nome.trim() && nome.trim() !== 'Usuário' && nome.trim() !== '') {
      console.log('getUserFullName - Nome encontrado no userInfo:', nome.trim());
      return nome.trim();
    }
  }
  
  // Se não encontrou, tenta obter do token JWT
  try {
    const token = localStorage.getItem('authToken');
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]));
      // Suporta várias chaves possíveis que podem representar o nome do usuário
      const nomeFromToken = payload.nome || payload.Nome || payload.name || payload.Name || payload.unique_name || payload.preferred_username || payload.upn || payload.email;
      if (nomeFromToken && typeof nomeFromToken === 'string' && nomeFromToken.trim() && nomeFromToken.trim() !== 'Usuário' && nomeFromToken.trim() !== '') {
        console.log('getUserFullName - Nome encontrado no token:', nomeFromToken.trim());
        return nomeFromToken.trim();
      }
    }
  } catch (error) {
    console.error('getUserFullName - Erro ao obter nome do token:', error);
  }
  
  console.warn('getUserFullName - Nome não encontrado, usando fallback "Usuário"');
  return 'Usuário';
};

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
   * Obtém lista de usuários e estatísticas
   */
  async getUsers() {
    return await apiClient.get('/api/Usuarios');
  },

  /**
   * Obtém informações de um único usuário
   * Note: /api/Usuarios/{id} endpoint may not be available, so we fallback to fetching all and filtering
   */
  async getUser(userId) {
    try {
      // Try direct endpoint first
      return await apiClient.get(`/api/Usuarios/${userId}`);
    } catch (error) {
      console.warn(`Direct endpoint /api/Usuarios/${userId} failed, attempting fallback...`);
      
      // Fallback: fetch all users and find the one we need
      try {
        const allData = await this.getUsers();
        let users = [];
        
        if (Array.isArray(allData)) {
          users = allData;
        } else if (allData?.usuarios && Array.isArray(allData.usuarios)) {
          users = allData.usuarios;
        } else if (allData?.items && Array.isArray(allData.items)) {
          users = allData.items;
        } else if (allData?.users && Array.isArray(allData.users)) {
          users = allData.users;
        }
        
        const foundUser = users.find(u => Number(u.id) === Number(userId));
        if (foundUser) {
          console.log(`User ${userId} found via fallback`);
          return foundUser;
        }
        
        throw new Error(`User ${userId} not found`);
      } catch (fallbackError) {
        console.error('Fallback also failed:', fallbackError);
        throw error; // Throw original error
      }
    }
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
    return await apiClient.post('/chamados', ticketData);
  },

  /**
   * Obtém lista de tickets
   * @param {Object} filters - Filtros opcionais (ex: { solicitanteId: 1 })
   */
  async getTickets(filters = {}) {
    const queryParams = new URLSearchParams();
    if (filters.solicitanteId) {
      queryParams.append('solicitanteId', filters.solicitanteId);
    }
    if (filters.status) {
      queryParams.append('status', filters.status);
    }
    const queryString = queryParams.toString();
    const endpoint = queryString ? `/chamados?${queryString}` : '/chamados';
    return await apiClient.get(endpoint);
  },

  /**
   * Obtém um ticket específico
   */
  async getTicket(ticketId) {
    return await apiClient.get(`/chamados/${ticketId}`);
  },

  /**
   * Atualiza um ticket
   */
  async updateTicket(ticketId, ticketData) {
    return await apiClient.put(`/chamados/${ticketId}`, ticketData);
  },

  /**
   * Remove um ticket
   */
  async deleteTicket(ticketId) {
    return await apiClient.delete(`/chamados/${ticketId}`);
  }
};

/**
 * Serviço para integração com IA (Gemini)
 */
export const aiService = {
  /**
   * Gera uma sugestão de resposta técnica usando Gemini AI
   * @param {string} titulo - Título do chamado
   * @param {string} descricao - Descrição do problema
   * @returns {Promise<{sugestao: string}>} Sugestão gerada pela IA
   */
  async gerarSugestao(titulo, descricao) {
    return await apiClient.post('/api/gemini/sugerir-resposta', {
      titulo: titulo || '',
      descricao: descricao
    }, false); // Não requer autenticação
  }
};

export default apiClient;

