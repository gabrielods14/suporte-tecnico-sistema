from flask import request, jsonify
import requests 

# ENDPOINT BASE da sua API externa (Azure)
API_URL_BASE = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net'

# Rota unificada para buscar (GET), atualizar (PUT) e excluir (DELETE) o usuário
def gerenciar_usuario(usuario_id):
    print(f'[gerenciar_usuario] Método: {request.method}, ID: {usuario_id}, URL: {request.url}')
    
    # Tratamento de requisições OPTIONS para CORS
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS')
        return response
    
    # Rota GET - Buscar usuário por ID
    if request.method == 'GET':
        try:
            url = f"{API_URL_BASE}/api/Usuarios/{usuario_id}"
            headers = {
                'Accept': 'application/json'
            }
            auth = request.headers.get('Authorization')
            if auth:
                headers['Authorization'] = auth
            
            resp = requests.get(url, headers=headers)
            
            if resp.status_code == 200:
                usuario_data = resp.json()
                # Debug: verificar dados recebidos da API C#
                print(f'[GET /usuarios/{usuario_id}] Dados recebidos da API C#:', usuario_data)
                
                # Normaliza os dados para o frontend
                normalized_data = {
                    'id': usuario_data.get('id') or usuario_data.get('Id'),
                    'nome': usuario_data.get('nome') or usuario_data.get('Nome') or '',
                    'email': usuario_data.get('email') or usuario_data.get('Email') or '',
                    'telefone': usuario_data.get('telefone') or usuario_data.get('Telefone') or '',
                    'cargo': usuario_data.get('cargo') or usuario_data.get('Cargo') or '',
                    'permissao': usuario_data.get('permissao') if usuario_data.get('permissao') is not None else usuario_data.get('Permissao')
                }
                
                print(f'[GET /usuarios/{usuario_id}] Dados normalizados:', normalized_data)
                return jsonify(normalized_data)
            
            try:
                msg = resp.json().get('message', f'Erro HTTP {resp.status_code} ao buscar usuário {usuario_id}.')
            except Exception:
                msg = f'Erro HTTP {resp.status_code} ao buscar usuário {usuario_id}.'
            return jsonify({'message': msg}), resp.status_code

        except requests.exceptions.RequestException as e:
            print(f'Erro ao conectar à API externa: {e}')
            return jsonify({'message': 'Serviço de usuários indisponível.'}), 503
    
    # Rota PUT - Atualizar usuário
    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"message": "Content-Type deve ser application/json"}), 400
        
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"message": "Dados JSON inválidos ou vazios"}), 400
        
        print(f'[PUT /api/Usuarios/{usuario_id}] Dados recebidos:', data)
        
        # Mapeamento dos campos que podem ser atualizados (aceita tanto minúsculas quanto maiúsculas)
        nome = data.get('nome') or data.get('Nome')
        email = data.get('email') or data.get('Email')
        telefone = data.get('telefone') or data.get('Telefone')
        cargo = data.get('cargo') or data.get('Cargo')
        permissao = data.get('permissao') if 'permissao' in data else (data.get('Permissao') if 'Permissao' in data else None)
        
        print(f'[PUT /api/Usuarios/{usuario_id}] Campos extraídos - nome: {nome}, email: {email}, cargo: {cargo}, permissao: {permissao}')
        
        # Validação mínima
        if not nome and not email and not telefone and not cargo and permissao is None:
            return jsonify({"message": "Pelo menos um campo deve ser fornecido para atualização."}), 400
        
        # Prepara os dados no formato esperado pela API do Azure
        dados_para_api = {}
        if nome:
            dados_para_api['Nome'] = nome
        if email:
            dados_para_api['Email'] = email
        if telefone is not None:  # Permite string vazia ou null
            dados_para_api['Telefone'] = telefone if telefone else ""
        if cargo:
            dados_para_api['Cargo'] = cargo
        if permissao is not None:
            dados_para_api['Permissao'] = int(permissao)  # Garante que seja inteiro
        
        try:
            # Endpoint de Atualização na API do Azure (PUT)
            url_atualizacao = f"{API_URL_BASE}/api/Usuarios/{usuario_id}"
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            auth = request.headers.get('Authorization')
            if auth:
                headers['Authorization'] = auth
            
            print(f'[PUT /api/Usuarios/{usuario_id}] Enviando para API Azure: {dados_para_api}')
            response = requests.put(url_atualizacao, json=dados_para_api, headers=headers)
            print(f'[PUT /api/Usuarios/{usuario_id}] Resposta da API Azure: {response.status_code}')
            
            # 1. Atualização BEM-SUCEDIDA
            if response.status_code in [200, 204]:
                # Se retornar dados, retorna; senão, retorna sucesso
                try:
                    return jsonify({
                        "message": "Perfil atualizado com sucesso!",
                        "user": response.json()
                    }), 200
                except:
                    return jsonify({"message": "Perfil atualizado com sucesso!"}), 200
            
            # 2. Usuário não encontrado
            elif response.status_code == 404:
                return jsonify({"message": "Usuário não encontrado."}), 404
            
            # 3. Outros erros
            else:
                try:
                    erro_message = response.json().get("message", f"Erro HTTP {response.status_code} na API do Azure.")
                except:
                    erro_message = f"Erro na API do Azure ({response.status_code}) sem mensagem específica."
                    
                return jsonify({"message": erro_message}), response.status_code
        
        except requests.exceptions.RequestException as e:
            # Erro de conexão com a API do Azure
            print(f"Erro ao conectar à API do Azure: {e}")
            return jsonify({"message": "Erro de conexão com o serviço de dados."}), 503
    
    # Rota DELETE - Excluir usuário
    if request.method == 'DELETE':
        try:
            print(f'[DELETE /api/Usuarios/{usuario_id}] Iniciando exclusão')
            url_delete = f"{API_URL_BASE}/api/Usuarios/{usuario_id}"
            headers = {
                'Accept': 'application/json'
            }
            auth = request.headers.get('Authorization')
            if auth:
                headers['Authorization'] = auth
            
            response = requests.delete(url_delete, headers=headers)
            print(f'[DELETE /api/Usuarios/{usuario_id}] Resposta da API Azure: {response.status_code}')
            
            # DELETE geralmente retorna 204 (No Content) ou 200
            if response.status_code in [200, 204]:
                return jsonify({"message": "Usuário excluído com sucesso!"}), 200
            
            # Usuário não encontrado
            elif response.status_code == 404:
                return jsonify({"message": "Usuário não encontrado."}), 404
            
            # Outros erros
            else:
                try:
                    erro_message = response.json().get("message", f"Erro HTTP {response.status_code} ao excluir usuário.")
                except:
                    erro_message = f"Erro HTTP {response.status_code} ao excluir usuário."
                return jsonify({"message": erro_message}), response.status_code
        
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar à API do Azure: {e}")
            return jsonify({"message": "Erro de conexão com o serviço de dados."}), 503

