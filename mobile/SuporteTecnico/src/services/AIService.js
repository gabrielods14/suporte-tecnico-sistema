import { Platform } from 'react-native';

// URL base do backend Flask (mesma estrutura do sistema web)
// Configuração: A URL pode ser definida via variável de ambiente ou usar valores padrão
// Em desenvolvimento Android: usar o IP da máquina (ex: http://192.168.1.100:5000)
// Em produção: URL do servidor Flask hospedado
// 
// IMPORTANTE: Para Android, localhost não funciona. Use o IP da sua máquina:
// - Windows: ipconfig (IPv4)
// - macOS/Linux: ifconfig ou ip addr
// - Exemplo: http://192.168.1.100:5000

const getFlaskApiUrl = () => {
  // Tentar usar variável de ambiente se disponível
  if (typeof process !== 'undefined' && process.env && process.env.FLASK_API_URL) {
    return process.env.FLASK_API_URL;
  }
  
  // Em desenvolvimento, usar IP da máquina para Android ou localhost para iOS
  if (__DEV__) {
    // IP da máquina detectado automaticamente (192.168.15.118)
    // Para Android: usar IP da máquina (localhost não funciona)
    // Para iOS: pode usar localhost ou IP da máquina
    const MACHINE_IP = '192.168.15.118'; // IP da máquina local
    
    // Detectar plataforma (Android ou iOS)
    if (Platform.OS === 'android') {
      // Android precisa do IP da máquina
      return `http://${MACHINE_IP}:5000`;
    } else {
      // iOS pode usar localhost
      return 'http://localhost:5000';
    }
  }
  
  // URL de produção (ajustar conforme necessário)
  return 'https://seu-backend-flask.herokuapp.com';
};

const FLASK_API_BASE_URL = getFlaskApiUrl();

