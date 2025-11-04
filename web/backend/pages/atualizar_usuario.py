from flask import request, jsonify
import requests 

# ENDPOINT BASE da sua API externa (Azure)
API_URL_BASE = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net'

# Rota para atualizar o perfil do usuário
def atualizar_usuario(usuario_id):
    # Tratamento de requisições OPTIONS para CORS
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'PUT, OPTIONS')
        return response
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
        url_atualizacao = f"{API_URL_BASE}/api/Usuarios/{usuario_id}"
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
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

