"""
UsersReportPage - Replica UsersReportPage.jsx do web
"""
import tkinter as tk
import customtkinter as ctk
from pages.base_page import BasePage
from api_client import UserService
from config import COLORS
import threading

def map_permissao_to_label(permissao):
    """Mapeia permissão para label"""
    n = int(permissao) if permissao else 1
    if n == 1:
        return 'Colaborador'
    if n == 2:
        return 'Suporte Técnico'
    if n == 3:
        return 'Administrador'
    return 'Desconhecido'

def get_permission_color(permissao):
    """Retorna cor da permissão"""
    n = int(permissao) if permissao else 1
    if n == 1:
        return '#4299e1'
    if n == 2:
        return '#f6ad55'
    if n == 3:
        return '#48bb78'
    return '#6c757d'

class UsersReportPage(BasePage):
    """Página de relatório de usuários - replica UsersReportPage.jsx"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page,
                 current_page, user_info, on_navigate_to_profile, on_view_user=None):
        super().__init__(parent, on_logout, on_navigate_to_page, current_page, user_info, 
                        page_title="RELATÓRIO DE USUÁRIOS", create_header_sidebar=False)
        
        self.on_navigate_to_home = on_navigate_to_home
        self.on_view_user = on_view_user
        self.users = []
        self.filtered_users = []
        self.loading = True
        self.search_term = ""
        
        self._create_ui()
        self._load_users()
    
    def _create_ui(self):
        """Cria interface"""
        # Container principal
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
        back_btn.pack(side="left", pady=(0, 24))
        
        # Barra de busca
        search_frame = tk.Frame(container, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        search_frame.pack(fill=tk.X, pady=(0, 24))
        
        search_inner = tk.Frame(search_frame, bg="#FFFFFF")
        search_inner.pack(fill=tk.X, padx=16, pady=12)
        
        tk.Label(
            search_inner,
            text="🔍",
            font=("Inter", 16),
            bg="#FFFFFF",
            fg="#666666"
        ).pack(side=tk.LEFT, padx=(0, 8))
        
        self.search_entry = tk.Entry(
            search_inner,
            font=("Inter", 14),
            bg="#FFFFFF",
            fg="#000000",
            bd=0,
            relief=tk.FLAT
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.insert(0, "Buscar por id, nome ou e-mail")
        self.search_entry.config(fg="#999999")
        self.search_entry.bind("<FocusIn>", self._on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self._on_search_focus_out)
        self.search_entry.bind("<KeyRelease>", self._on_search_change)
        
        # Tabela
        table_frame = tk.Frame(container, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho da tabela
        header_frame = tk.Frame(table_frame, bg="#A93226", height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        headers = ["ID", "NOME", "E-MAIL", "CARGO", "PERMISSÃO"]
        header_widths = [80, 200, 250, 150, 150]
        
        for i, (header_text, width) in enumerate(zip(headers, header_widths)):
            header_label = tk.Label(
                header_frame,
                text=header_text,
                font=("Inter", 12, "bold"),
                bg="#A93226",
                fg="white",
                width=width // 8,  # Aproximação
                anchor="w"
            )
            header_label.grid(row=0, column=i, sticky="ew", padx=8, pady=12)
        
        header_frame.grid_columnconfigure(0, weight=0)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(2, weight=1)
        header_frame.grid_columnconfigure(3, weight=1)
        header_frame.grid_columnconfigure(4, weight=1)
        
        # Frame scrollável para corpo da tabela usando Canvas
        self.table_canvas = tk.Canvas(table_frame, bg="#FFFFFF", highlightthickness=0)
        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.table_canvas.yview)
        
        self.table_body = tk.Frame(self.table_canvas, bg="#FFFFFF")
        canvas_window = self.table_canvas.create_window((0, 0), window=self.table_body, anchor="nw")
        
        def on_configure(event):
            canvas_width = event.width
            self.table_canvas.itemconfig(canvas_window, width=canvas_width)
            self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
        
        self.table_canvas.bind("<Configure>", on_configure)
        self.table_body.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))
        
        self.table_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.table_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mousewheel
        def on_mousewheel(event):
            self.table_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.table_canvas.bind("<MouseWheel>", on_mousewheel)
    
    def _on_search_focus_in(self, event):
        """Quando o campo de busca recebe foco"""
        if self.search_entry.get() == "Buscar por id, nome ou e-mail":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="#000000")
    
    def _on_search_focus_out(self, event):
        """Quando o campo de busca perde foco"""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Buscar por id, nome ou e-mail")
            self.search_entry.config(fg="#999999")
    
    def _on_search_change(self, event):
        """Quando o texto de busca muda"""
        if self.search_entry.get() != "Buscar por id, nome ou e-mail":
            self.search_term = self.search_entry.get().strip()
            self._apply_filter()
    
    def _apply_filter(self):
        """Aplica filtro de busca"""
        if not self.search_term:
            self.filtered_users = self.users
        else:
            q = self.search_term.lower()
            self.filtered_users = [
                u for u in self.users
                if str(u.get('id', '')).lower().find(q) >= 0 or
                   (u.get('nome', '') or '').lower().find(q) >= 0 or
                   (u.get('email', '') or '').lower().find(q) >= 0
            ]
        self._update_table()
    
    def _load_users(self):
        """Carrega usuários"""
        self.loading = True
        threading.Thread(target=self._do_load_users, daemon=True).start()
    
    def _do_load_users(self):
        """Faz carregamento de usuários"""
        try:
            response = UserService.get_users()
            
            # Normaliza resposta
            users_list = []
            if isinstance(response, list):
                users_list = response
            elif isinstance(response, dict):
                if isinstance(response.get('usuarios'), list):
                    users_list = response['usuarios']
                elif isinstance(response.get('items'), list):
                    users_list = response['items']
                elif isinstance(response.get('users'), list):
                    users_list = response['users']
                elif isinstance(response.get('data'), list):
                    users_list = response['data']
            
            # Normaliza campos
            normalized = []
            for u in users_list:
                normalized.append({
                    'id': u.get('id') or u.get('Id') or u.get('userId') or u.get('user_id'),
                    'nome': u.get('nome') or u.get('Nome') or u.get('name') or u.get('email') or 'Usuário',
                    'email': u.get('email') or u.get('Email') or u.get('username') or '',
                    'cargo': u.get('cargo') or u.get('Cargo') or '',
                    'permissao': u.get('permissao') or u.get('Permissao') or u.get('role') or 1
                })
            
            self.users = normalized
            self.filtered_users = normalized
        except Exception as e:
            print(f"Erro ao carregar usuários: {e}")
            self.users = []
            self.filtered_users = []
        finally:
            self.loading = False
            self.after(0, self._update_table)
    
    def _update_table(self):
        """Atualiza tabela"""
        # Limpa tabela
        for widget in self.table_body.winfo_children():
            widget.destroy()
        
        if self.loading:
            tk.Label(
                self.table_body,
                text="Carregando usuários...",
                font=("Inter", 14),
                bg="#FFFFFF",
                fg="#666666",
                pady=48
            ).pack(pady=48)
            self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
            return
        
        if not self.filtered_users:
            tk.Label(
                self.table_body,
                text="Nenhum usuário encontrado",
                font=("Inter", 14),
                bg="#FFFFFF",
                fg="#999999",
                pady=48
            ).pack(pady=48)
            self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
            return
        
        # Adiciona linhas
        for user in self.filtered_users:
            row_frame = tk.Frame(self.table_body, bg="#FFFFFF", height=50)
            row_frame.pack(fill=tk.X, padx=0, pady=1)
            row_frame.pack_propagate(False)
            
            # ID
            id_label = tk.Label(
                row_frame,
                text=str(user.get('id', '')),
                font=("Inter", 12),
                bg="#FFFFFF",
                fg="#000000",
                anchor="w"
            )
            id_label.grid(row=0, column=0, sticky="ew", padx=8, pady=12)
            
            # Nome
            nome_label = tk.Label(
                row_frame,
                text=user.get('nome', ''),
                font=("Inter", 12),
                bg="#FFFFFF",
                fg="#000000",
                anchor="w"
            )
            nome_label.grid(row=0, column=1, sticky="ew", padx=8, pady=12)
            
            # Email
            email_label = tk.Label(
                row_frame,
                text=user.get('email', ''),
                font=("Inter", 12),
                bg="#FFFFFF",
                fg="#000000",
                anchor="w"
            )
            email_label.grid(row=0, column=2, sticky="ew", padx=8, pady=12)
            
            # Cargo
            cargo_label = tk.Label(
                row_frame,
                text=user.get('cargo', ''),
                font=("Inter", 12),
                bg="#FFFFFF",
                fg="#000000",
                anchor="w"
            )
            cargo_label.grid(row=0, column=3, sticky="ew", padx=8, pady=12)
            
            # Permissão (badge)
            permissao = user.get('permissao', 1)
            permissao_text = map_permissao_to_label(permissao)
            permissao_color = get_permission_color(permissao)
            
            badge_frame = tk.Frame(row_frame, bg="#FFFFFF")
            badge_frame.grid(row=0, column=4, sticky="ew", padx=8, pady=12)
            
            badge_label = tk.Label(
                badge_frame,
                text=permissao_text,
                font=("Inter", 10, "bold"),
                bg=permissao_color,
                fg="white",
                padx=12,
                pady=4
            )
            badge_label.pack()
            
            # Configura grid
            row_frame.grid_columnconfigure(0, weight=0, minsize=80)
            row_frame.grid_columnconfigure(1, weight=1, minsize=200)
            row_frame.grid_columnconfigure(2, weight=1, minsize=250)
            row_frame.grid_columnconfigure(3, weight=1, minsize=150)
            row_frame.grid_columnconfigure(4, weight=1, minsize=150)
            
            # Bind para clique
            def make_click_handler(uid):
                def handler(event):
                    if self.on_view_user:
                        self.on_view_user(uid)
                    else:
                        # Fallback: navegar para user-activity usando arquivo temporário
                        try:
                            with open('.temp_user_id', 'w') as f:
                                f.write(str(uid))
                        except:
                            pass
                        if hasattr(self, 'on_navigate_to_page'):
                            self.on_navigate_to_page('user-activity')
                return handler
            
            row_frame.bind("<Button-1>", make_click_handler(user.get('id')))
            for widget in row_frame.winfo_children():
                widget.bind("<Button-1>", make_click_handler(user.get('id')))
            
            row_frame.config(cursor="hand2")
        
        # Atualiza scrollregion após renderizar tudo
        self.after(10, lambda: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

