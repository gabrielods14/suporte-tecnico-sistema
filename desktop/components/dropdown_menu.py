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
        
        # Cria uma janela popup
        self.window = tk.Toplevel(parent)
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.geometry(f"+{x}+{y}")
        self.window.configure(bg="#FFFFFF", bd=1, relief=tk.SOLID)
        
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
