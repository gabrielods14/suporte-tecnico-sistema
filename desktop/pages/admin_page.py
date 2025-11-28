"""
AdminPage - Página de funcionalidades administrativas
Inclui logs, auditoria e configurações do sistema
"""
import tkinter as tk
import customtkinter as ctk
from pages.base_page import BasePage
from config import COLORS
import threading
from datetime import datetime
from api_client import api_client, TicketService, UserService
from components.toast import show_toast

class AdminPage(BasePage):
    """Página de administração - logs, auditoria e configurações"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page,
                 current_page, user_info):
        super().__init__(parent, on_logout, on_navigate_to_page, current_page, user_info, 
                        page_title="ADMINISTRAÇÃO", create_header_sidebar=False)
        
        self.on_navigate_to_home = on_navigate_to_home
        self.logs = []
        self.audit_entries = []
        self.loading = False
        
        self._create_ui()
        self._load_data()
    
    def _create_ui(self):
        """Cria interface"""
        container = tk.Frame(self.main_content, bg="#F8F9FA")
        container.pack(fill=tk.BOTH, expand=True, padx=48, pady=48)
        
        # Botão voltar
        back_frame = tk.Frame(container, bg="#F8F9FA")
        back_frame.pack(fill="x", anchor="w", pady=(0, 20))
        
        back_btn = ctk.CTkButton(
            back_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color=COLORS['primary'],
            hover_color=COLORS['neutral_100'],
            anchor="w",
            command=self.on_navigate_to_home
        )
        back_btn.pack(side="left")
        
        # Tabs (simuladas com botões)
        tabs_frame = tk.Frame(container, bg="#F8F9FA")
        tabs_frame.pack(fill="x", pady=(0, 24))
        
        self.tabs = {}
        self.current_tab = 'logs'
        
        tabs = [
            ('logs', '📋 Logs do Sistema'),
            ('audit', '🔍 Auditoria'),
            ('settings', '⚙️ Configurações')
        ]
        
        for i, (tab_id, tab_label) in enumerate(tabs):
            btn = ctk.CTkButton(
                tabs_frame,
                text=tab_label,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=COLORS['primary'] if tab_id == 'logs' else COLORS['neutral_200'],
                hover_color=COLORS['primary_dark'],
                height=40,
                command=lambda t=tab_id: self._switch_tab(t)
            )
            btn.pack(side="left", padx=(0, 12))
            self.tabs[tab_id] = btn
        
        # Container de conteúdo
        self.content_frame = tk.Frame(container, bg="#F8F9FA")
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        self._show_logs_tab()
    
    def _switch_tab(self, tab_id):
        """Troca de aba"""
        self.current_tab = tab_id
        
        # Atualiza botões
        for tid, btn in self.tabs.items():
            if tid == tab_id:
                btn.configure(fg_color=COLORS['primary'])
            else:
                btn.configure(fg_color=COLORS['neutral_200'])
        
        # Limpa conteúdo
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Mostra conteúdo da aba
        if tab_id == 'logs':
            self._show_logs_tab()
        elif tab_id == 'audit':
            self._show_audit_tab()
        elif tab_id == 'settings':
            self._show_settings_tab()
    
    def _show_logs_tab(self):
        """Mostra aba de logs"""
        # Título
        title = tk.Label(
            self.content_frame,
            text="LOGS DO SISTEMA",
            font=("Inter", 20, "bold"),
            bg="#F8F9FA",
            fg="#2d3748"
        )
        title.pack(anchor="w", pady=(0, 20))
        
        # Card de logs
        logs_card = tk.Frame(self.content_frame, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        logs_card.pack(fill=tk.BOTH, expand=True)
        
        logs_inner = tk.Frame(logs_card, bg="#FFFFFF")
        logs_inner.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)
        
        # Cabeçalho da tabela
        header_frame = tk.Frame(logs_inner, bg="#A93226", height=40)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        headers = ["Data/Hora", "Nível", "Módulo", "Mensagem"]
        for i, header_text in enumerate(headers):
            label = tk.Label(
                header_frame,
                text=header_text,
                font=("Inter", 12, "bold"),
                bg="#A93226",
                fg="white",
                anchor="w"
            )
            label.grid(row=0, column=i, sticky="ew", padx=8, pady=8)
        
        for i in range(len(headers)):
            header_frame.grid_columnconfigure(i, weight=1)
        
        # Corpo scrollável
        canvas = tk.Canvas(logs_inner, bg="#FFFFFF", highlightthickness=0)
        scrollbar = tk.Scrollbar(logs_inner, orient="vertical", command=canvas.yview)
        
        body_frame = tk.Frame(canvas, bg="#FFFFFF")
        canvas_window = canvas.create_window((0, 0), window=body_frame, anchor="nw")
        
        def on_configure(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        canvas.bind("<Configure>", on_configure)
        body_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mousewheel
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<MouseWheel>", on_mousewheel)
        
        self.logs_body = body_frame
        self.logs_canvas = canvas
        
        # Carrega logs
        self._load_logs()
    
    def _show_audit_tab(self):
        """Mostra aba de auditoria"""
        title = tk.Label(
            self.content_frame,
            text="AUDITORIA DE AÇÕES",
            font=("Inter", 20, "bold"),
            bg="#F8F9FA",
            fg="#2d3748"
        )
        title.pack(anchor="w", pady=(0, 20))
        
        # Card de auditoria
        audit_card = tk.Frame(self.content_frame, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        audit_card.pack(fill=tk.BOTH, expand=True)
        
        audit_inner = tk.Frame(audit_card, bg="#FFFFFF")
        audit_inner.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)
        
        # Cabeçalho
        header_frame = tk.Frame(audit_inner, bg="#A93226", height=40)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        headers = ["Data/Hora", "Usuário", "Ação", "Detalhes"]
        for i, header_text in enumerate(headers):
            label = tk.Label(
                header_frame,
                text=header_text,
                font=("Inter", 12, "bold"),
                bg="#A93226",
                fg="white",
                anchor="w"
            )
            label.grid(row=0, column=i, sticky="ew", padx=8, pady=8)
        
        for i in range(len(headers)):
            header_frame.grid_columnconfigure(i, weight=1)
        
        # Corpo scrollável
        canvas = tk.Canvas(audit_inner, bg="#FFFFFF", highlightthickness=0)
        scrollbar = tk.Scrollbar(audit_inner, orient="vertical", command=canvas.yview)
        
        body_frame = tk.Frame(canvas, bg="#FFFFFF")
        canvas_window = canvas.create_window((0, 0), window=body_frame, anchor="nw")
        
        def on_configure(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        canvas.bind("<Configure>", on_configure)
        body_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<MouseWheel>", on_mousewheel)
        
        self.audit_body = body_frame
        self.audit_canvas = canvas
        
        # Carrega auditoria
        self._load_audit()
    
    def _show_settings_tab(self):
        """Mostra aba de configurações"""
        title = tk.Label(
            self.content_frame,
            text="CONFIGURAÇÕES DO SISTEMA",
            font=("Inter", 20, "bold"),
            bg="#F8F9FA",
            fg="#2d3748"
        )
        title.pack(anchor="w", pady=(0, 20))
        
        # Card de configurações
        settings_card = tk.Frame(self.content_frame, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        settings_card.pack(fill=tk.BOTH, expand=True)
        
        settings_inner = tk.Frame(settings_card, bg="#FFFFFF")
        settings_inner.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)
        
        # Configurações gerais
        tk.Label(
            settings_inner,
            text="Configurações Gerais",
            font=("Inter", 16, "bold"),
            bg="#FFFFFF",
            fg="#2d3748",
            anchor="w"
        ).pack(anchor="w", pady=(0, 16))
        
        # URL da API
        api_frame = tk.Frame(settings_inner, bg="#FFFFFF")
        api_frame.pack(fill=tk.X, pady=(0, 16))
        
        tk.Label(
            api_frame,
            text="URL da API:",
            font=("Inter", 14),
            bg="#FFFFFF",
            fg="#2d3748",
            anchor="w"
        ).pack(side="left", padx=(0, 12))
        
        from config import API_URL_BASE
        api_url = API_URL_BASE or "http://localhost:5232"
        
        api_entry = ctk.CTkEntry(
            api_frame,
            font=ctk.CTkFont(size=14),
            height=40,
            width=400
        )
        api_entry.insert(0, api_url)
        api_entry.pack(side="left", fill=tk.X, expand=True)
        
        # Botão salvar
        save_btn = ctk.CTkButton(
            settings_inner,
            text="Salvar Configurações",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_dark'],
            height=40,
            command=lambda: show_toast(self, "Configurações salvas com sucesso!", "success")
        )
        save_btn.pack(anchor="w", pady=(16, 0))
    
    def _load_data(self):
        """Carrega dados"""
        self._load_logs()
        self._load_audit()
    
    def _load_logs(self):
        """Carrega logs do sistema"""
        # Limpa logs anteriores
        for widget in self.logs_body.winfo_children():
            widget.destroy()
        
        # Logs mockados (em produção, viriam da API)
        logs = [
            (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "INFO", "Sistema", "Aplicação iniciada"),
            (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "INFO", "API", "Conexão estabelecida"),
            (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "WARN", "Autenticação", "Tentativa de login falhou"),
            (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "INFO", "Ticket", "Novo chamado criado"),
        ]
        
        for log in logs:
            row_frame = tk.Frame(self.logs_body, bg="#FFFFFF", height=40)
            row_frame.pack(fill=tk.X, padx=0, pady=1)
            row_frame.pack_propagate(False)
            
            for i, value in enumerate(log):
                label = tk.Label(
                    row_frame,
                    text=str(value),
                    font=("Inter", 12),
                    bg="#FFFFFF",
                    fg="#2d3748",
                    anchor="w"
                )
                label.grid(row=0, column=i, sticky="ew", padx=8, pady=8)
            
            for i in range(4):
                row_frame.grid_columnconfigure(i, weight=1)
        
        self.logs_canvas.configure(scrollregion=self.logs_canvas.bbox("all"))
    
    def _load_audit(self):
        """Carrega auditoria"""
        if not hasattr(self, 'audit_body'):
            return
        
        # Limpa auditoria anterior
        for widget in self.audit_body.winfo_children():
            widget.destroy()
        
        # Auditoria mockada (em produção, viria da API)
        audit = [
            (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "admin@helpwave.com", "Login", "Usuário fez login"),
            (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "admin@helpwave.com", "Criar Usuário", "Novo usuário criado: teste@helpwave.com"),
            (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "admin@helpwave.com", "Editar Usuário", "Usuário editado: ID 1"),
            (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "admin@helpwave.com", "Fechar Chamado", "Chamado #5 fechado"),
        ]
        
        for entry in audit:
            row_frame = tk.Frame(self.audit_body, bg="#FFFFFF", height=40)
            row_frame.pack(fill=tk.X, padx=0, pady=1)
            row_frame.pack_propagate(False)
            
            for i, value in enumerate(entry):
                label = tk.Label(
                    row_frame,
                    text=str(value),
                    font=("Inter", 12),
                    bg="#FFFFFF",
                    fg="#2d3748",
                    anchor="w"
                )
                label.grid(row=0, column=i, sticky="ew", padx=8, pady=8)
            
            for i in range(4):
                row_frame.grid_columnconfigure(i, weight=1)
        
        self.audit_canvas.configure(scrollregion=self.audit_canvas.bbox("all"))

