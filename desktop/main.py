"""
HelpWave Desktop - Aplicação Principal
Versão desktop baseada no projeto web
"""
import customtkinter as ctk
from login_page import LoginPage
from home_page import HomePage
from pages.register_employee_page import RegisterEmployeePage
from pages.new_ticket_page import NewTicketPage
from pages.pending_tickets_page import PendingTicketsPage
from pages.completed_tickets_page import CompletedTicketsPage
from pages.reports_page import ReportsPage
from pages.ticket_detail_page import TicketDetailPage
from pages.my_tickets_page import MyTicketsPage
from pages.contact_page import ContactPage
from pages.faq_page import FAQPage
from pages.user_profile_page import UserProfilePage
from pages.admin_page import AdminPage
from components.first_access_modal import FirstAccessModal
from components.loading_screen import LoadingScreen
from api_client import api_client, AuthService, UserService
import sys
import os
import threading

# Configuração do CustomTkinter
ctk.set_appearance_mode("light")  # Modo claro
ctk.set_default_color_theme("blue")  # Tema padrão (vamos customizar depois)

class AppManager:
    """
    Gerencia o fluxo principal do aplicativo, alternando entre as telas
    Baseado na estrutura do App.jsx do projeto web
    """
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("HelpWave - Sistema de Suporte Técnico")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)  # Largura mínima para acomodar todas as colunas da tabela
        
        # Configura o grid do root para usar grid em todos os frames
        # O root precisa ocupar toda a tela
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Maximiza a janela ao iniciar (após update_idletasks)
        self.root.update_idletasks()
        # Usa after para garantir que a janela esteja totalmente inicializada
        self.root.after(100, self._maximize_window)
        
        # Estado da aplicação
        self.current_page = 'home'
        self.user_info = None
        self.is_logged_in = False
        self.selected_ticket_id = None
        self.previous_page = None
        self.show_first_access_modal = False
        self.is_loading = True
        
        # Frame principal
        self.main_frame = None
        
        # Mostra loading screen inicialmente
        self._show_loading_screen()
        
        # Verifica autenticação ao iniciar (igual ao web)
        self.check_auth()
    
    def _maximize_window(self):
        """Maximiza a janela"""
        try:
            # Obtém a janela Tkinter subjacente
            tk_window = self.root.winfo_toplevel()
            
            # Tenta maximizar usando state (Windows)
            try:
                tk_window.state('zoomed')
                return
            except:
                pass
            
            # Tenta maximizar usando attributes (Linux)
            try:
                tk_window.attributes('-zoomed', True)
                return
            except:
                pass
            
            # Fallback: usa geometry para tela cheia
            self.root.update_idletasks()
            width = self.root.winfo_screenwidth()
            height = self.root.winfo_screenheight()
            self.root.geometry(f"{width}x{height}+0+0")
        except Exception as e:
            print(f"Erro ao maximizar janela: {e}")
            # Fallback final
            self.root.update_idletasks()
            width = self.root.winfo_screenwidth()
            height = self.root.winfo_screenheight()
            self.root.geometry(f"{width}x{height}+0+0")
    
    def _show_loading_screen(self):
        """Mostra tela de carregamento"""
        if self.main_frame:
            self.main_frame.destroy()
        self.main_frame = LoadingScreen(self.root, "Carregando...")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    
    def check_auth(self):
        """Verifica autenticação ao iniciar - igual ao web App.jsx checkAuth"""
        def do_check_auth():
            try:
                token = api_client.get_auth_token()
                print(f"[AppManager] Verificando autenticação, token existe: {bool(token)}")
                
                if token:
                    # Verifica se o token é válido e obtém informações do usuário
                    user_info_from_token = AuthService.get_user_info()
                    print(f"[AppManager] userInfoFromToken: {user_info_from_token}")
                    
                    if user_info_from_token:
                        user_id = (user_info_from_token.get('sub') or 
                                  user_info_from_token.get('id') or 
                                  user_info_from_token.get('userId') or 
                                  user_info_from_token.get('user_id'))
                        print(f"[AppManager] userId extraído: {user_id}")
                        
                        # Busca informações completas do usuário usando endpoint /meu-perfil
                        try:
                            print('[AppManager] Buscando dados do perfil via /api/Usuarios/meu-perfil')
                            full_user_data = UserService.get_meu_perfil()
                            
                            if full_user_data:
                                # Normaliza dados usando função auxiliar
                                normalized_data = self._normalize_user_data(
                                    full_user_data, 
                                    user_info_from_token, 
                                    full_user_data.get('email') or full_user_data.get('Email') or ''
                                )
                                print(f'[AppManager] Dados normalizados: {normalized_data}')
                                
                                self.user_info = normalized_data
                                self.is_logged_in = True
                                
                                # Verifica se é primeiro acesso
                                primeiro_acesso_raw = (
                                    full_user_data.get('primeiroAcesso') if full_user_data.get('primeiroAcesso') is not None else
                                    full_user_data.get('PrimeiroAcesso') if full_user_data.get('PrimeiroAcesso') is not None else
                                    normalized_data.get('primeiroAcesso') if normalized_data.get('primeiroAcesso') is not None else
                                    False
                                )
                                
                                primeiro_acesso = (
                                    primeiro_acesso_raw == True or 
                                    primeiro_acesso_raw == 'true' or 
                                    primeiro_acesso_raw == 1 or
                                    primeiro_acesso_raw == '1'
                                )
                                
                                print(f'[AppManager] PrimeiroAcesso: {primeiro_acesso}')
                                
                                if primeiro_acesso:
                                    self.show_first_access_modal = True
                                
                                # Atualiza UI na thread principal
                                self.root.after(0, self._on_auth_success)
                            else:
                                # Token inválido, limpa o token
                                print('[AppManager] Token inválido ou usuário não encontrado')
                                api_client.clear_auth_token()
                                self.root.after(0, self._on_auth_fail)
                        except Exception as e:
                            print(f'[AppManager] Erro ao buscar perfil da API: {e}')
                            # Se não conseguir buscar da API, usa dados do token normalizados
                            normalized_data = self._normalize_user_data({}, user_info_from_token, user_info_from_token.get('email', ''))
                            self.user_info = normalized_data
                            self.is_logged_in = True
                            self.root.after(0, self._on_auth_success)
                    else:
                        # Token inválido
                        print('[AppManager] Token inválido (não foi possível decodificar)')
                        api_client.clear_auth_token()
                        self.root.after(0, self._on_auth_fail)
                else:
                    print('[AppManager] Nenhum token encontrado')
                    self.root.after(0, self._on_auth_fail)
            except Exception as e:
                print(f'[AppManager] Erro ao verificar autenticação: {e}')
                api_client.clear_auth_token()
                self.root.after(0, self._on_auth_fail)
            finally:
                self.is_loading = False
        
        # Executa em thread separada
        threading.Thread(target=do_check_auth, daemon=True).start()
    
    def _normalize_user_data(self, user_data, token_payload=None, email=''):
        """Normaliza os dados do usuário - igual ao web normalizeUserData"""
        # Tenta obter nome de várias fontes (prioriza dados da API)
        nome = (user_data.get('nome') or user_data.get('Nome') or 
                user_data.get('name') or user_data.get('Name') or '')
        
        # Se não encontrou, tenta do token
        if not nome or nome.strip() == '':
            if token_payload:
                nome = (token_payload.get('nome') or token_payload.get('Nome') or 
                       token_payload.get('name') or token_payload.get('Name') or
                       token_payload.get('unique_name') or token_payload.get('preferred_username') or 
                       token_payload.get('upn') or '')
        
        # Se ainda não tem nome válido, tenta usar o email
        if not nome or nome.strip() == '' or nome == email:
            email_to_use = user_data.get('email') or user_data.get('Email') or email or ''
            if email_to_use and '@' in email_to_use:
                import re
                email_parts = re.split(r'[._-]', email_to_use.split('@')[0])
                nome = ' '.join([part.capitalize() for part in email_parts])
        
        # Garante que o nome não seja vazio
        if not nome or nome.strip() == '':
            nome = 'Usuário'
        
        # Extrai PrimeiroAcesso de todas as possíveis variações
        primeiro_acesso_value = (
            user_data.get('primeiroAcesso') if user_data.get('primeiroAcesso') is not None else
            user_data.get('PrimeiroAcesso') if user_data.get('PrimeiroAcesso') is not None else
            user_data.get('primeiro_acesso') if user_data.get('primeiro_acesso') is not None else
            False
        )
        
        return {
            'id': (user_data.get('id') or user_data.get('Id') or 
                  token_payload.get('sub') if token_payload else None or
                  token_payload.get('userId') if token_payload else None or
                  token_payload.get('id') if token_payload else None),
            'nome': nome.strip(),
            'email': user_data.get('email') or user_data.get('Email') or email or '',
            'telefone': user_data.get('telefone') or user_data.get('Telefone') or '',
            'cargo': user_data.get('cargo') or user_data.get('Cargo') or '',
            'permissao': (
                user_data.get('permissao') if user_data.get('permissao') is not None else
                (user_data.get('Permissao') if user_data.get('Permissao') is not None else
                (token_payload.get('role') if token_payload and token_payload.get('role') else 1))),
            'primeiroAcesso': primeiro_acesso_value
        }
    
    def _on_auth_success(self):
        """Callback quando autenticação é bem-sucedida"""
        if self.show_first_access_modal:
            self.show_home_page()
            self.root.after(200, self._show_first_access_modal)
        else:
            self.show_home_page()
    
    def _on_auth_fail(self):
        """Callback quando autenticação falha"""
        self.show_login_page()
    
    def show_login_page(self):
        """Exibe a tela de login"""
        self.is_logged_in = False
        self.current_page = 'login'
        self.user_info = None
        
        # Remove o frame anterior
        if self.main_frame:
            self.main_frame.destroy()
            self.main_frame = None
        
        # Cria o LoginPage
        self.main_frame = LoginPage(self.root, self.on_login_success)
        # Usa grid para compatibilidade com o layout interno do LoginPage
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Força atualização e foca no campo de usuário após renderização
        self.root.update_idletasks()
        self.root.after(100, self._focus_login_field)
    
    def _focus_login_field(self):
        """Foca no campo de usuário após logout"""
        try:
            if self.main_frame and hasattr(self.main_frame, 'username_entry'):
                self.main_frame.username_entry.focus_set()
                self.main_frame.username_entry.icursor(0)  # Posiciona cursor no início
        except:
            pass
    
    def on_login_success(self, user_data):
        """Callback chamada quando o login é bem-sucedido - igual ao web"""
        self.is_logged_in = True
        self.current_page = 'home'
        
        # Busca dados completos do usuário via /api/Usuarios/meu-perfil (igual ao web App.jsx)
        # Isso garante que temos todos os dados atualizados do banco de dados
        try:
            from api_client import UserService
            full_user_data = UserService.get_meu_perfil()
            if full_user_data:
                # Normaliza dados (igual ao web normalizeUserData)
                self.user_info = {
                    'id': full_user_data.get('id') or full_user_data.get('Id'),
                    'nome': full_user_data.get('nome') or full_user_data.get('Nome') or user_data.get('nome', ''),
                    'email': full_user_data.get('email') or full_user_data.get('Email') or user_data.get('email', ''),
                    'telefone': full_user_data.get('telefone') or full_user_data.get('Telefone') or user_data.get('telefone', ''),
                    'cargo': full_user_data.get('cargo') or full_user_data.get('Cargo') or user_data.get('cargo', ''),
                    'permissao': full_user_data.get('permissao') or full_user_data.get('Permissao') or user_data.get('permissao', 1),
                    'primeiroAcesso': full_user_data.get('primeiroAcesso') or full_user_data.get('PrimeiroAcesso') or False
                }
            else:
                # Fallback: usa dados do login
                self.user_info = user_data
        except Exception as e:
            print(f"[AppManager] Erro ao buscar perfil completo: {e}")
            # Fallback: usa dados do login
            self.user_info = user_data
        
        # Verifica se é primeiro acesso
        primeiro_acesso = self.user_info.get('primeiroAcesso', False) or self.user_info.get('PrimeiroAcesso', False)
        if primeiro_acesso:
            self.show_first_access_modal = True
            self.show_home_page()
            # Mostra modal após um pequeno delay
            self.root.after(200, self._show_first_access_modal)
        else:
            self.show_home_page()
    
    def _show_first_access_modal(self):
        """Mostra modal de primeiro acesso"""
        if self.show_first_access_modal and self.main_frame:
            modal = FirstAccessModal(
                self.main_frame,
                is_open=True,
                on_success=self._handle_first_access_success
            )
    
    def _handle_first_access_success(self):
        """Lida com sucesso do primeiro acesso - igual ao web handleFirstAccessSuccess"""
        self.show_first_access_modal = False
        
        # Recarrega os dados do usuário após alterar a senha
        def reload_user_data():
            try:
                full_user_data = UserService.get_meu_perfil()
                if full_user_data:
                    user_info_from_token = AuthService.get_user_info()
                    normalized_data = self._normalize_user_data(
                        full_user_data, 
                        user_info_from_token, 
                        full_user_data.get('email') or full_user_data.get('Email') or ''
                    )
                    self.user_info = normalized_data
                    print('[AppManager] Dados do usuário recarregados após primeiro acesso')
            except Exception as e:
                print(f'[AppManager] Erro ao recarregar dados do usuário: {e}')
        
        threading.Thread(target=reload_user_data, daemon=True).start()
    
    def show_home_page(self):
        """Exibe a página inicial/dashboard - igual ao web"""
        if not self.is_logged_in:
            self.show_login_page()
            return
        
        # Remove o frame anterior
        if self.main_frame:
            self.main_frame.destroy()
            self.main_frame = None
        
        # Cria HomePage diretamente (igual ao web)
        self.main_frame = HomePage(
            self.root,
            on_logout=self.handle_logout,
            on_navigate_to_register=self.navigate_to_register,
            on_navigate_to_new_ticket=self.navigate_to_new_ticket,
            on_navigate_to_page=self.navigate_to_page,
            current_page=self.current_page,
            user_info=self.user_info,
            on_navigate_to_profile=self.navigate_to_profile
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    
    def handle_logout(self):
        """Lida com o logout - igual ao web"""
        api_client.clear_auth_token()
        self.is_logged_in = False
        self.current_page = 'home'
        self.user_info = None
        self.show_login_page()
    
    def navigate_to_page(self, page_id):
        """Navega para uma página específica - igual ao web"""
        self.current_page = page_id
        
        if page_id == 'home':
            self.show_home_page()
        elif page_id == 'register':
            self.show_register_page()
        elif page_id == 'newticket':
            self.show_new_ticket_page()
        elif page_id == 'pending-tickets':
            self.show_pending_tickets_page()
        elif page_id == 'completed-tickets':
            self.show_completed_tickets_page()
        elif page_id == 'my-tickets':
            self.show_my_tickets_page()
        elif page_id == 'reports':
            self.show_reports_page()
        elif page_id == 'dashboard':
            self.show_dashboard_page()
        elif page_id == 'ticket-detail':
            self.show_ticket_detail_page()
        elif page_id == 'profile':
            self.show_profile_page()
        elif page_id == 'faq':
            self.show_faq_page()
        elif page_id == 'contact':
            self.show_contact_page()
        elif page_id == 'user-activity':
            self.show_user_activity_page()
        elif page_id == 'admin':
            self.show_admin_page()
        else:
            self.show_home_page()
    
    def navigate_to_register(self):
        """Navega para página de cadastro - igual ao web"""
        self.current_page = 'register'
        self.show_register_page()
    
    def navigate_to_new_ticket(self):
        """Navega para página de novo ticket - igual ao web"""
        self.current_page = 'newticket'
        self.show_new_ticket_page()
    
    def navigate_to_home(self):
        """Navega para home - igual ao web"""
        self.current_page = 'home'
        self.show_home_page()
    
    def navigate_to_ticket_detail(self, ticket_id, from_page=None):
        """Navega para detalhes do ticket - igual ao web"""
        self.selected_ticket_id = ticket_id
        self.previous_page = from_page or self.current_page
        self.current_page = 'ticket-detail'
        self.show_ticket_detail_page()
    
    def navigate_to_profile(self):
        """Navega para página de perfil - igual ao web"""
        self.current_page = 'profile'
        self.show_profile_page()
    
    def show_my_tickets_page(self):
        """Exibe página de meus chamados (colaboradores)"""
        if not self.is_logged_in:
            self.show_login_page()
            return
        
        # Usa HomePage para gerenciar Header e Sidebar
        if not isinstance(self.main_frame, HomePage):
            if self.main_frame:
                self.main_frame.destroy()
                self.main_frame = None
            
            self.main_frame = HomePage(
                self.root,
                user_info=self.user_info,
                on_logout=self.handle_logout,
                on_navigate=self.navigate_to_page,
                current_page='my-tickets',
                on_navigate_to_register=self.navigate_to_register,
                on_navigate_to_new_ticket=self.navigate_to_new_ticket,
                on_navigate_to_page=self.navigate_to_page,
                on_navigate_to_profile=self.navigate_to_profile
            )
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        else:
            # Se já é HomePage, apenas navega para a página
            self.main_frame.show_page('my-tickets')
    
    def show_profile_page(self):
        """Exibe página de perfil"""
        if not self.is_logged_in:
            self.show_login_page()
            return
        
        if self.main_frame:
            self.main_frame.destroy()
            self.main_frame = None
        
        from home_page import HomePage
        self.main_frame = HomePage(
            self.root,
            user_info=self.user_info,
            on_logout=self.handle_logout,
            on_navigate=self.navigate_to_page,
            current_page='profile',
            on_navigate_to_register=self.navigate_to_register,
            on_navigate_to_new_ticket=self.navigate_to_new_ticket,
            on_navigate_to_page=self.navigate_to_page,
            on_navigate_to_profile=self.navigate_to_profile
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    
    def show_faq_page(self):
        """Exibe página FAQ"""
        if not self.is_logged_in:
            self.show_login_page()
            return
        
        if self.main_frame:
            self.main_frame.destroy()
            self.main_frame = None
        
        from home_page import HomePage
        self.main_frame = HomePage(
            self.root,
            user_info=self.user_info,
            on_logout=self.handle_logout,
            on_navigate=self.navigate_to_page,
            current_page='faq',
            on_navigate_to_register=self.navigate_to_register,
            on_navigate_to_new_ticket=self.navigate_to_new_ticket,
            on_navigate_to_page=self.navigate_to_page,
            on_navigate_to_profile=self.navigate_to_profile
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    
    def show_contact_page(self):
        """Exibe página de contato"""
        if not self.is_logged_in:
            self.show_login_page()
            return
        
        if self.main_frame:
            self.main_frame.destroy()
            self.main_frame = None
        
        from home_page import HomePage
        self.main_frame = HomePage(
            self.root,
            user_info=self.user_info,
            on_logout=self.handle_logout,
            on_navigate=self.navigate_to_page,
            current_page='contact',
            on_navigate_to_register=self.navigate_to_register,
            on_navigate_to_new_ticket=self.navigate_to_new_ticket,
            on_navigate_to_page=self.navigate_to_page,
            on_navigate_to_profile=self.navigate_to_profile
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    
    def show_dashboard_page(self):
        """Exibe página de dashboard (admin)"""
        if not self.is_logged_in:
            self.show_login_page()
            return
        
        # Usa HomePage para gerenciar Header e Sidebar
        if not isinstance(self.main_frame, HomePage):
            if self.main_frame:
                self.main_frame.destroy()
                self.main_frame = None
            
            self.main_frame = HomePage(
                self.root,
                user_info=self.user_info,
                on_logout=self.handle_logout,
                on_navigate=self.navigate_to_page,
                current_page='dashboard',
                on_navigate_to_register=self.navigate_to_register,
                on_navigate_to_new_ticket=self.navigate_to_new_ticket,
                on_navigate_to_page=self.navigate_to_page,
                on_navigate_to_profile=self.navigate_to_profile
            )
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        else:
            # Se já é HomePage, apenas navega para a página
            self.main_frame.show_page('dashboard')
    
    def show_user_activity_page(self):
        """Exibe página de atividade do usuário"""
        if not self.is_logged_in:
            self.show_login_page()
            return
        
        # Tenta obter userId do arquivo temporário
        userId = None
        try:
            if os.path.exists('.temp_user_id'):
                with open('.temp_user_id', 'r') as f:
                    userId = int(f.read().strip())
                os.remove('.temp_user_id')
        except:
            pass
        
        # Usa HomePage para gerenciar Header e Sidebar
        if not isinstance(self.main_frame, HomePage):
            if self.main_frame:
                self.main_frame.destroy()
                self.main_frame = None
            
            self.main_frame = HomePage(
                self.root,
                user_info=self.user_info,
                on_logout=self.handle_logout,
                on_navigate=self.navigate_to_page,
                current_page='user-activity',
                on_navigate_to_register=self.navigate_to_register,
                on_navigate_to_new_ticket=self.navigate_to_new_ticket,
                on_navigate_to_page=self.navigate_to_page,
                on_navigate_to_profile=self.navigate_to_profile
            )
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Navega para a página com userId
        self.main_frame.show_page('user-activity', userId=userId)
    
    def show_page(self):
        """Mostra a página atual baseada em current_page"""
        if self.current_page == 'home':
            self.show_home_page()
        elif self.current_page == 'register':
            self.show_register_page()
        elif self.current_page == 'newticket':
            self.show_new_ticket_page()
        elif self.current_page == 'pending-tickets':
            self.show_pending_tickets_page()
        elif self.current_page == 'completed-tickets':
            self.show_completed_tickets_page()
        elif self.current_page == 'reports':
            self.show_reports_page()
        elif self.current_page == 'ticket-detail':
            self.show_ticket_detail_page()
        else:
            self.show_home_page()
    
    def show_register_page(self):
        """Exibe página de cadastro de funcionário"""
        if not self.is_logged_in:
            self.show_login_page()
            return
        
        # Usa HomePage para gerenciar Header e Sidebar
        if not isinstance(self.main_frame, HomePage):
            if self.main_frame:
                self.main_frame.destroy()
                self.main_frame = None
            
            self.main_frame = HomePage(
                self.root,
                user_info=self.user_info,
                on_logout=self.handle_logout,
                on_navigate=self.navigate_to_page,
                current_page='register',
                on_navigate_to_register=self.navigate_to_register,
                on_navigate_to_new_ticket=self.navigate_to_new_ticket,
                on_navigate_to_page=self.navigate_to_page,
                on_navigate_to_profile=self.navigate_to_profile
            )
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        else:
            # Se já é HomePage, apenas navega para a página
            self.main_frame.show_page('register')
    
    def show_new_ticket_page(self):
        """Exibe página de novo ticket"""
        if not self.is_logged_in:
            self.show_login_page()
            return
        
        # Usa HomePage para gerenciar Header e Sidebar
        if not isinstance(self.main_frame, HomePage):
            if self.main_frame:
                self.main_frame.destroy()
                self.main_frame = None
            
            self.main_frame = HomePage(
                self.root,
                user_info=self.user_info,
                on_logout=self.handle_logout,
                on_navigate=self.navigate_to_page,
                current_page='newticket',
                on_navigate_to_register=self.navigate_to_register,
                on_navigate_to_new_ticket=self.navigate_to_new_ticket,
                on_navigate_to_page=self.navigate_to_page,
                on_navigate_to_profile=self.navigate_to_profile
            )
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        else:
            # Se já é HomePage, apenas navega para a página
            self.main_frame.show_page('newticket')
    
    def show_pending_tickets_page(self):
        """Exibe página de chamados em andamento"""
        if not self.is_logged_in:
            self.show_login_page()
            return
        
        # Usa HomePage para gerenciar Header e Sidebar
        if not isinstance(self.main_frame, HomePage):
            if self.main_frame:
                self.main_frame.destroy()
                self.main_frame = None
            
            self.main_frame = HomePage(
                self.root,
                user_info=self.user_info,
                on_logout=self.handle_logout,
                on_navigate=self.navigate_to_page,
                current_page='pending-tickets',
                on_navigate_to_register=self.navigate_to_register,
                on_navigate_to_new_ticket=self.navigate_to_new_ticket,
                on_navigate_to_page=self.navigate_to_page,
                on_navigate_to_profile=self.navigate_to_profile
            )
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        else:
            # Se já é HomePage, apenas navega para a página
            self.main_frame.show_page('pending-tickets')
    
    def show_completed_tickets_page(self):
        """Exibe página de chamados concluídos"""
        if not self.is_logged_in:
            self.show_login_page()
            return
        
        # Usa HomePage para gerenciar Header e Sidebar
        if not isinstance(self.main_frame, HomePage):
            if self.main_frame:
                self.main_frame.destroy()
                self.main_frame = None
            
            self.main_frame = HomePage(
                self.root,
                user_info=self.user_info,
                on_logout=self.handle_logout,
                on_navigate=self.navigate_to_page,
                current_page='completed-tickets',
                on_navigate_to_register=self.navigate_to_register,
                on_navigate_to_new_ticket=self.navigate_to_new_ticket,
                on_navigate_to_page=self.navigate_to_page,
                on_navigate_to_profile=self.navigate_to_profile
            )
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        else:
            # Se já é HomePage, apenas navega para a página
            self.main_frame.show_page('completed-tickets')
    
    def show_reports_page(self):
        """Exibe página de relatórios"""
        if not self.is_logged_in:
            self.show_login_page()
            return
        
        # Usa HomePage para gerenciar Header e Sidebar
        if not isinstance(self.main_frame, HomePage):
            if self.main_frame:
                self.main_frame.destroy()
                self.main_frame = None
            
            self.main_frame = HomePage(
                self.root,
                user_info=self.user_info,
                on_logout=self.handle_logout,
                on_navigate=self.navigate_to_page,
                current_page='reports',
                on_navigate_to_register=self.navigate_to_register,
                on_navigate_to_new_ticket=self.navigate_to_new_ticket,
                on_navigate_to_page=self.navigate_to_page,
                on_navigate_to_profile=self.navigate_to_profile
            )
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        else:
            # Se já é HomePage, apenas navega para a página
            self.main_frame.show_page('reports')
    
    def show_ticket_detail_page(self):
        """Exibe página de detalhes do ticket"""
        if not self.is_logged_in:
            self.show_login_page()
            return
        
        if self.main_frame:
            self.main_frame.destroy()
            self.main_frame = None
        
        from home_page import HomePage
        self.main_frame = HomePage(
            self.root,
            user_info=self.user_info,
            on_logout=self.handle_logout,
            on_navigate=self.navigate_to_page,
            current_page='ticket-detail',
            on_navigate_to_register=self.navigate_to_register,
            on_navigate_to_new_ticket=self.navigate_to_new_ticket,
            on_navigate_to_page=self.navigate_to_page,
            on_navigate_to_profile=self.navigate_to_profile
        )
        # Navega para a página de detalhes com os parâmetros corretos
        self.main_frame.show_page('ticket-detail', ticket_id=self.selected_ticket_id, previous_page=self.previous_page)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    
    def run(self):
        """Inicia o loop principal da aplicação"""
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = AppManager()
        app.run()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

