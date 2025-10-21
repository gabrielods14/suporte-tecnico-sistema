from flask import request, jsonify
from app import app
import requests 
# Não usamos o bcrypt aqui, pois enviamos a senha para a API do Azure validar.

# ENDPOINT BASE da sua API externa (Azure)
API_URL_BASE = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net'

# Usuário administrador padrão para testes
ADMIN_USER = {
    'email': 'admin@helpwave.com',
    'senha': 'admin123',
    'nome': 'Administrador',
    'cargo': 'Administrador',
    'permissao': 1
}

# Rota para o Login. O front-end envia email e senha para este endpoint.
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    
    # O login geralmente só precisa de email e senha
    email = data.get('email')
    senha = data.get('senha')
    
    if not email or not senha:
        return jsonify({"message": "Email e senha são obrigatórios para login."}), 400

    # Verifica se é o usuário administrador padrão
    if email == ADMIN_USER['email'] and senha == ADMIN_USER['senha']:
        return jsonify({
            "message": "Login realizado com sucesso!",
            "token": "admin_token_12345",
            "user": {
                "nome": ADMIN_USER['nome'],
                "email": ADMIN_USER['email'],
                "cargo": ADMIN_USER['cargo'],
                "permissao": ADMIN_USER['permissao']
            }
        }), 200

    # Prepara os dados no formato que a API do Azure espera para login
    # CORREÇÃO: A API C# espera Email e Senha com maiúsculas
    dados_para_api = {
        'Email': email,  # Maiúscula conforme DTO da API C#
        'Senha': senha   # Maiúscula conforme DTO da API C#
    }

    try:
        # CORREÇÃO: Endpoint correto da API C# é /api/Auth/login
        url_autenticacao = f"{API_URL_BASE}/api/Auth/login" 
        
        # CORREÇÃO: Adicionar headers corretos
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.post(url_autenticacao, json=dados_para_api, headers=headers)
        
        # DEBUG: Log da resposta para facilitar debug
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Content: {response.text}")

        # ----------------------------------------------------
        # 1. Login BEM-SUCEDIDO (Geralmente retorna 200)
        # ----------------------------------------------------
        if response.status_code == 200:
            # A API do Azure deve retornar o Token de Autenticação (JWT) e dados do usuário
            token_data = response.json()
            
            # Repassa a resposta completa (incluindo o token) de volta para o front-end
            return jsonify(token_data), 200
        
        # ----------------------------------------------------
        # 2. Login FALHOU (Credenciais Inválidas)
        # ----------------------------------------------------
        elif response.status_code in [401, 400, 404]:
            return jsonify({"message": "Email ou senha incorretos."}), 401
        
        # ----------------------------------------------------
        # 3. Outros Erros da API do Azure (500, etc.)
        # ----------------------------------------------------
        else:
            try:
                erro_message = response.json().get("message", f"Erro interno ({response.status_code}) na API do Azure.")
            except:
                erro_message = f"Erro interno ({response.status_code}) sem mensagem específica."
                
            return jsonify({"message": erro_message}), response.status_code

    except requests.exceptions.RequestException as e:
        # Erro de rede ou servidor indisponível
        print(f"Erro ao conectar à API do Azure: {e}")
        return jsonify({"message": "Serviço indisponível. Verifique a conexão com a API externa."}), 503
