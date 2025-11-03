import tkinter as tk
from tkinter import messagebox
from supabase_service import supabase # Importa o cliente Supabase

class LoginApp(tk.Frame): # LoginApp agora herda de tk.Frame
    """
    Classe para a interface de Login.
    Permite ao utilizador inserir credenciais e fazer login no Supabase.
    """
    def __init__(self, master, on_login_success):
        super().__init__(master, bg="#1C1C1C") # Inicializa como um Frame
        self.pack(fill=tk.BOTH, expand=True) # Empacota o Frame da LoginApp

        self.on_login_success = on_login_success # Callback para ser chamada no sucesso do login

        # Define as cores base da interface
        self.primary_color = "#8B0000"  # Vermelho escuro (ajustado para o header)
        self.background_dark = "#1C1C1C" # Quase preto
        self.text_color_light = "white"
        self.text_color_dark = "black"
        self.button_hover_color = "#A52A2A" # Um vermelho um pouco mais claro para hover
        self.entry_bg = "#D3D3D3" # Cinza claro para campos de entrada

        # Frame principal que divide a tela em duas colunas (vermelha e preta)
        self.main_frame = tk.Frame(self, bg=self.background_dark) # Usa self como master
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bind para ajustar proporções quando a janela redimensionar
        self.bind('<Configure>', self._adjust_proportions)

        # Frame para a seção vermelha (esquerda) - 60% da tela
        self.red_section = tk.Frame(self.main_frame, bg=self.primary_color)
        
        # Frame para a seção preta (direita) - 40% da tela  
        self.login_section = tk.Frame(self.main_frame, bg=self.background_dark)
        
        # Configurar proporções iniciais
        self._adjust_proportions()

        # Conteúdo da seção vermelha (esquerda)
        self._create_red_section_content()
        
        # Centraliza o formulário de login na seção preta
        self.login_form_frame = tk.Frame(self.login_section, bg=self.background_dark)
        self.login_form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Título LOGIN moderno
        self.login_label = tk.Label(self.login_form_frame, text="🔐 LOGIN", font=("Inter", 20, "bold"), fg=self.text_color_light, bg=self.background_dark)
        self.login_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # Subtítulo
        subtitle_label = tk.Label(self.login_form_frame, text="Acesse sua conta", font=("Inter", 12), fg="#CCCCCC", bg=self.background_dark)
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 30))

        # Campo Usuário moderno
        username_frame = tk.Frame(self.login_form_frame, bg=self.background_dark)
        username_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        self.username_label = tk.Label(username_frame, text="👤 USUÁRIO", font=("Inter", 11, "bold"), fg=self.text_color_light, bg=self.background_dark)
        self.username_label.pack(anchor="w", pady=(0, 8))
        
        self.username_entry = tk.Entry(username_frame, width=35, font=("Inter", 13), bg="#2A2A2A", fg="white", 
                                     bd=1, relief=tk.SOLID, insertbackground="white")
        self.username_entry.pack(fill=tk.X, ipady=12)

        # Campo Senha moderno
        password_frame = tk.Frame(self.login_form_frame, bg=self.background_dark)
        password_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        self.password_label = tk.Label(password_frame, text="🔒 SENHA", font=("Inter", 11, "bold"), fg=self.text_color_light, bg=self.background_dark)
        self.password_label.pack(anchor="w", pady=(0, 8))
        
        self.password_entry = tk.Entry(password_frame, width=35, show="*", font=("Inter", 13), bg="#2A2A2A", fg="white",
                                      bd=1, relief=tk.SOLID, insertbackground="white")
        self.password_entry.pack(fill=tk.X, ipady=12)

        # Opções modernas
        options_frame = tk.Frame(self.login_form_frame, bg=self.background_dark)
        options_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 30))
        
        # Checkbox Lembrar moderno
        self.remember_var = tk.BooleanVar()
        self.remember_checkbox = tk.Checkbutton(options_frame, text="Lembrar-me", variable=self.remember_var, 
                                              fg=self.text_color_light, bg=self.background_dark, 
                                              selectcolor="#8B0000", activebackground=self.background_dark, 
                                              activeforeground=self.text_color_light, font=("Inter", 10),
                                              cursor="hand2")
        self.remember_checkbox.pack(side=tk.LEFT)

        # Botão Esqueci a senha moderno
        self.forgot_password_button = tk.Button(options_frame, text="Esqueci a senha", 
                                               fg=self.primary_color, bg=self.background_dark, bd=0, relief=tk.FLAT, 
                                               font=("Inter", 10), cursor="hand2", 
                                               command=self._forgot_password_placeholder)
        self.forgot_password_button.pack(side=tk.RIGHT)

        # Botão ENTRAR moderno
        self.login_button = tk.Button(self.login_form_frame, text="🚀 ENTRAR", 
                                    font=("Inter", 14, "bold"), fg=self.text_color_light, bg=self.primary_color, 
                                    activebackground=self.button_hover_color, activeforeground=self.text_color_light, 
                                    bd=0, relief=tk.FLAT, command=self._login, cursor="hand2")
        self.login_button.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 20), ipady=15)
        
        # Indicador de Carregamento
        self.loading_label = tk.Label(self.login_form_frame, text="⏳ Verificando...", font=("Inter", 11), fg="#CCCCCC", bg=self.background_dark)
        self.loading_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        self.loading_label.grid_remove() # Inicia oculto

        # Bind para a tecla Enter
        self.master.bind('<Return>', lambda event=None: self._login())

    def _adjust_proportions(self, event=None):
        """Ajusta as proporções das seções para 60% vermelho e 40% preto."""
        # Obtém as dimensões da janela principal
        self.update_idletasks()
        width = self.winfo_width()
        
        if width > 1:  # Evita divisão por zero
            red_width = int(width * 0.6)  # 60% para vermelho
            black_width = int(width * 0.4)  # 40% para preto
            
            # Remove os frames existentes se já existirem
            try:
                self.red_section.pack_forget()
                self.login_section.pack_forget()
            except:
                pass
            
            # Reposiciona com as novas proporções
            self.red_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
            self.login_section.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
            
            # Define larguras específicas
            self.red_section.configure(width=red_width)
            self.login_section.configure(width=black_width)

    def _create_red_section_content(self):
        """Cria o conteúdo moderno para a seção vermelha."""
        # Container central para o conteúdo
        content_frame = tk.Frame(self.red_section, bg=self.primary_color)
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Logo principal
        logo_frame = tk.Frame(content_frame, bg=self.primary_color)
        logo_frame.pack(pady=(0, 40))
        
        tk.Label(logo_frame, text="📋", font=("Inter", 48), fg=self.text_color_light, bg=self.primary_color).pack()
        tk.Label(logo_frame, text="HelpWave", font=("Inter", 24, "bold"), fg=self.text_color_light, bg=self.primary_color).pack(pady=(10, 0))
        tk.Label(logo_frame, text="Sistema de Suporte", font=("Inter", 14), fg=self.text_color_light, bg=self.primary_color).pack()
        
        # Características do sistema
        features_frame = tk.Frame(content_frame, bg=self.primary_color)
        features_frame.pack(pady=(20, 0))
        
        features = [
            "🎯 Gestão Inteligente de Chamados",
            "⚡ Respostas Rápidas e Eficientes", 
            "📊 Relatórios Detalhados",
            "🔒 Acesso Seguro e Controlado"
        ]
        
        for feature in features:
            tk.Label(features_frame, text=feature, font=("Inter", 12), 
                   fg=self.text_color_light, bg=self.primary_color, anchor="w").pack(pady=8)

    def _login(self):
        """
        Função para lidar com o login do utilizador.
        Verifica as credenciais no Supabase.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos de login.")
            return

        # Mostra o indicador de carregamento
        self.loading_label.grid()
        self.update() # Atualiza a interface para mostrar o label

        try:
            # Busca explicitamente todas as colunas necessárias, incluindo Hierarquia
            response = supabase.table("usuarios").select("id, login, senha, departamento, email, telefone, Hierarquia").eq("login", username).eq("senha", password).execute()

            user_data = response.data
            
            # Esconde o indicador de carregamento após a resposta
            self.loading_label.grid_remove()

            if user_data:
                # Login bem-sucedido - Removemos o pop-up
                self.on_login_success(user_data[0]) # Chama o callback com os dados do usuário
                self.destroy() # Destrói o próprio frame da LoginApp
            else:
                messagebox.showerror("Erro de Login", "Utilizador ou senha inválidos.")
        except Exception as e:
            # Esconde o indicador de carregamento em caso de erro de conexão
            self.loading_label.grid_remove()
            messagebox.showerror("Erro de Conexão", f"Ocorreu um erro ao tentar fazer login: {e}")

    def _forgot_password_placeholder(self):
        """Placeholder para a funcionalidade de 'Esqueci a senha'."""
        messagebox.showinfo("Esqueci a Senha", "Funcionalidade 'Esqueci a senha' ainda não implementada.")