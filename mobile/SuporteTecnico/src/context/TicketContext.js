import React, { createContext, useContext, useReducer, useEffect } from 'react';
import ApiService from '../services/api';

const TicketContext = createContext();

// Tipos de ação
const TICKET_ACTIONS = {
  CREATE_TICKET: 'CREATE_TICKET',
  UPDATE_TICKET: 'UPDATE_TICKET',
  RESPOND_TO_TICKET: 'RESPOND_TO_TICKET',
  COMPLETE_TICKET: 'COMPLETE_TICKET',
  SET_AI_SUGGESTION: 'SET_AI_SUGGESTION',
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
  SET_TICKETS: 'SET_TICKETS',
};

// Estado inicial
const initialState = {
  tickets: [],
  loading: false,
  error: null,
};

// Reducer
const ticketReducer = (state, action) => {
  switch (action.type) {
    case TICKET_ACTIONS.SET_LOADING:
      return {
        ...state,
        loading: action.payload,
      };

    case TICKET_ACTIONS.SET_ERROR:
      return {
        ...state,
        error: action.payload,
        loading: false,
      };

    case TICKET_ACTIONS.SET_TICKETS:
      return {
        ...state,
        tickets: action.payload,
        loading: false,
        error: null,
      };

    case TICKET_ACTIONS.CREATE_TICKET:
      return {
        ...state,
        tickets: [...state.tickets, action.payload],
        loading: false,
      };

    case TICKET_ACTIONS.UPDATE_TICKET:
      return {
        ...state,
        tickets: state.tickets.map(ticket =>
          ticket.id === action.payload.id
            ? { ...ticket, ...action.payload.updates }
            : ticket
        ),
      };

    case TICKET_ACTIONS.RESPOND_TO_TICKET:
      return {
        ...state,
        tickets: state.tickets.map(ticket =>
          ticket.id === action.payload.ticketId
            ? {
                ...ticket,
                responses: [...ticket.responses, action.payload.response],
                status: 'Em Atendimento',
                lastRespondedBy: action.payload.technicianName,
                lastResponseDate: new Date().toLocaleString('pt-BR'),
              }
            : ticket
        ),
      };

    case TICKET_ACTIONS.COMPLETE_TICKET:
      return {
        ...state,
        tickets: state.tickets.map(ticket =>
          ticket.id === action.payload.ticketId
            ? {
                ...ticket,
                status: 'Fechado',
                completedAt: new Date().toLocaleString('pt-BR'),
                completedBy: action.payload.technicianName,
              }
            : ticket
        ),
      };

    case TICKET_ACTIONS.SET_AI_SUGGESTION:
      return {
        ...state,
        tickets: state.tickets.map(ticket =>
          ticket.id === action.payload.ticketId
            ? { ...ticket, aiSuggestion: action.payload.suggestion }
            : ticket
        ),
      };

    default:
      return state;
  }
};

