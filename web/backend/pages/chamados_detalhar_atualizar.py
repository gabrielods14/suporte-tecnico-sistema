from flask import request, jsonify
from app import app
import requests

API_URL_BASE = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net'


@app.route('/chamados/<int:chamado_id>', methods=['GET'])
def detalhar_chamado(chamado_id: int):
    try:
        url = f"{API_URL_BASE}/api/Chamados/{chamado_id}"
        resp = requests.get(url)
        if resp.status_code == 200:
            return jsonify(resp.json())

        try:
            msg = resp.json().get('message', f'Erro HTTP {resp.status_code} ao buscar chamado {chamado_id}.')
        except Exception:
            msg = f'Erro HTTP {resp.status_code} ao buscar chamado {chamado_id}.'
        return jsonify({'message': msg}), resp.status_code

    except requests.exceptions.RequestException as e:
        print(f'Erro ao conectar à API externa: {e}')
        return jsonify({'message': 'Serviço de chamados indisponível.'}), 503


@app.route('/chamados/<int:chamado_id>', methods=['PUT'])
def atualizar_chamado(chamado_id: int):
    dados = request.json or {}

    payload_api = {
        'tipo': dados.get('tipo'),
        'titulo': dados.get('titulo'),
        'descricao': dados.get('descricao'),
        'prioridade': dados.get('prioridade'),
        'dataMaximaConclusao': dados.get('dataMaximaConclusao'),
        'emailContato': dados.get('emailContato'),
        'telefoneContato': dados.get('telefoneContato'),
        'sugestaoResolucao': dados.get('sugestaoResolucao'),
        'resolucao': dados.get('resolucao'),
        'status': dados.get('status')
    }
    payload_api = {k: v for k, v in payload_api.items() if v is not None}

    if not payload_api:
        return jsonify({'message': 'Nenhum campo para atualizar.'}), 400

    try:
        url = f"{API_URL_BASE}/api/Chamados/{chamado_id}"
        resp = requests.put(url, json=payload_api)
        if resp.status_code in [200, 204]:
            return jsonify(resp.json() if resp.content else {'message': 'Chamado atualizado com sucesso.'})

        try:
            msg = resp.json().get('message', f'Erro HTTP {resp.status_code} ao atualizar chamado {chamado_id}.')
        except Exception:
            msg = f'Erro HTTP {resp.status_code} ao atualizar chamado {chamado_id}.'
        return jsonify({'message': msg}), resp.status_code

    except requests.exceptions.RequestException as e:
        print(f'Erro ao conectar à API externa: {e}')
        return jsonify({'message': 'Serviço de chamados indisponível.'}), 503



