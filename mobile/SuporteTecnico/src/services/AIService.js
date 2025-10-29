import GeminiService from './GeminiService';

const AIService = {
  // Configurar chave de API do Gemini
  setGeminiApiKey: (apiKey) => {
    GeminiService.setApiKey(apiKey);
  },

  // Obter sugestão usando Gemini Pro
  getSuggestion: async (problemType, description, userContext = '') => {
    try {
      console.log('=== AIService: Iniciando busca de sugestão ===');
      console.log('Tipo:', problemType);
      console.log('Descrição:', description);
      console.log('Contexto:', userContext);

      // Usar Gemini Service para obter sugestão inteligente
      const suggestion = await GeminiService.generateResolutionSuggestion(
        problemType, 
        description, 
        userContext
      );

      console.log('=== AIService: Sugestão obtida com sucesso ===');
      console.log('Sugestão:', suggestion);

      return suggestion;

    } catch (error) {
      console.log('=== AIService: Erro ao obter sugestão ===');
      console.log('Erro:', error);

      // Fallback para sugestão básica em caso de erro
      return AIService.getFallbackSuggestion(problemType, description);
    }
  },

  // Gerar resposta automática para técnico
  generateAutoResponse: (suggestion, problemType) => {
    return GeminiService.generateTechnicianResponse(suggestion, problemType);
  },

  // Sugestão de fallback (mantida do código original)
  getFallbackSuggestion: (problemType, description) => {
    console.log('=== AIService: Usando sugestão de fallback ===');

    let suggestion = {
      analysis: "Análise inicial do problema.",
      steps: ["Verificar informações básicas.", "Coletar mais dados."],
      additional: "Consulte a base de conhecimento para casos semelhantes.",
      confidence: "70%",
      sentiment: "Neutro",
      estimatedTime: "20-30 minutos",
      priority: "Média"
    };

    switch (problemType) {
      case 'hardware':
        suggestion = {
          analysis: "O problema parece estar relacionado a componentes físicos do equipamento.",
          steps: [
            "Verificar se todos os cabos estão conectados corretamente (energia, dados).",
            "Reiniciar o equipamento e aguardar 30 segundos antes de ligar novamente.",
            "Realizar um diagnóstico de hardware (se disponível no sistema operacional)."
          ],
          additional: "Se o problema persistir, considere a substituição do componente defeituoso.",
          confidence: "90%",
          sentiment: "Preocupado",
          estimatedTime: "15-30 minutos",
          priority: "Média"
        };
        break;
      case 'software':
        suggestion = {
          analysis: "Indica uma falha ou mau funcionamento de um aplicativo ou sistema operacional.",
          steps: [
            "Verificar se o software está atualizado para a versão mais recente.",
            "Limpar o cache e os dados temporários do aplicativo.",
            "Reinstalar o software se as etapas anteriores não resolverem."
          ],
          additional: "Verifique os logs de erro do sistema para identificar a causa raiz.",
          confidence: "85%",
          sentiment: "Frustrado",
          estimatedTime: "20-45 minutos",
          priority: "Média"
        };
        break;
      case 'network':
        suggestion = {
          analysis: "Problemas de conectividade podem ser causados por falhas no hardware de rede ou configurações incorretas.",
          steps: [
            "Verificar conexão física do cabo de rede ou status do Wi-Fi.",
            "Reiniciar o roteador/modem e o computador/dispositivo.",
            "Verificar configurações de IP (DHCP, IP estático) e DNS."
          ],
          additional: "Testar a conectividade com outros dispositivos na mesma rede.",
          confidence: "95%",
          sentiment: "Irritado",
          estimatedTime: "10-25 minutos",
          priority: "Alta"
        };
        break;
      case 'printer':
        suggestion = {
          analysis: "Problemas comuns incluem atolamento de papel, falta de tinta/toner ou drivers desatualizados.",
          steps: [
            "Verificar se há papel na bandeja e se não há papel preso.",
            "Verificar os níveis de tinta ou toner.",
            "Reinstalar ou atualizar os drivers da impressora."
          ],
          additional: "Realizar uma página de teste para verificar o funcionamento.",
          confidence: "80%",
          sentiment: "Impaciente",
          estimatedTime: "15-30 minutos",
          priority: "Média"
        };
        break;
      case 'email':
        suggestion = {
          analysis: "Dificuldades no envio ou recebimento de e-mails, ou acesso à conta.",
          steps: [
            "Verificar configurações do servidor de e-mail (IMAP/POP3, SMTP).",
            "Testar a conexão com a internet.",
            "Verificar se a caixa de entrada não está cheia ou se há filtros incorretos."
          ],
          additional: "Confirmar as credenciais de login com o usuário.",
          confidence: "75%",
          sentiment: "Incomodado",
          estimatedTime: "20-40 minutos",
          priority: "Média"
        };
        break;
      case 'password':
        suggestion = {
          analysis: "Solicitação de redefinição de senha para acesso a sistemas ou contas.",
          steps: [
            "Verificar a identidade do usuário de forma segura.",
            "Gerar uma nova senha temporária e comunicar ao usuário.",
            "Orientar o usuário a alterar a senha temporária no primeiro login."
          ],
          additional: "Reforçar a política de senhas seguras.",
          confidence: "100%",
          sentiment: "Urgente",
          estimatedTime: "5-15 minutos",
          priority: "Alta"
        };
        break;
      case 'access':
        suggestion = {
          analysis: "Solicitação de permissões ou acesso a novos sistemas/recursos.",
          steps: [
            "Verificar a necessidade e a aprovação da solicitação de acesso.",
            "Configurar as permissões necessárias no sistema.",
            "Confirmar com o usuário se o acesso foi concedido corretamente."
          ],
          additional: "Documentar a concessão de acesso para auditoria.",
          confidence: "90%",
          sentiment: "Expectante",
          estimatedTime: "10-20 minutos",
          priority: "Média"
        };
        break;
      default:
        suggestion = {
          analysis: "O problema não se encaixa em categorias padrão, requer análise mais aprofundada.",
          steps: [
            "Coletar o máximo de informações detalhadas do usuário.",
            "Consultar a base de conhecimento para problemas similares ou incomuns.",
            "Escalar para um especialista se a solução não for evidente."
          ],
          additional: "Manter o usuário informado sobre o andamento da investigação.",
          confidence: "70%",
          sentiment: "Curioso",
          estimatedTime: "30-60 minutos",
          priority: "Média"
        };
    }

    return suggestion;
  },

  // Analisa a descrição do problema para dar sugestões mais específicas
  analyzeDescription: (description) => {
    const lowerDesc = description.toLowerCase();
    
    if (lowerDesc.includes('erro') || lowerDesc.includes('error')) {
      return "Detectado erro no sistema. Verifique logs de erro e mensagens específicas.";
    }
    
    if (lowerDesc.includes('lento') || lowerDesc.includes('demora')) {
      return "Problema de performance detectado. Considere otimizações de sistema.";
    }
    
    if (lowerDesc.includes('não funciona') || lowerDesc.includes('não está funcionando')) {
      return "Falha funcional identificada. Verifique configurações e dependências.";
    }
    
    if (lowerDesc.includes('conexão') || lowerDesc.includes('conectar')) {
      return "Problema de conectividade detectado. Verifique configurações de rede.";
    }
    
    return "Análise geral do problema realizada. Siga as etapas sugeridas.";
  },

  // Simula análise de sentimento do usuário
  async analyzeUserSentiment(description) {
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const lowerDesc = description.toLowerCase();
    const urgentWords = ['urgente', 'emergência', 'crítico', 'importante', 'asap'];
    const frustratedWords = ['frustrado', 'irritado', 'cansado', 'problema', 'não funciona'];
    
    const urgency = urgentWords.some(word => lowerDesc.includes(word)) ? 'Alta' : 'Normal';
    const sentiment = frustratedWords.some(word => lowerDesc.includes(word)) ? 'Frustrado' : 'Neutro';
    
    return {
      urgency,
      sentiment,
      priority: urgency === 'Alta' ? 'Alta' : 'Média',
    };
  }
};

export default AIService;