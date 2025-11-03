import tkinter as tk
from tkinter import messagebox

class HomePage(tk.Frame):
    """
    Página de conteúdo Home, exibindo os botões de ação.
    """
    def __init__(self, master_frame, dashboard_controller, user_info):
        super().__init__(master_frame, bg="#D3D3D3")
        self.pack(fill=tk.BOTH, expand=True)

        self.dashboard_controller = dashboard_controller # Referência ao DashboardBase
        self.user_info = user_info # Armazena as informações do usuário logado

        # Botões de ação do dashboard
        self.action_buttons_frame = tk.Frame(self, bg=self["bg"]) # Usa a cor de fundo do próprio frame
        self.action_buttons_frame.pack(pady=20, expand=True)

        # Botões de ação
        self._create_action_button(self.action_buttons_frame, "✎", "NOVO CHAMADO", lambda: self.dashboard_controller.show_page('Novo Chamado'), row=0, column=0)
        self._create_action_button(self.action_buttons_frame, "📋", "CHAMADOS\nEM ANDAMENTO", self._pending_calls_placeholder, row=0, column=1)
        self._create_action_button(self.action_buttons_frame, "✅", "CHAMADOS\nCONCLUÍDOS", self._completed_calls_placeholder, row=0, column=2)
        self._create_action_button(self.action_buttons_frame, "📊", "RELATÓRIOS", self._reports_placeholder, row=1, column=1)

        # Lógica para mostrar o botão de cadastro apenas para o TI
        if self.user_info.get('Hierarquia', '').upper() == 'TI':
            self._create_action_button(self.action_buttons_frame, "👥", "CADASTRAR\nUSUÁRIO", lambda: self.dashboard_controller.show_page('Cadastrar Usuário'), row=1, column=0)


    def _create_action_button(self, parent_frame, icon_text, text, command, row, column):
        """
        Cria um botão de ação com ícone e texto no dashboard.
        Garanto tamanho fixo e evita mudança de tamanho no hover.
        """
        # Cores
        primary_color = "#8B0000"
        background_dark = "#1C1C1C"
        text_color_light = "white"

        # Define um tamanho fixo para o frame do botão de ação
        btn_frame = tk.Frame(parent_frame, bg=primary_color, width=150, height=150, bd=0, relief=tk.FLAT)
        btn_frame.grid(row=row, column=column, padx=20, pady=20)
        btn_frame.grid_propagate(False) # Impede que o frame se redimensione para caber nos widgets internos

        # Usa Label para ícone e texto e os posiciona com .place() para controle absoluto
        btn_icon_label = tk.Label(btn_frame, text=icon_text, font=("Inter", 40), fg=text_color_light, bg=primary_color)
        btn_icon_label.place(relx=0.5, rely=0.35, anchor=tk.CENTER) # Posição relativa para centralizar o ícone

        btn_text_label = tk.Label(btn_frame, text=text, font=("Inter", 10, "bold"), fg=text_color_light, bg=primary_color, wraplength=120, justify=tk.CENTER)
        btn_text_label.place(relx=0.5, rely=0.75, anchor=tk.CENTER) # Posição relativa para centralizar o texto

        # Lista de widgets para o efeito de hover
        hover_widgets = [btn_frame, btn_icon_label, btn_text_label]

        # Adicionar um comando ao clique em qualquer parte do frame do botão
        for widget in hover_widgets:
            widget.bind("<Button-1>", lambda e: command())

        # Adicionar efeito de hover sem mudar o tamanho e com cor de fundo preto
        def on_enter_action(event):
            for widget in hover_widgets:
                widget.config(bg=background_dark) # Fundo preto no hover

        def on_leave_action(event):
            for widget in hover_widgets:
                widget.config(bg=primary_color) # Volta para o vermelho original

        for widget in hover_widgets:
            widget.bind("<Enter>", on_enter_action)
            widget.bind("<Leave>", on_leave_action)

        return btn_frame

    # --- Funções Placeholder para os botões de ação ---
    def _pending_calls_placeholder(self):
        """Navega para a página de Chamados em Andamento."""
        self.dashboard_controller.show_page("Chamados em Andamento")

    def _completed_calls_placeholder(self):
        self.dashboard_controller.show_page("CHAMADOS CONCLUÍDOS") # Placeholder para navegação

    def _reports_placeholder(self):
        self.dashboard_controller.show_page("RELATÓRIOS") # Placeholder para navegação