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
        
        prompt = f"""
        Você é um assistente técnico de TI especializado em gerar relatórios detalhados de atendimento técnico para rastreabilidade.

        CONTEXTO DO CHAMADO:
        - Título: "{titulo}"
        - Descrição do problema reportado: "{descricao}"
        
        OBJETIVO:
        Gere uma resposta técnica COMPLETA e DETALHADA que descreva TODAS as ações realizadas pelo técnico para resolver este problema.
        Esta resposta será registrada permanentemente no histórico do chamado e deve fornecer rastreabilidade completa.
        Outro técnico deve ser capaz de ler esta resposta e entender EXATAMENTE o que foi feito, como foi feito e por que foi feito.
        
        ESTRUTURA OBRIGATÓRIA DA RESPOSTA:
        
        1. ANÁLISE INICIAL DO PROBLEMA:
        - Descreva o problema identificado com base na descrição fornecida
        - Identifique os sintomas observados
        - Mencione possíveis causas iniciais consideradas
        
        2. PROCESSO DE DIAGNÓSTICO REALIZADO:
        - Liste TODAS as verificações realizadas (ex: "Verifiquei os logs do sistema em /var/log/app.log")
        - Mencione TODOS os testes executados (ex: "Executei ping para verificar conectividade de rede")
        - Descreva comandos ou ferramentas utilizadas para diagnóstico
        - Indique o que foi verificado e qual foi o resultado de cada verificação
        
        3. IDENTIFICAÇÃO DA CAUSA RAIZ:
        - Explique claramente qual foi a causa raiz identificada
        - Descreva como a causa foi identificada (através de qual verificação/teste)
        
        4. AÇÕES CORRETIVAS EXECUTADAS (Passo a Passo Detalhado):
        - Liste TODAS as ações realizadas em ordem cronológica
        - Para cada ação, seja ESPECÍFICO:
          * Se executou um comando, mencione o comando exato (ex: "Executei o comando: ipconfig /flushdns")
          * Se modificou configuração, mencione o arquivo/caminho e o que foi alterado
          * Se reiniciou um serviço, mencione qual serviço (ex: "Reiniciei o serviço spooler de impressão")
          * Se atualizou software, mencione a versão anterior e nova
          * Se fez backup, mencione onde foi salvo
        
        5. CONFIGURAÇÕES OU AJUSTES REALIZADOS:
        - Se houver configurações modificadas, detalhe exatamente o que foi alterado
        - Mencione valores anteriores e novos (quando aplicável)
        - Indique arquivos de configuração modificados com caminhos completos
        
        6. VERIFICAÇÃO E TESTES DE CONFIRMAÇÃO:
        - Descreva como foi verificado que o problema foi resolvido
        - Mencione testes realizados para confirmar a solução
        - Indique resultados dos testes (ex: "Teste de conectividade realizado com sucesso, ping retornou resposta em 10ms")
        
        7. RESULTADO FINAL:
        - Confirme que o problema foi resolvido
        - Mencione se há recomendações adicionais ou ações preventivas
        
        DIRETRIZES DE QUALIDADE:
        - Seja EXTREMAMENTE específico e detalhado
        - Use linguagem técnica profissional mas clara
        - Mencione comandos exatos, caminhos de arquivos, nomes de serviços, versões, etc.
        - Evite generalizações como "problema analisado" ou "solução aplicada"
        - Use tempo passado para descrever o que FOI FEITO (ex: "Executei", "Verifiquei", "Modifiquei")
        - A resposta deve ter no mínimo 150-200 palavras com detalhes técnicos específicos
        - Pense como se estivesse documentando para um relatório técnico formal
        
        FORMATO:
        Gere uma resposta em texto corrido, profissional, completa e bem estruturada que descreva TODO o processo de resolução do problema com máximo detalhamento técnico.
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
