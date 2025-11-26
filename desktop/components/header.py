"""
Componente Header - Replica Header.jsx do web
"""
import tkinter as tk
from tkinter import Menu
from components.dropdown_menu import DropdownMenu
from components.confirm_logout_modal import ConfirmLogoutModal

class Header(tk.Frame):
    """Header do dashboard - replica Header.jsx"""
    
    def __init__(self, parent, on_logout, user_name='Administrador', user_info=None, on_navigate_to_profile=None, page_title=""):
        super().__init__(parent, bg="#A93226", height=70)
        self.pack_propagate(False)
        
        self.on_logout = on_logout
        self.user_name = user_name
        self.user_info = user_info or {}
        self.on_navigate_to_profile = on_navigate_to_profile
        self.is_dropdown_open = False
        self.show_logout_modal = False
        self.dropdown_menu = None
        
        # Usa o nome completo do userInfo diretamente
        display_name = self.user_info.get('nome', user_name) if self.user_info else user_name
        
        # Container principal com padding igual ao CSS (var(--space-xl) = 32px)
        # box-shadow: 0 8px 25px rgba(169, 50, 38, 0.3)
        container = tk.Frame(self, bg="#A93226")
        container.pack(fill=tk.BOTH, expand=True, padx=32, pady=0)
        
        # Configura grid para layout lado a lado
        container.grid_columnconfigure(0, weight=1)  # Título ocupa espaço disponível
        container.grid_columnconfigure(1, weight=0)  # Informações do usuário tamanho fixo
        container.grid_rowconfigure(0, weight=1)  # Centraliza verticalmente
        
        # Lado esquerdo - Título da página
        # Garante que o título seja sempre visível, mesmo quando vazio
        self.title_label = tk.Label(
            container,
            text=page_title if page_title else " ",
            font=("Inter", 20, "bold"),
            fg="white",
            bg="#A93226",
            anchor="w",
            justify="left"
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=(0, 20))
        
        # Lado direito - Informações do usuário
        right_frame = tk.Frame(container, bg="#A93226")
        right_frame.grid(row=0, column=1, sticky="e")
        
        # Ícone do usuário (clicável para perfil)
        user_icon = tk.Label(
            right_frame,
            text="👤",
            font=("Inter", 18),
            fg="white",
            bg="#A93226"
        )
        if on_navigate_to_profile:
            user_icon.config(cursor="hand2")
            user_icon.bind("<Button-1>", lambda e: self._handle_user_icon_click())
        user_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        # Texto de boas-vindas
        welcome_text = tk.Label(
            right_frame,
            text=f"BEM-VINDO(A), {display_name.upper()}",
            font=("Inter", 12),
            fg="white",
            bg="#A93226"
        )
        welcome_text.pack(side=tk.LEFT, padx=(0, 8), pady=0)
        
        # Botão de configurações (ícone engrenagem) com animação de rotação no hover
        self.settings_icon = tk.Label(
            right_frame,
            text="⚙️",
            font=("Inter", 16),
            fg="white",
            bg="#A93226",
            cursor="hand2"
        )
        self.settings_icon.pack(side=tk.LEFT, padx=(0, 8))
        self.settings_icon.bind("<Button-1>", self._toggle_dropdown)
        
        # Efeito hover: rotação (simulado com mudança de fonte)
        def on_settings_enter(e):
            self.settings_icon.config(font=("Inter", 17))
        def on_settings_leave(e):
            self.settings_icon.config(font=("Inter", 16))
        self.settings_icon.bind("<Enter>", on_settings_enter)
        self.settings_icon.bind("<Leave>", on_settings_leave)
        
        # Seta dropdown
        dropdown_arrow = tk.Label(
            right_frame,
            text="▼",
            font=("Inter", 12),
            fg="white",
            bg="#A93226",
            cursor="hand2"
        )
        dropdown_arrow.pack(side=tk.LEFT)
        dropdown_arrow.bind("<Button-1>", self._toggle_dropdown)
        
        # Atualiza referências para usar display_name
        self.display_name = display_name
    
    def _handle_user_icon_click(self):
        """Lida com clique no ícone do usuário"""
        if self.on_navigate_to_profile:
            self.on_navigate_to_profile()
    
    def _handle_profile_click(self):
        """Lida com clique em Perfil no dropdown"""
        self._close_dropdown()
        if self.on_navigate_to_profile:
            self.on_navigate_to_profile()
    
    def _toggle_dropdown(self, event=None):
        """Abre/fecha o menu dropdown"""
        if self.is_dropdown_open:
            self._close_dropdown()
        else:
            self._open_dropdown(event)
    
    def _open_dropdown(self, event=None):
        """Abre o dropdown menu"""
        if self.dropdown_menu:
            self.dropdown_menu.close()
        
        # Calcula posição
        if event:
            x = event.x_root
            y = event.y_root + 10
        else:
            x = self.winfo_rootx() + self.winfo_width() - 150
            y = self.winfo_rooty() + self.winfo_height()
        
        self.dropdown_menu = DropdownMenu(
            self,
            x, y,
            on_logout=self._handle_logout_click,
            on_navigate_to_profile=self._handle_profile_click
        )
        self.is_dropdown_open = True
    
    def _close_dropdown(self):
        """Fecha o dropdown menu"""
        if self.dropdown_menu:
            self.dropdown_menu.close()
            self.dropdown_menu = None
        self.is_dropdown_open = False
    
    def _handle_logout_click(self):
        """Abre modal de confirmação de logout"""
        self._close_dropdown()
        self.show_logout_modal = True
        self._show_logout_modal()
    
    def _show_logout_modal(self):
        """Mostra modal de confirmação de logout"""
        if self.show_logout_modal:
            modal = ConfirmLogoutModal(
                self,
                is_open=True,
                on_confirm=self._handle_logout,
                on_cancel=self._cancel_logout
            )
    
    def _cancel_logout(self):
        """Cancela logout"""
        self.show_logout_modal = False
    
    def _handle_logout(self):
        """Chama o callback de logout"""
        self.show_logout_modal = False
        if self.on_logout:
            self.on_logout()
    
    def set_title(self, title):
        """Atualiza o título da página no header"""
        if hasattr(self, 'title_label'):
            # Usa espaço em branco se título vazio para manter o label visível
            display_text = title if title else " "
            self.title_label.config(text=display_text)
            # Força atualização do layout
            self.title_label.update_idletasks()
