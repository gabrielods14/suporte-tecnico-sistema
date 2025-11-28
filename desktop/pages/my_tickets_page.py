"""
MyTicketsPage - Página de Meus Chamados (para Colaboradores)
Mesma identidade visual da página de cadastro de funcionários
"""
import customtkinter as ctk
import tkinter as tk
from api_client import TicketService
from components.toast import show_toast
from config import COLORS
import threading
from datetime import datetime, timedelta


class MyTicketsPage(ctk.CTkFrame):
    """Página de meus chamados - mesma identidade visual do cadastro de funcionários"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page, 
                 current_page, user_info, on_navigate_to_ticket_detail, on_navigate_to_profile):
        super().__init__(parent, fg_color="#F8F9FA")
        
        self.on_logout = on_logout
        self.on_navigate_to_home = on_navigate_to_home
        self.on_navigate_to_page = on_navigate_to_page
        self.current_page = current_page
        self.user_info = user_info
        self.on_navigate_to_ticket_detail = on_navigate_to_ticket_detail
        self.on_navigate_to_profile = on_navigate_to_profile
        
        self.tickets = []
        self.filtered_tickets = []
        self.loading = True
        self.search_term = tk.StringVar(value="")
        self.search_term.trace('w', self._on_search_change)
        self.sort_by = "codigo"
        self.sort_order = "desc"
        
        self._create_ui()
        self._load_tickets()
    
    def _create_ui(self):
        """Cria interface com mesma identidade visual do cadastro de funcionários"""
        # Container principal
        main_container = ctk.CTkFrame(self, fg_color="#F8F9FA")
        main_container.pack(fill="both", expand=True, padx=48, pady=48)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(2, weight=1)
        
        # Botão voltar
        back_btn = ctk.CTkButton(
            main_container,
            text="← Voltar",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color=COLORS['primary'],
            hover_color=COLORS['neutral_100'],
            anchor="w",
            command=self.on_navigate_to_home
        )
        back_btn.grid(row=0, column=0, sticky="w", pady=(0, 20))
        
        # === FILTROS E BUSCA (Card branco) ===
        filters_card = ctk.CTkFrame(main_container, fg_color="#FFFFFF", corner_radius=16)
        filters_card.grid(row=1, column=0, sticky="ew", pady=(0, 24))
        filters_card.grid_columnconfigure(0, weight=1)
        
        filters_inner = ctk.CTkFrame(filters_card, fg_color="transparent")
        filters_inner.pack(fill="both", expand=True, padx=48, pady=32)
        filters_inner.grid_columnconfigure(0, weight=1)
        
        # Container para busca e ordenação
        controls_frame = ctk.CTkFrame(filters_inner, fg_color="transparent")
        controls_frame.grid(row=0, column=0, sticky="ew", pady=(0, 0))
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=0)
        
        # Campo de busca
        search_entry = ctk.CTkEntry(
            controls_frame,
            placeholder_text="Buscar por código ou título...",
            font=ctk.CTkFont(size=16),
            height=50,
            corner_radius=8,
            fg_color="#FFFFFF",
            text_color="#1A1A1A",
            border_width=2,
            border_color="#E5E5E5",
            textvariable=self.search_term
        )
        search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 16))
        search_entry.bind("<FocusIn>", lambda e: search_entry.configure(border_color="#A93226"))
        search_entry.bind("<FocusOut>", lambda e: search_entry.configure(border_color="#E5E5E5"))
        
        # Frame de ordenação
        sort_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        sort_frame.grid(row=0, column=1, sticky="e")
        
        sort_label = ctk.CTkLabel(
            sort_frame,
            text="Ordenar por:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#333333"
        )
        sort_label.pack(side="left", padx=(0, 8))
        
        self.sort_var = tk.StringVar(value="Código")
        sort_combo = ctk.CTkComboBox(
            sort_frame,
            values=["Código", "Título", "Prioridade", "Data Abertura"],
            variable=self.sort_var,
            command=self._on_sort_combo_change,
            font=ctk.CTkFont(size=14),
            height=50,
            width=150,
            corner_radius=8,
            fg_color="#FFFFFF",
            text_color="#1A1A1A",
            border_width=2,
            border_color="#E5E5E5",
            button_color="#E5E5E5",
            button_hover_color="#D5D5D5",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#1A1A1A",
            dropdown_hover_color="#F0F0F0"
        )
        sort_combo.pack(side="left", padx=(0, 8))
        
        self.order_var = tk.StringVar(value="desc")
        order_combo = ctk.CTkComboBox(
            sort_frame,
            values=["Crescente", "Decrescente"],
            variable=self.order_var,
            command=self._on_order_combo_change,
            font=ctk.CTkFont(size=14),
            height=50,
            width=150,
            corner_radius=8,
            fg_color="#FFFFFF",
            text_color="#1A1A1A",
            border_width=2,
            border_color="#E5E5E5",
            button_color="#E5E5E5",
            button_hover_color="#D5D5D5",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#1A1A1A",
            dropdown_hover_color="#F0F0F0"
        )
        order_combo.pack(side="left")
        
        # === TABELA (Card branco) ===
        table_card = ctk.CTkFrame(main_container, fg_color="#FFFFFF", corner_radius=16)
        table_card.grid(row=2, column=0, sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)
        
        # Padding interno
        table_inner = ctk.CTkFrame(table_card, fg_color="transparent")
        table_inner.pack(fill="both", expand=True, padx=48, pady=48)
        table_inner.grid_columnconfigure(0, weight=1)
        table_inner.grid_rowconfigure(1, weight=1)
        
        # Define larguras fixas para as colunas (em pixels) - COMPARTILHADO entre header e body
        col_widths = [120, 300, 150, 150, 150, 200]
        self.column_widths = col_widths  # Guarda para usar nas linhas
        
        # Calcula largura total exata (soma das colunas + padding de 16px de cada lado por coluna)
        # Armazena como atributo da classe para usar em _update_table
        self.total_table_width = sum(col_widths) + (len(col_widths) * 32)
        total_table_width = self.total_table_width
        
        # Container único para header e body - garante alinhamento perfeito
        table_wrapper = ctk.CTkFrame(table_inner, fg_color="transparent")
        table_wrapper.grid(row=0, column=0, sticky="nsew")
        table_wrapper.grid_columnconfigure(0, weight=1)
        table_wrapper.grid_rowconfigure(1, weight=1)
        
        # Cabeçalho da tabela - expande para ocupar toda a largura disponível
        header_frame = ctk.CTkFrame(table_wrapper, fg_color="#A93226", corner_radius=8, height=50)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        
        # Configura colunas - TÍTULO expande para ocupar espaço restante
        header_frame.grid_columnconfigure(0, weight=0, minsize=120)
        header_frame.grid_columnconfigure(1, weight=1)  # TÍTULO expande
        header_frame.grid_columnconfigure(2, weight=0, minsize=150)
        header_frame.grid_columnconfigure(3, weight=0, minsize=150)
        header_frame.grid_columnconfigure(4, weight=0, minsize=150)
        header_frame.grid_columnconfigure(5, weight=0, minsize=200)
        
        # Colunas do cabeçalho
        headers = [
            ("CÓDIGO", 0),
            ("TÍTULO", 1),
            ("PRIORIDADE", 2),
            ("DATA LIMITE", 3),
            ("STATUS", 4),
            ("TÉCNICO RESPONSÁVEL", 5)
        ]
        
        self.header_labels = {}
        for text, col in headers:
            label = ctk.CTkLabel(
                header_frame,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#FFFFFF",
                anchor="w" if col > 0 else "center"
            )
            # Padding consistente: todas as colunas usam padx=16
            label.grid(row=0, column=col, sticky="ew", padx=16, pady=16)
            if col in [0, 1, 2, 3]:  # Colunas clicáveis
                label.bind("<Button-1>", lambda e, c=col: self._handle_sort_click(c))
                label.configure(cursor="hand2")
                self.header_labels[col] = label
        
        # Container para o corpo da tabela usando Canvas - MESMA largura do header
        body_container = ctk.CTkFrame(table_wrapper, fg_color="transparent")
        body_container.grid(row=1, column=0, sticky="nsew")
        body_container.grid_columnconfigure(0, weight=1)
        body_container.grid_rowconfigure(0, weight=1)
        
        # Canvas e Scrollbar para controle preciso das larguras
        self.table_canvas = tk.Canvas(
            body_container,
            bg="#FFFFFF",
            highlightthickness=0,
            bd=0
        )
        self.table_scrollbar = tk.Scrollbar(
            body_container,
            orient="vertical",
            command=self.table_canvas.yview
        )
        
        # Frame wrapper que terá EXATAMENTE a mesma largura do cabeçalho
        self.table_body_wrapper = ctk.CTkFrame(
            self.table_canvas,
            fg_color="transparent"
        )
        
        # Configura as MESMAS colunas do cabeçalho (idêntico ao header)
        self.table_body_wrapper.grid_columnconfigure(0, weight=0, minsize=120)
        self.table_body_wrapper.grid_columnconfigure(1, weight=1)  # TÍTULO expande
        self.table_body_wrapper.grid_columnconfigure(2, weight=0, minsize=150)
        self.table_body_wrapper.grid_columnconfigure(3, weight=0, minsize=150)
        self.table_body_wrapper.grid_columnconfigure(4, weight=0, minsize=150)
        self.table_body_wrapper.grid_columnconfigure(5, weight=0, minsize=200)
        
        # Cria janela no canvas
        self.canvas_window = self.table_canvas.create_window(
            (0, 0),
            window=self.table_body_wrapper,
            anchor="nw"
        )
        
        # Configura scroll
        self.table_canvas.configure(yscrollcommand=self.table_scrollbar.set)
        
        # Função para sincronizar larguras - garante que body tenha mesma largura do header
        def sync_width(event=None):
            try:
                # Obtém largura do cabeçalho
                header_width = header_frame.winfo_width()
                canvas_width = self.table_canvas.winfo_width()
                
                if header_width > 1 and canvas_width > 1:
                    # Usa a largura do cabeçalho para o frame interno
                    self.table_canvas.itemconfig(self.canvas_window, width=header_width)
                    # Atualiza scrollregion
                    self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
            except:
                pass
        
        self.table_body_wrapper.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))
        self.table_canvas.bind("<Configure>", sync_width)
        header_frame.bind("<Configure>", sync_width)
        header_frame.bind("<Configure>", sync_width)
        
        # Pack canvas e scrollbar
        self.table_canvas.grid(row=0, column=0, sticky="nsew")
        self.table_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind mousewheel - funciona em toda a área da tabela
        def on_mousewheel(event):
            if hasattr(self, 'table_canvas') and self.table_canvas.winfo_exists():
                try:
                    self.table_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                except:
                    pass
        
        # Bind em múltiplos widgets para capturar scroll em toda a área da tabela
        self.table_canvas.bind("<MouseWheel>", on_mousewheel)
        body_container.bind("<MouseWheel>", on_mousewheel)
        if hasattr(self, 'table_body_wrapper'):
            self.table_body_wrapper.bind("<MouseWheel>", on_mousewheel)
        
        # Armazena função de scroll para usar nas linhas da tabela
        self._on_mousewheel = on_mousewheel
    
    def _on_search_change(self, *args):
        """Callback quando busca muda"""
        self._apply_filters_and_sort()
    
    def _on_sort_combo_change(self, value):
        """Callback quando combo de ordenação muda"""
        sort_map = {"Código": "codigo", "Título": "titulo", "Prioridade": "prioridade", "Data Abertura": "dataAbertura"}
        self.sort_by = sort_map.get(value, "dataAbertura")
        self._apply_filters_and_sort()
    
    def _on_order_combo_change(self, value):
        """Callback quando combo de ordem muda"""
        order_map = {"Crescente": "asc", "Decrescente": "desc"}
        self.sort_order = order_map.get(value, "desc")
        self._apply_filters_and_sort()
    
    def _handle_sort_click(self, column):
        """Handle clique na coluna do cabeçalho"""
        column_map = {0: "codigo", 1: "titulo", 2: "prioridade", 3: "dataAbertura"}
        column_name = column_map.get(column)
        
        if not column_name:
            return
        
        if self.sort_by == column_name:
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
        else:
            self.sort_by = column_name
            self.sort_order = "asc"
        
        # Atualiza combo boxes
        sort_map = {"codigo": "Código", "titulo": "Título", "prioridade": "Prioridade", "dataAbertura": "Data Abertura"}
        self.sort_var.set(sort_map.get(self.sort_by, "Código"))
        order_map = {"asc": "Crescente", "desc": "Decrescente"}
        self.order_var.set(order_map.get(self.sort_order, "Decrescente"))
        
        self._apply_filters_and_sort()
    
    def _get_priority_color(self, priority):
        """Retorna cor da prioridade"""
        colors = {
            'ALTA': '#dc3545',
            'MÉDIA': '#ffc107',
            'BAIXA': '#28a745'
        }
        return colors.get(priority, '#6c757d')
    
    def _get_status_color(self, status):
        """Retorna cor do status"""
        return {1: '#007bff', 2: '#ffc107', 3: '#6c757d'}.get(status, '#6c757d')
    
    def _map_priority(self, p):
        """Mapeia prioridade numérica para texto"""
        if isinstance(p, int):
            return 'ALTA' if p == 3 else 'MÉDIA' if p == 2 else 'BAIXA'
        p_str = str(p).upper()
        if 'ALTA' in p_str:
            return 'ALTA'
        if 'MÉDIA' in p_str or 'MEDIA' in p_str:
            return 'MÉDIA'
        return 'BAIXA'
    
    def _map_status(self, s):
        """Mapeia status numérico para texto"""
        if isinstance(s, int):
            return {1: 'ABERTO', 2: 'EM ATENDIMENTO', 3: 'FECHADO'}.get(s, 'DESCONHECIDO')
        return 'DESCONHECIDO'
    
    def _format_date(self, date_string):
        """Formata data"""
        try:
            date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return date.strftime('%d/%m/%Y')
        except:
            return date_string if date_string else 'N/A'
    
    def _load_tickets(self):
        """Carrega tickets do usuário"""
        self.loading = True
        threading.Thread(target=self._do_load_tickets, daemon=True).start()
    
    def _do_load_tickets(self):
        """Faz carregamento dos tickets"""
        try:
            user_id = self.user_info.get('id')
            print(f"[MyTicketsPage] user_info: {self.user_info}")
            print(f"[MyTicketsPage] user_id extraído: {user_id} (tipo: {type(user_id)})")
            
            if not user_id:
                print("[MyTicketsPage] user_id não encontrado, retornando lista vazia")
                self.after(0, lambda: setattr(self, 'loading', False))
                self.after(0, lambda: self._set_tickets([]))
                return
            
            # Garante que user_id seja int
            try:
                user_id_int = int(user_id)
            except (ValueError, TypeError):
                print(f"[MyTicketsPage] Erro ao converter user_id para int: {user_id}")
                self.after(0, lambda: setattr(self, 'loading', False))
                self.after(0, lambda: self._set_tickets([]))
                return
            
            filters = {'solicitanteId': user_id_int}
            print(f"[MyTicketsPage] Filtros aplicados: {filters}")
            tickets = TicketService.get_tickets(filters)
            print(f"[MyTicketsPage] Tickets retornados: {len(tickets) if tickets else 0}")
            if tickets:
                print(f"[MyTicketsPage] Primeiros 3 tickets - solicitanteId: {[t.get('solicitanteId') for t in tickets[:3]]}")
            
            if tickets:
                mapped = []
                for t in tickets:
                    # Filtra apenas tickets do usuário logado (segurança adicional)
                    ticket_solicitante_id = t.get('solicitanteId') or t.get('solicitante', {}).get('id') if isinstance(t.get('solicitante'), dict) else None
                    
                    # Converte para int para comparação
                    try:
                        ticket_solicitante_id = int(ticket_solicitante_id) if ticket_solicitante_id else None
                    except (ValueError, TypeError):
                        ticket_solicitante_id = None
                    
                    # Só adiciona se o ticket pertencer ao usuário logado
                    if ticket_solicitante_id != user_id_int:
                        print(f"[MyTicketsPage] Ticket {t.get('id')} ignorado - solicitanteId: {ticket_solicitante_id} != user_id: {user_id_int}")
                        continue
                    
                    prioridade = self._map_priority(t.get('prioridade', 2))
                    status_text = self._map_status(t.get('status', 1))
                    
                    mapped.append({
                        'id': t.get('id'),
                        'codigo': str(t.get('id', 0)).zfill(6),
                        'titulo': t.get('titulo', ''),
                        'prioridade': prioridade,
                        'status': t.get('status', 1),
                        'statusText': status_text,
                        'dataAbertura': t.get('dataAbertura', ''),
                        'dataLimite': t.get('dataLimite', ''),
                        'dataFechamento': t.get('dataFechamento'),
                        'tecnico': t.get('tecnicoResponsavel', {}).get('nome', 'N/A') if isinstance(t.get('tecnicoResponsavel'), dict) else 'N/A'
                    })
                
                print(f"[MyTicketsPage] Tickets filtrados para o usuário: {len(mapped)}")
                self.after(0, lambda: self._set_tickets(mapped))
            else:
                self.after(0, lambda: self._set_tickets([]))
        except Exception as e:
            self.after(0, lambda: show_toast(self, f"Erro ao carregar tickets: {str(e)}", "error"))
            self.after(0, lambda: self._set_tickets([]))
        finally:
            self.after(0, lambda: setattr(self, 'loading', False))
    
    def _set_tickets(self, tickets):
        """Define tickets e atualiza UI"""
        self.tickets = tickets or []
        self.loading = False
        self._apply_filters_and_sort()
    
    def _apply_filters_and_sort(self):
        """Aplica filtros e ordenação"""
        filtered = list(self.tickets)
        
        search = self.search_term.get().lower()
        if search:
            filtered = [t for t in filtered if 
                       search in t['titulo'].lower() or 
                       search in t['codigo'].lower()]
        
        def sort_key(t):
            if self.sort_by == 'codigo':
                return int(t['codigo'])
            elif self.sort_by == 'titulo':
                return t['titulo'].lower()
            elif self.sort_by == 'prioridade':
                order = {'ALTA': 1, 'MÉDIA': 2, 'BAIXA': 3}
                return order.get(t['prioridade'], 4)
            elif self.sort_by == 'dataAbertura':
                try:
                    return datetime.fromisoformat((t.get('dataAbertura') or '').replace('Z', '+00:00'))
                except:
                    return datetime.now()
            return datetime.now()
        
        filtered.sort(key=sort_key, reverse=(self.sort_order == 'desc'))
        self.filtered_tickets = filtered
        self._update_table()
    
    def _update_table(self):
        """Atualiza tabela"""
        # Verifica se o widget ainda existe antes de usar
        if not hasattr(self, 'table_body_wrapper') or not self.table_body_wrapper.winfo_exists():
            return
        
        # Limpa tabela
        try:
            for widget in self.table_body_wrapper.winfo_children():
                widget.destroy()
        except Exception:
            return
        
        # Atualiza indicadores de ordenação no cabeçalho
        column_map = {0: "codigo", 1: "titulo", 2: "prioridade", 3: "dataAbertura"}
        for col, label in self.header_labels.items():
            if label:
                try:
                    column_name = column_map.get(col)
                    if column_name and self.sort_by == column_name:
                        arrow = "▲" if self.sort_order == "asc" else "▼"
                        text = label.cget("text").split()[0] if " " in label.cget("text") else label.cget("text")
                        label.configure(text=f"{text} {arrow}")
                    else:
                        text = label.cget("text").split()[0] if " " in label.cget("text") else label.cget("text")
                        label.configure(text=text)
                except:
                    pass
        
        if self.loading:
            try:
                loading_label = ctk.CTkLabel(
                    self.table_body_wrapper,
                    text="Carregando...",
                    font=ctk.CTkFont(size=14),
                    text_color="#666666",
                    fg_color="transparent"
                )
                loading_label.grid(row=0, column=0, columnspan=6, pady=48)
                if hasattr(self, 'table_canvas') and self.table_canvas.winfo_exists():
                    self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
            except Exception:
                pass
            return
        
        if not self.filtered_tickets:
            try:
                no_data_label = ctk.CTkLabel(
                    self.table_body_wrapper,
                    text="Nenhum chamado encontrado",
                    font=ctk.CTkFont(size=14),
                    text_color="#999999",
                    fg_color="transparent"
                )
                no_data_label.grid(row=0, column=0, columnspan=6, pady=48)
                if hasattr(self, 'table_canvas') and self.table_canvas.winfo_exists():
                    self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
            except Exception:
                pass
            return
        
        # Cria linhas da tabela usando CTkFrame para cada linha
        try:
            for i, ticket in enumerate(self.filtered_tickets):
                # Verifica novamente se o widget ainda existe durante o loop
                if not hasattr(self, 'table_body_wrapper') or not self.table_body_wrapper.winfo_exists():
                    break
                
                row_bg = "#FFFFFF" if i % 2 == 0 else "#FAFAFA"
                
                # Frame da linha - expande para ocupar toda a largura disponível
                row_frame = ctk.CTkFrame(
                    self.table_body_wrapper,
                    fg_color=row_bg,
                    corner_radius=0,
                    height=60
                )
                row_frame.grid(row=i, column=0, columnspan=6, sticky="ew", padx=0, pady=1)
                
                # Configura as MESMAS colunas do cabeçalho (idêntico - mesma ordem, mesmas configurações)
                row_frame.grid_columnconfigure(0, weight=0, minsize=120)
                row_frame.grid_columnconfigure(1, weight=1)  # TÍTULO expande
                row_frame.grid_columnconfigure(2, weight=0, minsize=150)
                row_frame.grid_columnconfigure(3, weight=0, minsize=150)
                row_frame.grid_columnconfigure(4, weight=0, minsize=150)
                row_frame.grid_columnconfigure(5, weight=0, minsize=200)
                
                # Bind para clique
                def make_click_handler(tid):
                    def handler(event=None):
                        self._on_ticket_click(tid)
                    return handler
                
                click_handler = make_click_handler(ticket['id'])
                row_frame.bind("<Button-1>", click_handler)
                row_frame.configure(cursor="hand2")
                
                # Código
                code_label = ctk.CTkLabel(
                    row_frame,
                    text=ticket['codigo'],
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#A93226",
                    anchor="center",
                    fg_color="transparent"
                )
                code_label.grid(row=0, column=0, sticky="ew", padx=16, pady=16)
                code_label.bind("<Button-1>", click_handler)
                code_label.configure(cursor="hand2")
                
                # Título
                title_label = ctk.CTkLabel(
                    row_frame,
                    text=ticket['titulo'],
                    font=ctk.CTkFont(size=14),
                    text_color="#262626",
                    anchor="w",
                    fg_color="transparent"
                )
                title_label.grid(row=0, column=1, sticky="ew", padx=16, pady=16)
                title_label.bind("<Button-1>", click_handler)
                title_label.configure(cursor="hand2")
                
                # Prioridade (badge) - usando CTkLabel com corner_radius
                priority_color = self._get_priority_color(ticket['prioridade'])
                priority_badge = ctk.CTkLabel(
                    row_frame,
                    text=ticket['prioridade'],
                    font=ctk.CTkFont(size=12, weight="bold"),
                    fg_color=priority_color,
                    text_color="#FFFFFF",
                    corner_radius=999,
                    anchor="center"
                )
                priority_badge.grid(row=0, column=2, sticky="ew", padx=16, pady=16)
                priority_badge.bind("<Button-1>", click_handler)
                priority_badge.configure(cursor="hand2")
                
                # Data Limite
                date_text = self._format_date(ticket.get('dataLimite') or ticket.get('dataAbertura')) if (ticket.get('dataLimite') or ticket.get('dataAbertura')) else 'N/A'
                date_label = ctk.CTkLabel(
                    row_frame,
                    text=date_text,
                    font=ctk.CTkFont(size=14),
                    text_color="#666666",
                    anchor="w",
                    fg_color="transparent"
                )
                date_label.grid(row=0, column=3, sticky="ew", padx=16, pady=16)
                date_label.bind("<Button-1>", click_handler)
                date_label.configure(cursor="hand2")
                
                # Status (badge)
                status_color = self._get_status_color(ticket['status'])
                status_badge = ctk.CTkLabel(
                    row_frame,
                    text=ticket['statusText'],
                    font=ctk.CTkFont(size=12, weight="bold"),
                    fg_color=status_color,
                    text_color="#FFFFFF",
                    corner_radius=999,
                    anchor="center"
                )
                status_badge.grid(row=0, column=4, sticky="ew", padx=16, pady=16)
                status_badge.bind("<Button-1>", click_handler)
                status_badge.configure(cursor="hand2")
                
                # Técnico Responsável
                tecnico_label = ctk.CTkLabel(
                    row_frame,
                    text=ticket['tecnico'],
                    font=ctk.CTkFont(size=14),
                    text_color="#666666",
                    anchor="w",
                    fg_color="transparent"
                )
                tecnico_label.grid(row=0, column=5, sticky="ew", padx=16, pady=16)
                tecnico_label.bind("<Button-1>", click_handler)
                tecnico_label.configure(cursor="hand2")
        except Exception:
            pass
        
        # Atualiza scrollregion
        try:
            if hasattr(self, 'table_canvas') and self.table_canvas.winfo_exists():
                self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
        except Exception:
            pass
    
    def _on_ticket_click(self, ticket_id):
        """Handle clique no ticket"""
        if self.on_navigate_to_ticket_detail:
            self.on_navigate_to_ticket_detail(ticket_id)
