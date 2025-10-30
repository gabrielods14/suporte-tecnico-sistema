import google.generativeai as genai
import os

# Configure sua chave de API do Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def gerar_sugestao(titulo, descricao):
    prompt = f"""
    Você é um assistente técnico de TI.
    O técnico está respondendo a um chamado com o título: "{titulo}".
    Descrição do problema: "{descricao}".
    Gere uma sugestão de resposta técnica clara, profissional e útil para o técnico enviar ao cliente.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text
