from flask import request, jsonify
from app import app
import requests

API_URL_BASE = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net'


@app.route('/chamados', methods=['POST'])
def criar_chamado():
    dados = request.json or {}

    tipo = dados.get('tipo')
    titulo = dados.get('titulo')
    descricao = dados.get('descricao')

    if not tipo or not titulo or not descricao:
        return jsonify({'message': 'Campos obrigatórios: tipo, titulo e descricao.'}), 400

    payload_api = {
        'tipo': tipo,
        'titulo': titulo,
        'descricao': descricao,
        'prioridade': dados.get('prioridade'),
        'anexos': dados.get('anexos'),
        'solicitanteId': dados.get('solicitanteId'),
    }
    payload_api = {k: v for k, v in payload_api.items() if v is not None}

    try:
        url = f"{API_URL_BASE}/api/Chamados"
        resp = requests.post(url, json=payload_api)
        if resp.status_code in [200, 201]:
            return jsonify(resp.json() if resp.content else {'message': 'Chamado criado com sucesso.'}), 201

        try:
            msg = resp.json().get('message', f'Erro HTTP {resp.status_code} ao criar chamado.')
        except Exception:
            msg = f'Erro HTTP {resp.status_code} ao criar chamado.'
        return jsonify({'message': msg}), resp.status_code

    except requests.exceptions.RequestException as e:
        print(f'Erro ao conectar à API externa: {e}')
        return jsonify({'message': 'Serviço de chamados indisponível.'}), 503



