from flask import Blueprint, request, jsonify
# Importa o serviço local de Gemini (em web/IAAPI/gemini_service.py)
from web.IAAPI.gemini_service import gerar_sugestao

gemini_bp = Blueprint('gemini', __name__)

@gemini_bp.route('/sugerir-resposta', methods=['POST'])
def sugerir_resposta():
    """
    Endpoint para gerar sugestão de resposta técnica usando Gemini AI.
    
    Espera um JSON com:
    - descricao (obrigatório): Descrição do problema do chamado
    - titulo (opcional): Título do chamado
    
    Retorna:
    - 200: {"sugestao": "texto da sugestão"}
    - 400: {"erro": "mensagem de erro"}
    - 500: {"erro": "mensagem de erro do servidor"}
    """
    try:
        # Valida se há dados JSON na requisição
        if not request.is_json:
            return jsonify({"erro": "Content-Type deve ser application/json"}), 400
        
        data = request.json
        if not data:
            return jsonify({"erro": "Corpo da requisição vazio"}), 400
        
        descricao = data.get('descricao', '').strip()
        titulo = data.get('titulo', '').strip()

        # Valida se a descrição foi fornecida
        if not descricao:
            return jsonify({"erro": "Descrição do chamado é obrigatória"}), 400

        # Gera a sugestão usando o Gemini AI
        sugestao = gerar_sugestao(titulo, descricao)
        
        return jsonify({"sugestao": sugestao}), 200

    except ValueError as e:
        # Erros de validação (ex: chave de API não configurada)
        error_msg = str(e)
        print(f"[GeminiController] Erro de validação: {error_msg}")
        if "GEMINI_API_KEY" in error_msg.upper():
            error_msg = "GEMINI_API_KEY não configurada. Configure a chave no arquivo .env ou env em web/backend/"
        return jsonify({"erro": error_msg}), 400
    except Exception as e:
        # Outros erros (ex: erro de comunicação com API)
        error_msg = str(e)
        print(f"[GeminiController] Erro ao processar solicitação: {error_msg}")
        import traceback
        print(f"[GeminiController] Traceback completo:")
        traceback.print_exc()
        if "GEMINI_API_KEY" in error_msg.upper() or "API key" in error_msg:
            error_msg = "GEMINI_API_KEY não configurada ou inválida. Execute: python configurar_chave_api.py ou configure manualmente no arquivo .env ou env em web/backend/"
        elif "modelo" in error_msg.lower() or "model" in error_msg.lower():
            error_msg = f"Erro ao acessar modelo do Gemini: {error_msg}"
        return jsonify({"erro": f"Erro ao processar solicitação: {error_msg}"}), 500
