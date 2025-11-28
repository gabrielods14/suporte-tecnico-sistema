import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env no diretório do backend
# Procura o arquivo .env no diretório web/backend
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
env_path = os.path.join(backend_dir, '.env')
load_dotenv(dotenv_path=env_path)

# Configure sua chave de API do Gemini
api_key = os.getenv("GEMINI_API_KEY")

# Só configura o genai se a chave estiver disponível
# A validação acontece na função gerar_sugestao
if api_key:
    genai.configure(api_key=api_key)

def gerar_sugestao(titulo, descricao):
    """
    Gera uma sugestão de resposta técnica para um chamado usando o Gemini AI.
    
    Args:
        titulo (str): Título do chamado
        descricao (str): Descrição do problema
    
    Returns:
        str: Sugestão de resposta técnica gerada pelo Gemini
    
    Raises:
        ValueError: Se a chave de API não estiver configurada
        Exception: Se houver erro na comunicação com a API do Gemini
    """
    try:
        # Recarrega variáveis de ambiente do arquivo .env
        backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
        env_path = os.path.join(backend_dir, '.env')
        load_dotenv(dotenv_path=env_path, override=True)
        current_api_key = os.getenv("GEMINI_API_KEY")
        
        if not current_api_key:
            raise ValueError("GEMINI_API_KEY não configurada. Configure no arquivo .env em web/backend/.env ou execute: python configurar_chave_api.py")
        
        # Configura o genai com a chave atual (se ainda não foi configurado)
        if current_api_key != api_key:
            genai.configure(api_key=current_api_key)
        
        # Detectar tipo de problema baseado no título e descrição
        titulo_lower = titulo.lower() if titulo else ""
        descricao_lower = descricao.lower() if descricao else ""
        
        # Identificar tipo de problema
        is_password_reset = any(palavra in titulo_lower + " " + descricao_lower for palavra in 
                               ['senha', 'password', 'reset', 'redefinir', 'esqueci', 'esqueceu', 'perdeu'])
        is_access_request = any(palavra in titulo_lower + " " + descricao_lower for palavra in 
                               ['acesso', 'permissão', 'permissao', 'autorização', 'autorizacao'])
        is_hardware = any(palavra in titulo_lower + " " + descricao_lower for palavra in 
                         ['hardware', 'equipamento', 'computador', 'notebook', 'mouse', 'teclado', 'monitor'])
        is_network = any(palavra in titulo_lower + " " + descricao_lower for palavra in 
                        ['rede', 'network', 'internet', 'wifi', 'wi-fi', 'conexão', 'conexao', 'dns'])
        is_software = any(palavra in titulo_lower + " " + descricao_lower for palavra in 
                         ['software', 'aplicativo', 'programa', 'sistema', 'erro', 'bug'])
        is_printer = any(palavra in titulo_lower + " " + descricao_lower for palavra in 
                        ['impressora', 'printer', 'impressão', 'impressao'])
        is_email = any(palavra in titulo_lower + " " + descricao_lower for palavra in 
                      ['email', 'e-mail', 'correio', 'outlook', 'gmail'])
        
        # Prompt base
        prompt_base = f"""
        Você é um assistente técnico de TI especializado em gerar relatórios detalhados de atendimento técnico para rastreabilidade.

        CONTEXTO DO CHAMADO:
        - Título: "{titulo}"
        - Descrição do problema reportado: "{descricao}"
        """
        
        # Adicionar instruções específicas baseadas no tipo de problema
        if is_password_reset:
            prompt_base += """
        
        TIPO DE PROBLEMA IDENTIFICADO: RESET/REDEFINIÇÃO DE SENHA
        
        INSTRUÇÕES ESPECÍFICAS PARA RESET DE SENHA:
        Você deve gerar uma resposta detalhada que descreva o processo completo de reset de senha, incluindo:
        
        1. VERIFICAÇÃO DE IDENTIDADE:
        - Descreva como foi verificada a identidade do usuário (ex: "Verifiquei a identidade do usuário através de confirmação de dados cadastrais: nome completo, CPF, e-mail corporativo e departamento")
        - Mencione quais informações foram confirmadas para garantir segurança
        - Indique se houve verificação com superior hierárquico ou administrador
        
        2. PROCESSO DE RESET DE SENHA:
        - Descreva EXATAMENTE como a senha foi redefinida:
          * Se foi através de sistema administrativo, mencione qual sistema (ex: "Acessei o painel administrativo do Active Directory")
          * Se foi através de comando, mencione o comando exato (ex: "Executei o comando: net user [usuario] [nova_senha]")
          * Se foi através de interface web, mencione a URL e os passos (ex: "Acessei o portal de gestão de usuários em https://admin.empresa.com/usuarios")
        - Mencione se foi gerada uma senha temporária ou se o usuário escolheu a nova senha
        - Indique o comprimento e complexidade da senha gerada (se aplicável)
        
        3. COMUNICAÇÃO COM O USUÁRIO:
        - Descreva como a nova senha foi comunicada ao usuário (ex: "Enviei a senha temporária através de e-mail corporativo seguro para [email]")
        - Mencione instruções fornecidas ao usuário (ex: "Orientei o usuário a alterar a senha temporária no primeiro login e a criar uma senha forte seguindo a política de segurança")
        - Indique se foi solicitado que o usuário confirme o recebimento
        
        4. POLÍTICAS DE SEGURANÇA APLICADAS:
        - Mencione se a senha temporária expira após determinado tempo (ex: "A senha temporária foi configurada para expirar em 24 horas")
        - Descreva requisitos de complexidade aplicados (ex: "A nova senha deve conter no mínimo 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais")
        - Indique se foi necessário desbloquear a conta antes do reset
        
        5. REGISTRO E AUDITORIA:
        - Mencione que o reset foi registrado no sistema de auditoria
        - Indique data e hora do reset
        - Descreva quem autorizou o reset (se necessário)
        
        6. ORIENTAÇÕES FINAIS FORNECIDAS:
        - Liste todas as orientações dadas ao usuário sobre:
          * Como fazer login com a nova senha
          * Importância de alterar a senha temporária
          * Boas práticas de segurança de senha
          * O que fazer em caso de problemas no login
        
        7. CONFIRMAÇÃO DE RESOLUÇÃO:
        - Confirme que o reset foi realizado com sucesso
        - Mencione se o usuário conseguiu fazer login após o reset
        - Indique se há pendências ou próximos passos
        
        IMPORTANTE: Para reset de senha, seja MUITO específico sobre o processo de verificação de identidade, o método usado para redefinir a senha, e como a nova senha foi comunicada ao usuário. Isso é crítico para segurança e auditoria.
        """
        elif is_access_request:
            prompt_base += """
        
        TIPO DE PROBLEMA IDENTIFICADO: SOLICITAÇÃO DE ACESSO/PERMISSÃO
        
        INSTRUÇÕES ESPECÍFICAS PARA SOLICITAÇÃO DE ACESSO:
        Você deve gerar uma resposta detalhada que descreva o processo completo de concessão de acesso, incluindo:
        
        1. VERIFICAÇÃO DE NECESSIDADE E AUTORIZAÇÃO:
        - Descreva como foi verificada a necessidade do acesso solicitado
        - Mencione quem autorizou o acesso (superior hierárquico, gestor, etc.)
        - Indique se houve análise de perfil de cargo e responsabilidades
        
        2. PROCESSO DE CONCESSÃO DE ACESSO:
        - Descreva EXATAMENTE como o acesso foi concedido:
          * Sistema ou recurso ao qual o acesso foi concedido (ex: "Concedi acesso ao sistema ERP no módulo de Vendas")
          * Nível de permissão concedido (ex: "Acesso concedido com permissão de leitura e escrita, sem permissão de exclusão")
          * Grupo de segurança ou role atribuído (ex: "Usuário adicionado ao grupo 'Vendedores' no Active Directory")
        - Mencione comandos ou interfaces utilizadas (ex: "Através do painel administrativo, adicionei o usuário ao grupo 'SG_Vendas_RW'")
        
        3. CONFIGURAÇÕES ESPECÍFICAS:
        - Liste todas as permissões específicas concedidas
        - Mencione restrições ou limitações aplicadas
        - Indique se há horários ou locais específicos para o acesso
        
        4. TESTE E VERIFICAÇÃO:
        - Descreva como foi verificado que o acesso está funcionando
        - Mencione testes realizados (ex: "Solicitei que o usuário fizesse login e testasse o acesso ao módulo solicitado")
        - Confirme que o usuário conseguiu acessar os recursos necessários
        
        5. DOCUMENTAÇÃO E AUDITORIA:
        - Mencione que o acesso foi documentado no sistema de auditoria
        - Indique data de concessão e data de revisão (se aplicável)
        - Descreva quem autorizou e quem executou a concessão
        
        6. ORIENTAÇÕES FORNECIDAS:
        - Liste orientações dadas ao usuário sobre como usar o acesso
        - Mencione políticas de uso e responsabilidades
        - Indique recursos de treinamento ou documentação fornecidos
        """
        else:
            # Prompt genérico melhorado para outros tipos de problemas
            prompt_base += """
        
        OBJETIVO:
        Gere uma resposta técnica COMPLETA e DETALHADA que descreva TODAS as ações realizadas pelo técnico para resolver este problema.
        Esta resposta será registrada permanentemente no histórico do chamado e deve fornecer rastreabilidade completa.
        Outro técnico deve ser capaz de ler esta resposta e entender EXATAMENTE o que foi feito, como foi feito e por que foi feito.
        """
        
        # Adicionar estrutura comum
        prompt = prompt_base + """
        
        ESTRUTURA OBRIGATÓRIA DA RESPOSTA:
        
        1. ANÁLISE INICIAL DO PROBLEMA:
        - Descreva o problema identificado com base na descrição fornecida
        - Identifique os sintomas observados de forma específica
        - Mencione possíveis causas iniciais consideradas e por que foram consideradas
        
        2. PROCESSO DE DIAGNÓSTICO REALIZADO:
        - Liste TODAS as verificações realizadas com resultados específicos (ex: "Verifiquei os logs do sistema em /var/log/app.log e identifiquei o erro 'Connection timeout' na linha 1247 às 14:32")
        - Mencione TODOS os testes executados com resultados (ex: "Executei ping para google.com e obtive resposta em 15ms, confirmando conectividade básica")
        - Descreva comandos ou ferramentas utilizadas para diagnóstico com saídas relevantes
        - Indique o que foi verificado e qual foi o resultado específico de cada verificação
        
        3. IDENTIFICAÇÃO DA CAUSA RAIZ:
        - Explique claramente qual foi a causa raiz identificada
        - Descreva como a causa foi identificada (através de qual verificação/teste específico)
        - Mencione por que outras causas foram descartadas
        
        4. AÇÕES CORRETIVAS EXECUTADAS (Passo a Passo Detalhado):
        - Liste TODAS as ações realizadas em ordem cronológica com detalhes específicos
        - Para cada ação, seja EXTREMAMENTE ESPECÍFICO:
          * Se executou um comando, mencione o comando exato com parâmetros (ex: "Executei o comando: ipconfig /flushdns no PowerShell como administrador")
          * Se modificou configuração, mencione o arquivo/caminho completo e o que foi alterado (ex: "Modifiquei o arquivo /etc/resolv.conf, alterando o DNS de 8.8.8.8 para 1.1.1.1")
          * Se reiniciou um serviço, mencione qual serviço e como (ex: "Reiniciei o serviço 'Spooler' através do comando: net stop spooler && net start spooler")
          * Se atualizou software, mencione a versão anterior e nova (ex: "Atualizei o driver da impressora HP LaserJet de versão 2.5.3 para 2.7.1")
          * Se fez backup, mencione onde foi salvo (ex: "Realizei backup do arquivo de configuração em C:\\Backups\\config_backup_20250115_1430.bak")
        
        5. CONFIGURAÇÕES OU AJUSTES REALIZADOS:
        - Se houver configurações modificadas, detalhe exatamente o que foi alterado
        - Mencione valores anteriores e novos com precisão (ex: "Alterei o timeout de conexão de 30 segundos para 60 segundos no arquivo config.ini")
        - Indique arquivos de configuração modificados com caminhos completos
        - Mencione se foram feitos backups antes das alterações
        
        6. VERIFICAÇÃO E TESTES DE CONFIRMAÇÃO:
        - Descreva como foi verificado que o problema foi resolvido com resultados específicos
        - Mencione testes realizados para confirmar a solução (ex: "Teste de conectividade realizado com sucesso: ping para 8.8.8.8 retornou resposta em 10ms, confirmando que o problema de DNS foi resolvido")
        - Indique resultados dos testes de forma quantitativa quando possível
        - Mencione se o usuário testou e confirmou a resolução
        
        7. RESULTADO FINAL:
        - Confirme que o problema foi resolvido de forma definitiva
        - Mencione se há recomendações adicionais ou ações preventivas
        - Indique se há necessidade de monitoramento adicional
        
        DIRETRIZES DE QUALIDADE:
        - Seja EXTREMAMENTE específico e detalhado - evite generalizações
        - Use linguagem técnica profissional mas clara
        - Mencione comandos exatos, caminhos de arquivos, nomes de serviços, versões, IPs, etc.
        - Evite frases genéricas como "problema analisado" ou "solução aplicada" - seja específico
        - Use tempo passado para descrever o que FOI FEITO (ex: "Executei", "Verifiquei", "Modifiquei", "Testei")
        - A resposta deve ter no mínimo 200-300 palavras com detalhes técnicos específicos e acionáveis
        - Pense como se estivesse documentando para um relatório técnico formal que será auditado
        - Inclua informações que permitam a outro técnico replicar ou entender completamente o que foi feito
        
        FORMATO:
        Gere uma resposta em texto corrido, profissional, completa e bem estruturada que descreva TODO o processo de resolução do problema com máximo detalhamento técnico e rastreabilidade.
        """

        # Usa um modelo estável disponível (gemini-2.0-flash ou gemini-flash-latest)
        # Estes são modelos estáveis e rápidos disponíveis na API
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
        except:
            # Fallback para modelo alternativo
            model = genai.GenerativeModel("gemini-flash-latest")
        response = model.generate_content(prompt)

        if not response or not response.text:
            raise Exception("Resposta vazia do Gemini API")

        return response.text
    
    except Exception as e:
        raise Exception(f"Erro ao gerar sugestão com Gemini: {str(e)}")