const AIService = {
  // Obter sugestão usando o endpoint do backend Flask (mesmo do sistema web)
  getSuggestion: async (problemType, description, userContext = '') => {
    try {
      console.log('=== AIService: Iniciando busca de sugestão via Flask API ===');
      console.log('Tipo:', problemType);
      console.log('Descrição:', description);
      console.log('Contexto:', userContext);

      // Preparar dados no formato esperado pelo endpoint Flask
      const titulo = `${problemType} - ${description.substring(0, 50)}...`;
      const descricaoCompleta = description + (userContext ? `\n\nContexto: ${userContext}` : '');

      // Chamar endpoint do Flask (mesmo do sistema web)
      const response = await fetch(`${FLASK_API_BASE_URL}/api/gemini/sugerir-resposta`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          titulo: titulo,
          descricao: descricaoCompleta,
        }),
      });

      console.log('Status da resposta Flask:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.log('Erro da API Flask:', errorText);
        throw new Error(`Erro ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      console.log('Resposta do Flask:', data);

      // A API Flask retorna { "sugestao": "texto da sugestão" }
      const sugestaoTexto = data.sugestao || data.sugestao_texto || '';

      if (!sugestaoTexto) {
        throw new Error('Resposta vazia do serviço de IA');
      }

      // Converter a resposta de texto para o formato estruturado esperado pelo mobile
      const suggestion = AIService.parseSuggestionText(sugestaoTexto, problemType, description);

      console.log('=== AIService: Sugestão obtida com sucesso ===');
      console.log('Sugestão:', suggestion);

      return suggestion;

    } catch (error) {
      console.log('=== AIService: Erro ao obter sugestão ===');
      console.log('Erro:', error.message);

      // Fallback para sugestão básica em caso de erro
      return AIService.getFallbackSuggestion(problemType, description);
    }
  },

  // Converter texto da sugestão para formato estruturado
  parseSuggestionText: (text, problemType, description) => {
    // Tentar extrair estrutura JSON se o texto contiver JSON
    try {
      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        if (parsed.analysis || parsed.steps) {
          return {
            analysis: parsed.analysis || text,
            steps: parsed.steps || parsed.stepByStepSolution || [],
            stepByStepSolution: parsed.stepByStepSolution || parsed.steps || [],
            specificCommands: parsed.specificCommands || [],
            rootCause: parsed.rootCause || '',
            symptoms: parsed.symptoms || [],
            additional: parsed.additional || parsed.additionalInfo || '',
            verificationSteps: parsed.verificationSteps || [],
            confidence: parsed.confidence || '75%',
            estimatedTime: parsed.estimatedTime || '20-30 minutos',
            priority: parsed.priority || 'Média',
            sentiment: parsed.sentiment || 'Neutro',
          };
        }
      }
    } catch (e) {
      console.log('Erro ao parsear JSON da sugestão, usando texto direto');
    }

    // Se não conseguir parsear JSON, usar o texto completo como análise detalhada
    // O prompt foi melhorado para gerar texto corrido e detalhado
    const textCleaned = text.trim();
    
    // Tentar extrair informações estruturadas do texto
    const lines = textCleaned.split('\n').filter(line => line.trim());
    
    // Extrair comandos mencionados (linhas que contêm comandos comuns)
    const commands = [];
    const steps = [];
    const verificationSteps = [];
    
    lines.forEach(line => {
      const lowerLine = line.toLowerCase();
      // Detectar comandos (contêm palavras-chave como "executado", "comando", "run", etc.)
      if (lowerLine.includes('comando') || lowerLine.includes('executado') || 
          lowerLine.includes('run') || lowerLine.includes('cmd') ||
          lowerLine.match(/^[a-z]+\s+[a-z-]+/i)) {
        commands.push(line.trim());
      }
      // Detectar passos (numerados ou com marcadores)
      if (line.match(/^\d+[\.\)]\s+/) || line.match(/^[-•]\s+/)) {
        steps.push(line.replace(/^[\d\.\)\-\•\s]+/, '').trim());
      }
      // Detectar verificações
      if (lowerLine.includes('verificado') || lowerLine.includes('verificação') ||
          lowerLine.includes('testado') || lowerLine.includes('confirmado')) {
        verificationSteps.push(line.trim());
      }
    });
    
    return {
      // Usar o texto completo como análise detalhada (o prompt foi melhorado)
      analysis: textCleaned.length > 100 ? textCleaned : (textCleaned || 'Análise técnica detalhada do problema realizada.'),
      steps: steps.length > 0 ? steps : (lines.slice(0, 5).filter(line => line.trim()) || []),
      stepByStepSolution: steps.length > 0 ? steps : (lines.slice(0, 5).filter(line => line.trim()) || []),
      specificCommands: commands.length > 0 ? commands : [],
      rootCause: '',
      symptoms: [],
      verificationSteps: verificationSteps.length > 0 ? verificationSteps : [],
      additional: '',
      confidence: '75%',
      estimatedTime: '20-30 minutos',
      priority: 'Média',
      sentiment: 'Neutro',
    };
  },

  // Gerar resposta automática para técnico baseada na sugestão
  generateAutoResponse: (suggestion, ticket) => {
    // Se a sugestão contém texto direto da IA (análise detalhada), usar ele como base principal
    // O prompt foi melhorado para gerar texto corrido e detalhado
    if (suggestion.analysis && suggestion.analysis.length > 100) {
      // A análise já contém o texto completo e detalhado da IA
      // Usar como resposta principal, pois contém toda a rastreabilidade
      let response = suggestion.analysis;
      
      // Se a análise não for muito longa, adicionar informações complementares estruturadas
      if (suggestion.analysis.length < 500) {
        // Adicionar passo-a-passo se disponível e não já incluído na análise
        if (suggestion.stepByStepSolution && suggestion.stepByStepSolution.length > 0) {
          response += `\n\nAÇÕES DETALHADAS REALIZADAS:\n`;
          suggestion.stepByStepSolution.forEach((step, index) => {
            if (!suggestion.analysis.includes(step.substring(0, 30))) {
              response += `${index + 1}. ${step}\n`;
            }
          });
        }
        
        // Adicionar comandos executados se não já mencionados
        if (suggestion.specificCommands && suggestion.specificCommands.length > 0) {
          response += `\nCOMANDOS EXECUTADOS:\n`;
          suggestion.specificCommands.forEach((cmd) => {
            if (!suggestion.analysis.includes(cmd.substring(0, 20))) {
              response += `- ${cmd}\n`;
            }
          });
        }
        
        // Adicionar verificação final se não já mencionada
        if (suggestion.verificationSteps && suggestion.verificationSteps.length > 0) {
          response += `\nVERIFICAÇÕES REALIZADAS:\n`;
          suggestion.verificationSteps.forEach((step) => {
            if (!suggestion.analysis.includes(step.substring(0, 30))) {
              response += `- ${step}\n`;
            }
          });
        }
      }
      
      // Garantir que termina com status
      if (!response.toLowerCase().includes('resolvido') && !response.toLowerCase().includes('sucesso')) {
        response += '\n\nSTATUS: Problema resolvido com sucesso.';
      }
      
      return response;
    }
    
    // Fallback: criar resposta estruturada mesmo sem análise detalhada
    if (!suggestion || !suggestion.stepByStepSolution) {
      return 'Problema analisado e solução técnica aplicada com sucesso.';
    }

    // Construir resposta detalhada com todas as informações disponíveis
    let response = 'RESOLUÇÃO DO CHAMADO\n\n';
    
    // Análise inicial
    if (suggestion.analysis) {
      response += `ANÁLISE INICIAL:\n${suggestion.analysis}\n\n`;
    }
    
    // Causa raiz
    if (suggestion.rootCause) {
      response += `CAUSA RAIZ IDENTIFICADA:\n${suggestion.rootCause}\n\n`;
    }
    
    // Sintomas identificados
    if (suggestion.symptoms && suggestion.symptoms.length > 0) {
      response += `SINTOMAS IDENTIFICADOS:\n`;
      suggestion.symptoms.forEach((symptom, index) => {
        response += `${index + 1}. ${symptom}\n`;
      });
      response += '\n';
    }
    
    // Ações realizadas (passo-a-passo)
    if (suggestion.stepByStepSolution && suggestion.stepByStepSolution.length > 0) {
      response += `AÇÕES REALIZADAS:\n`;
      suggestion.stepByStepSolution.forEach((step, index) => {
        response += `${index + 1}. ${step}\n`;
      });
      response += '\n';
    }
    
    // Comandos executados
    if (suggestion.specificCommands && suggestion.specificCommands.length > 0) {
      response += `COMANDOS EXECUTADOS:\n`;
      suggestion.specificCommands.forEach((cmd, index) => {
        response += `- ${cmd}\n`;
      });
      response += '\n';
    }
    
    // Verificação final
    if (suggestion.verificationSteps && suggestion.verificationSteps.length > 0) {
      response += `VERIFICAÇÃO FINAL:\n`;
      suggestion.verificationSteps.forEach((step, index) => {
        response += `- ${step}\n`;
      });
      response += '\n';
    }
    
    // Informações adicionais
    if (suggestion.additional) {
      response += `INFORMAÇÕES ADICIONAIS:\n${suggestion.additional}\n\n`;
    }
    
    response += 'STATUS: Problema resolvido com sucesso.';
    return response;
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
          analysis: `ANÁLISE INICIAL: Identifiquei um problema relacionado a componentes físicos do equipamento. Realizei uma inspeção visual completa dos componentes e verificações de conexão. DIAGNÓSTICO: Executei verificações de conexão física de todos os cabos (energia, dados, periféricos). Testei a alimentação elétrica e verifiquei indicadores LED. AÇÕES REALIZADAS: 1) Verifiquei e reconectei todos os cabos de energia e dados; 2) Realizei reinicialização completa do equipamento (desligamento completo por 30 segundos); 3) Executei diagnóstico de hardware integrado do sistema operacional; 4) Verifiquei temperatura e ventilação dos componentes. VERIFICAÇÃO: Testei o funcionamento após as correções e confirmei que o problema foi resolvido.`,
          steps: [
            "Verifiquei e reconectei todos os cabos de energia e dados",
            "Realizei reinicialização completa do equipamento (desligamento por 30 segundos)",
            "Executei diagnóstico de hardware integrado do sistema operacional",
            "Verifiquei temperatura e ventilação dos componentes"
          ],
          stepByStepSolution: [
            "Verifiquei e reconectei todos os cabos de energia e dados",
            "Realizei reinicialização completa do equipamento (desligamento por 30 segundos)",
            "Executei diagnóstico de hardware integrado do sistema operacional",
            "Verifiquei temperatura e ventilação dos componentes"
          ],
          specificCommands: [
            "Verificação visual de conexões físicas",
            "Diagnóstico de hardware: verificação de componentes"
          ],
          verificationSteps: [
            "Teste de funcionamento do equipamento após correções",
            "Verificação de indicadores LED e status do sistema"
          ],
          additional: "Se o problema persistir, recomendo substituição do componente defeituoso após análise técnica adicional.",
          confidence: "90%",
          sentiment: "Preocupado",
          estimatedTime: "15-30 minutos",
          priority: "Média"
        };
        break;
      case 'software':
        suggestion = {
          analysis: `ANÁLISE INICIAL: Identifiquei uma falha ou mau funcionamento relacionado a aplicativo ou sistema operacional. Realizei análise dos sintomas reportados e verificação de logs do sistema. DIAGNÓSTICO: Consultei os logs de erro do sistema em /var/log/syslog (Linux) ou Visualizador de Eventos (Windows). Verifiquei a versão atual do software e comparei com a versão mais recente disponível. AÇÕES REALIZADAS: 1) Verifiquei e atualizei o software para a versão mais recente disponível; 2) Limpei o cache e dados temporários do aplicativo (limpeza de cache e arquivos temporários); 3) Verifiquei dependências e bibliotecas necessárias; 4) Reinstalei o software após desinstalação completa. VERIFICAÇÃO: Testei o funcionamento do aplicativo após as correções e confirmei que o problema foi resolvido.`,
          steps: [
            "Verifiquei e atualizei o software para a versão mais recente disponível",
            "Limpei o cache e dados temporários do aplicativo",
            "Verifiquei dependências e bibliotecas necessárias",
            "Reinstalei o software após desinstalação completa"
          ],
          stepByStepSolution: [
            "Verifiquei e atualizei o software para a versão mais recente disponível",
            "Limpei o cache e dados temporários do aplicativo",
            "Verifiquei dependências e bibliotecas necessárias",
            "Reinstalei o software após desinstalação completa"
          ],
          specificCommands: [
            "Verificação de versão: verificação de atualizações disponíveis",
            "Limpeza de cache: remoção de arquivos temporários"
          ],
          verificationSteps: [
            "Teste de funcionamento do aplicativo após atualização",
            "Verificação de logs para confirmar ausência de erros"
          ],
          additional: "Monitorei os logs de erro do sistema para identificar e documentar a causa raiz do problema.",
          confidence: "85%",
          sentiment: "Frustrado",
          estimatedTime: "20-45 minutos",
          priority: "Média"
        };
        break;
      case 'network':
        suggestion = {
          analysis: `ANÁLISE INICIAL: Identifiquei problemas de conectividade de rede. Realizei diagnóstico completo da conexão de rede. DIAGNÓSTICO: Executei testes de conectividade (ping para gateway e DNS). Verifiquei status da conexão física (cabo de rede ou Wi-Fi). Consultei configurações de rede do sistema. AÇÕES REALIZADAS: 1) Verifiquei conexão física do cabo de rede e status do Wi-Fi (verificação de indicadores); 2) Reiniciei o roteador/modem e aguardei 60 segundos antes de reconectar; 3) Reiniciei o computador/dispositivo para renovar configurações de rede; 4) Verifiquei e corrigi configurações de IP (DHCP ativado ou IP estático configurado corretamente); 5) Verifiquei e atualizei configurações de DNS (usando DNS públicos como 8.8.8.8 e 8.8.4.4). VERIFICAÇÃO: Executei ping para verificar conectividade (ping bem-sucedido). Testei acesso a sites e serviços de rede. Confirmei que o problema foi resolvido.`,
          steps: [
            "Verifiquei conexão física do cabo de rede e status do Wi-Fi",
            "Reiniciei o roteador/modem e aguardei 60 segundos",
            "Reiniciei o computador/dispositivo para renewar configurações",
            "Verifiquei e corrigi configurações de IP (DHCP/IP estático)",
            "Verifiquei e atualizei configurações de DNS"
          ],
          stepByStepSolution: [
            "Verifiquei conexão física do cabo de rede e status do Wi-Fi",
            "Reiniciei o roteador/modem e aguardei 60 segundos",
            "Reiniciei o computador/dispositivo para renewar configurações",
            "Verifiquei e corrigi configurações de IP (DHCP/IP estático)",
            "Verifiquei e atualizei configurações de DNS"
          ],
          specificCommands: [
            "ping 8.8.8.8 - teste de conectividade",
            "ipconfig /flushdns - limpeza de cache DNS (Windows)",
            "ipconfig /renew - renovação de configurações IP"
          ],
          verificationSteps: [
            "Teste de ping para gateway e DNS: conectividade confirmada",
            "Teste de acesso a sites web: acesso funcionando normalmente"
          ],
          additional: "Testei a conectividade com outros dispositivos na mesma rede para confirmar que o problema estava isolado.",
          confidence: "95%",
          sentiment: "Irritado",
          estimatedTime: "10-25 minutos",
          priority: "Alta"
        };
        break;
      case 'printer':
        suggestion = {
          analysis: `ANÁLISE INICIAL: Identifiquei problemas relacionados à impressora. Realizei diagnóstico completo do equipamento e configurações. DIAGNÓSTICO: Verifiquei status físico da impressora (papel, tinta, atolamentos). Consultei logs de impressão e fila de impressão do sistema. Verifiquei drivers instalados e versão. AÇÕES REALIZADAS: 1) Verifiquei e corrigi bandeja de papel (verificação de papel e remoção de possíveis atolamentos); 2) Verifiquei níveis de tinta/toner e substituí se necessário; 3) Limpei a fila de impressão (spooler) e removi trabalhos pendentes; 4) Reinstalei ou atualizei os drivers da impressora para a versão mais recente; 5) Reconectei a impressora ao sistema. VERIFICAÇÃO: Executei página de teste de impressão e confirmei que o problema foi resolvido. Testei impressão de documento de teste.`,
          steps: [
            "Verifiquei e corrigi bandeja de papel (remoção de atolamentos)",
            "Verifiquei níveis de tinta/toner e substituí se necessário",
            "Limpei a fila de impressão (spooler) e removi trabalhos pendentes",
            "Reinstalei ou atualizei os drivers da impressora",
            "Reconectei a impressora ao sistema"
          ],
          stepByStepSolution: [
            "Verifiquei e corrigi bandeja de papel (remoção de atolamentos)",
            "Verifiquei níveis de tinta/toner e substituí se necessário",
            "Limpei a fila de impressão (spooler) e removi trabalhos pendentes",
            "Reinstalei ou atualizei os drivers da impressora",
            "Reconectei a impressora ao sistema"
          ],
          specificCommands: [
            "Limpeza de spooler: net stop spooler / net start spooler (Windows)",
            "Verificação de drivers: verificação de versão e atualização"
          ],
          verificationSteps: [
            "Execução de página de teste de impressão: impressão bem-sucedida",
            "Teste de impressão de documento: funcionamento confirmado"
          ],
          additional: "Realizei limpeza completa da fila de impressão e verificação de conectividade da impressora.",
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