# web/backend/pages/login.py
from flask import request, jsonify
import requests

# ENDPOINT BASE da sua API externa (Azure)
API_URL_BASE = 'https://api-suporte-grupoads-e4hmccf7gaczdbht.brazilsouth-01.azurewebsites.net'

def login_user():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({"message": "Email e senha são obrigatórios."}), 400

    # Prepara os dados para a API do Azure
    dados_para_api = {
        'email': email,
        'senha': senha
    }

    try:
        # Endpoint de Autenticação na API do Azure
        url_login = f"{API_URL_BASE}/api/Autenticacao"
        response = requests.post(url_login, json=dados_para_api)

        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            # Repassa a mensagem de erro da API do Azure, se houver
            error_message = response.json().get("message", "Usuário ou senha inválidos.")
            return jsonify({"message": error_message}), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar à API do Azure: {e}")
        return jsonify({"message": "Erro de conexão com o serviço de autenticação."}), 503
