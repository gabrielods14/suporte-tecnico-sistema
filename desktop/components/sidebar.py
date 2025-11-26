"""
Componente Sidebar - Replica Sidebar.jsx do web
"""
import tkinter as tk
from tkinter import PhotoImage
import os

class Sidebar(tk.Frame):
    """Sidebar do dashboard - replica Sidebar.jsx"""
    
    def __init__(self, parent, current_page, on_navigate, user_info=None):
        super().__init__(parent, bg="#A93226", width=280)
        self.pack_propagate(False)
        
        self.current_page = current_page
        self.on_navigate = on_navigate
        self.user_info = user_info or {}
        
        # Determina permissões
        permissao = self.user_info.get('permissao', 1)
        self.is_colaborador = permissao == 1
        self.is_suporte_tecnico = permissao == 2
        self.is_admin = permissao == 3
        
        # Container principal com padding igual ao CSS (var(--space-xl) = 32px vertical)
        container = tk.Frame(self, bg="#A93226")
        container.pack(fill=tk.BOTH, expand=True, padx=0, pady=32)
        
        # Logo (padding horizontal var(--space-lg) = 24px)
        # Tenta carregar a imagem do logo, se não existir mostra texto
        logo_frame = tk.Frame(container, bg="#A93226")
        logo_frame.pack(fill=tk.X, padx=24, pady=(0, 48))  # margin-bottom: var(--space-2xl) = 48px
        
        # Tenta carregar o logo da versão web
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "web", "my-project", "public", "logo.png")
        logo_image = None
        logo_label = None
        
        if os.path.exists(logo_path):
            try:
                logo_image = PhotoImage(file=logo_path)
                # Redimensiona a imagem se necessário (max 140px de largura como no web)
                original_width = logo_image.width()
                if original_width > 140:
                    # Usa subsample para reduzir (subsample divide o tamanho)
                    scale_factor = original_width // 140
                    if scale_factor > 1:
                        logo_image = logo_image.subsample(scale_factor)
                
                logo_label = tk.Label(
                    logo_frame,
                    image=logo_image,
                    bg="#A93226"
                )
                logo_label.image = logo_image  # Mantém referência para evitar garbage collection
                logo_label.pack()
            except Exception as e:
                print(f"[Sidebar] Erro ao carregar logo: {e}")
                logo_image = None
        
        # Se não conseguiu carregar a imagem, mostra texto como fallback
        if logo_image is None:
            logo_text = tk.Label(
                logo_frame,
                text="HELPWAVE",
                font=("Inter", 24, "bold"),  # var(--font-size-2xl)
                fg="white",
                bg="#A93226"
            )
            logo_text.pack()
        
        # Navegação
        nav_frame = tk.Frame(container, bg="#A93226")
        nav_frame.pack(fill=tk.BOTH, expand=True)
        
        # Itens do menu baseados em permissões
        menu_items = [
            ("🏠", "HOME", "home"),
        ]
        
        # Colaborador: só vê "Meus Chamados"
        if self.is_colaborador:
            menu_items.append(("📋", "MEUS CHAMADOS", "my-tickets"))
        else:
            # Técnico/Admin: vê Chamado, Concluídos, Relatórios
            menu_items.append(("📋", "CHAMADOS", "pending-tickets"))
            menu_items.append(("✅", "CONCLUÍDOS", "completed-tickets"))
            # Dashboard - apenas admin
            if self.is_admin:
                menu_items.append(("📊", "DASHBOARD", "dashboard"))
            menu_items.append(("📊", "RELATÓRIOS", "reports"))
        
        # Todos veem FQA e CONTATO
        menu_items.append(("❓", "FQA", "faq"))
        menu_items.append(("📞", "CONTATO", "contact"))
        
        self.menu_buttons = {}
        for icon, text, page_id in menu_items:
            btn = self._create_menu_item(nav_frame, icon, text, page_id)
            self.menu_buttons[page_id] = btn
    
    def _create_menu_item(self, parent, icon, text, page_id):
        """Cria um item do menu"""
        # Frame do item com padding igual ao CSS
        # padding: var(--space-md) var(--space-lg) = 16px vertical, 24px horizontal
        item_frame = tk.Frame(parent, bg="#A93226")
        item_frame.pack(fill=tk.X, padx=24, pady=8)
        
        # Borda esquerda para item ativo (border-left: 3px solid var(--primary-dark))
        border_frame = tk.Frame(item_frame, bg="#8B0000", width=3)  # var(--primary-dark)
        # Escondido por padrão, será mostrado se ativo
        
        # Ícone (font-size: var(--font-size-lg) = 18px)
        icon_label = tk.Label(
            item_frame,
            text=icon,
            font=("Inter", 18),
            fg="white",
            bg="#A93226"
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 16))  # gap: var(--space-md) = 16px
        
        # Texto (font-weight: var(--font-weight-medium) = 500)
        text_label = tk.Label(
            item_frame,
            text=text,
            font=("Inter", 14, "normal"),  # font-size base, weight medium
            fg="white",
            bg="#A93226",
            anchor="w"
        )
        text_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Lista de widgets para hover
        hover_widgets = [item_frame, icon_label, text_label]
        
        # Verifica se está ativo
        is_active = self.current_page == page_id
        # Cor para item ativo: simula rgba(255, 255, 255, 0.1) sobre #A93226
        # Calculado: 10% branco + 90% vermelho = #B83D35
        active_bg = "#B83D35"
        if is_active:
            # Mostra borda esquerda
            border_frame.pack(side=tk.LEFT, fill=tk.Y)
            for widget in hover_widgets:
                widget.config(bg=active_bg)
        
        # Comando de clique
        def handle_click(event):
            if self.on_navigate:
                self.on_navigate(page_id)
        
        for widget in hover_widgets:
            widget.bind("<Button-1>", handle_click)
            widget.config(cursor="hand2")
        
        # Efeito hover - apenas muda cor, sem movimento
        # Cor para hover: simula rgba(255, 255, 255, 0.1) sobre #A93226
        hover_bg = "#B83D35"
        
        def on_enter(event):
            if not is_active:
                for widget in hover_widgets:
                    widget.config(bg=hover_bg)
        
        def on_leave(event):
            if not is_active:
                for widget in hover_widgets:
                    widget.config(bg="#A93226")
        
        for widget in hover_widgets:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        
        # Armazena border_frame para poder mostrar/esconder
        item_frame.border_frame = border_frame
        
        return item_frame
    
    def set_current_page(self, page_id):
        """Atualiza a página atual e recalcula os estados dos itens do menu"""
        self.current_page = page_id
        # Atualiza visualmente os itens do menu
        for page_key, item_frame in self.menu_buttons.items():
            is_active = page_key == page_id
            active_bg = "#B83D35"
            hover_widgets = [item_frame]
            # Encontra os widgets filhos (icon_label, text_label)
            for child in item_frame.winfo_children():
                if isinstance(child, tk.Label):
                    hover_widgets.append(child)
            
            if is_active:
                # Mostra borda esquerda se existir
                if hasattr(item_frame, 'border_frame'):
                    item_frame.border_frame.pack(side=tk.LEFT, fill=tk.Y)
                for widget in hover_widgets:
                    widget.config(bg=active_bg)
            else:
                # Esconde borda esquerda se existir
                if hasattr(item_frame, 'border_frame'):
                    item_frame.border_frame.pack_forget()
                for widget in hover_widgets:
                    widget.config(bg="#A93226")