from flask import request, jsonify
import requests

# ENDPOINT BASE da sua API externa (Azure)
API_URL_BASE = 'https://api-suporte-grupoads-e4hmccf7gaczdbht.brazilsouth-01.azurewebsites.net'

# Rota unificada para GET (meu perfil) e PUT (atualizar meu perfil)
def gerenciar_meu_perfil():
    # Tratamento de requisições OPTIONS para CORS
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, OPTIONS')
        return response
    
    # Rota GET - Buscar meu perfil (usuário logado)
    if request.method == 'GET':
        try:
            url = f"{API_URL_BASE}/api/Usuarios/meu-perfil"
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
                print(f'[GET /api/Usuarios/meu-perfil] Dados recebidos da API C#:', usuario_data)
                
                # Normaliza os dados para o frontend
                normalized_data = {
                    'id': usuario_data.get('id') or usuario_data.get('Id'),
                    'nome': usuario_data.get('nome') or usuario_data.get('Nome') or '',
                    'email': usuario_data.get('email') or usuario_data.get('Email') or '',
                    'telefone': usuario_data.get('telefone') or usuario_data.get('Telefone') or '',
                    'cargo': usuario_data.get('cargo') or usuario_data.get('Cargo') or '',
                    'permissao': usuario_data.get('permissao') if usuario_data.get('permissao') is not None else usuario_data.get('Permissao'),
                    # IMPORTANTE: Inclui o campo primeiroAcesso para o modal de primeiro acesso funcionar
                    'primeiroAcesso': usuario_data.get('primeiroAcesso') if usuario_data.get('primeiroAcesso') is not None else usuario_data.get('PrimeiroAcesso', False)
                }
                
                print(f'[GET /api/Usuarios/meu-perfil] Dados normalizados:', normalized_data)
                return jsonify(normalized_data)
            
            try:
                msg = resp.json().get('message', f'Erro HTTP {resp.status_code} ao buscar seu perfil.')
            except Exception:
                msg = f'Erro HTTP {resp.status_code} ao buscar seu perfil.'
            return jsonify({'message': msg}), resp.status_code

        except requests.exceptions.RequestException as e:
            print(f'Erro ao conectar à API externa: {e}')
            return jsonify({'message': 'Serviço de perfil indisponível.'}), 503
    
    # Rota PUT - Atualizar meu próprio perfil (usuário logado)
    if request.method == 'PUT':
        data = request.json
        
        # Mapeamento dos campos que podem ser atualizados
        nome = data.get('nome')
        email = data.get('email')
        telefone = data.get('telefone')
        cargo = data.get('cargo')
        
        # Validação mínima
        if not nome and not email and not telefone and not cargo:
            return jsonify({"message": "Pelo menos um campo deve ser fornecido para atualização."}), 400
        
        # Prepara os dados no formato esperado pela API do Azure
        dados_para_api = {}
        if nome:
            dados_para_api['Nome'] = nome
        if email:
            dados_para_api['Email'] = email
        if telefone is not None:  # Permite string vazia
            dados_para_api['Telefone'] = telefone or ""
        if cargo:
            dados_para_api['Cargo'] = cargo
        
        try:
            # Endpoint de Atualização na API do Azure (PUT)
            url_atualizacao = f"{API_URL_BASE}/api/Usuarios/meu-perfil"
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            auth = request.headers.get('Authorization')
            if auth:
                headers['Authorization'] = auth
            
            response = requests.put(url_atualizacao, json=dados_para_api, headers=headers)
            
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
                return jsonify({"message": "Seu perfil não foi encontrado."}), 404
            
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
