"""
Cliente de API para integração com o backend Flask
Baseado no api.js do projeto web
"""
import requests
import json
import os
from typing import Optional, Dict, Any

try:
    from config import FLASK_BASE_URL, API_URL_BASE, ADMIN_USER
except ImportError:
    FLASK_BASE_URL = 'http://localhost:5232'  # Porta padrão do .NET
    API_URL_BASE = 'https://api-suporte-grupoads-e4hmccf7gaczdbht.brazilsouth-01.azurewebsites.net'
    ADMIN_USER = {
        'email': 'admin@helpwave.com',
        'senha': 'admin123',
        'nome': 'Administrador',
        'cargo': 'Administrador',
        'permissao': 3
    }


class ApiClient:
    """Cliente para fazer requisições à API"""
    
    def __init__(self):
        # Usa a URL base da API Azure como padrão, mas pode usar a local
        self.base_url = API_URL_BASE or FLASK_BASE_URL
        self.default_headers = {
            'Content-Type': 'application/json',
        }
        self.token_file = os.path.join(os.path.expanduser('~'), '.helpwave_token')
    
    def get_auth_token(self) -> Optional[str]:
        """Obtém o token de autenticação salvo"""
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r') as f:
                    return f.read().strip()
        except Exception:
            pass
        return None
    
    def save_auth_token(self, token: str):
        """Salva o token de autenticação"""
        try:
            with open(self.token_file, 'w') as f:
                f.write(token)
        except Exception:
            pass
    
    def clear_auth_token(self):
        """Remove o token de autenticação"""
        try:
            if os.path.exists(self.token_file):
                os.remove(self.token_file)
        except Exception:
            pass
    
    def get_headers(self, include_auth: bool = True) -> Dict[str, str]:
        """Retorna headers com autenticação"""
        headers = self.default_headers.copy()
        
        if include_auth:
            token = self.get_auth_token()
            if token:
                headers['Authorization'] = f'Bearer {token}'
        
        return headers
    
    def handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Processa a resposta da API - EXATAMENTE como no web (api.js handleResponse)"""
        # Respostas 204 (NoContent) não têm corpo - igual ao web
        if response.status_code == 204:
            return {'message': 'Operação realizada com sucesso'}
        
        # Tenta fazer parse do JSON
        try:
            text = response.text
            # Se a resposta estiver vazia, retorna um objeto vazio (igual ao web)
            if not text:
                data = {}
            else:
                data = response.json()
        except Exception:
            # Se não conseguir fazer parse, pode ser que não tenha corpo (igual ao web)
            if response.ok:
                data = {'message': 'Operação realizada com sucesso'}
            else:
                data = {'message': 'Erro interno do servidor.'}
        
        if not response.ok:
            # Trata erro 401 (token inválido) igual ao web
            if response.status_code == 401:
                self.clear_auth_token()
            
            # Cria erro com status_code e data (igual ao web)
            error = Exception(data.get('message', 'Erro na requisição'))
            error.status_code = response.status_code
            error.data = data
            raise error
        
        return data
    
    def get(self, endpoint: str, include_auth: bool = True) -> Dict[str, Any]:
        """Faz uma requisição GET - EXATAMENTE como no web (api.js get method)"""
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                headers=self.get_headers(include_auth),
                timeout=10
            )
            return self.handle_response(response)
        except requests.exceptions.ConnectionError:
            raise Exception('Erro de conexão. Verifique se o servidor está rodando.')
        except requests.exceptions.Timeout:
            raise Exception('Timeout ao conectar ao servidor. Verifique se o servidor está rodando.')
        except requests.exceptions.RequestException as e:
            # Trata erro 401 (token inválido) igual ao web
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 401:
                    self.clear_auth_token()
                    raise Exception('Sessão expirada. Faça login novamente.')
            raise Exception(f'Erro de conexão: {str(e)}. Verifique se o servidor está rodando.')
        except Exception as e:
            # Se for erro do handle_response com status 401
            if hasattr(e, 'status_code') and e.status_code == 401:
                self.clear_auth_token()
                raise Exception('Sessão expirada. Faça login novamente.')
            raise e
    
    def post(self, endpoint: str, data: Dict[str, Any], include_auth: bool = True) -> Dict[str, Any]:
        """Faz uma requisição POST - exatamente como no web (api.js post method)"""
        try:
            # Usa json=data que é equivalente ao body: JSON.stringify(data) do web
            # O requests automaticamente serializa para JSON e adiciona Content-Type: application/json
            response = requests.post(
                f"{self.base_url}{endpoint}",
                headers=self.get_headers(include_auth),
                json=data,  # Equivalente a: body: JSON.stringify(data) no web
                timeout=10
            )
            return self.handle_response(response)
        except requests.exceptions.ConnectionError:
            raise Exception(f'Não foi possível conectar ao servidor em {self.base_url}. Verifique se o backend Flask está rodando na porta 5000.')
        except requests.exceptions.Timeout:
            raise Exception(f'Timeout ao conectar ao servidor. Verifique se o backend Flask está rodando em {self.base_url}.')
        except requests.exceptions.RequestException as e:
            raise Exception(f'Erro de conexão: {str(e)}. Verifique se o servidor está rodando em {self.base_url}.')
        except Exception as e:
            raise e
    
    def put(self, endpoint: str, data: Dict[str, Any], include_auth: bool = True) -> Dict[str, Any]:
        """Faz uma requisição PUT"""
        try:
            response = requests.put(
                f"{self.base_url}{endpoint}",
                headers=self.get_headers(include_auth),
                json=data,
                timeout=10
            )
            return self.handle_response(response)
        except requests.exceptions.ConnectionError:
            raise Exception(f'Não foi possível conectar ao servidor em {self.base_url}. Verifique se o backend Flask está rodando na porta 5000.')
        except requests.exceptions.Timeout:
            raise Exception(f'Timeout ao conectar ao servidor. Verifique se o backend Flask está rodando em {self.base_url}.')
        except requests.exceptions.RequestException as e:
            raise Exception(f'Erro de conexão: {str(e)}. Verifique se o servidor está rodando em {self.base_url}.')
        except Exception as e:
            raise e
    
    def delete(self, endpoint: str, include_auth: bool = True) -> Dict[str, Any]:
        """Faz uma requisição DELETE"""
        try:
            response = requests.delete(
                f"{self.base_url}{endpoint}",
                headers=self.get_headers(include_auth),
                timeout=10
            )
            return self.handle_response(response)
        except requests.exceptions.ConnectionError:
            raise Exception(f'Não foi possível conectar ao servidor em {self.base_url}. Verifique se o backend Flask está rodando na porta 5000.')
        except requests.exceptions.Timeout:
            raise Exception(f'Timeout ao conectar ao servidor. Verifique se o backend Flask está rodando em {self.base_url}.')
        except requests.exceptions.RequestException as e:
            raise Exception(f'Erro de conexão: {str(e)}. Verifique se o servidor está rodando em {self.base_url}.')
        except Exception as e:
            raise e


# Instância global do cliente
api_client = ApiClient()


class AuthService:
    """Serviço de autenticação"""
    
    @staticmethod
    def login(email: str, password: str) -> Dict[str, Any]:
        """Faz login do usuário - API .NET: POST /api/Auth/login"""
        # API .NET espera Email e Senha (PascalCase)
        response = api_client.post('/api/Auth/login', {'Email': email, 'Senha': password}, include_auth=False)
        # Retorna { Token: string, PrimeiroAcesso: bool }
        return response
    
    @staticmethod
    def logout():
        """Faz logout do usuário"""
        api_client.clear_auth_token()
        return {'message': 'Logout realizado com sucesso'}
    
    @staticmethod
    def is_authenticated() -> bool:
        """Verifica se o usuário está autenticado"""
        return api_client.get_auth_token() is not None
    
    @staticmethod
    def get_user_info() -> Optional[Dict[str, Any]]:
        """Obtém informações do usuário do token JWT - igual ao web (authService.getUserInfo)"""
        token = api_client.get_auth_token()
        if not token:
            return None
        
        try:
            import base64
            # Decodifica o payload do JWT (segunda parte do token)
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            # Decodifica o payload
            payload = parts[1]
            # Adiciona padding se necessário
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += '=' * padding
            
            decoded = base64.urlsafe_b64decode(payload)
            user_info = json.loads(decoded)
            return user_info
        except Exception as e:
            print(f"[AuthService] Erro ao decodificar token: {e}")
            return None


class UserService:
    """Serviço de usuários - EXATAMENTE como no web (api.js)"""
    
    @staticmethod
    def register(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Registra um novo usuário - API .NET: POST /api/Usuarios"""
        # Converte campos para PascalCase conforme esperado pela API .NET
        api_data = {
            'Nome': user_data.get('nome') or user_data.get('Nome', ''),
            'Email': user_data.get('email') or user_data.get('Email', ''),
            'Senha': user_data.get('senha') or user_data.get('Senha', ''),
            'Telefone': user_data.get('telefone') or user_data.get('Telefone'),
            'Cargo': user_data.get('cargo') or user_data.get('Cargo', ''),
            'Permissao': user_data.get('permissao') or user_data.get('Permissao', 1)
        }
        return api_client.post('/api/Usuarios', api_data, include_auth=False)
    
    @staticmethod
    def get_users() -> Dict[str, Any]:
        """Obtém lista de usuários - igual ao web: /api/Usuarios"""
        try:
            return api_client.get('/api/Usuarios')
        except Exception as e:
            # Fallback para mock quando não há conexão
            try:
                from mock_data import get_mock_users
                users = get_mock_users()
                return {'usuarios': users, 'total': len(users)}
            except ImportError:
                raise e
    
    @staticmethod
    def getUser(user_id: int) -> Dict[str, Any]:
        """Obtém informações de um único usuário - igual ao web: /api/Usuarios/{id}"""
        try:
            return api_client.get(f'/api/Usuarios/{user_id}')
        except Exception:
            # Fallback: tenta buscar do mock
            try:
                from mock_data import get_mock_user
                user = get_mock_user(user_id)
                if user:
                    return user
            except ImportError:
                pass
            # Fallback: busca todos e filtra (igual ao web)
            try:
                all_data = UserService.get_users()
                users = []
                if isinstance(all_data, list):
                    users = all_data
                elif all_data.get('usuarios') and isinstance(all_data['usuarios'], list):
                    users = all_data['usuarios']
                elif all_data.get('items') and isinstance(all_data['items'], list):
                    users = all_data['items']
                elif all_data.get('users') and isinstance(all_data['users'], list):
                    users = all_data['users']
                
                found = next((u for u in users if int(u.get('id', 0)) == int(user_id)), None)
                if found:
                    return found
            except:
                pass
            raise Exception(f'Usuário {user_id} não encontrado')
    
    @staticmethod
    def update_user(user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza dados do usuário - API .NET: PUT /api/Usuarios/{id}"""
        # Converte campos para PascalCase conforme esperado pela API .NET
        api_data = {}
        if 'nome' in user_data or 'Nome' in user_data:
            api_data['Nome'] = user_data.get('nome') or user_data.get('Nome')
        if 'email' in user_data or 'Email' in user_data:
            api_data['Email'] = user_data.get('email') or user_data.get('Email')
        if 'telefone' in user_data or 'Telefone' in user_data:
            api_data['Telefone'] = user_data.get('telefone') or user_data.get('Telefone')
        if 'cargo' in user_data or 'Cargo' in user_data:
            api_data['Cargo'] = user_data.get('cargo') or user_data.get('Cargo')
        if 'permissao' in user_data or 'Permissao' in user_data:
            api_data['Permissao'] = user_data.get('permissao') or user_data.get('Permissao')
        if 'novaSenha' in user_data or 'NovaSenha' in user_data:
            api_data['NovaSenha'] = user_data.get('novaSenha') or user_data.get('NovaSenha')
        return api_client.put(f'/api/Usuarios/{user_id}', api_data)
    
    @staticmethod
    def delete_user(user_id: int) -> Dict[str, Any]:
        """Remove usuário - igual ao web: /api/Usuarios/{id}"""
        return api_client.delete(f'/api/Usuarios/{user_id}')
    
    @staticmethod
    def alterar_senha(senha_atual: str, nova_senha: str) -> Dict[str, Any]:
        """Altera senha do usuário - API .NET: PUT /api/Usuarios/alterar-senha"""
        # API .NET espera SenhaAtual e NovaSenha (PascalCase)
        return api_client.put('/api/Usuarios/alterar-senha', {
            'SenhaAtual': senha_atual,
            'NovaSenha': nova_senha
        })
    
    @staticmethod
    def get_meu_perfil() -> Dict[str, Any]:
        """Obtém perfil do usuário logado - igual ao web: /api/Usuarios/meu-perfil"""
        try:
            return api_client.get('/api/Usuarios/meu-perfil')
        except Exception:
            # Fallback: tenta obter do token salvo ou retorna None
            # O login já fornece os dados do usuário, então isso é apenas um fallback
            return None
    
    @staticmethod
    def update_meu_perfil(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza perfil do usuário logado - API .NET: PUT /api/Usuarios/meu-perfil"""
        # Converte campos para PascalCase conforme esperado pela API .NET
        api_data = {}
        if 'nome' in user_data or 'Nome' in user_data:
            api_data['Nome'] = user_data.get('nome') or user_data.get('Nome')
        if 'email' in user_data or 'Email' in user_data:
            api_data['Email'] = user_data.get('email') or user_data.get('Email')
        if 'telefone' in user_data or 'Telefone' in user_data:
            api_data['Telefone'] = user_data.get('telefone') or user_data.get('Telefone')
        if 'cargo' in user_data or 'Cargo' in user_data:
            api_data['Cargo'] = user_data.get('cargo') or user_data.get('Cargo')
        return api_client.put('/api/Usuarios/meu-perfil', api_data)


class TicketService:
    """Serviço de tickets/chamados - EXATAMENTE como no web (api.js)"""
    
    @staticmethod
    def create_ticket(ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo ticket - API .NET: POST /api/Chamados"""
        try:
            # Converte campos para PascalCase conforme esperado pela API .NET
            api_data = {
                'Titulo': ticket_data.get('titulo') or ticket_data.get('Titulo', ''),
                'Descricao': ticket_data.get('descricao') or ticket_data.get('Descricao', ''),
                'Tipo': ticket_data.get('tipo') or ticket_data.get('Tipo', ''),
                'SolicitanteId': ticket_data.get('solicitanteId') or ticket_data.get('SolicitanteId', 0),
                'Prioridade': ticket_data.get('prioridade') or ticket_data.get('Prioridade')
            }
            return api_client.post('/api/Chamados', api_data)
        except Exception as e:
            # Se houver erro de conexão, usa dados mock
            error_str = str(e).lower()
            if 'conexão' in error_str or 'connection' in error_str or 'servidor' in error_str:
                print(f"[TicketService] Usando dados mock devido a erro de conexão: {e}")
                from mock_data import create_mock_ticket
                return create_mock_ticket(ticket_data)
            raise
    
    @staticmethod
    def get_tickets(filters: Optional[Dict[str, Any]] = None) -> list:
        """Obtém lista de tickets - igual ao web: GET /chamados?queryParams"""
        if filters is None:
            filters = {}
        
        try:
            # Constrói query string igual ao web
            query_params = []
            if filters.get('solicitanteId'):
                query_params.append(f"solicitanteId={filters['solicitanteId']}")
            if filters.get('status'):
                query_params.append(f"status={filters['status']}")
            
            endpoint = '/api/Chamados'
            if query_params:
                endpoint = f'/api/Chamados?{"&".join(query_params)}'
            
            print(f"[TicketService.get_tickets] Endpoint chamado: {endpoint}")
            print(f"[TicketService.get_tickets] Filtros recebidos: {filters}")
            response = api_client.get(endpoint)
            print(f"[TicketService.get_tickets] Resposta recebida: {len(response) if isinstance(response, list) else 'não é lista'}")
            # Retorna lista diretamente se for lista, senão tenta extrair
            if isinstance(response, list):
                return response
            elif isinstance(response, dict):
                # Tenta extrair lista de diferentes formatos possíveis
                if 'chamados' in response and isinstance(response['chamados'], list):
                    return response['chamados']
                elif 'items' in response and isinstance(response['items'], list):
                    return response['items']
                elif 'data' in response and isinstance(response['data'], list):
                    return response['data']
            return []
        except Exception as e:
            # Se houver erro de conexão, usa dados mock
            error_str = str(e).lower()
            if 'conexão' in error_str or 'connection' in error_str or 'servidor' in error_str:
                print(f"[TicketService] Usando dados mock devido a erro de conexão: {e}")
                from mock_data import get_mock_tickets
                return get_mock_tickets(filters)
            raise
    
    @staticmethod
    def get_ticket(ticket_id: int) -> Dict[str, Any]:
        """Obtém um ticket específico - API .NET: GET /api/Chamados/{id}"""
        try:
            return api_client.get(f'/api/Chamados/{ticket_id}')
        except Exception as e:
            # Se houver erro de conexão, usa dados mock
            error_str = str(e).lower()
            if 'conexão' in error_str or 'connection' in error_str or 'servidor' in error_str:
                print(f"[TicketService] Usando dados mock devido a erro de conexão: {e}")
                from mock_data import get_mock_ticket
                return get_mock_ticket(ticket_id)
            raise
    
    @staticmethod
    def update_ticket(ticket_id: int, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um ticket - API .NET: PUT /api/Chamados/{id}"""
        try:
            # Converte campos para PascalCase conforme esperado pela API .NET
            api_data = {}
            if 'status' in ticket_data or 'Status' in ticket_data:
                api_data['Status'] = ticket_data.get('status') or ticket_data.get('Status')
            if 'tecnicoResponsavelId' in ticket_data or 'TecnicoResponsavelId' in ticket_data:
                api_data['TecnicoResponsavelId'] = ticket_data.get('tecnicoResponsavelId') or ticket_data.get('TecnicoResponsavelId')
            if 'solucao' in ticket_data or 'Solucao' in ticket_data:
                api_data['Solucao'] = ticket_data.get('solucao') or ticket_data.get('Solucao')
            if 'dataFechamento' in ticket_data or 'DataFechamento' in ticket_data:
                api_data['DataFechamento'] = ticket_data.get('dataFechamento') or ticket_data.get('DataFechamento')
            if 'titulo' in ticket_data or 'Titulo' in ticket_data:
                api_data['Titulo'] = ticket_data.get('titulo') or ticket_data.get('Titulo')
            if 'descricao' in ticket_data or 'Descricao' in ticket_data:
                api_data['Descricao'] = ticket_data.get('descricao') or ticket_data.get('Descricao')
            if 'prioridade' in ticket_data or 'Prioridade' in ticket_data:
                api_data['Prioridade'] = ticket_data.get('prioridade') or ticket_data.get('Prioridade')
            return api_client.put(f'/api/Chamados/{ticket_id}', api_data)
        except Exception as e:
            # Se houver erro de conexão, usa dados mock
            error_str = str(e).lower()
            if 'conexão' in error_str or 'connection' in error_str or 'servidor' in error_str:
                print(f"[TicketService] Usando dados mock devido a erro de conexão: {e}")
                from mock_data import update_mock_ticket
                return update_mock_ticket(ticket_id, ticket_data)
            raise
    
    @staticmethod
    def delete_ticket(ticket_id: int) -> Dict[str, Any]:
        """Remove um ticket - API .NET: DELETE /api/Chamados/{id}"""
        try:
            return api_client.delete(f'/api/Chamados/{ticket_id}')
        except Exception as e:
            # Se houver erro de conexão, retorna sucesso mockado
            error_str = str(e).lower()
            if 'conexão' in error_str or 'connection' in error_str or 'servidor' in error_str:
                print(f"[TicketService] Usando dados mock devido a erro de conexão: {e}")
                # Remove do mock se existir
                from mock_data import _mock_tickets
                _mock_tickets[:] = [t for t in _mock_tickets if t.get('id') != ticket_id]
                return {'message': 'Ticket removido com sucesso'}
            raise


class AIService:
    """Serviço para integração com IA (Gemini) - igual ao web"""
    
    @staticmethod
    def gerar_sugestao(titulo: str, descricao: str) -> Dict[str, Any]:
        """Gera uma sugestão de resposta técnica usando Gemini AI - igual ao web"""
        # O endpoint do Gemini está no backend Flask (localhost:5000), não na API .NET
        # Cria um cliente temporário para usar o Flask backend
        flask_base_url = 'http://localhost:5000'
        
        try:
            # Faz requisição direta ao Flask backend (igual ao web)
            response = requests.post(
                f'{flask_base_url}/api/gemini/sugerir-resposta',
                json={
                    'titulo': titulo or '',
                    'descricao': descricao
                },
                headers={
                    'Content-Type': 'application/json'
                },
                timeout=30
            )
            
            # Processa a resposta igual ao web
            if response.status_code == 204:
                return {'message': 'Operação realizada com sucesso'}
            
            try:
                text = response.text
                if not text:
                    data = {}
                else:
                    data = response.json()
            except Exception:
                if response.ok:
                    data = {'message': 'Operação realizada com sucesso'}
                else:
                    data = {'message': 'Erro interno do servidor.'}
            
            if not response.ok:
                # Cria erro com status_code e data (igual ao web)
                error = Exception(data.get('erro') or data.get('message', 'Erro na requisição'))
                error.status_code = response.status_code
                error.data = data
                raise error
            
            # Retorna no formato esperado (igual ao web)
            # O backend Flask retorna {"sugestao": "..."} ou {"erro": "..."}
            return data
            
        except requests.exceptions.ConnectionError as e:
            # Erro de conexão - servidor não está rodando ou não está acessível
            error = Exception('Erro de conexão. Verifique se o servidor Flask está rodando em http://localhost:5000')
            error.status_code = 0
            error.data = {'erro': 'Erro de conexão. Verifique se o servidor Flask está rodando em http://localhost:5000'}
            error.message = str(e)  # Armazena mensagem original para debug
            raise error
        except requests.exceptions.Timeout as e:
            # Timeout na requisição
            error = Exception('Timeout na requisição. O servidor pode estar demorando muito para responder.')
            error.status_code = 0
            error.data = {'erro': 'Timeout na requisição. O servidor pode estar demorando muito para responder.'}
            error.message = str(e)
            raise error
        except requests.exceptions.RequestException as e:
            # Outros erros de requisição
            error_msg = str(e)
            error = Exception(f'Erro na requisição: {error_msg}')
            error.status_code = 0
            error.data = {'erro': f'Erro na requisição: {error_msg}'}
            error.message = error_msg
            raise error


def _gerar_sugestao_mock(titulo: str, descricao: str) -> Dict[str, Any]:
    """Gera uma sugestão mock quando a API do Gemini não estiver disponível"""
    descricao_lower = descricao.lower()
    titulo_lower = (titulo or '').lower()
    
    # Detecta o tipo de problema baseado nas palavras-chave
    if any(palavra in descricao_lower or palavra in titulo_lower 
           for palavra in ['impressora', 'imprimir', 'print']):
        sugestao = """ANÁLISE INICIAL DO PROBLEMA:
Identifiquei problemas relacionados à impressão. Os sintomas indicam dificuldades no processo de impressão.

PROCESSO DE DIAGNÓSTICO REALIZADO:
1. Verifiquei o status do serviço de impressão no sistema operacional
2. Testei a conectividade com a impressora através do ping
3. Verifiquei os drivers instalados e sua compatibilidade
4. Analisei a fila de impressão para identificar travamentos

IDENTIFICAÇÃO DA CAUSA RAIZ:
A causa raiz foi identificada como possível problema de driver desatualizado ou fila de impressão corrompida.

AÇÕES CORRETIVAS EXECUTADAS:
1. Limpei a fila de impressão usando o comando: net stop spooler && net start spooler
2. Verifiquei e atualizei os drivers da impressora para a versão mais recente
3. Reiniciei o serviço de spooler de impressão
4. Executei teste de impressão de página de teste

VERIFICAÇÃO E TESTES DE CONFIRMAÇÃO:
Realizei teste de impressão de uma página de teste. A impressão foi concluída com sucesso, confirmando que o problema foi resolvido.

RESULTADO FINAL:
O problema de impressão foi resolvido com sucesso. A impressora está funcionando normalmente. Recomendo manter os drivers atualizados e verificar periodicamente o status do serviço de impressão."""
    
    elif any(palavra in descricao_lower or palavra in titulo_lower 
             for palavra in ['internet', 'conexão', 'rede', 'wi-fi', 'wifi', 'network']):
        sugestao = """ANÁLISE INICIAL DO PROBLEMA:
Identifiquei problemas relacionados à conectividade de rede ou internet. Os sintomas indicam falhas na conexão de rede.

PROCESSO DE DIAGNÓSTICO REALIZADO:
1. Executei diagnóstico de rede usando ipconfig /all para verificar configurações
2. Realizei teste de conectividade com ping para gateway e servidor DNS
3. Verifiquei se os adaptadores de rede estão habilitados
4. Analisei os logs do sistema de rede

IDENTIFICAÇÃO DA CAUSA RAIZ:
A causa raiz foi identificada como configuração de DNS incorreta ou adaptador de rede desabilitado.

AÇÕES CORRETIVAS EXECUTADAS:
1. Reiniciei o adaptador de rede através do Gerenciador de Dispositivos
2. Executei o comando: ipconfig /flushdns para limpar o cache DNS
3. Executei o comando: ipconfig /release seguido de ipconfig /renew para renovar o IP
4. Configurei o DNS para usar servidores públicos (8.8.8.8 e 8.8.4.4) temporariamente

VERIFICAÇÃO E TESTES DE CONFIRMAÇÃO:
Realizei teste de conectividade executando ping para google.com. O teste retornou resposta com latência de 15ms, confirmando que a conexão está funcionando.

RESULTADO FINAL:
O problema de conectividade foi resolvido com sucesso. A conexão de rede está funcionando normalmente. Recomendo verificar periodicamente as configurações de rede."""
    
    elif any(palavra in descricao_lower or palavra in titulo_lower 
             for palavra in ['email', 'outlook', 'gmail', 'correio']):
        sugestao = """ANÁLISE INICIAL DO PROBLEMA:
Identifiquei problemas relacionados ao serviço de e-mail. Os sintomas indicam dificuldades no envio ou recebimento de mensagens.

PROCESSO DE DIAGNÓSTICO REALIZADO:
1. Verifiquei as configurações da conta de e-mail
2. Testei a conectividade com o servidor de e-mail através de telnet
3. Analisei os logs do cliente de e-mail
4. Verifiquei se as credenciais estão corretas

IDENTIFICAÇÃO DA CAUSA RAIZ:
A causa raiz foi identificada como credenciais incorretas ou configurações de servidor desatualizadas.

AÇÕES CORRETIVAS EXECUTADAS:
1. Atualizei as configurações do servidor de e-mail com os parâmetros corretos
2. Removi e recriei o perfil de e-mail do usuário
3. Executei teste de envio e recebimento de e-mail de teste
4. Configurei a sincronização automática do cliente de e-mail

VERIFICAÇÃO E TESTES DE CONFIRMAÇÃO:
Realizei teste de envio de e-mail para conta externa e recebimento de e-mail de teste. Ambos os testes foram bem-sucedidos, confirmando que o serviço está funcionando.

RESULTADO FINAL:
O problema de e-mail foi resolvido com sucesso. O cliente de e-mail está funcionando normalmente. Recomendo verificar periodicamente as configurações e manter as credenciais atualizadas."""
    
    else:
        sugestao = f"""ANÁLISE INICIAL DO PROBLEMA:
Analisei o chamado relacionado a "{titulo}". Com base na descrição fornecida, identifiquei que há necessidade de intervenção técnica.

PROCESSO DE DIAGNÓSTICO REALIZADO:
1. Analisei a descrição detalhada do problema reportado
2. Verifiquei os logs do sistema para identificar possíveis erros relacionados
3. Realizei verificação das configurações do sistema
4. Testei funcionalidades relacionadas ao problema reportado

IDENTIFICAÇÃO DA CAUSA RAIZ:
Após análise detalhada, identifiquei que a causa raiz está relacionada às questões mencionadas na descrição do chamado.

AÇÕES CORRETIVAS EXECUTADAS:
1. Executei procedimentos de diagnóstico específicos para o problema
2. Realizei ajustes necessários nas configurações do sistema
3. Apliquei correções apropriadas para resolver o problema identificado
4. Executei testes para validar as correções aplicadas

VERIFICAÇÃO E TESTES DE CONFIRMAÇÃO:
Realizei testes para confirmar que o problema foi resolvido. Os testes indicaram que a solução aplicada está funcionando corretamente.

RESULTADO FINAL:
O problema reportado foi resolvido com sucesso. O sistema está funcionando normalmente. Recomendo monitorar o sistema para garantir que o problema não se repita."""
    
    return {'sugestao': sugestao}
