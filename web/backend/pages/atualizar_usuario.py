from flask import request, jsonify
import requests 

# ENDPOINT BASE da sua API externa (Azure)
API_URL_BASE = 'https://api-suporte-grupoads-e4hmccf7gaczdbht.brazilsouth-01.azurewebsites.net'

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
        
        # Extração do campo NovaSenha (verifica se existe e não está vazio)
        nova_senha = None
        if 'novaSenha' in data:
            valor = data['novaSenha']
            if valor and isinstance(valor, str) and valor.strip():
                nova_senha = valor.strip()
        if not nova_senha and 'NovaSenha' in data:
            valor = data['NovaSenha']
            if valor and isinstance(valor, str) and valor.strip():
                nova_senha = valor.strip()
        
        print(f'[PUT /api/Usuarios/{usuario_id}] Campos extraídos - nome: {nome}, email: {email}, cargo: {cargo}, permissao: {permissao}')
        print(f'[PUT /api/Usuarios/{usuario_id}] Campos recebidos no JSON: {list(data.keys())}')
        print(f'[PUT /api/Usuarios/{usuario_id}] NovaSenha presente no JSON? {"Sim" if "NovaSenha" in data or "novaSenha" in data else "Não"}')
        if 'NovaSenha' in data or 'novaSenha' in data:
            valor_recebido = data.get('NovaSenha') or data.get('novaSenha') or ''
            print(f'[PUT /api/Usuarios/{usuario_id}] NovaSenha valor recebido (tipo): {type(valor_recebido)}, tamanho: {len(str(valor_recebido)) if valor_recebido else 0}')
        print(f'[PUT /api/Usuarios/{usuario_id}] NovaSenha será enviada? {"Sim" if nova_senha else "Não"}')
        
        # Validação mínima (agora inclui nova_senha)
        if not nome and not email and not telefone and not cargo and permissao is None and not nova_senha:
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
        # CRÍTICO: Adiciona NovaSenha sempre que fornecida (independente de outros campos)
        if nova_senha:
            dados_para_api['NovaSenha'] = nova_senha  # Campo para atualização de senha pelo admin
            print(f'[PUT /api/Usuarios/{usuario_id}] ✅ NovaSenha ADICIONADA ao payload: *** (oculta)')
        else:
            print(f'[PUT /api/Usuarios/{usuario_id}] ❌ NovaSenha NÃO será enviada (campo ausente ou vazio)')
        
        # Prepara um dicionário para log (oculta senha por segurança)
        dados_para_log = dados_para_api.copy()
        if 'NovaSenha' in dados_para_log:
            dados_para_log['NovaSenha'] = '*** (ocultada por segurança)'
        
        print(f'[PUT /api/Usuarios/{usuario_id}] Total de campos no payload: {len(dados_para_api)}')
        print(f'[PUT /api/Usuarios/{usuario_id}] Campos no payload: {list(dados_para_api.keys())}')
        
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
            
            print(f'[PUT /api/Usuarios/{usuario_id}] 🚀 Enviando para API Azure - Campos: {list(dados_para_api.keys())}')
            print(f'[PUT /api/Usuarios/{usuario_id}] 📦 Payload (senha ocultada): {dados_para_log}')
            
            response = requests.put(url_atualizacao, json=dados_para_api, headers=headers, timeout=30)
            
            print(f'[PUT /api/Usuarios/{usuario_id}] ✅ Resposta da API Azure: Status {response.status_code}')
            
            # Log detalhado da resposta
            try:
                if response.status_code in [200, 204]:
                    response_data = response.json() if response.content else {}
                    print(f'[PUT /api/Usuarios/{usuario_id}] ✅ Resposta (sucesso): {response_data}')
                else:
                    response_text = response.text[:1000]  # Limita a 1000 caracteres
                    print(f'[PUT /api/Usuarios/{usuario_id}] ❌ Resposta (erro): {response_text}')
            except Exception as e:
                print(f'[PUT /api/Usuarios/{usuario_id}] ⚠️ Erro ao processar resposta: {e}')
            
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

