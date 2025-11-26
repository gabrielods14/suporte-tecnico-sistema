"""
Base Page - Classe base para todas as páginas com Header e Sidebar
"""
import tkinter as tk
from components.header import Header
from components.sidebar import Sidebar

class BasePage(tk.Frame):
    """Classe base para páginas com Header e Sidebar"""
    
    def __init__(self, parent, on_logout, on_navigate_to_page, current_page, user_info, page_title="", create_header_sidebar=True):
        super().__init__(parent, bg="#F8F9FA")
        
        self.on_logout = on_logout
        self.on_navigate_to_page = on_navigate_to_page
        self.current_page = current_page
        self.user_info = user_info or {}
        
        # Obtém primeiro nome
        self.first_name = self._get_first_name()
        
        if create_header_sidebar:
            # Configura grid layout (igual ao CSS do web)
            self.grid_columnconfigure(0, weight=0, minsize=280)  # Sidebar fixo
            self.grid_columnconfigure(1, weight=1)  # Header + Main
            self.grid_rowconfigure(0, weight=0, minsize=70)  # Header
            self.grid_rowconfigure(1, weight=1)  # Main
            
            # Sidebar - precisa receber user_info para mostrar opções baseadas em permissões
            self.sidebar = Sidebar(self, current_page, on_navigate_to_page, user_info)
            self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
            
            # Header - precisa receber user_info e on_navigate_to_profile
            # on_navigate_to_profile será passado pelas subclasses se necessário
            self.header = Header(self, on_logout, self.first_name, user_info=user_info, page_title=page_title)
            self.header.grid(row=0, column=1, sticky="ew")
            
            # Main content (será preenchido pelas subclasses)
            self.main_content = tk.Frame(self, bg="#F8F9FA")
            self.main_content.grid(row=1, column=1, sticky="nsew")
        else:
            # Quando não cria Header e Sidebar, usa o frame inteiro como main_content
            # Usa grid para compatibilidade com o layout do HomePage
            self.main_content = tk.Frame(self, bg="#F8F9FA")
            self.main_content.grid(row=0, column=0, sticky="nsew")
            # Configura grid para expandir
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.header = None  # Header será gerenciado pelo HomePage
            self.sidebar = None  # Sidebar será gerenciado pelo HomePage
        
        # Garante que o main_content expanda corretamente
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=1)
        
        # Força atualização do layout para garantir que seja exibido
        self.update_idletasks()
    
    def _get_first_name(self):
        """Extrai o primeiro nome do user_info"""
        nome = self.user_info.get('nome', '')
        if nome and isinstance(nome, str):
            parts = nome.strip().split()
            if parts:
                return parts[0]
        
        email = self.user_info.get('email', '')
        if email and isinstance(email, str):
            return email.split('@')[0]
        
        return ''
    
    def set_header_title(self, title):
        """Atualiza o título no header"""
        if hasattr(self, 'header') and self.header and hasattr(self.header, 'set_title'):
            self.header.set_title(title)
        # Se não tem header próprio, tenta atualizar o header do HomePage (se existir)
        elif hasattr(self, 'on_set_header_title') and self.on_set_header_title:
            self.on_set_header_title(title)
        # Tenta encontrar o HomePage através da hierarquia de widgets
        elif hasattr(self, 'master'):
            parent = self.master
            # Procura até 3 níveis acima para encontrar o HomePage
            for _ in range(3):
                if parent and hasattr(parent, 'set_header_title'):
                    parent.set_header_title(title)
                    break
                if hasattr(parent, 'master'):
                    parent = parent.master
                else:
                    break

