"""
Página de Login
Baseada no LoginPage.jsx do projeto web
"""
import customtkinter as ctk
import tkinter as tk
from api_client import AuthService, api_client
from components.toast import show_toast
from components.forgot_password_modal import ForgotPasswordModal
from config import COLORS, ADMIN_USER
import threading
import os


class LoginPage(ctk.CTkFrame):
    """Página de login do HelpWave"""
    
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        
        self.on_login_success = on_login_success
        self.is_loading = False
        self.login_canvas = None
        self.update_scroll_region = None
        self.forgot_password_modal = None
        self.remember_email_file = os.path.join(os.path.expanduser('~'), '.helpwave_remembered_email')
        
        # Carrega email lembrado se existir
        self.remembered_email = self._load_remembered_email()
        
        # Configuração do frame - gradiente vermelho como fundo
        self.configure(fg_color=COLORS['primary'])
        
        # Configuração do grid para layout em 2 colunas (hero | formulário)
        # 60% vermelho / 40% branco - usando proporção 6:4
        self.grid_columnconfigure(0, weight=6)  # Hero vermelho - 60%
        self.grid_columnconfigure(1, weight=4)  # Formulário branco - 40%
        self.grid_rowconfigure(0, weight=1)
        
        # Seção Hero (esquerda) - com gradiente vermelho
        hero_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS['primary'],
            corner_radius=0
        )
        hero_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        hero_frame.grid_columnconfigure(0, weight=1)
        hero_frame.grid_rowconfigure(0, weight=1)
        
        hero_container = ctk.CTkFrame(hero_frame, fg_color="transparent")
        hero_container.grid(row=0, column=0, sticky="")
        
        hero_label = ctk.CTkLabel(
            hero_container,
            text="HelpWave - Simplificando o seu suporte.",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=COLORS['text_inverse']
        )
        hero_label.pack(pady=20)
        
        # Frame do formulário - diretamente no grid, sem container branco
        form_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        form_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_rowconfigure(0, weight=1)
        
        # Função para ajustar proporções dinamicamente (60% vermelho / 40% branco)
        def adjust_proportions(event=None):
            try:
                # Verifica se o evento é da janela principal
                if event and hasattr(event, 'widget'):
                    widget = event.widget
                    if widget != self and widget != self.winfo_toplevel():
                        return
                
                total_width = self.winfo_width()
                if total_width > 450:  # Só ajusta se janela for grande o suficiente
                    # Calcula larguras exatas para 60/40
                    hero_width = int(total_width * 0.6)
                    form_width = int(total_width * 0.4)
                    # Força as larguras através do minsize, mas mantém weight para expansão
                    self.grid_columnconfigure(0, weight=6, minsize=max(hero_width, 200))
                    self.grid_columnconfigure(1, weight=4, minsize=max(form_width, 250))
            except Exception as e:
                # Ignora erros durante configuração inicial
                pass
        
        # Bind para redimensionamento da janela
        root = self.winfo_toplevel()
        def on_window_configure(e):
            if e.widget == root:
                adjust_proportions()
        root.bind("<Configure>", on_window_configure)
        
        # Ajusta proporções após inicialização
        self.after(100, adjust_proportions)
        
        # Container interno scrollável para o conteúdo do formulário
        # Canvas e Scrollbar para scroll vertical
        canvas = tk.Canvas(form_frame, highlightthickness=0, bg="white")
        scrollbar = tk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        # Variável para armazenar o window_id do canvas
        canvas_window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.login_canvas = canvas
        self.scrollable_frame = scrollable_frame
        self.canvas_window_id = canvas_window_id
        
        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Centraliza verticalmente se o conteúdo for menor que a altura do canvas
            canvas.update_idletasks()
            canvas_height = canvas.winfo_height()
            frame_height = scrollable_frame.winfo_reqheight()
            if frame_height < canvas_height and canvas_height > 1:
                # Centraliza o frame verticalmente
                y_pos = (canvas_height - frame_height) // 2
                canvas.coords(canvas_window_id, 0, y_pos)
            else:
                # Se precisa scroll, mantém no topo
                canvas.coords(canvas_window_id, 0, 0)
        
        self.update_scroll_region = update_scroll_region
        scrollable_frame.bind("<Configure>", update_scroll_region)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def on_canvas_configure(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window_id, width=canvas_width)
            update_scroll_region()
        
        canvas.bind("<Configure>", on_canvas_configure)
        
        canvas.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        scrollbar.grid(row=0, column=1, sticky="ns")
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_rowconfigure(0, weight=1)
        
        # Container interno para centralizar o conteúdo
        form_content = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        form_content.pack(fill="x", padx=40, pady=40)
        form_content.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            form_content,
            text="LOGIN",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=COLORS['secondary']
        )
        title_label.pack(pady=(0, 30))
        
        # Campo de usuário - se adapta ao container
        self.username_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="USUÁRIO",
            height=50,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_width=1
        )
        self.username_entry.pack(fill="x", pady=(0, 20))
        
        # Foca no campo de usuário após renderização
        self.after(150, lambda: self.username_entry.focus_set())
        
        # Campo de senha
        password_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 20))
        
        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="SENHA",
            height=50,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_width=1,
            show="*"
        )
        self.password_entry.pack(side="left", fill="x", expand=True)
        
        # Botão mostrar/ocultar senha
        self.show_password_var = ctk.BooleanVar(value=False)
        show_password_btn = ctk.CTkCheckBox(
            password_frame,
            text="👁",
            variable=self.show_password_var,
            command=self.toggle_password,
            width=50,
            height=50,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_dark']
        )
        show_password_btn.pack(side="right", padx=(10, 0))
        
        # Opções (Lembrar, Esqueci senha)
        options_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        options_frame.pack(fill="x", pady=(0, 20))
        
        self.remember_var = ctk.BooleanVar(value=bool(self.remembered_email))
        remember_check = ctk.CTkCheckBox(
            options_frame,
            text="Lembrar",
            font=ctk.CTkFont(size=12),
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_dark'],
            variable=self.remember_var
        )
        remember_check.pack(side="left")
        
        forgot_password_btn = ctk.CTkButton(
            options_frame,
            text="Esqueci a senha",
            font=ctk.CTkFont(size=12, underline=True),
            fg_color="transparent",
            text_color=COLORS['text_secondary'],
            hover_color=COLORS['neutral_100'],
            anchor="w",
            command=self.handle_forgot_password
        )
        forgot_password_btn.pack(side="right")
        
        # Botão de login - se adapta ao container
        self.login_button = ctk.CTkButton(
            form_content,
            text="ENTRAR",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_dark'],
            corner_radius=8,
            command=self.handle_login
        )
        self.login_button.pack(fill="x", pady=(0, 20))
        
        # Credenciais de teste
        self.show_credentials_var = ctk.BooleanVar(value=False)
        credentials_toggle = ctk.CTkButton(
            form_content,
            text="Mostrar credenciais de teste",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            text_color=COLORS['text_secondary'],
            hover_color=COLORS['neutral_100'],
            command=self._toggle_credentials
        )
        credentials_toggle.pack()
        
        self.credentials_frame = None
        
        # Binding Enter para fazer login
        self.username_entry.bind("<Return>", lambda e: self.handle_login())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
    
    def toggle_password(self):
        """Alterna entre mostrar/ocultar senha"""
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
    
    def handle_forgot_password(self):
        """Lida com esqueci a senha"""
        if not hasattr(self, 'forgot_password_modal') or not self.forgot_password_modal:
            self.forgot_password_modal = ForgotPasswordModal(
                self,
                is_open=True,
                on_close=self._close_forgot_password_modal
            )
    
    def _close_forgot_password_modal(self):
        """Fecha o modal de esqueci senha"""
        if hasattr(self, 'forgot_password_modal'):
            self.forgot_password_modal = None
    
    def handle_login(self):
        """Processa o login"""
        if self.is_loading:
            return
        
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            show_toast(self, "Por favor, preencha usuário e senha", "error")
            return
        
        # Handle remember me logic - igual ao web
        if self.remember_var.get():
            self._save_remembered_email(username)
        else:
            self._clear_remembered_email()
        
        # Desabilita o botão e mostra loading
        self.is_loading = True
        self.login_button.configure(text="ENTRANDO...", state="disabled")
        self.username_entry.configure(state="disabled")
        self.password_entry.configure(state="disabled")
        
        # Faz login em thread separada para não travar a UI
        threading.Thread(target=self._do_login, args=(username, password), daemon=True).start()
    
    def _load_remembered_email(self):
        """Carrega email lembrado do arquivo"""
        try:
            if os.path.exists(self.remember_email_file):
                with open(self.remember_email_file, 'r') as f:
                    return f.read().strip()
        except Exception:
            pass
        return ''
    
    def _save_remembered_email(self, email):
        """Salva email para lembrar"""
        try:
            with open(self.remember_email_file, 'w') as f:
                f.write(email)
        except Exception:
            pass
    
    def _clear_remembered_email(self):
        """Remove email lembrado"""
        try:
            if os.path.exists(self.remember_email_file):
                os.remove(self.remember_email_file)
        except Exception:
            pass
    
    def _do_login(self, username, password):
        """Faz o login de fato - exatamente como no web"""
        try:
            # CREDENCIAIS DE TESTE - Remover quando conectar com o banco de dados
            # Usuário 1: Administrador (Permissão 3)
            if username.lower() == "gabriel" and password == "senha":
                user_data = {
                    'nome': 'Gabriel',
                    'email': 'gabriel@teste.com',
                    'cargo': 'Administrador',
                    'permissao': 3,
                    'id': 1
                }
                self.after(0, self._login_success, user_data)
                return
            
            # Usuário 2: Colaborador (Permissão 1)
            if username.lower() == "colaborador" and password == "senha123":
                user_data = {
                    'nome': 'João Silva',
                    'email': 'joao@teste.com',
                    'cargo': 'Colaborador',
                    'permissao': 1,
                    'id': 2
                }
                self.after(0, self._login_success, user_data)
                return
            
            # Usuário 3: Suporte Técnico (Permissão 2)
            if username.lower() == "suporte" and password == "senha123":
                user_data = {
                    'nome': 'Maria Santos',
                    'email': 'maria@teste.com',
                    'cargo': 'Suporte Técnico',
                    'permissao': 2,
                    'id': 3
                }
                self.after(0, self._login_success, user_data)
                return
            
            response = AuthService.login(username, password)
            
            # API .NET retorna { Token: string, PrimeiroAcesso: bool }
            token = response.get('Token') or response.get('token') or response.get('access_token')
            primeiro_acesso = response.get('PrimeiroAcesso', False)
            
            if token:
                api_client.save_auth_token(token)
            
            # Busca dados completos do usuário via /api/Usuarios/meu-perfil (API .NET)
            user_data = {}
            if token:
                try:
                    from api_client import UserService
                    full_user_data = UserService.get_meu_perfil()
                    # Usa dados completos se disponíveis
                    if full_user_data:
                        # Normaliza campos PascalCase para camelCase
                        user_data = {
                            'id': full_user_data.get('Id') or full_user_data.get('id'),
                            'nome': full_user_data.get('Nome') or full_user_data.get('nome', ''),
                            'email': full_user_data.get('Email') or full_user_data.get('email', ''),
                            'telefone': full_user_data.get('Telefone') or full_user_data.get('telefone'),
                            'cargo': full_user_data.get('Cargo') or full_user_data.get('cargo', ''),
                            'permissao': full_user_data.get('Permissao') or full_user_data.get('permissao', 1),
                            'primeiroAcesso': full_user_data.get('PrimeiroAcesso') or full_user_data.get('primeiroAcesso', primeiro_acesso)
                        }
                except Exception as e:
                    print(f"[LOGIN] Erro ao buscar perfil completo: {e}")
                    # Fallback se não conseguir buscar perfil
                    user_data = {
                        'nome': username.split('@')[0] if '@' in username else username,
                        'email': username,
                        'primeiroAcesso': primeiro_acesso
                    }
            else:
                # Fallback se não tiver token
                user_data = {
                    'nome': username.split('@')[0] if '@' in username else username,
                    'email': username,
                    'primeiroAcesso': primeiro_acesso
                }
            
            # Sucesso - volta para thread principal
            self.after(0, self._login_success, user_data)
            
        except Exception as e:
            # Tratamento de erro idêntico ao web (LoginPage.jsx linhas 56-74)
            error_str = str(e).lower()
            error_message = 'Usuário ou senha incorretos.'  # Mensagem padrão
            
            # Verifica primeiro se é erro de conexão (prioridade)
            if 'conexão' in error_str or 'connection' in error_str or 'não foi possível conectar' in error_str or 'conect' in error_str:
                # Erro de conexão (igual ao web linha 77)
                error_message = 'Erro de conexão. Verifique se o servidor está rodando.'
            elif hasattr(e, 'status_code'):
                status = e.status_code
                # Se a API retornou uma mensagem específica, usa ela
                if hasattr(e, 'data') and e.data and e.data.get('message'):
                    error_message = e.data.get('message')
                elif status == 404:
                    error_message = 'Usuário ou senha incorretos.'
                elif status == 401:
                    error_message = 'Usuário ou senha incorretos.'
                elif status == 400:
                    error_message = 'Dados inválidos. Verifique email e senha.'
                elif status >= 500:
                    error_message = 'Erro interno do servidor. Tente novamente mais tarde.'
            
            # Erro - volta para thread principal
            self.after(0, self._login_error, error_message)
    
    def _login_success(self, user_data):
        """Callback de sucesso do login"""
        print(f"[DEBUG LOGIN] _login_success chamado com user_data: {user_data}")
        self.is_loading = False
        self.login_button.configure(text="ENTRAR", state="normal")
        self.username_entry.configure(state="normal")
        self.password_entry.configure(state="normal")
        
        show_toast(self, "Login realizado com sucesso!", "success")
        
        # Chama callback após um pequeno delay
        print("[DEBUG LOGIN] Agendando callback on_login_success")
        # IMPORTANTE: Captura user_data em closure para evitar problemas
        def call_callback():
            print("[DEBUG LOGIN] Executando callback...")
            try:
                self.on_login_success(user_data)
                print("[DEBUG LOGIN] Callback executado com sucesso")
            except Exception as e:
                print(f"[DEBUG LOGIN] ERRO no callback: {e}")
                import traceback
                traceback.print_exc()
        self.after(500, call_callback)
    
    def _login_error(self, error_message):
        """Callback de erro do login"""
        self.is_loading = False
        self.login_button.configure(text="ENTRAR", state="normal")
        self.username_entry.configure(state="normal")
        self.password_entry.configure(state="normal")
        
        show_toast(self, error_message, "error")
    
    def _toggle_credentials(self):
        """Mostra/oculta credenciais de teste"""
        if self.credentials_frame is None:
            # Cria frame de credenciais simples
            form_content = self.username_entry.master
            self.credentials_frame = ctk.CTkFrame(
                form_content,
                fg_color="#F8F9FA",
                corner_radius=8
            )
            self.credentials_frame.pack(fill="x", pady=(16, 16))
            
            # Título
            title = ctk.CTkLabel(
                self.credentials_frame,
                text="Credenciais de Teste:",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=COLORS['text_primary']
            )
            title.pack(anchor="w", padx=16, pady=(16, 8))
            
            # Lista de usuários
            usuarios = [
                ("👤 Administrador", "gabriel", "senha", "Permissão 3 - Acesso total"),
                ("👤 Colaborador", "colaborador", "senha123", "Permissão 1 - Apenas meus chamados"),
                ("👤 Suporte Técnico", "suporte", "senha123", "Permissão 2 - Gerencia chamados")
            ]
            
            for i, (icon_text, usuario, senha, descricao) in enumerate(usuarios):
                user_frame = ctk.CTkFrame(self.credentials_frame, fg_color="white", corner_radius=4)
                bottom_padding = 16 if i == len(usuarios) - 1 else 6
                user_frame.pack(fill="x", padx=16, pady=(0, bottom_padding))
                
                inner_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
                inner_frame.pack(fill="x", padx=12, pady=6)
                
                # Ícone e título
                header = ctk.CTkLabel(
                    inner_frame,
                    text=icon_text,
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=COLORS['text_primary']
                )
                header.pack(anchor="w")
                
                # Descrição
                desc = ctk.CTkLabel(
                    inner_frame,
                    text=descricao,
                    font=ctk.CTkFont(size=9),
                    text_color=COLORS['text_secondary']
                )
                desc.pack(anchor="w", pady=(1, 2))
                
                # Credenciais
                cred_text = ctk.CTkLabel(
                    inner_frame,
                    text=f"Usuário: {usuario} | Senha: {senha}",
                    font=ctk.CTkFont(size=10, family="monospace"),
                    text_color=COLORS['primary']
                )
                cred_text.pack(anchor="w")
                
                # Botão para usar essas credenciais
                use_btn = ctk.CTkButton(
                    inner_frame,
                    text="Usar estas credenciais",
                    font=ctk.CTkFont(size=9),
                    fg_color=COLORS['primary'],
                    hover_color=COLORS['primary_dark'],
                    height=26,
                    command=lambda u=usuario, s=senha: self._use_credentials(u, s)
                )
                use_btn.pack(anchor="w", pady=(4, 0))
            
            self.show_credentials_var.set(True)
            # Atualiza a centralização após adicionar credenciais
            if self.update_scroll_region:
                self.after(100, self.update_scroll_region)
        else:
            if self.show_credentials_var.get():
                self.credentials_frame.pack_forget()
                self.show_credentials_var.set(False)
                # Atualiza a centralização após remover credenciais
                if self.update_scroll_region:
                    self.after(100, self.update_scroll_region)
            else:
                self.credentials_frame.pack(fill="x", pady=(16, 16))
                self.show_credentials_var.set(True)
                # Atualiza a centralização após adicionar credenciais
                if self.update_scroll_region:
                    self.after(100, self.update_scroll_region)
    
    def _use_credentials(self, usuario, senha):
        """Preenche campos com credenciais de teste"""
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, usuario)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, senha)