import tkinter as tk
from tkinter import messagebox
from home_page import HomePage
from new_call_page import NewCallPage
from pending_calls_page import PendingCallsPage
from call_details_page import CallDetailsPage
from create_user_page import CreateUserPage


class DashboardBase(tk.Frame):
    """
    Classe base para o Dashboard, contendo o cabeçalho, menu lateral e rodapé comuns.
    Gerencia a exibição de diferentes páginas de conteúdo na área principal.
    """
    def __init__(self, master, user_info, app_manager_callback):
        super().__init__(master, bg="#D3D3D3")
        self.pack(fill=tk.BOTH, expand=True)

        self.master = master # Adicionamos esta linha para poder referenciar a janela principal
        self.user_info = user_info
        self.app_manager_callback = app_manager_callback
        self.current_page_title = "HOME"
        self.current_page_widget = None

        self.primary_color = "#8B0000"
        self.background_light = "#D3D3D3"
        self.background_dark = "#1C1C1C"
        self.text_color_light = "white"
        self.text_color_dark = "black"
        self.button_hover_color = "#A52A2A"
        self.icon_color = "#F0F0F0"

        # --- Cabeçalho (cinza claro) ---
        self.header_frame = tk.Frame(self, bg=self.background_light, height=70)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        self.header_frame.pack_propagate(False)

        self.logo_label = tk.Label(self.header_frame, text="LOGO", font=("Inter", 20, "bold"), fg=self.text_color_dark, bg=self.background_light)
        self.logo_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.user_info_frame = tk.Frame(self.header_frame, bg=self.background_light)
        self.user_info_frame.pack(side=tk.RIGHT, padx=20, pady=10)

        self.user_icon_label = tk.Label(self.user_info_frame, text="👤", font=("Inter", 20), fg=self.text_color_dark, bg=self.background_light)
        self.user_icon_label.pack(side=tk.LEFT, padx=5)

        self.welcome_label = tk.Label(self.user_info_frame, text=f"BEM-VINDO(A)\n{user_info.get('login', 'UTILIZADOR')}", font=("Inter", 10, "bold"), fg=self.text_color_dark, bg=self.background_light)
        self.welcome_label.pack(side=tk.LEFT, padx=5)

        self.settings_icon_label = tk.Label(self.user_info_frame, text="⚙️", font=("Inter", 20), fg=self.text_color_dark, bg=self.background_light)
        self.settings_icon_label.pack(side=tk.LEFT, padx=5)
        self.settings_icon_label.bind("<Button-1>", self._show_dropdown_menu) # Adiciona a função ao clique da engrenagem

        self.dropdown_label = tk.Label(self.user_info_frame, text="▼", font=("Inter", 12), fg=self.text_color_dark, bg=self.background_light)
        self.dropdown_label.pack(side=tk.LEFT, padx=5)
        self.dropdown_label.bind("<Button-1>", self._show_dropdown_menu) # Adiciona a função ao clique da seta
        
        # --- Barra Vermelha do Título ---
        self.title_bar_frame = tk.Frame(self, bg=self.primary_color, height=50)
        self.title_bar_frame.pack(side=tk.TOP, fill=tk.X)
        self.title_bar_frame.pack_propagate(False)

        self.page_title_label = tk.Label(self.title_bar_frame, text=self.current_page_title, font=("Inter", 14, "bold"), fg=self.text_color_light, bg=self.primary_color)
        self.page_title_label.pack(pady=10)

        # --- Seção do Conteúdo Principal ---
        self.main_content_area = tk.Frame(self, bg=self.background_light)
        self.main_content_area.pack(fill=tk.BOTH, expand=True)

        # --- Menu Lateral ---
        self.menu_frame = tk.Frame(self.main_content_area, bg=self.primary_color, width=220)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        self.menu_frame.pack_propagate(False)

        # Logo do menu
        logo_frame = tk.Frame(self.menu_frame, bg=self.primary_color, height=80)
        logo_frame.pack(fill=tk.X, pady=(0, 20))
        logo_frame.pack_propagate(False)
        
        tk.Label(logo_frame, text="📋", font=("Inter", 24), fg=self.text_color_light, bg=self.primary_color).pack(pady=(15, 5))
        tk.Label(logo_frame, text="HelpWave", font=("Inter", 12, "bold"), fg=self.text_color_light, bg=self.primary_color).pack()

        self.menu_buttons = {}
        self.menu_buttons["HOME"] = self._create_menu_button("🏠", "HOME", lambda: self.show_page('Home'))
        self.menu_buttons["FQA"] = self._create_menu_button("❓", "FQA", lambda: self.show_page('FQA'))
        self.menu_buttons["CONTACTO"] = self._create_menu_button("📞", "CONTACTO", lambda: self.show_page('Contacto'))
        
        if self.user_info.get('Hierarquia', '').upper() == 'TI':
            self.menu_buttons["CADASTRAR"] = self._create_menu_button("👥", "CADASTRAR USUÁRIO", lambda: self.show_page('Cadastrar Usuário'))


        self.dashboard_content_frame = tk.Frame(self.main_content_area, bg=self.background_light)
        self.dashboard_content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # --- Rodapé ---
        self.footer_frame = tk.Frame(self, bg=self.primary_color, height=50)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.footer_frame.pack_propagate(False)

        self.footer_label = tk.Label(self.footer_frame, text="HelpWave — Simplificando o seu suporte. © 2025 HelpWave", fg=self.text_color_light, bg=self.primary_color, font=("Inter", 10))
        self.footer_label.pack(pady=15)

        self.show_page('Home')


    def _create_menu_button(self, icon, text, command, pady=8):
        """Cria um botão de menu lateral moderno com ícone e texto."""
        # Frame principal do botão
        btn_frame = tk.Frame(self.menu_frame, bg=self.primary_color, height=50)
        btn_frame.pack(fill=tk.X, padx=15, pady=pady)
        btn_frame.pack_propagate(False)
        
        # Frame interno para o conteúdo
        content_frame = tk.Frame(btn_frame, bg=self.primary_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)
        
        # Ícone
        icon_label = tk.Label(content_frame, text=icon, font=("Inter", 16), 
                             fg=self.text_color_light, bg=self.primary_color)
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Texto
        text_label = tk.Label(content_frame, text=text, font=("Inter", 11, "bold"), 
                             fg=self.text_color_light, bg=self.primary_color, anchor="w")
        text_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Lista de widgets para efeitos
        hover_widgets = [btn_frame, content_frame, icon_label, text_label]
        
        # Comando de clique
        def handle_click(event):
            self._handle_menu_click(text, command)
        
        for widget in hover_widgets:
            widget.bind("<Button-1>", handle_click)
        
        # Efeitos de hover
        def on_enter_menu(event):
            for widget in hover_widgets:
                widget.config(bg=self.button_hover_color)
        
        def on_leave_menu(event):
            for widget in hover_widgets:
                widget.config(bg=self.primary_color)
        
        for widget in hover_widgets:
            widget.bind("<Enter>", on_enter_menu)
            widget.bind("<Leave>", on_leave_menu)
        
        return btn_frame

    def _handle_menu_click(self, item_name, command):
        """Gerencia o clique nos itens do menu, atualizando a seleção visual."""
        if item_name != "MENU":
            command()

    def _select_menu_item(self, item_name):
        """Define um item do menu como selecionado, desmarcando outros."""
        for name, button in self.menu_buttons.items():
            if name == item_name:
                # Marca como selecionado com cor mais escura
                for widget in button.winfo_children():
                    if isinstance(widget, tk.Frame):
                        for child in widget.winfo_children():
                            child.config(bg=self.background_dark)
                        widget.config(bg=self.background_dark)
                    else:
                        widget.config(bg=self.background_dark)
                button.config(bg=self.background_dark)
            else:
                # Volta para a cor original
                for widget in button.winfo_children():
                    if isinstance(widget, tk.Frame):
                        for child in widget.winfo_children():
                            child.config(bg=self.primary_color)
                        widget.config(bg=self.primary_color)
                    else:
                        widget.config(bg=self.primary_color)
                button.config(bg=self.primary_color)

    def _show_dropdown_menu(self, event):
        """Exibe o menu drop-down ao clicar na engrenagem ou na seta."""
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Configuração", command=self._settings_placeholder)
        menu.add_command(label="Log Out", command=self._logout)
        menu.add_command(label="Finalizar programa", command=self._close_app)
        
        # Exibe o menu na posição do botão
        menu.tk_popup(event.x_root, event.y_root)

    def _settings_placeholder(self):
        messagebox.showinfo("Configurações", "Página de configurações ainda não implementada.")
    
    def _logout(self):
        """Faz o logout do usuário e retorna à página de login."""
        self.app_manager_callback.show_login_page()
    
    def _close_app(self):
        """Fecha a aplicação."""
        self.master.destroy()


    def show_page(self, page_name: str, *args, **kwargs):
        """
        Exibe a página de conteúdo especificada na área principal.
        Aceita argumentos adicionais para as páginas (como o ID do chamado).
        """
        if self.current_page_widget:
            self.current_page_widget.destroy()
            self.current_page_widget = None

        if page_name == 'Home':
            self.current_page_title = "HOME"
            self.current_page_widget = HomePage(self.dashboard_content_frame, self, self.user_info)
            self._select_menu_item('HOME')
        elif page_name == 'Novo Chamado':
            self.current_page_title = "NOVO CHAMADO"
            self.current_page_widget = NewCallPage(self.dashboard_content_frame, self.user_info.get('login', ''), self)
            self._select_menu_item('HOME')
        elif page_name == 'Chamados em Andamento':
            self.current_page_title = "CHAMADOS EM ANDAMENTO"
            self.current_page_widget = PendingCallsPage(self.dashboard_content_frame, self.user_info, self)
            self._select_menu_item('HOME')
        elif page_name == 'Detalhes do Chamado':
            self.current_page_title = "DETALHES DO CHAMADO"
            call_id = kwargs.get('call_id')
            self.current_page_widget = CallDetailsPage(self.dashboard_content_frame, call_id, self, user_info=self.user_info)
            self._select_menu_item('HOME')
        elif page_name == 'Cadastrar Usuário':
            self.current_page_title = "CADASTRO DE USUÁRIO"
            self.current_page_widget = CreateUserPage(self.dashboard_content_frame, self)
            self._select_menu_item('CADASTRAR')
        elif page_name == 'FQA':
            self.current_page_title = "FQA"
            tk.Label(self.dashboard_content_frame, text="Página FQA em construção...", bg=self.background_light, fg=self.text_color_dark, font=("Inter", 12)).pack(pady=50)
            self._select_menu_item('FQA')
        elif page_name == 'Contacto':
            self.current_page_title = "CONTACTO"
            tk.Label(self.dashboard_content_frame, text="Página de Contacto em construção...", bg=self.background_light, fg=self.text_color_dark, font=("Inter", 12)).pack(pady=50)
            self._select_menu_item('CONTACTO')

        self.page_title_label.config(text=self.current_page_title)

    def _menu_placeholder(self):
        messagebox.showinfo("Menu", "Funcionalidade de MENU ainda não implementada.")