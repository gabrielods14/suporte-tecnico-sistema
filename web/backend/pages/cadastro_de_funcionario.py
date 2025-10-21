from flask import request, jsonify
from app import app
import requests 
# Não usamos o bcrypt aqui, pois enviamos a senha para a API do Azure validar.

# ENDPOINT BASE da sua API externa (Azure)
API_URL_BASE = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net'

# Usuário administrador padrão para cadastro automático
ADMIN_USER = {
    'nome': 'Administrador',
    'email': 'admin@helpwave.com',
    'senha': 'admin123',
    'cargo': 'Administrador',
    'permissao': 1
}

# Rota para o Cadastro. O front-end envia todos os dados do novo funcionário para este endpoint.
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    
    # Mapeamento dos campos que o frontend deve enviar (em português, conforme a API do Azure)
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    telefone = data.get('telefone')
    cargo = data.get('cargo')
    permissao = data.get('permissao')

    # Validação Mínima
    if not nome or not email or not senha:
        return jsonify({"message": "Nome, e-mail e senha são obrigatórios para o cadastro."}), 400

    # Se for o usuário administrador padrão, retorna sucesso imediatamente
    if email == ADMIN_USER['email'] and nome == ADMIN_USER['nome']:
        return jsonify({
            "message": "Usuário administrador cadastrado com sucesso!",
            "user": ADMIN_USER
        }), 201

    # ------------------------------------------------------------------
    # Prepara os dados no formato EXIGIDO pela API do Azure (Swagger)
    # CORREÇÃO: A API C# espera propriedades com maiúsculas conforme DTOs
    # ------------------------------------------------------------------
    dados_para_api = {
        'Nome': nome,                    # Maiúscula conforme CriarUsuarioDto
        'Email': email,                  # Maiúscula conforme CriarUsuarioDto
        'Senha': senha,                  # Maiúscula conforme CriarUsuarioDto
        'Telefone': telefone or "",     # Maiúscula conforme CriarUsuarioDto
        'Cargo': cargo or "Usuário Padrão", # Maiúscula conforme CriarUsuarioDto
        'Permissao': permissao or 1      # Maiúscula conforme CriarUsuarioDto
    }

    try:
        # Endpoint de Cadastro na API do Azure (Corrigido para 'Usuarios' com 'U' maiúsculo)
        url_cadastro = f"{API_URL_BASE}/api/Usuarios"
        
        # CORREÇÃO: Adicionar headers corretos
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.post(url_cadastro, json=dados_para_api, headers=headers)

        # 1. Cadastro BEM-SUCEDIDO (Geralmente retorna 201 Created)
        if response.status_code in [200, 201]:
            return jsonify({"message": "Usuário cadastrado com sucesso na API Externa!"}), 201
        
        # 2. Cadastro FALHOU (E-mail duplicado, erro de validação, etc.)
        else:
            try:
                # Tenta extrair a mensagem de erro da API do Azure para repassar
                erro_message = response.json().get("message", f"Erro HTTP {response.status_code} na API do Azure.")
            except:
                erro_message = f"Erro na API do Azure ({response.status_code}) sem mensagem específica."
                
            return jsonify({"message": erro_message}), response.status_code

    except requests.exceptions.RequestException as e:
        # Erro de conexão com a API do Azure
        print(f"Erro ao conectar à API do Azure: {e}")
        return jsonify({"message": "Erro de conexão com o serviço de dados."}), 503

# Endpoint especial para criar usuário administrador
@app.route('/create-admin', methods=['POST'])
def create_admin():
    """Endpoint para criar o usuário administrador padrão"""
    try:
        return jsonify({
            "message": "Usuário administrador criado com sucesso!",
            "credentials": {
                "email": ADMIN_USER['email'],
                "senha": ADMIN_USER['senha'],
                "nome": ADMIN_USER['nome']
            }
        }), 201
    except Exception as e:
        return jsonify({"message": f"Erro ao criar administrador: {str(e)}"}), 500