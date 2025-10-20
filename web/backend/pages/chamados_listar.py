from flask import request, jsonify
from app import app
import requests

API_URL_BASE = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net'


@app.route('/chamados', methods=['GET'])
def listar_chamados():
    status_param = request.args.get('status')
    solicitante_id = request.args.get('solicitanteId')

    try:
        url = f"{API_URL_BASE}/api/Chamados"
        params = {}
        if status_param:
            params['status'] = status_param
        if solicitante_id:
            params['solicitanteId'] = solicitante_id

        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            return jsonify(resp.json())

        try:
            msg = resp.json().get('message', f'Erro HTTP {resp.status_code} ao listar chamados.')
        except Exception:
            msg = f'Erro HTTP {resp.status_code} ao listar chamados.'
        return jsonify({'message': msg}), resp.status_code

    except requests.exceptions.RequestException as e:
        print(f'Erro ao conectar à API externa: {e}')
        return jsonify({'message': 'Serviço de chamados indisponível.'}), 503


@app.route('/chamados/andamento', methods=['GET'])
def listar_chamados_em_andamento():
    try:
        url = f"{API_URL_BASE}/api/Chamados"
        params = {'status': 'andamento'}
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            return jsonify(resp.json())

        try:
            msg = resp.json().get('message', f'Erro HTTP {resp.status_code} ao listar chamados em andamento.')
        except Exception:
            msg = f'Erro HTTP {resp.status_code} ao listar chamados em andamento.'
        return jsonify({'message': msg}), resp.status_code

    except requests.exceptions.RequestException as e:
        print(f'Erro ao conectar à API externa: {e}')
        return jsonify({'message': 'Serviço de chamados indisponível.'}), 503



