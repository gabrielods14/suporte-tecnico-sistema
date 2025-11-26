from flask import request, jsonify
import requests

# ENDPOINT BASE da sua API externa (Azure)
API_URL_BASE = 'https://api-suporte-grupoads-e4hmccf7gaczdbht.brazilsouth-01.azurewebsites.net'

# Rota para listar usuários e obter estatísticas
def listar_usuarios():
    # Tratamento de requisições OPTIONS para CORS
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        return response
    
    # Rota GET - Listar todos os usuários
    if request.method == 'GET':
        try:
            url = f"{API_URL_BASE}/api/Usuarios"
            headers = {
                'Accept': 'application/json'
            }
            auth = request.headers.get('Authorization')
            if auth:
                headers['Authorization'] = auth
            
            resp = requests.get(url, headers=headers)
            
            if resp.status_code == 200:
                usuarios_data = resp.json()
                
                # Se a resposta for um dict com 'data' ou similar, ajusta
                if isinstance(usuarios_data, dict) and 'data' in usuarios_data:
                    usuarios = usuarios_data['data']
                elif isinstance(usuarios_data, list):
                    usuarios = usuarios_data
                else:
                    usuarios = []
                
                # Debug: verificar dados recebidos da API C#
                print(f'[GET /api/Usuarios] Total de usuários recebidos da API C#: {len(usuarios)}')
                
                # Normaliza os dados para o frontend
                usuarios_normalizados = []
                contador_por_permissao = {
                    'colaborador': 0,
                    'suporte': 0,
                    'admin': 0
                }
                
                for usuario in usuarios:
                    usuarios_normalizados.append({
                        'id': usuario.get('id') or usuario.get('Id'),
                        'nome': usuario.get('nome') or usuario.get('Nome') or '',
                        'email': usuario.get('email') or usuario.get('Email') or '',
                        'telefone': usuario.get('telefone') or usuario.get('Telefone') or '',
                        'cargo': usuario.get('cargo') or usuario.get('Cargo') or '',
                        'permissao': usuario.get('permissao') if usuario.get('permissao') is not None else usuario.get('Permissao')
                    })
                    
                    # Contar por nível de permissão
                    permissao = usuario.get('permissao') if usuario.get('permissao') is not None else usuario.get('Permissao')
                    if permissao == 1:
                        contador_por_permissao['colaborador'] += 1
                    elif permissao == 2:
                        contador_por_permissao['suporte'] += 1
                    elif permissao == 3:
                        contador_por_permissao['admin'] += 1
                
                print(f'[GET /api/Usuarios] Usuários normalizados:', len(usuarios_normalizados))
                print(f'[GET /api/Usuarios] Contagem por permissão:', contador_por_permissao)
                
                # Retorna dados compilados
                return jsonify({
                    'total': len(usuarios_normalizados),
                    'usuarios': usuarios_normalizados,
                    'porPermissao': contador_por_permissao
                })
            
            try:
                msg = resp.json().get('message', f'Erro HTTP {resp.status_code} ao listar usuários.')
            except Exception:
                msg = f'Erro HTTP {resp.status_code} ao listar usuários.'
            return jsonify({'message': msg}), resp.status_code

        except requests.exceptions.RequestException as e:
            print(f'Erro ao conectar à API externa: {e}')
            return jsonify({'message': 'Serviço de usuários indisponível.'}), 503
