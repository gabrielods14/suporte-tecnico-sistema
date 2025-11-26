# web/backend/pages/chamados.py
from flask import request, jsonify
import requests

# ENDPOINT BASE da sua API externa (Azure)
API_URL_BASE = 'https://api-suporte-grupoads-e4hmccf7gaczdbht.brazilsouth-01.azurewebsites.net'

def _get_auth_header():
    """ Extrai o token do header da requisição. """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None, (jsonify({"message": "Token de autorização ausente."}), 401)
    return {'Authorization': auth_header}, None

def get_all_tickets():
    headers, error = _get_auth_header()
    if error:
        return error

    try:
        url = f"{API_URL_BASE}/api/Chamados"
        response = requests.get(url, headers=headers)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"message": f"Erro ao buscar chamados: {e}"}), 503

def get_ticket_by_id(ticket_id):
    headers, error = _get_auth_header()
    if error:
        return error

    try:
        url = f"{API_URL_BASE}/api/Chamados/{ticket_id}"
        response = requests.get(url, headers=headers)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"message": f"Erro ao buscar chamado: {e}"}), 503

def create_ticket():
    headers, error = _get_auth_header()
    if error:
        return error

    ticket_data = request.json
    if not ticket_data:
        return jsonify({"message": "Dados do chamado ausentes."}), 400

    # Adiciona o header Content-Type para o POST
    headers['Content-Type'] = 'application/json'

    try:
        url = f"{API_URL_BASE}/api/Chamados"
        response = requests.post(url, json=ticket_data, headers=headers)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"message": f"Erro ao criar chamado: {e}"}), 503

def update_ticket(ticket_id):
    headers, error = _get_auth_header()
    if error:
        return error

    update_data = request.json
    if not update_data:
        return jsonify({"message": "Dados para atualização ausentes."}), 400

    # Adiciona o header Content-Type para o PUT
    headers['Content-Type'] = 'application/json'

    try:
        url = f"{API_URL_BASE}/api/Chamados/{ticket_id}"
        # A API C# espera um PUT para atualização completa do objeto
        response = requests.put(url, json=update_data, headers=headers)
        
        if response.status_code == 204: # No Content (sucesso para PUT/DELETE)
            return '', 204
            
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"message": f"Erro ao atualizar chamado: {e}"}), 503
