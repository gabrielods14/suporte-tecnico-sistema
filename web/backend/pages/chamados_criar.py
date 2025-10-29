from flask import request, jsonify
import requests

API_URL_BASE = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net'


def criar_chamado():
    dados = request.json or {}

    tipoChamado = dados.get('tipoChamado') or dados.get('tipo')
    titulo = dados.get('titulo')
    descricao = dados.get('descricao')
    prioridade = dados.get('prioridade', 'MÉDIA')

    if not tipoChamado or not titulo or not descricao:
        return jsonify({'message': 'Campos obrigatórios: tipoChamado, titulo e descricao.'}), 400

    payload_api = {
        'tipo': tipoChamado,
        'titulo': titulo,
        'descricao': descricao,
        'prioridade': prioridade,
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



