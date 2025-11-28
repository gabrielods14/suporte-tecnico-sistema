"""
DropdownMenu - Menu dropdown do header
Replica DropdownMenu.jsx do web
"""
import tkinter as tk
from tkinter import ttk

class DropdownMenu:
    """Menu dropdown para opções do usuário"""
    
    def __init__(self, parent, x, y, on_logout, on_navigate_to_profile=None):
        self.on_logout = on_logout
        self.on_navigate_to_profile = on_navigate_to_profile
        
        # Obtém a janela principal para calcular limites
        toplevel = parent.winfo_toplevel()
        
        # Cria uma janela popup
        self.window = tk.Toplevel(parent)
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.configure(bg="#FFFFFF", bd=1, relief=tk.SOLID)
        
        # Configura posição inicial
        self.window.geometry(f"+{x}+{y}")
        
        # Aguarda um momento para que o conteúdo seja renderizado
        self.window.update_idletasks()
        
        # Obtém dimensões reais do dropdown
        dropdown_width = self.window.winfo_reqwidth()
        dropdown_height = self.window.winfo_reqheight()
        
        # Obtém limites da janela principal
        window_x = toplevel.winfo_x()
        window_y = toplevel.winfo_y()
        window_width = toplevel.winfo_width()
        window_height = toplevel.winfo_height()
        
        window_right = window_x + window_width
        window_bottom = window_y + window_height
        
        # Ajusta posição se necessário
        final_x = x
        final_y = y
        
        # Ajusta horizontalmente
        if final_x + dropdown_width > window_right:
            final_x = window_right - dropdown_width - 5
        if final_x < window_x:
            final_x = window_x + 5
        
        # Ajusta verticalmente
        if final_y + dropdown_height > window_bottom:
            # Tenta posicionar acima
            final_y = y - dropdown_height - 20
            if final_y < window_y:
                # Se não couber acima, alinha no topo
                final_y = window_y + 5
        
        # Aplica posição final
        if final_x != x or final_y != y:
            self.window.geometry(f"+{final_x}+{final_y}")
        
        # Frame do menu
        menu_frame = tk.Frame(self.window, bg="#FFFFFF", bd=0)
        menu_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Item Perfil
        if on_navigate_to_profile:
            profile_item = tk.Frame(menu_frame, bg="#FFFFFF", cursor="hand2")
            profile_item.pack(fill=tk.X, padx=0, pady=0)
            profile_item.bind("<Button-1>", lambda e: self._handle_profile())
            profile_item.bind("<Enter>", lambda e: profile_item.config(bg="#F5F5F5"))
            profile_item.bind("<Leave>", lambda e: profile_item.config(bg="#FFFFFF"))
            
            profile_label = tk.Label(
                profile_item,
                text="👤 Perfil",
                font=("Inter", 14),
                bg="#FFFFFF",
                fg="#333333",
                anchor="w",
                padx=16,
                pady=12
            )
            profile_label.pack(fill=tk.X)
            profile_label.bind("<Button-1>", lambda e: self._handle_profile())
            profile_label.bind("<Enter>", lambda e: profile_item.config(bg="#F5F5F5"))
            profile_label.bind("<Leave>", lambda e: profile_item.config(bg="#FFFFFF"))
        
        # Separador
        separator = tk.Frame(menu_frame, bg="#E5E5E5", height=1)
        separator.pack(fill=tk.X, padx=0, pady=0)
        
        # Item Logout
        logout_item = tk.Frame(menu_frame, bg="#FFFFFF", cursor="hand2")
        logout_item.pack(fill=tk.X, padx=0, pady=0)
        logout_item.bind("<Button-1>", lambda e: self._handle_logout())
        logout_item.bind("<Enter>", lambda e: logout_item.config(bg="#F5F5F5"))
        logout_item.bind("<Leave>", lambda e: logout_item.config(bg="#FFFFFF"))
        
        logout_label = tk.Label(
            logout_item,
            text="🚪 Logout",
            font=("Inter", 14),
            bg="#FFFFFF",
            fg="#333333",
            anchor="w",
            padx=16,
            pady=12
        )
        logout_label.pack(fill=tk.X)
        logout_label.bind("<Button-1>", lambda e: self._handle_logout())
        logout_label.bind("<Enter>", lambda e: logout_item.config(bg="#F5F5F5"))
        logout_label.bind("<Leave>", lambda e: logout_item.config(bg="#FFFFFF"))
        
        # Fecha ao clicar fora
        self.window.bind("<FocusOut>", lambda e: self.close())
        self.window.focus_set()
    
    def _handle_profile(self):
        """Lida com clique em Perfil"""
        self.close()
        if self.on_navigate_to_profile:
            self.on_navigate_to_profile()
    
    def _handle_logout(self):
        """Lida com clique em Logout"""
        self.close()
        if self.on_logout:
            self.on_logout()
    
    def close(self):
        """Fecha o menu"""
        if self.window:
            self.window.destroy()