// Provider
export const TicketProvider = ({ children }) => {
  const [state, dispatch] = useReducer(ticketReducer, initialState);

  // Carregar chamados da API
  const loadTickets = async () => {
    try {
      dispatch({ type: TICKET_ACTIONS.SET_LOADING, payload: true });
      const chamados = await ApiService.getChamados();
      
      // Converter dados da API para o formato esperado pelo app
      const tickets = chamados.map(chamado => ({
        id: chamado.id.toString(),
        title: chamado.titulo,
        type: chamado.tipo.toLowerCase(),
        description: chamado.descricao,
        user: chamado.solicitante?.nome || 'Usuário',
        userEmail: chamado.solicitante?.email || 'usuario@empresa.com',
        status: getStatusText(chamado.status),
        priority: getPriorityText(chamado.prioridade),
        createdAt: new Date(chamado.dataAbertura).toLocaleString('pt-BR'),
        responses: [],
        aiSuggestion: '',
        completedAt: chamado.dataFechamento ? new Date(chamado.dataFechamento).toLocaleString('pt-BR') : null,
        lastRespondedBy: chamado.tecnicoResponsavel?.nome || null,
        lastResponseDate: null,
        completedBy: chamado.dataFechamento ? chamado.tecnicoResponsavel?.nome : null,
      }));
      
      dispatch({ type: TICKET_ACTIONS.SET_TICKETS, payload: tickets });
    } catch (error) {
      dispatch({ type: TICKET_ACTIONS.SET_ERROR, payload: error.message });
    }
  };

  // Função auxiliar para converter status numérico para texto
  // Conforme enum StatusChamado do backend: Aberto=1, EmAtendimento=2, Fechado=3
  const getStatusText = (status) => {
    const statusMap = {
      1: 'Aberto',
      2: 'Em Atendimento',
      3: 'Fechado'
    };
    return statusMap[status] || 'Aberto';
  };

  // Função auxiliar para converter prioridade numérica para texto
  const getPriorityText = (priority) => {
    const priorityMap = {
      1: 'Baixa',
      2: 'Média',
      3: 'Alta'
    };
    return priorityMap[priority] || 'Média';
  };

  const createTicket = async (ticketData) => {
    try {
      dispatch({ type: TICKET_ACTIONS.SET_LOADING, payload: true });
      
      // Converter dados do app para o formato da API
      const chamadoData = {
        titulo: ticketData.title,
        descricao: ticketData.description,
        tipo: ticketData.type,
        solicitanteId: 1, // ID do usuário atual (deveria vir do contexto de autenticação)
        prioridade: getPriorityNumber(ticketData.priority),
      };
      
      const novoChamado = await ApiService.criarChamado(chamadoData);
      
      // Converter resposta da API para o formato do app
      const ticket = {
        id: novoChamado.id.toString(),
        title: novoChamado.titulo,
        type: novoChamado.tipo.toLowerCase(),
        description: novoChamado.descricao,
        user: novoChamado.solicitante?.nome || 'Usuário',
        userEmail: novoChamado.solicitante?.email || 'usuario@empresa.com',
        status: 'Aberto',
        priority: getPriorityText(novoChamado.prioridade),
        createdAt: new Date(novoChamado.dataAbertura).toLocaleString('pt-BR'),
        responses: [],
        aiSuggestion: '',
        completedAt: null,
        lastRespondedBy: null,
        lastResponseDate: null,
        completedBy: null,
      };
      
      dispatch({ type: TICKET_ACTIONS.CREATE_TICKET, payload: ticket });
    } catch (error) {
      dispatch({ type: TICKET_ACTIONS.SET_ERROR, payload: error.message });
    }
  };

  // Função auxiliar para converter prioridade texto para número
  const getPriorityNumber = (priority) => {
    const priorityMap = {
      'Baixa': 1,
      'Média': 2,
      'Alta': 3
    };
    return priorityMap[priority] || 2;
  };

  const updateTicket = (ticketId, updates) => {
    dispatch({
      type: TICKET_ACTIONS.UPDATE_TICKET,
      payload: { id: ticketId, updates },
    });
  };

  const respondToTicket = async (ticketId, response, technicianName = 'Técnico Atual') => {
    try {
      dispatch({ type: TICKET_ACTIONS.SET_LOADING, payload: true });
      
      // Atualizar o chamado na API com a resposta
      // Conforme enum StatusChamado: EmAtendimento = 2
      await ApiService.atualizarChamado(ticketId, {
        status: 2, // Em Atendimento
        tecnicoResponsavelId: 1, // ID do técnico (deveria vir do contexto de autenticação)
      });
      
      dispatch({
        type: TICKET_ACTIONS.RESPOND_TO_TICKET,
        payload: {
          ticketId,
          response: {
            id: Date.now().toString(),
            text: response,
            technician: technicianName,
            timestamp: new Date().toLocaleString('pt-BR'),
          },
          technicianName,
        },
      });
    } catch (error) {
      dispatch({ type: TICKET_ACTIONS.SET_ERROR, payload: error.message });
    }
  };

  const completeTicket = async (ticketId, technicianName = 'Técnico Atual') => {
    try {
      dispatch({ type: TICKET_ACTIONS.SET_LOADING, payload: true });
      
      // Atualizar o chamado na API para status "Fechado"
      // Conforme enum StatusChamado: Fechado = 3
      await ApiService.atualizarChamado(ticketId, {
        status: 3, // Fechado
        dataFechamento: new Date().toISOString(),
        tecnicoResponsavelId: 1, // ID do técnico (deveria vir do contexto de autenticação)
      });
      
      dispatch({
        type: TICKET_ACTIONS.COMPLETE_TICKET,
        payload: { ticketId, technicianName },
      });
    } catch (error) {
      dispatch({ type: TICKET_ACTIONS.SET_ERROR, payload: error.message });
    }
  };

  const setAISuggestion = (ticketId, suggestion) => {
    dispatch({
      type: TICKET_ACTIONS.SET_AI_SUGGESTION,
      payload: { ticketId, suggestion },
    });
  };

  const getTicketsByStatus = (status) => {
    return state.tickets.filter(ticket => ticket.status === status);
  };

  const getTicketById = (id) => {
    return state.tickets.find(ticket => ticket.id === id);
  };

  const value = {
    ...state,
    loadTickets,
    createTicket,
    updateTicket,
    respondToTicket,
    completeTicket,
    setAISuggestion,
    getTicketsByStatus,
    getTicketById,
  };

  return (
    <TicketContext.Provider value={value}>
      {children}
    </TicketContext.Provider>
  );
};

// Hook personalizado
export const useTickets = () => {
  const context = useContext(TicketContext);
  if (!context) {
    throw new Error('useTickets deve ser usado dentro de um TicketProvider');
  }
  return context;
};

export default TicketContext;
