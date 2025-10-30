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
        Você é um assistente técnico de TI.
        O técnico está respondendo a um chamado com o título: "{titulo}".
        Descrição do problema: "{descricao}".
        Gere uma sugestão de resposta técnica clara, profissional e útil para o técnico enviar ao cliente.
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
