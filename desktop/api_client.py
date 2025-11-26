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
    FLASK_BASE_URL = 'http://localhost:5000'
    API_URL_BASE = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net'
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
        self.base_url = FLASK_BASE_URL
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
        """Faz login do usuário - exatamente como no web (api.js authService.login)"""
        # Envia exatamente como o web: { email: username, senha: password }
        return api_client.post('/login', {'email': email, 'senha': password}, include_auth=False)
    
    @staticmethod
    def logout():
        """Faz logout do usuário"""
        api_client.clear_auth_token()
        return {'message': 'Logout realizado com sucesso'}
    
    @staticmethod
    def is_authenticated() -> bool:
        """Verifica se o usuário está autenticado"""
        return api_client.get_auth_token() is not None


class UserService:
    """Serviço de usuários - EXATAMENTE como no web (api.js)"""
    
    @staticmethod
    def register(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Registra um novo usuário - igual ao web"""
        return api_client.post('/register', user_data, include_auth=False)
    
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
        """Atualiza dados do usuário - igual ao web: /api/Usuarios/{id}"""
        return api_client.put(f'/api/Usuarios/{user_id}', user_data)
    
    @staticmethod
    def delete_user(user_id: int) -> Dict[str, Any]:
        """Remove usuário - igual ao web: /api/Usuarios/{id}"""
        return api_client.delete(f'/api/Usuarios/{user_id}')
    
    @staticmethod
    def alterar_senha(senha_atual: str, nova_senha: str) -> Dict[str, Any]:
        """Altera senha do usuário - igual ao web: /api/Usuarios/alterar-senha"""
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
        """Atualiza perfil do usuário logado - igual ao web: /api/Usuarios/meu-perfil"""
        return api_client.put('/api/Usuarios/meu-perfil', user_data)


class TicketService:
    """Serviço de tickets/chamados - EXATAMENTE como no web (api.js)"""
    
    @staticmethod
    def create_ticket(ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo ticket - igual ao web: POST /chamados"""
        try:
            return api_client.post('/chamados', ticket_data)
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
            
            endpoint = '/chamados'
            if query_params:
                endpoint = f'/chamados?{"&".join(query_params)}'
            
            response = api_client.get(endpoint)
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
        """Obtém um ticket específico - igual ao web: GET /chamados/{id}"""
        try:
            return api_client.get(f'/chamados/{ticket_id}')
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
        """Atualiza um ticket - igual ao web: PUT /chamados/{id}"""
        try:
            return api_client.put(f'/chamados/{ticket_id}', ticket_data)
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
        """Remove um ticket - igual ao web: DELETE /chamados/{id}"""
        try:
            return api_client.delete(f'/chamados/{ticket_id}')
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
    """Serviço para integração com IA (Gemini)"""
    
    @staticmethod
    def gerar_sugestao(titulo: str, descricao: str) -> Dict[str, Any]:
        """Gera uma sugestão de resposta técnica usando Gemini AI"""
        try:
            response = api_client.post('/api/gemini/sugerir-resposta', {
                'titulo': titulo or '',
                'descricao': descricao
            }, include_auth=False)
            return response
        except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as e:
            # Fallback para sugestão mock quando a API não estiver disponível
            print(f"[AIService] Erro ao conectar com API do Gemini: {e}")
            print("[AIService] Usando sugestão mock como fallback")
            return _gerar_sugestao_mock(titulo or '', descricao)
        except Exception as e:
            # Se o erro for sobre API não configurada, usa fallback mock
            error_str = str(e).lower()
            if 'gemini' in error_str or 'api' in error_str or 'configurada' in error_str or 'erro' in error_str:
                print(f"[AIService] API do Gemini não disponível: {e}")
                print("[AIService] Usando sugestão mock como fallback")
                return _gerar_sugestao_mock(titulo or '', descricao)
            raise


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
