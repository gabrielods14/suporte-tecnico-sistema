// GeminiService.js - Integração com Google Gemini Pro API

// Configuração da API do Gemini
const GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY'; // Substitua pela sua chave de API
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';

class GeminiService {
  constructor() {
    this.apiKey = GEMINI_API_KEY;
  }

  // Configurar a chave de API
  setApiKey(apiKey) {
    this.apiKey = apiKey;
  }

  // Gerar sugestão de resolução baseada no tipo e descrição do problema
  async generateResolutionSuggestion(problemType, description, userContext = '') {
    try {
      console.log('=== INICIANDO CHAMADA PARA GEMINI ===');
      console.log('Tipo do problema:', problemType);
      console.log('Descrição:', description);
      console.log('Contexto do usuário:', userContext);

      const prompt = this.buildPrompt(problemType, description, userContext);
      console.log('Prompt enviado para Gemini:', prompt);

      const response = await fetch(`${GEMINI_API_URL}?key=${this.apiKey}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: prompt
            }]
          }],
          generationConfig: {
            temperature: 0.7,
            topK: 40,
            topP: 0.95,
            maxOutputTokens: 1024,
          },
          safetySettings: [
            {
              category: "HARM_CATEGORY_HARASSMENT",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
              category: "HARM_CATEGORY_HATE_SPEECH",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
              category: "HARM_CATEGORY_SEXUALLY_EXPLICIT",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
              category: "HARM_CATEGORY_DANGEROUS_CONTENT",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            }
          ]
        })
      });

      console.log('Status da resposta Gemini:', response.status);
      console.log('Headers da resposta:', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        const errorText = await response.text();
        console.log('Erro da API Gemini:', errorText);
        throw new Error(`Erro ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      console.log('Resposta completa do Gemini:', data);

      if (!data.candidates || !data.candidates[0] || !data.candidates[0].content) {
        throw new Error('Resposta inválida do Gemini');
      }

      const generatedText = data.candidates[0].content.parts[0].text;
      console.log('Texto gerado pelo Gemini:', generatedText);

      // Parsear a resposta estruturada
      const suggestion = this.parseGeminiResponse(generatedText);
      console.log('Sugestão parseada:', suggestion);

      return suggestion;

    } catch (error) {
      console.log('=== ERRO NO GEMINI SERVICE ===');
      console.log('Tipo do erro:', error.constructor.name);
      console.log('Mensagem do erro:', error.message);
      console.log('Stack trace:', error.stack);

      // Retornar sugestão de fallback em caso de erro
      return this.getFallbackSuggestion(problemType, description);
    }
  }

  // Construir prompt otimizado para o Gemini com foco em soluções técnicas detalhadas
  buildPrompt(problemType, description, userContext) {
    const problemTypeMap = {
      'hardware': 'problema de hardware',
      'software': 'problema de software',
      'network': 'problema de rede/conectividade',
      'printer': 'problema com impressora',
      'email': 'problema com email',
      'password': 'reset de senha',
      'access': 'solicitação de acesso',
      'other': 'outro tipo de problema'
    };

    const problemTypeText = problemTypeMap[problemType] || 'problema técnico';

    return `Você é um especialista técnico sênior em uma conversa de chat ao vivo. Um técnico de suporte está me perguntando sobre um problema específico. Analise a descrição como se fosse uma pergunta direta em um chat e forneça uma resposta técnica detalhada e específica.

PROBLEMA RELATADO:
"${description}"

TIPO DE PROBLEMA: ${problemTypeText}
${userContext ? `CONTEXTO ADICIONAL: ${userContext}` : ''}

INSTRUÇÕES IMPORTANTES:
1. Analise a descrição como se fosse uma pergunta real de um técnico
2. Identifique os sintomas específicos mencionados
3. Forneça um passo-a-passo detalhado baseado na descrição exata
4. Inclua comandos específicos, caminhos exatos e configurações precisas
5. Mencione logs específicos que devem ser verificados
6. Sugira ferramentas específicas com comandos exatos
7. Forneça verificações específicas para confirmar a solução

FORMATO DE RESPOSTA (JSON):

{
  "analysis": "Análise técnica específica do problema baseada na descrição exata fornecida",
  "symptoms": [
    "Sintoma específico mencionado na descrição",
    "Outro sintoma identificado",
    "Comportamento específico relatado"
  ],
  "rootCause": "Causa raiz específica baseada nos sintomas descritos",
  "stepByStepSolution": [
    "Passo 1: Comando específico ou ação exata a ser executada",
    "Passo 2: Próxima ação específica com parâmetros exatos",
    "Passo 3: Verificação específica ou configuração exata",
    "Passo 4: Teste específico para confirmar a solução"
  ],
  "specificCommands": [
    "Comando exato: comando --parametro valor",
    "Outro comando: caminho/para/executavel -opcao",
    "Terceiro comando: ferramenta específica com flags"
  ],
  "logsToCheck": [
    "Caminho específico: /var/log/arquivo.log",
    "Comando de verificação: tail -f /caminho/log | grep 'erro'",
    "Filtro específico: journalctl -u servico --since '1 hour ago'"
  ],
  "configurationFiles": [
    "Arquivo: /etc/caminho/arquivo.conf",
    "Registro: HKEY_LOCAL_MACHINE\\Software\\Chave",
    "Configuração: ~/.config/aplicacao/settings.json"
  ],
  "toolsNeeded": [
    "Ferramenta: nome_da_ferramenta --help",
    "Utilitário: comando específico com opções",
    "Diagnóstico: ferramenta_de_diagnostico -v"
  ],
  "verificationSteps": [
    "Teste específico: comando de teste com parâmetros",
    "Verificação: como confirmar que funcionou",
    "Indicador: o que observar para confirmar sucesso"
  ],
  "commonIssues": [
    "Problema comum: descrição específica e solução",
    "Erro típico: código de erro e workaround",
    "Falha conhecida: sintoma e correção específica"
  ],
  "additional": "Informações técnicas adicionais específicas para este caso",
  "confidence": "Nível de confiança baseado na especificidade da análise",
  "estimatedTime": "Tempo real estimado para esta solução específica",
  "priority": "Prioridade baseada no impacto descrito",
  "escalationCriteria": "Quando escalar baseado nos sintomas específicos"
}

EXEMPLOS DE ANÁLISE CONVERSACIONAL:

Se a descrição for: "O computador não consegue conectar à internet, aparece erro DNS"
- Analise: Problema de resolução DNS específico
- Sintomas: Falha de conexão, erro DNS específico
- Solução: Comandos específicos para DNS como "ipconfig /flushdns", "nslookup google.com"
- Logs: Verificar logs de DNS específicos
- Verificação: Teste específico de conectividade

Se a descrição for: "A impressora não imprime, fica na fila"
- Analise: Problema de spooler de impressão
- Sintomas: Documentos na fila, não impressão
- Solução: Comandos específicos para spooler como "net stop spooler", "net start spooler"
- Logs: Verificar logs do spooler específicos
- Verificação: Teste de impressão específico

IMPORTANTE: 
- Seja específico baseado na descrição exata
- Forneça comandos exatos que podem ser copiados e colados
- Analise os sintomas específicos mencionados
- Dê soluções práticas e aplicáveis imediatamente
- Evite respostas genéricas - seja específico para o problema descrito`;
  }

  // Parsear resposta do Gemini para formato estruturado
  parseGeminiResponse(text) {
    try {
      // Tentar extrair JSON da resposta
      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const jsonStr = jsonMatch[0];
        const parsed = JSON.parse(jsonStr);
        
        // Validar campos obrigatórios e criar estrutura completa
        if (parsed.analysis) {
          return {
            analysis: parsed.analysis,
            symptoms: parsed.symptoms || [],
            rootCause: parsed.rootCause || '',
            stepByStepSolution: parsed.stepByStepSolution || [],
            specificCommands: parsed.specificCommands || [],
            logsToCheck: parsed.logsToCheck || [],
            configurationFiles: parsed.configurationFiles || [],
            toolsNeeded: parsed.toolsNeeded || [],
            verificationSteps: parsed.verificationSteps || [],
            commonIssues: parsed.commonIssues || [],
            additional: parsed.additional || '',
            confidence: parsed.confidence || '80%',
            estimatedTime: parsed.estimatedTime || '15-30 minutos',
            priority: parsed.priority || 'Média',
            escalationCriteria: parsed.escalationCriteria || '',
            // Manter compatibilidade com formato antigo
            steps: parsed.stepByStepSolution || parsed.solutionSteps || parsed.steps || [],
            diagnosticSteps: parsed.diagnosticSteps || [],
            solutionSteps: parsed.solutionSteps || [],
            commonErrors: parsed.commonErrors || [],
            sentiment: parsed.sentiment || 'Neutro'
          };
        }
      }

      // Se não conseguir parsear JSON, extrair informações do texto
      return this.extractInfoFromText(text);

    } catch (error) {
      console.log('Erro ao parsear resposta do Gemini:', error);
      return this.extractInfoFromText(text);
    }
  }

