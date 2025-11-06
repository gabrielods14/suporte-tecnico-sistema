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
      console.log('=== INÍCIO DO LOGIN ===');
      console.log('Email:', email);
      console.log('Senha:', senha ? '***' : 'vazia');
      console.log('URL da API:', `${API_BASE_URL}/api/Auth/login`);
      
      // A API C# espera "Email" e "Senha" com maiúsculas (conforme DTO da API C#)
      const requestBody = { 
        Email: email,  // Com maiúscula
        Senha: senha   // Com maiúscula
      };
      console.log('Corpo da requisição:', JSON.stringify(requestBody));
      
      // Timeout de 30 segundos para a requisição
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000);

      const response = await fetch(`${API_BASE_URL}/api/Auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);
      
      console.log('Status da resposta:', response.status);
      console.log('Status Text:', response.statusText);
      console.log('Headers da resposta:', Object.fromEntries(response.headers.entries()));
      
      const responseText = await response.text();
      console.log('Resposta bruta:', responseText);
      
      if (!response.ok) {
        console.log('Erro na resposta da API');
        let errorMessage = `Erro ${response.status}: ${response.statusText}`;
        
        try {
          const errorData = JSON.parse(responseText);
          errorMessage = errorData.message || errorMessage;
        } catch (e) {
          errorMessage = responseText || errorMessage;
        }
        
        console.log('Mensagem de erro:', errorMessage);
        throw new Error(errorMessage);
      }
      
      const data = JSON.parse(responseText);
      console.log('Dados parseados:', data);
      
      // Armazenar o token JWT
      if (data.token) {
        this.setToken(data.token);
        console.log('Token armazenado com sucesso');
      } else {
        console.log('AVISO: Nenhum token recebido na resposta');
      }
      
      console.log('=== LOGIN CONCLUÍDO COM SUCESSO ===');
      return data;
    } catch (error) {
      console.log('=== ERRO NO LOGIN ===');
      console.log('Tipo do erro:', error.constructor.name);
      console.log('Mensagem do erro:', error.message);
      console.log('Stack trace:', error.stack);
      
      // Tratamento específico de erros
      if (error.name === 'AbortError') {
        throw new Error('Tempo de conexão excedido. Verifique sua internet e tente novamente.');
      }
      
      if (error.message.includes('Network request failed') || 
          error.message.includes('fetch') ||
          error.message.includes('Failed to connect')) {
        throw new Error('Erro de conexão. Verifique sua internet e tente novamente.');
      }
      
      if (error.message.includes('401') || error.message.includes('Unauthorized')) {
        throw new Error('E-mail ou senha inválidos. Verifique suas credenciais.');
      }
      
      throw new Error(error.message || 'Erro desconhecido ao fazer login');
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
