from flask import request, jsonify
import requests

# ENDPOINT BASE da sua API externa (Azure)
API_URL_BASE = 'https://api-suporte-grupoads-e4hmccf7gaczdbht.brazilsouth-01.azurewebsites.net'

def alterar_senha():
    # Tratamento de requisições OPTIONS para CORS
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'PUT, OPTIONS')
        return response
    
    # Rota PUT - Alterar senha do usuário logado
    if request.method == 'PUT':
        try:
            data = request.json
            
            # Validação dos campos obrigatórios
            senha_atual = data.get('senhaAtual') or data.get('SenhaAtual')
            nova_senha = data.get('novaSenha') or data.get('NovaSenha')
            
            if not senha_atual or not nova_senha:
                return jsonify({"message": "Senha atual e nova senha são obrigatórias."}), 400
            
            # Prepara os dados no formato esperado pela API do Azure
            dados_para_api = {
                'SenhaAtual': senha_atual,
                'NovaSenha': nova_senha
            }
            
            # Endpoint de alteração de senha na API do Azure
            url = f"{API_URL_BASE}/api/Usuarios/alterar-senha"
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            auth = request.headers.get('Authorization')
            if auth:
                headers['Authorization'] = auth
            
            print(f'[PUT /api/Usuarios/alterar-senha] Enviando para API Azure: {url}')
            print(f'[PUT /api/Usuarios/alterar-senha] Headers: {headers}')
            print(f'[PUT /api/Usuarios/alterar-senha] Payload (senha ocultada): {{"SenhaAtual": "***", "NovaSenha": "***"}}')
            
            response = requests.put(url, json=dados_para_api, headers=headers)
            
            print(f'[PUT /api/Usuarios/alterar-senha] Resposta da API Azure: {response.status_code}')
            print(f'[PUT /api/Usuarios/alterar-senha] Resposta (text): {response.text[:200]}')
            
            # Resposta bem-sucedida
            if response.status_code in [200, 204]:
                try:
                    return jsonify(response.json()), 200
                except:
                    return jsonify({"message": "Senha alterada com sucesso!"}), 200
            
            # Erros específicos
            elif response.status_code == 400:
                try:
                    erro_message = response.json().get("message", "Dados inválidos.")
                except:
                    erro_message = "Dados inválidos."
                return jsonify({"message": erro_message}), 400
            
            elif response.status_code == 401:
                return jsonify({"message": "Não autorizado. Verifique suas credenciais."}), 401
            
            elif response.status_code == 404:
                return jsonify({"message": "Usuário não encontrado."}), 404
            
            # Outros erros
            else:
                try:
                    erro_message = response.json().get("message", f"Erro HTTP {response.status_code} na API do Azure.")
                except:
                    erro_message = f"Erro na API do Azure ({response.status_code}) sem mensagem específica."
                
                return jsonify({"message": erro_message}), response.status_code
        
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar à API do Azure: {e}")
            return jsonify({"message": "Erro de conexão com o serviço de dados."}), 503
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return jsonify({"message": "Erro interno do servidor."}), 500

