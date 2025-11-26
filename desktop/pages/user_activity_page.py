"""
UserActivityPage - Replica UserActivityPage.jsx do web
"""
import tkinter as tk
from pages.base_page import BasePage
from api_client import UserService, TicketService
from datetime import datetime
import threading
import os

def map_status_label(status):
    """Mapeia status para label"""
    s = int(status) if status else 1
    if s == 1:
        return 'Aberto'
    if s == 2:
        return 'Em Atendimento'
    if s == 3:
        return 'Fechado'
    return 'Desconhecido'

def map_permissao_label(permissao):
    """Mapeia permissão para label"""
    p = int(permissao) if permissao else 1
    if p == 1:
        return 'Colaborador'
    if p == 2:
        return 'Suporte Técnico'
    if p == 3:
        return 'Administrador'
    return 'Desconhecido'

class UserActivityPage(BasePage):
    """Página de atividade do usuário - replica UserActivityPage.jsx"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page,
                 current_page, user_info, on_navigate_to_profile, userId=None, on_back=None):
        super().__init__(parent, on_logout, on_navigate_to_page, current_page, user_info, 
                        page_title="ATIVIDADE DO USUÁRIO", create_header_sidebar=False)
        
        self.on_navigate_to_home = on_navigate_to_home
        self.on_back = on_back
        self.user_id = userId
        self.user = None
        self.tickets_opened = []
        self.tickets_resolved = []
        self.login_count = None
        self.loading = True
        
        # Tenta obter user_id do arquivo temporário se não fornecido
        if not self.user_id:
            try:
                if os.path.exists('.temp_user_id'):
                    with open('.temp_user_id', 'r') as f:
                        self.user_id = int(f.read().strip())
                    os.remove('.temp_user_id')
            except:
                pass
        
        self._create_ui()
        if self.user_id:
            self._load_activity()
    
    def _create_ui(self):
        """Cria interface"""
        # Container principal
        container = tk.Frame(self.main_content, bg="#F8F9FA")
        container.pack(fill=tk.BOTH, expand=True, padx=48, pady=48)
        
        
        # Título
        title_label = tk.Label(
            container,
            text="ATIVIDADE DO USUÁRIO",
            font=("Inter", 24, "bold"),
            bg="#F8F9FA",
            fg="#000000"
        )
        title_label.pack(anchor="w", pady=(0, 24))
        
        # Container de conteúdo (será preenchido quando carregar)
        self.content_frame = tk.Frame(container, bg="#F8F9FA")
        self.content_frame.pack(fill=tk.BOTH, expand=True)
    
    def _load_activity(self):
        """Carrega atividade do usuário"""
        self.loading = True
        threading.Thread(target=self._do_load_activity, daemon=True).start()
    
    def _do_load_activity(self):
        """Faz carregamento"""
        try:
            # Buscar dados do usuário
            try:
                user_data = UserService.getUser(self.user_id)
            except:
                # Fallback: obter lista completa e procurar
                try:
                    all_data = UserService.get_users()
                    all_users = []
                    if isinstance(all_data, list):
                        all_users = all_data
                    elif isinstance(all_data, dict):
                        all_users = all_data.get('usuarios', []) or all_data.get('items', []) or all_data.get('users', [])
                    
                    user_data = next((u for u in all_users if int(u.get('id') or 0) == int(self.user_id)), None)
                except:
                    user_data = None
            
            self.user = user_data or {'id': self.user_id, 'nome': f'Usuário {self.user_id}'}
            
            # Buscar chamados abertos pelo usuário
            try:
                opened = TicketService.get_tickets({'solicitanteId': self.user_id})
                tickets_data = opened if isinstance(opened, list) else []
            except:
                try:
                    all_tickets = TicketService.get_tickets()
                    all_list = all_tickets if isinstance(all_tickets, list) else []
                    tickets_data = [t for t in all_list if int(t.get('solicitanteId') or 0) == int(self.user_id)]
                except:
                    tickets_data = []
            
            # Separar resolvidos dos abertos
            resolved = [t for t in tickets_data if int(t.get('status', 0)) == 3]
            opened_list = [t for t in tickets_data if int(t.get('status', 0)) != 3]
            
            # Para técnicos, incluir chamados onde ele é responsável
            if self.user and int(self.user.get('permissao', 1)) == 2:
                try:
                    assigned = TicketService.get_tickets()
                    assigned_list = assigned if isinstance(assigned, list) else []
                    resolved_by_tech = [
                        t for t in assigned_list
                        if int(t.get('tecnicoResponsavel', {}).get('id', 0) or t.get('tecnicoResponsavelId', 0)) == int(self.user_id)
                        and int(t.get('status', 0)) == 3
                    ]
                    resolved.extend(resolved_by_tech)
                except:
                    pass
            
            self.tickets_opened = opened_list
            self.tickets_resolved = resolved
            
            # Tentar buscar contagem de logins (opcional)
            try:
                # Nota: Endpoint de logins pode não estar implementado
                self.login_count = None
            except:
                pass
        except Exception as e:
            print(f"Erro ao carregar atividade: {e}")
            self.user = {'id': self.user_id, 'nome': f'Usuário {self.user_id}'}
            self.tickets_opened = []
            self.tickets_resolved = []
        finally:
            self.loading = False
            self.after(0, self._update_ui)
    
    def _format_date(self, date_string):
        """Formata data"""
        if not date_string:
            return 'N/A'
        try:
            if isinstance(date_string, str):
                dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            else:
                dt = date_string
            return dt.strftime('%d/%m/%Y %H:%M')
        except:
            return str(date_string)
    
    def _calc_open_time(self, ticket):
        """Calcula tempo que o ticket ficou aberto"""
        try:
            open_date = datetime.fromisoformat((ticket.get('dataAbertura') or ticket.get('createdAt') or '').replace('Z', '+00:00'))
            close_date = ticket.get('dataFechamento')
            if close_date:
                close_date = datetime.fromisoformat(str(close_date).replace('Z', '+00:00'))
            else:
                close_date = datetime.now()
            
            diff = abs((close_date - open_date).total_seconds())
            days = int(diff // (24 * 3600))
            hours = int((diff % (24 * 3600)) // 3600)
            return f"{days}d {hours}h"
        except:
            return 'N/A'
    
    def _update_ui(self):
        """Atualiza UI"""
        # Limpa conteúdo
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if self.loading:
            tk.Label(
                self.content_frame,
                text="Carregando atividade do usuário...",
                font=("Inter", 14),
                bg="#F8F9FA",
                fg="#666666",
                pady=48
            ).pack(pady=48)
            return
        
        if not self.user:
            tk.Label(
                self.content_frame,
                text="Usuário não encontrado",
                font=("Inter", 14),
                bg="#F8F9FA",
                fg="#DC3545",
                pady=48
            ).pack(pady=48)
            return
        
        # Resumo do usuário
        summary_frame = tk.Frame(self.content_frame, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        summary_frame.pack(fill=tk.X, pady=(0, 24))
        
        summary_inner = tk.Frame(summary_frame, bg="#FFFFFF")
        summary_inner.pack(fill=tk.X, padx=24, pady=24)
        
        tk.Label(
            summary_inner,
            text=self.user.get('nome', f'Usuário {self.user_id}'),
            font=("Inter", 20, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        ).pack(anchor="w", pady=(0, 16))
        
        info_text = f"ID: {self.user.get('id', 'N/A')}\n"
        info_text += f"E-mail: {self.user.get('email', 'N/A')}\n"
        info_text += f"Cargo: {self.user.get('cargo', 'N/A')}\n"
        info_text += f"Permissão: {map_permissao_label(self.user.get('permissao', 1))}\n"
        info_text += f"Logins: {self.login_count if self.login_count is not None else 'N/D'}"
        
        tk.Label(
            summary_inner,
            text=info_text,
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#666666",
            anchor="w",
            justify=tk.LEFT
        ).pack(anchor="w")
        
        # Chamados abertos
        self._create_tickets_section(
            f"CHAMADOS ABERTOS PELO USUÁRIO ({len(self.tickets_opened)})",
            self.tickets_opened,
            ['CÓDIGO', 'TÍTULO', 'STATUS', 'DATA ABERTURA', 'TEMPO ABERTO'],
            self._get_opened_ticket_row
        )
        
        # Chamados resolvidos
        self._create_tickets_section(
            f"CHAMADOS RESOLVIDOS ({len(self.tickets_resolved)})",
            self.tickets_resolved,
            ['CÓDIGO', 'TÍTULO', 'DATA ABERTURA', 'DATA FECHAMENTO', 'TEMPO ABERTO'],
            self._get_resolved_ticket_row
        )
    
    def _create_tickets_section(self, title, tickets, headers, row_func):
        """Cria seção de tickets"""
        section_frame = tk.Frame(self.content_frame, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        section_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 24))
        
        # Título da seção
        title_frame = tk.Frame(section_frame, bg="#FFFFFF")
        title_frame.pack(fill=tk.X, padx=24, pady=(24, 16))
        
        tk.Label(
            title_frame,
            text=title,
            font=("Inter", 16, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        ).pack(anchor="w")
        
        # Tabela
        table_frame = tk.Frame(section_frame, bg="#FFFFFF")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))
        
        # Cabeçalho
        header_frame = tk.Frame(table_frame, bg="#A93226", height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        for i, header_text in enumerate(headers):
            header_label = tk.Label(
                header_frame,
                text=header_text,
                font=("Inter", 12, "bold"),
                bg="#A93226",
                fg="white",
                anchor="w"
            )
            header_label.grid(row=0, column=i, sticky="ew", padx=8, pady=12)
        
        for i in range(len(headers)):
            header_frame.grid_columnconfigure(i, weight=1)
        
        # Corpo da tabela
        from pages.pending_tickets_page import ScrollableFrame
        scrollable = ScrollableFrame(table_frame, bg="#FFFFFF")
        scrollable.pack(fill=tk.BOTH, expand=True)
        
        body_frame = scrollable.scrollable_frame
        
        if not tickets:
            tk.Label(
                body_frame,
                text="Nenhum chamado encontrado",
                font=("Inter", 12),
                bg="#FFFFFF",
                fg="#999999",
                pady=48
            ).pack(pady=48)
            return
        
        # Adiciona linhas
        for ticket in tickets:
            row_frame = tk.Frame(body_frame, bg="#FFFFFF", height=50)
            row_frame.pack(fill=tk.X, padx=0, pady=1)
            row_frame.pack_propagate(False)
            
            row_func(row_frame, ticket, headers)
        
        self.after(10, lambda: scrollable.update_scroll())
    
    def _get_opened_ticket_row(self, row_frame, ticket, headers):
        """Cria linha para ticket aberto"""
        # Código
        code_label = tk.Label(
            row_frame,
            text=str(ticket.get('id', 0)).zfill(6),
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        code_label.grid(row=0, column=0, sticky="ew", padx=8, pady=12)
        
        # Título
        title_label = tk.Label(
            row_frame,
            text=ticket.get('titulo', ''),
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        title_label.grid(row=0, column=1, sticky="ew", padx=8, pady=12)
        
        # Status
        status_label = tk.Label(
            row_frame,
            text=map_status_label(ticket.get('status', 1)),
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        status_label.grid(row=0, column=2, sticky="ew", padx=8, pady=12)
        
        # Data abertura
        date_label = tk.Label(
            row_frame,
            text=self._format_date(ticket.get('dataAbertura') or ticket.get('createdAt')),
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        date_label.grid(row=0, column=3, sticky="ew", padx=8, pady=12)
        
        # Tempo aberto
        time_label = tk.Label(
            row_frame,
            text=self._calc_open_time(ticket),
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        time_label.grid(row=0, column=4, sticky="ew", padx=8, pady=12)
        
        # Configura grid
        for i in range(5):
            row_frame.grid_columnconfigure(i, weight=1)
    
    def _get_resolved_ticket_row(self, row_frame, ticket, headers):
        """Cria linha para ticket resolvido"""
        # Código
        code_label = tk.Label(
            row_frame,
            text=str(ticket.get('id', 0)).zfill(6),
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        code_label.grid(row=0, column=0, sticky="ew", padx=8, pady=12)
        
        # Título
        title_label = tk.Label(
            row_frame,
            text=ticket.get('titulo', ''),
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        title_label.grid(row=0, column=1, sticky="ew", padx=8, pady=12)
        
        # Data abertura
        date_label = tk.Label(
            row_frame,
            text=self._format_date(ticket.get('dataAbertura')),
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        date_label.grid(row=0, column=2, sticky="ew", padx=8, pady=12)
        
        # Data fechamento
        close_label = tk.Label(
            row_frame,
            text=self._format_date(ticket.get('dataFechamento')),
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        close_label.grid(row=0, column=3, sticky="ew", padx=8, pady=12)
        
        # Tempo aberto
        time_label = tk.Label(
            row_frame,
            text=self._calc_open_time(ticket),
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        time_label.grid(row=0, column=4, sticky="ew", padx=8, pady=12)
        
        # Configura grid
        for i in range(5):
            row_frame.grid_columnconfigure(i, weight=1)

