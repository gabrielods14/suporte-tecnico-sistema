from flask import request, jsonify, current_app
import requests

# Importação será feita dinamicamente
app = None 
# Não usamos o bcrypt aqui, pois enviamos a senha para a API do Azure validar.

# ENDPOINT BASE da sua API externa (Azure)
API_URL_BASE = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net'

# Rota para o Login. O front-end envia email e senha para este endpoint.
def login_user():
    data = request.json
    
    # O login geralmente só precisa de email e senha
    email = data.get('email')
    senha = data.get('senha')
    
    if not email or not senha:
        return jsonify({"message": "Email e senha são obrigatórios para login."}), 400

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
            # A API do Azure deve retornar o Token de Autenticação (JWT)
            token_payload = response.json() or {}
            # Normaliza a chave do token para minúsculo para o front-end
            token_value = token_payload.get('token') or token_payload.get('Token')

            user_info = None
            try:
                # Decodifica o payload do JWT sem validação (apenas para obter o ID)
                # O formato é header.payload.signature (base64url)
                import base64, json
                parts = (token_value or '').split('.')
                if len(parts) >= 2:
                    padded = parts[1] + '==='  # padding para base64url
                    decoded = base64.urlsafe_b64decode(padded)
                    payload_obj = json.loads(decoded.decode('utf-8'))
                    user_id = payload_obj.get('sub')
                    user_role = payload_obj.get('role')

                    if user_id:
                        # Busca dados do usuário para obter nome e permissão
                        usuario_resp = requests.get(f"{API_URL_BASE}/api/Usuarios/{user_id}")
                        print(f"[Login] Resposta da API de usuário: Status {usuario_resp.status_code}")
                        
                        if usuario_resp.status_code == 200:
                            usuario_json = usuario_resp.json() or {}
                            print(f"[Login] Dados recebidos da API C#: {usuario_json}")
                            
                            # Normaliza campos (pode vir com maiúscula ou minúscula)
                            nome_api = usuario_json.get('nome') or usuario_json.get('Nome') or ''
                            email_api = usuario_json.get('email') or usuario_json.get('Email') or email
                            cargo_api = usuario_json.get('cargo') or usuario_json.get('Cargo') or ''
                            telefone_api = usuario_json.get('telefone') or usuario_json.get('Telefone') or ''
                            
                            print(f"[Login] Nome extraído: '{nome_api}'")
                            print(f"[Login] Email extraído: '{email_api}'")
                            print(f"[Login] Cargo extraído: '{cargo_api}'")
                            
                            user_info = {
                                'id': usuario_json.get('id') or usuario_json.get('Id') or user_id,
                                'nome': nome_api,
                                'email': email_api,
                                'cargo': cargo_api,
                                'telefone': telefone_api,
                                'permissao': usuario_json.get('permissao') if usuario_json.get('permissao') is not None else (usuario_json.get('Permissao') if usuario_json.get('Permissao') is not None else user_role)
                            }
                            print(f"[Login] user_info final: {user_info}")
                        else:
                            print(f"[Login] Erro ao buscar usuário: {usuario_resp.status_code}")
                            # Fallback: retorna apenas dados do token
                            user_info = {
                                'id': user_id,
                                'nome': '',
                                'email': email,
                                'cargo': '',
                                'telefone': '',
                                'permissao': user_role if user_role else 1  # Default para colaborador se não houver role
                            }
            except Exception as e:
                print(f"Falha ao enriquecer dados do usuário pós-login: {e}")
                # Garantir que sempre há um user_info válido
                if not user_info:
                    user_info = {
                        'id': None,
                        'nome': '',
                        'email': email,
                        'permissao': 1  # Default para colaborador
                    }

            # Garantir que user_info não seja None antes de retornar
            if not user_info:
                user_info = {
                    'id': None,
                    'nome': '',
                    'email': email,
                    'permissao': 1
                }

            # Monta resposta unificada
            return jsonify({
                'token': token_value,
                'user': user_info
            }), 200
        
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
