// Serviço para simular API de IA
export const AIService = {
  // Simula uma chamada para API de IA que analisa o problema e sugere soluções
  async getSuggestion(problemType, description) {
    // Simula delay da API
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Sugestões baseadas no tipo de problema
    const suggestions = {
      hardware: {
        title: "Sugestões para Problemas de Hardware",
        steps: [
          "1. Verificar se todos os cabos estão conectados corretamente",
          "2. Reiniciar o equipamento e aguardar 30 segundos",
          "3. Verificar se há indicadores de luz piscando",
          "4. Testar com outro cabo ou fonte de energia",
          "5. Verificar se o equipamento está na garantia"
        ],
        additional: "Se o problema persistir, pode ser necessário substituição de peças ou envio para assistência técnica."
      },
      software: {
        title: "Sugestões para Problemas de Software",
        steps: [
          "1. Reiniciar o aplicativo completamente",
          "2. Verificar se há atualizações disponíveis",
          "3. Limpar cache e dados temporários",
          "4. Verificar permissões do sistema",
          "5. Testar em modo de compatibilidade"
        ],
        additional: "Considere reinstalar o software se os passos anteriores não resolverem."
      },
      network: {
        title: "Sugestões para Problemas de Rede",
        steps: [
          "1. Verificar conexão física do cabo de rede",
          "2. Reiniciar o roteador/modem",
          "3. Testar conectividade com ping",
          "4. Verificar configurações de IP",
          "5. Testar com cabo diferente"
        ],
        additional: "Verifique se outros dispositivos na rede estão funcionando normalmente."
      },
      printer: {
        title: "Sugestões para Problemas de Impressora",
        steps: [
          "1. Verificar se há papel na bandeja",
          "2. Limpar papel preso cuidadosamente",
          "3. Verificar nível de tinta/tônner",
          "4. Executar limpeza de cabeçote",
          "5. Verificar drivers da impressora"
        ],
        additional: "Execute o teste de impressão para verificar se o problema foi resolvido."
      },
      email: {
        title: "Sugestões para Problemas de Email",
        steps: [
          "1. Verificar configurações de servidor",
          "2. Limpar cache do cliente de email",
          "3. Verificar filtros de spam",
          "4. Testar com outro cliente de email",
          "5. Verificar espaço em disco"
        ],
        additional: "Contate o administrador do servidor se o problema persistir."
      },
      password: {
        title: "Sugestões para Reset de Senha",
        steps: [
          "1. Verificar política de senhas da empresa",
          "2. Gerar nova senha temporária",
          "3. Configurar nova senha segura",
          "4. Informar usuário sobre nova senha",
          "5. Solicitar primeiro login para alteração"
        ],
        additional: "Certifique-se de que a nova senha atende aos critérios de segurança."
      },
      access: {
        title: "Sugestões para Solicitação de Acesso",
        steps: [
          "1. Verificar perfil de usuário necessário",
          "2. Consultar política de acesso da empresa",
          "3. Solicitar aprovação do gestor",
          "4. Configurar permissões adequadas",
          "5. Testar acesso após configuração"
        ],
        additional: "Documente a solicitação para auditoria futura."
      },
      other: {
        title: "Sugestões Gerais",
        steps: [
          "1. Documentar detalhadamente o problema",
          "2. Verificar logs do sistema",
          "3. Consultar base de conhecimento",
          "4. Escalar para especialista se necessário",
          "5. Manter comunicação com o usuário"
        ],
        additional: "Considere criar um artigo na base de conhecimento para casos similares."
      }
    };

    const suggestion = suggestions[problemType] || suggestions.other;
    
    // Adiciona análise específica baseada na descrição
    const analysis = this.analyzeDescription(description);
    
    return {
      ...suggestion,
      analysis,
      confidence: Math.floor(Math.random() * 30) + 70, // 70-100% de confiança
      timestamp: new Date().toLocaleString('pt-BR'),
    };
  },

  // Analisa a descrição do problema para dar sugestões mais específicas
  analyzeDescription(description) {
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
