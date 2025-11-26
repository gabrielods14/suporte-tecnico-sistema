"""
Mock Data - Dados fictícios para testes sem conexão ao banco de dados
"""
from datetime import datetime, timedelta
import random

# Dados mockados de tickets
_mock_tickets = []
_next_ticket_id = 1

def _generate_mock_tickets():
    """Gera tickets mockados iniciais"""
    global _mock_tickets, _next_ticket_id
    
    if _mock_tickets:
        return  # Já foram gerados
    
    # Status: 1=Aberto, 2=EmAndamento, 3=Pendente, 4=Resolvido, 5=Fechado
    statuses_abertos = [1]  # Aberto
    statuses_andamento = [2]  # EmAndamento
    statuses_concluidos = [4, 5]  # Resolvido ou Fechado
    prioridades = [1, 2, 3]  # 1=Baixa, 2=Média, 3=Alta
    tipos = ['Hardware', 'Software', 'Rede', 'Outro']
    
    # Tickets abertos
    for i in range(5):
        data_abertura = datetime.now() - timedelta(days=random.randint(1, 30))
        data_limite = data_abertura + timedelta(days=random.randint(1, 7))
        
        ticket = {
            'id': _next_ticket_id,
            'codigo': f"CH{str(_next_ticket_id).zfill(6)}",
            'titulo': f"Problema com {random.choice(['impressora', 'computador', 'internet', 'software', 'email'])}",
            'descricao': f"Descrição detalhada do problema número {_next_ticket_id}. O usuário relatou dificuldades com o equipamento/sistema.",
            'tipo': random.choice(tipos),
            'prioridade': random.choice(prioridades),
            'status': 1,  # Aberto
            'solicitante': {
                'id': random.choice([1, 2, 3]),  # Aleatório entre os 3 usuários
                'nome': random.choice(['Gabriel', 'João Silva', 'Maria Santos']),
                'email': random.choice(['gabriel@teste.com', 'joao@teste.com', 'maria@teste.com']),
                'cargo': random.choice(['Administrador', 'Colaborador', 'Suporte Técnico'])
            },
            'solicitanteId': random.choice([1, 2, 3]),
            'tecnicoResponsavel': None,
            'tecnicoResponsavelId': None,
            'dataAbertura': data_abertura.strftime('%Y-%m-%dT%H:%M:%S'),
            'dataLimite': data_limite.strftime('%Y-%m-%dT%H:%M:%S'),
            'dataFechamento': None,
            'solucao': None
        }
        _mock_tickets.append(ticket)
        _next_ticket_id += 1
    
    # Tickets em andamento
    for i in range(3):
        data_abertura = datetime.now() - timedelta(days=random.randint(1, 15))
        data_limite = data_abertura + timedelta(days=random.randint(1, 5))
        
        ticket = {
            'id': _next_ticket_id,
            'codigo': f"CH{str(_next_ticket_id).zfill(6)}",
            'titulo': f"Suporte necessário para {random.choice(['instalação', 'configuração', 'atualização'])}",
            'descricao': f"Descrição do chamado {_next_ticket_id} em andamento.",
            'tipo': random.choice(tipos),
            'prioridade': random.choice(prioridades),
            'status': 2,  # EmAndamento
            'solicitante': {
                'id': random.choice([1, 2, 3]),  # Aleatório entre os 3 usuários
                'nome': random.choice(['Gabriel', 'João Silva', 'Maria Santos']),
                'email': random.choice(['gabriel@teste.com', 'joao@teste.com', 'maria@teste.com']),
                'cargo': random.choice(['Administrador', 'Colaborador', 'Suporte Técnico'])
            },
            'solicitanteId': random.choice([1, 2, 3]),
            'tecnicoResponsavel': {
                'id': 3,  # Maria Santos (Suporte Técnico)
                'nome': 'Maria Santos',
                'email': 'maria@teste.com'
            },
            'tecnicoResponsavelId': 3,
            'dataAbertura': data_abertura.strftime('%Y-%m-%dT%H:%M:%S'),
            'dataLimite': data_limite.strftime('%Y-%m-%dT%H:%M:%S'),
            'dataFechamento': None,
            'solucao': None
        }
        _mock_tickets.append(ticket)
        _next_ticket_id += 1
    
    # Tickets concluídos
    for i in range(4):
        data_abertura = datetime.now() - timedelta(days=random.randint(10, 60))
        data_fechamento = data_abertura + timedelta(days=random.randint(1, 5))
        
        ticket = {
            'id': _next_ticket_id,
            'codigo': f"CH{str(_next_ticket_id).zfill(6)}",
            'titulo': f"Problema resolvido: {random.choice(['impressora', 'internet', 'software'])}",
            'descricao': f"Chamado {_next_ticket_id} que foi resolvido anteriormente.",
            'tipo': random.choice(tipos),
            'prioridade': random.choice(prioridades),
            'status': random.choice([4, 5]),  # Resolvido ou Fechado
            'solicitante': {
                'id': random.choice([1, 2, 3]),  # Aleatório entre os 3 usuários
                'nome': random.choice(['Gabriel', 'João Silva', 'Maria Santos']),
                'email': random.choice(['gabriel@teste.com', 'joao@teste.com', 'maria@teste.com']),
                'cargo': random.choice(['Administrador', 'Colaborador', 'Suporte Técnico'])
            },
            'solicitanteId': random.choice([1, 2, 3]),
            'tecnicoResponsavel': {
                'id': 3,  # Maria Santos (Suporte Técnico)
                'nome': 'Maria Santos',
                'email': 'maria@teste.com'
            },
            'tecnicoResponsavelId': 3,
            'dataAbertura': data_abertura.strftime('%Y-%m-%dT%H:%M:%S'),
            'dataLimite': (data_abertura + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S'),
            'dataFechamento': data_fechamento.strftime('%Y-%m-%dT%H:%M:%S'),
            'solucao': f"Problema resolvido através de {random.choice(['atualização de drivers', 'reconfiguração', 'substituição de peça', 'ajuste de configurações'])}."
        }
        _mock_tickets.append(ticket)
        _next_ticket_id += 1

def get_mock_tickets(filters=None):
    """Retorna lista de tickets mockados com filtros"""
    global _mock_tickets
    _generate_mock_tickets()
    
    tickets = _mock_tickets.copy()
    
    # Aplica filtros
    if filters:
        if filters.get('solicitanteId'):
            tickets = [t for t in tickets if t.get('solicitanteId') == filters['solicitanteId']]
        
        if filters.get('status'):
            status_filter = filters['status']
            if status_filter == 'Aberto' or status_filter == 1:
                tickets = [t for t in tickets if t.get('status') == 1]
            elif status_filter == 'EmAndamento' or status_filter == 2:
                tickets = [t for t in tickets if t.get('status') == 2]
            elif status_filter == 'Concluido' or status_filter in [4, 5]:
                tickets = [t for t in tickets if t.get('status') in [4, 5]]
    
    return tickets

def get_mock_ticket(ticket_id):
    """Retorna um ticket mockado específico"""
    global _mock_tickets
    _generate_mock_tickets()
    
    for ticket in _mock_tickets:
        if ticket.get('id') == ticket_id:
            return ticket
    
    raise Exception(f'Ticket {ticket_id} não encontrado')

def create_mock_ticket(ticket_data):
    """Cria um novo ticket mockado"""
    global _mock_tickets, _next_ticket_id
    
    _generate_mock_tickets()
    
    # Gera código único
    codigo = f"CH{str(_next_ticket_id).zfill(6)}"
    
    # Cria novo ticket
    new_ticket = {
        'id': _next_ticket_id,
        'codigo': codigo,
        'titulo': ticket_data.get('titulo', 'Novo Chamado'),
        'descricao': ticket_data.get('descricao', ''),
        'tipo': ticket_data.get('tipo', 'Outro'),
        'prioridade': ticket_data.get('prioridade', 2),
        'status': 1,  # Aberto
        'solicitante': {
            'id': ticket_data.get('solicitanteId', 1),
            'nome': 'Gabriel',
            'email': 'gabriel@teste.com',
            'cargo': 'Administrador'
        },
        'solicitanteId': ticket_data.get('solicitanteId', 1),
        'tecnicoResponsavel': None,
        'tecnicoResponsavelId': None,
        'dataAbertura': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        'dataLimite': ticket_data.get('dataLimite', (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S')),
        'dataFechamento': None,
        'solucao': None
    }
    
    _mock_tickets.append(new_ticket)
    _next_ticket_id += 1
    
    return new_ticket

def update_mock_ticket(ticket_id, ticket_data):
    """Atualiza um ticket mockado"""
    global _mock_tickets
    _generate_mock_tickets()
    
    for i, ticket in enumerate(_mock_tickets):
        if ticket.get('id') == ticket_id:
            # Atualiza campos
            if 'titulo' in ticket_data:
                ticket['titulo'] = ticket_data['titulo']
            if 'descricao' in ticket_data:
                ticket['descricao'] = ticket_data['descricao']
            if 'tipo' in ticket_data:
                ticket['tipo'] = ticket_data['tipo']
            if 'prioridade' in ticket_data:
                ticket['prioridade'] = ticket_data['prioridade']
            if 'status' in ticket_data:
                ticket['status'] = ticket_data['status']
                # Se status for Concluido/Resolvido/Fechado, atualiza dataFechamento
                if ticket_data['status'] in [4, 5] and not ticket.get('dataFechamento'):
                    ticket['dataFechamento'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            if 'tecnicoResponsavelId' in ticket_data:
                ticket['tecnicoResponsavelId'] = ticket_data['tecnicoResponsavelId']
                if ticket_data['tecnicoResponsavelId']:
                    ticket['tecnicoResponsavel'] = {
                        'id': ticket_data['tecnicoResponsavelId'],
                        'nome': 'Técnico Suporte',
                        'email': 'tecnico@teste.com'
                    }
            if 'solucao' in ticket_data:
                ticket['solucao'] = ticket_data['solucao']
                if ticket_data['solucao'] and not ticket.get('dataFechamento'):
                    ticket['dataFechamento'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                    ticket['status'] = 4  # Resolvido
            
            _mock_tickets[i] = ticket
            return ticket
    
    raise Exception(f'Ticket {ticket_id} não encontrado')

def reset_mock_data():
    """Reseta os dados mockados (útil para testes)"""
    global _mock_tickets, _next_ticket_id
    _mock_tickets = []
    _next_ticket_id = 1

# Dados mockados de usuários para testes
_mock_users = [
    {
        'id': 1,
        'nome': 'Gabriel',
        'email': 'gabriel@teste.com',
        'cargo': 'Administrador',
        'permissao': 3,  # Administrador
        'telefone': '(11) 99999-9999'
    },
    {
        'id': 2,
        'nome': 'João Silva',
        'email': 'joao@teste.com',
        'cargo': 'Colaborador',
        'permissao': 1,  # Colaborador
        'telefone': '(11) 98888-8888'
    },
    {
        'id': 3,
        'nome': 'Maria Santos',
        'email': 'maria@teste.com',
        'cargo': 'Suporte Técnico',
        'permissao': 2,  # Suporte Técnico
        'telefone': '(11) 97777-7777'
    }
]

def get_mock_users():
    """Retorna lista de usuários mockados"""
    return _mock_users.copy()

def get_mock_user(user_id):
    """Retorna um usuário mockado específico"""
    for user in _mock_users:
        if user.get('id') == user_id:
            return user.copy()
    return None

def get_mock_user_by_email(email):
    """Retorna um usuário mockado pelo email"""
    for user in _mock_users:
        if user.get('email', '').lower() == email.lower():
            return user.copy()
    return None

