from flask import Blueprint, request, jsonify
# Importa o serviço local de Gemini (em web/IAAPI/gemini_service.py)
from web.IAAPI.gemini_service import gerar_sugestao

gemini_bp = Blueprint('gemini', __name__)

@gemini_bp.route('/sugerir-resposta', methods=['POST'])
def sugerir_resposta():
    try:
        data = request.json
        descricao = data.get('descricao', '')
        titulo = data.get('titulo', '')

        if not descricao:
            return jsonify({"erro": "Descrição do chamado é obrigatória"}), 400

        sugestao = gerar_sugestao(titulo, descricao)
        return jsonify({"sugestao": sugestao}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
