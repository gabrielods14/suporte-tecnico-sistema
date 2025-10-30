from flask import request, jsonify
from app import app
import requests

API_URL_BASE = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net'


def detalhar_chamado(chamado_id: int):
    # Tratamento para requisições OPTIONS (CORS preflight)
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, OPTIONS')
        return response
    
    # Rota GET - Buscar chamado por ID
    if request.method == 'GET':
        try:
            url = f"{API_URL_BASE}/api/Chamados/{chamado_id}"
            headers = { 'Accept': 'application/json' }
            auth = request.headers.get('Authorization')
            if auth:
                headers['Authorization'] = auth
            resp = requests.get(url, headers=headers)
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
    
    # Rota PUT - Atualizar chamado
    if request.method == 'PUT':
        dados = request.json or {}

        payload_api = {
            'status': dados.get('status'),
            'tecnicoResponsavelId': dados.get('tecnicoResponsavelId'),
            'dataFechamento': dados.get('dataFechamento'),
            'titulo': dados.get('titulo'),
            'descricao': dados.get('descricao'),
            'solucao': dados.get('solucao'),
            'prioridade': dados.get('prioridade')
        }
        payload_api = {k: v for k, v in payload_api.items() if v is not None}

        if not payload_api:
            return jsonify({'message': 'Nenhum campo para atualizar.'}), 400

        try:
            url = f"{API_URL_BASE}/api/Chamados/{chamado_id}"
            headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' }
            auth = request.headers.get('Authorization')
            if auth:
                headers['Authorization'] = auth
            resp = requests.put(url, json=payload_api, headers=headers)
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