  // Extrair informações do texto quando JSON não está disponível
  extractInfoFromText(text) {
    const lines = text.split('\n').filter(line => line.trim());
    
    return {
      analysis: lines[0] || 'Análise técnica específica baseada na descrição do problema.',
      symptoms: [
        'Sintoma específico identificado na descrição',
        'Comportamento relatado pelo usuário',
        'Indicador técnico observado'
      ],
      rootCause: 'Causa raiz específica baseada nos sintomas descritos',
      stepByStepSolution: [
        'Passo 1: Ação específica baseada na descrição',
        'Passo 2: Comando técnico específico',
        'Passo 3: Verificação específica',
        'Passo 4: Teste de confirmação'
      ],
      specificCommands: [
        'Comando específico para este problema',
        'Utilitário técnico com parâmetros',
        'Ferramenta de diagnóstico específica'
      ],
      logsToCheck: [
        'Log específico: /var/log/arquivo.log',
        'Comando: tail -f /caminho/log | grep erro',
        'Verificação: journalctl -u servico'
      ],
      configurationFiles: [
        'Arquivo: /etc/caminho/config.conf',
        'Registro: HKEY_LOCAL_MACHINE\\Software\\Chave',
        'Configuração: ~/.config/app/settings.json'
      ],
      toolsNeeded: [
        'Ferramenta: nome_ferramenta --help',
        'Utilitário: comando específico -opcao',
        'Diagnóstico: ferramenta_diagnostico -v'
      ],
      verificationSteps: [
        'Teste específico: comando de verificação',
        'Verificação: indicador de sucesso',
        'Confirmação: teste final'
      ],
      commonIssues: [
        'Problema comum: descrição e solução específica',
        'Erro típico: código e workaround',
        'Falha conhecida: sintoma e correção'
      ],
      additional: 'Informações técnicas adicionais específicas para este caso.',
      confidence: '75%',
      sentiment: 'Neutro',
      estimatedTime: '20-30 minutos',
      priority: 'Média',
      escalationCriteria: 'Escalar se sintomas persistirem após aplicar soluções',
      // Manter compatibilidade
      steps: [
        'Passo específico baseado na descrição',
        'Ação técnica detalhada',
        'Verificação de resolução'
      ],
      diagnosticSteps: [],
      solutionSteps: [],
      commonErrors: []
    };
  }

