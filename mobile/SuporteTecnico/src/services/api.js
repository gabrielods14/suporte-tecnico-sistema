// URL da API real hospedada no Azure
const API_BASE_URL = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net';

class ApiService {
  // Armazenar token JWT
  constructor() {
    this.token = null;
  }

  // Definir token JWT
  setToken(token) {
    this.token = token;
  }

  // Obter headers com autenticação
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };
    
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    
    return headers;
  }

  async login(email, senha) {
    try {
      console.log('Tentando fazer login com:', { email, senha });
      console.log('URL da API:', `${API_BASE_URL}/api/Auth/login`);
      
      const response = await fetch(`${API_BASE_URL}/api/Auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, senha }),
      });
      
      console.log('Status da resposta:', response.status);
      console.log('Headers da resposta:', response.headers);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.log('Erro da API:', errorText);
        throw new Error(`Erro ${response.status}: ${errorText}`);
      }
      
      const data = await response.json();
      console.log('Resposta da API:', data);
      
      // Armazenar o token JWT
      if (data.token) {
        this.setToken(data.token);
        console.log('Token armazenado:', data.token);
      }
      
      return data;
    } catch (error) {
      console.log('Erro completo:', error);
      throw new Error('Erro ao fazer login: ' + error.message);
    }
  }

  async getChamados() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/Chamados`, {
        method: 'GET',
        headers: this.getHeaders(),
      });
      
      if (!response.ok) {
        throw new Error('Erro ao buscar chamados');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      throw new Error('Erro ao buscar chamados: ' + error.message);
    }
  }

  async getChamadoById(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/Chamados/${id}`, {
        method: 'GET',
        headers: this.getHeaders(),
      });
      
      if (!response.ok) {
        throw new Error('Erro ao buscar chamado');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      throw new Error('Erro ao buscar chamado: ' + error.message);
    }
  }

  async criarChamado(chamadoData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/Chamados`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(chamadoData),
      });
      
      if (!response.ok) {
        throw new Error('Erro ao criar chamado');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      throw new Error('Erro ao criar chamado: ' + error.message);
    }
  }

  async atualizarChamado(id, dadosAtualizacao) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/Chamados/${id}`, {
        method: 'PUT',
        headers: this.getHeaders(),
        body: JSON.stringify(dadosAtualizacao),
      });
      
      if (!response.ok) {
        throw new Error('Erro ao atualizar chamado');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      throw new Error('Erro ao atualizar chamado: ' + error.message);
    }
  }

  // Métodos para compatibilidade com o código existente
  async getTickets() {
    return this.getChamados();
  }

  async getTicketById(id) {
    return this.getChamadoById(id);
  }

  async updateTicketStatus(id, status) {
    return this.atualizarChamado(id, { status });
  }
}

export default new ApiService();
