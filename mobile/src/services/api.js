// Mock API service para simular chamadas ao backend
const mockTickets = [
  {
    id: 1,
    title: 'Problema com impressora',
    description: 'A impressora nÃ£o estÃ¡ funcionando corretamente',
    status: 'Aberto',
    priority: 'MÃ©dia',
    createdAt: '2024-01-15T10:30:00Z',
    updatedAt: '2024-01-15T14:20:00Z',
    messages: [
      {
        id: 1,
        text: 'A impressora nÃ£o estÃ¡ funcionando corretamente',
        sender: 'user',
        timestamp: '2024-01-15T10:30:00Z'
      },
      {
        id: 2,
        text: 'OlÃ¡! Vou verificar o problema da impressora. Pode me informar qual modelo?',
        sender: 'support',
        timestamp: '2024-01-15T11:15:00Z'
      }
    ]
  },
  {
    id: 2,
    title: 'Acesso ao sistema',
    description: 'NÃ£o consigo acessar o sistema interno',
    status: 'Fechado',
    priority: 'Alta',
    createdAt: '2024-01-10T09:00:00Z',
    updatedAt: '2024-01-12T16:45:00Z',
    messages: [
      {
        id: 1,
        text: 'NÃ£o consigo acessar o sistema interno',
        sender: 'user',
        timestamp: '2024-01-10T09:00:00Z'
      },
      {
        id: 2,
        text: 'Problema resolvido. Sua senha foi resetada.',
        sender: 'support',
        timestamp: '2024-01-12T16:45:00Z'
      }
    ]
  },
  {
    id: 3,
    title: 'InstalaÃ§Ã£o de software',
    description: 'Preciso instalar o Adobe Creative Suite',
    status: 'Aberto',
    priority: 'Baixa',
    createdAt: '2024-01-14T14:20:00Z',
    updatedAt: '2024-01-14T14:20:00Z',
    messages: [
      {
        id: 1,
        text: 'Preciso instalar o Adobe Creative Suite',
        sender: 'user',
        timestamp: '2024-01-14T14:20:00Z'
      }
    ]
  },
  {
    id: 4,
    title: 'Problema com email',
    description: 'Email nÃ£o estÃ¡ sendo recebido',
    status: 'Fechado',
    priority: 'MÃ©dia',
    createdAt: '2024-01-08T08:30:00Z',
    updatedAt: '2024-01-09T10:15:00Z',
    messages: [
      {
        id: 1,
        text: 'Email nÃ£o estÃ¡ sendo recebido',
        sender: 'user',
        timestamp: '2024-01-08T08:30:00Z'
      },
      {
        id: 2,
        text: 'Problema resolvido. Filtros de spam foram ajustados.',
        sender: 'support',
        timestamp: '2024-01-09T10:15:00Z'
      }
    ]
  },
  {
    id: 5,
    title: 'ConfiguraÃ§Ã£o de VPN',
    description: 'Preciso configurar VPN para trabalho remoto',
    status: 'Aberto',
    priority: 'Alta',
    createdAt: '2024-01-16T09:15:00Z',
    updatedAt: '2024-01-16T09:15:00Z',
    messages: [
      {
        id: 1,
        text: 'Preciso configurar VPN para trabalho remoto',
        sender: 'user',
        timestamp: '2024-01-16T09:15:00Z'
      }
    ]
  }
];

export const api = {
  // Simula login
  login: async (email, password) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        if (email && password) {
          resolve({ success: true, user: { id: 1, email, name: 'UsuÃ¡rio Teste' } });
        } else {
          resolve({ success: false, error: 'Credenciais invÃ¡lidas' });
        }
      }, 1000);
    });
  },

  // Busca todos os chamados
  getTickets: async () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(mockTickets);
      }, 500);
    });
  },

  // Busca chamado especÃ­fico
  getTicket: async (id) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const ticket = mockTickets.find(t => t.id === parseInt(id));
        resolve(ticket);
      }, 300);
    });
  },

  // Adiciona resposta ao chamado
  addMessage: async (ticketId, message) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const ticket = mockTickets.find(t => t.id === parseInt(ticketId));
        if (ticket) {
          const newMessage = {
            id: ticket.messages.length + 1,
            text: message,
            sender: 'user',
            timestamp: new Date().toISOString()
          };
          ticket.messages.push(newMessage);
          ticket.updatedAt = newMessage.timestamp;
          resolve({ success: true, message: newMessage });
        } else {
          resolve({ success: false, error: 'Chamado nÃ£o encontrado' });
        }
      }, 500);
    });
  }
};