  // Sugestão de fallback em caso de erro na API
  getFallbackSuggestion(problemType, description) {
    const fallbackSuggestions = {
      hardware: {
        analysis: "Problema de hardware identificado. Recomenda-se verificação física dos componentes.",
        steps: [
          "Verificar conexões físicas e cabos",
          "Reiniciar o equipamento e aguardar 30 segundos",
          "Executar diagnóstico de hardware se disponível"
        ],
        additional: "Se o problema persistir, considere substituição do componente.",
        confidence: "70%",
        sentiment: "Preocupado",
        estimatedTime: "15-30 minutos",
        priority: "Média"
      },
      software: {
        analysis: "Problema de software detectado. Verificação de configurações e atualizações necessária.",
        steps: [
          "Verificar se o software está atualizado",
          "Limpar cache e dados temporários",
          "Reinstalar o software se necessário"
        ],
        additional: "Verifique os logs de erro para mais detalhes.",
        confidence: "75%",
        sentiment: "Frustrado",
        estimatedTime: "20-45 minutos",
        priority: "Média"
      },
      network: {
        analysis: "Problema de conectividade identificado. Verificação de rede e configurações necessária.",
        steps: [
          "Verificar conexão física (cabo/Wi-Fi)",
          "Reiniciar roteador e dispositivo",
          "Verificar configurações de IP e DNS"
        ],
        additional: "Teste a conectividade com outros dispositivos.",
        confidence: "85%",
        sentiment: "Irritado",
        estimatedTime: "10-25 minutos",
        priority: "Alta"
      },
      printer: {
        analysis: "Problema com impressora identificado. Verificação de hardware e drivers necessária.",
        steps: [
          "Verificar papel na bandeja e possíveis atolamentos",
          "Verificar níveis de tinta/toner",
          "Reinstalar drivers da impressora"
        ],
        additional: "Execute uma página de teste após as correções.",
        confidence: "80%",
        sentiment: "Impaciente",
        estimatedTime: "15-30 minutos",
        priority: "Média"
      },
      email: {
        analysis: "Problema com email identificado. Verificação de configurações e conectividade necessária.",
        steps: [
          "Verificar configurações do servidor (IMAP/POP3, SMTP)",
          "Testar conectividade com a internet",
          "Verificar filtros e capacidade da caixa de entrada"
        ],
        additional: "Confirme as credenciais de login com o usuário.",
        confidence: "75%",
        sentiment: "Incomodado",
        estimatedTime: "20-40 minutos",
        priority: "Média"
      },
      password: {
        analysis: "Solicitação de reset de senha. Processo de redefinição segura necessário.",
        steps: [
          "Verificar identidade do usuário de forma segura",
          "Gerar nova senha temporária",
          "Orientar alteração da senha no primeiro login"
        ],
        additional: "Reforçar políticas de senhas seguras.",
        confidence: "100%",
        sentiment: "Urgente",
        estimatedTime: "5-15 minutos",
        priority: "Alta"
      },
      access: {
        analysis: "Solicitação de acesso identificada. Processo de concessão de permissões necessário.",
        steps: [
          "Verificar necessidade e aprovação da solicitação",
          "Configurar permissões no sistema",
          "Confirmar funcionamento do acesso"
        ],
        additional: "Documentar concessão para auditoria.",
        confidence: "90%",
        sentiment: "Expectante",
        estimatedTime: "10-20 minutos",
        priority: "Média"
      },
      other: {
        analysis: "Problema não categorizado identificado. Análise mais detalhada necessária.",
        steps: [
          "Coletar informações detalhadas do usuário",
          "Consultar base de conhecimento",
          "Escalar para especialista se necessário"
        ],
        additional: "Manter usuário informado sobre o progresso.",
        confidence: "60%",
        sentiment: "Curioso",
        estimatedTime: "30-60 minutos",
        priority: "Média"
      }
    };

    return fallbackSuggestions[problemType] || fallbackSuggestions.other;
  }

