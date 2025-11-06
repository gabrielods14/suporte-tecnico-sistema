from flask import request, jsonify
import requests

API_URL_BASE = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net'


def listar_chamados():
    status_param = request.args.get('status')
    solicitante_id = request.args.get('solicitanteId')

    try:
        url = f"{API_URL_BASE}/api/Chamados"
        headers = {
            'Accept': 'application/json'
        }
        auth = request.headers.get('Authorization')
        if auth:
            headers['Authorization'] = auth
        
        # A API C# não suporta filtros por query parameters, então buscamos todos e filtramos aqui
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            chamados = resp.json()
            
            # Filtrar por solicitanteId se fornecido (para colaboradores verem apenas seus chamados)
            if solicitante_id:
                try:
                    solicitante_id_int = int(solicitante_id)
                    chamados = [
                        chamado for chamado in chamados 
                        if (chamado.get('solicitanteId') == solicitante_id_int or 
                            chamado.get('SolicitanteId') == solicitante_id_int)
                    ]
                except (ValueError, TypeError):
                    pass
            
            # Filtrar por status se fornecido
            if status_param:
                # Mapear status textual para numérico se necessário
                status_map = {
                    'andamento': 2,
                    'em_andamento': 2,
                    'resolvido': 4,
                    'fechado': 5,
                    'aberto': 1
                }
                status_value = status_map.get(status_param.lower(), status_param)
                try:
                    status_int = int(status_value)
                    chamados = [c for c in chamados if c.get('status') == status_int]
                except (ValueError, TypeError):
                    pass
            
            return jsonify(chamados)

        try:
            msg = resp.json().get('message', f'Erro HTTP {resp.status_code} ao listar chamados.')
        except Exception:
            msg = f'Erro HTTP {resp.status_code} ao listar chamados.'
        return jsonify({'message': msg}), resp.status_code

    except requests.exceptions.RequestException as e:
        print(f'Erro ao conectar à API externa: {e}')
        return jsonify({'message': 'Serviço de chamados indisponível.'}), 503


def listar_chamados_em_andamento():
    try:
        url = f"{API_URL_BASE}/api/Chamados"
        headers = {
            'Accept': 'application/json'
        }
        auth = request.headers.get('Authorization')
        if auth:
            headers['Authorization'] = auth
        params = {'status': 'andamento'}
        resp = requests.get(url, params=params, headers=headers)
        if resp.status_code == 200:
            return jsonify(resp.json())

        try:
            msg = resp.json().get('message', f'Erro HTTP {resp.status_code} ao listar chamados em andamento.')
        except Exception:
            msg = f'Erro HTTP {resp.status_code} ao listar chamados em andamento.'
        return jsonify({'message': msg}), resp.status_code

    except requests.exceptions.RequestException as e:
        print(f'Erro ao conectar à API externa: {e}')
        return jsonify({'message': 'Serviço de chamados indisponível.'}), 503



