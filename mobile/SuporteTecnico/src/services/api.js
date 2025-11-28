// URL da API real hospedada no Azure
const API_BASE_URL = 'https://api-suporte-grupoads-e4hmccf7gaczdbht.brazilsouth-01.azurewebsites.net';

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
      
      // Armazenar o token JWT (a API retorna "Token" com T maiúsculo)
      const token = data.Token || data.token;
      if (token) {
        this.setToken(token);
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
        const errorText = await response.text();
        let errorMessage = 'Erro ao buscar chamados';
        try {
          const errorData = JSON.parse(errorText);
          errorMessage = errorData.message || errorMessage;
        } catch (e) {
          errorMessage = errorText || errorMessage;
        }
        throw new Error(errorMessage);
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
        const errorText = await response.text();
        let errorMessage = 'Erro ao buscar chamado';
        try {
          const errorData = JSON.parse(errorText);
          errorMessage = errorData.message || errorMessage;
        } catch (e) {
          errorMessage = errorText || errorMessage;
        }
        throw new Error(errorMessage);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      throw new Error('Erro ao buscar chamado: ' + error.message);
    }
  }

  async criarChamado(chamadoData) {
    try {
      // Garantir que os dados estão no formato correto esperado pela API
      // A API espera: Titulo, Descricao, Tipo, SolicitanteId, Prioridade (opcional)
      const requestData = {
        Titulo: chamadoData.titulo || chamadoData.Titulo || chamadoData.title,
        Descricao: chamadoData.descricao || chamadoData.Descricao || chamadoData.description,
        Tipo: chamadoData.tipo || chamadoData.Tipo || chamadoData.type,
        SolicitanteId: chamadoData.solicitanteId || chamadoData.SolicitanteId || chamadoData.solicitante_id || 1,
        Prioridade: chamadoData.prioridade || chamadoData.Prioridade || null
      };

      const response = await fetch(`${API_BASE_URL}/api/Chamados`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(requestData),
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        let errorMessage = 'Erro ao criar chamado';
        try {
          const errorData = JSON.parse(errorText);
          errorMessage = errorData.message || errorMessage;
        } catch (e) {
          errorMessage = errorText || errorMessage;
        }
        throw new Error(errorMessage);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      throw new Error('Erro ao criar chamado: ' + error.message);
    }
  }

  async atualizarChamado(id, dadosAtualizacao) {
    try {
      // Garantir que os dados estão no formato correto esperado pela API
      // A API espera campos opcionais: Status, TecnicoResponsavelId, DataFechamento, Titulo, Descricao, Solucao, Prioridade
      const requestData = {};
      
      if (dadosAtualizacao.status !== undefined) {
        requestData.Status = dadosAtualizacao.status;
      }
      if (dadosAtualizacao.tecnicoResponsavelId !== undefined || dadosAtualizacao.TecnicoResponsavelId !== undefined) {
        requestData.TecnicoResponsavelId = dadosAtualizacao.tecnicoResponsavelId || dadosAtualizacao.TecnicoResponsavelId;
      }
      if (dadosAtualizacao.dataFechamento !== undefined || dadosAtualizacao.DataFechamento !== undefined) {
        requestData.DataFechamento = dadosAtualizacao.dataFechamento || dadosAtualizacao.DataFechamento;
      }
      if (dadosAtualizacao.titulo !== undefined || dadosAtualizacao.Titulo !== undefined) {
        requestData.Titulo = dadosAtualizacao.titulo || dadosAtualizacao.Titulo;
      }
      if (dadosAtualizacao.descricao !== undefined || dadosAtualizacao.Descricao !== undefined) {
        requestData.Descricao = dadosAtualizacao.descricao || dadosAtualizacao.Descricao;
      }
      if (dadosAtualizacao.solucao !== undefined || dadosAtualizacao.Solucao !== undefined) {
        requestData.Solucao = dadosAtualizacao.solucao || dadosAtualizacao.Solucao;
      }
      if (dadosAtualizacao.prioridade !== undefined || dadosAtualizacao.Prioridade !== undefined) {
        requestData.Prioridade = dadosAtualizacao.prioridade || dadosAtualizacao.Prioridade;
      }

      const response = await fetch(`${API_BASE_URL}/api/Chamados/${id}`, {
        method: 'PUT',
        headers: this.getHeaders(),
        body: JSON.stringify(requestData),
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        let errorMessage = 'Erro ao atualizar chamado';
        try {
          const errorData = JSON.parse(errorText);
          errorMessage = errorData.message || errorMessage;
        } catch (e) {
          errorMessage = errorText || errorMessage;
        }
        throw new Error(errorMessage);
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