  // Gerar resposta automática para técnico baseada na sugestão
  generateTechnicianResponse(suggestion, problemType) {
    const responseTemplates = {
      hardware: `Identifiquei o problema de hardware relatado. ${suggestion.steps.slice(0, 2).join(' ')} Problema resolvido com sucesso.`,
      software: `Analisei o problema de software. ${suggestion.steps.slice(0, 2).join(' ')} Aplicação funcionando normalmente.`,
      network: `Verifiquei a conectividade de rede. ${suggestion.steps.slice(0, 2).join(' ')} Conexão restabelecida.`,
      printer: `Resolvi o problema da impressora. ${suggestion.steps.slice(0, 2).join(' ')} Impressão funcionando corretamente.`,
      email: `Corrigi as configurações de email. ${suggestion.steps.slice(0, 2).join(' ')} Serviço de email operacional.`,
      password: `Reset de senha realizado com sucesso. ${suggestion.steps.slice(0, 2).join(' ')} Usuário pode fazer login normalmente.`,
      access: `Solicitação de acesso processada. ${suggestion.steps.slice(0, 2).join(' ')} Permissões configuradas corretamente.`,
      other: `Problema analisado e resolvido. ${suggestion.steps.slice(0, 2).join(' ')} Situação normalizada.`,
    };

    return responseTemplates[problemType] || responseTemplates.other;
  }
}

export default new GeminiService();
