from flask import request, jsonify
import requests

API_URL_BASE = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net'


def criar_chamado():
    dados = request.json or {}

    tipoChamado = dados.get('tipoChamado') or dados.get('tipo')
    titulo = dados.get('titulo')
    descricao = dados.get('descricao')
    prioridade = dados.get('prioridade', 2)  # padrão: Média
    solicitante_id = dados.get('solicitanteId') or dados.get('solicitante_id')

    if not tipoChamado or not titulo or not descricao or not solicitante_id:
        return jsonify({'message': 'Campos obrigatórios: tipoChamado, titulo, descricao e solicitanteId.'}), 400

    # Normaliza prioridade para o enum numérico esperado pela API C# (1=Baixa,2=Media,3=Alta)
    if isinstance(prioridade, str):
        p = prioridade.strip().lower()
        if 'alta' in p:
            prioridade = 3
        elif 'baix' in p:
            prioridade = 1
        else:
            prioridade = 2

    payload_api = {
        'tipo': tipoChamado,
        'titulo': titulo,
        'descricao': descricao,
        'solicitanteId': int(solicitante_id),
        'prioridade': int(prioridade),
    }
    payload_api = {k: v for k, v in payload_api.items() if v is not None}

    try:
        url = f"{API_URL_BASE}/api/Chamados"
        headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        auth = request.headers.get('Authorization')
        if auth:
            headers['Authorization'] = auth
        resp = requests.post(url, json=payload_api, headers=headers)
        if resp.status_code in [200, 201]:
            return jsonify(resp.json() if resp.content else {'message': 'Chamado criado com sucesso.'}), 201

        try:
            msg = resp.json().get('message', f'Erro HTTP {resp.status_code} ao criar chamado.')
        except Exception:
            msg = f'Erro HTTP {resp.status_code} ao criar chamado.'
        return jsonify({'message': msg}), resp.status_code

    except requests.exceptions.RequestException as e:
        print(f'Erro ao conectar à API externa: {e}')
        return jsonify({'message': 'Serviço de chamados indisponível.'}), 503



