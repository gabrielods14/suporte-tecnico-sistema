"""
CompletedTicketsPage - Página de chamados concluídos
Mesma identidade visual da página de cadastro de funcionários
"""
import customtkinter as ctk
import tkinter as tk
from api_client import TicketService
from config import COLORS
import threading
from datetime import datetime


class CompletedTicketsPage(ctk.CTkFrame):
    """Página de chamados concluídos - mesma identidade visual do cadastro de funcionários"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page,
                 current_page, user_info, on_navigate_to_ticket_detail):
        super().__init__(parent, fg_color="#F8F9FA")
        
        self.on_logout = on_logout
        self.on_navigate_to_home = on_navigate_to_home
        self.on_navigate_to_page = on_navigate_to_page
        self.current_page = current_page
        self.user_info = user_info
        self.on_navigate_to_ticket_detail = on_navigate_to_ticket_detail
        
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
            values=["Código", "Título", "Prioridade", "Data Fechamento"],
            variable=self.sort_var,
            command=self._on_sort_combo_change,
            font=ctk.CTkFont(size=14),
            height=50,
            width=180,
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
        
        # Cabeçalho da tabela
        header_frame = ctk.CTkFrame(table_inner, fg_color="#A93226", corner_radius=8, height=50)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        # 6 colunas (sem STATUS)
        header_frame.grid_columnconfigure(0, weight=0, minsize=120)  # CÓDIGO
        header_frame.grid_columnconfigure(1, weight=1)                # TÍTULO
        header_frame.grid_columnconfigure(2, weight=0, minsize=150)  # PRIORIDADE
        header_frame.grid_columnconfigure(3, weight=0, minsize=150)  # SOLICITANTE
        header_frame.grid_columnconfigure(4, weight=0, minsize=150)  # TÉCNICO
        header_frame.grid_columnconfigure(5, weight=0, minsize=180)  # DATA
        header_frame.pack_propagate(False)
        
        # Colunas do cabeçalho (6 colunas - sem STATUS)
        headers = [
            ("CÓDIGO", 0),
            ("TÍTULO", 1),
            ("PRIORIDADE", 2),
            ("SOLICITANTE", 3),
            ("TÉCNICO", 4),
            ("DATA FECHAMENTO", 5)
        ]
        
        self.header_labels = {}
        for text, col in headers:
            anchor = "e" if col == 5 else ("w" if col > 0 else "center")
            label = ctk.CTkLabel(
                header_frame,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#FFFFFF",
                anchor=anchor
            )
            if col == 0:
                label.grid(row=0, column=col, sticky="ew", padx=(16, 8), pady=16)
            elif col == 5:
                label.grid(row=0, column=col, sticky="ew", padx=(8, 16), pady=16)
            else:
                label.grid(row=0, column=col, sticky="ew", padx=8, pady=16)
            if col in [0, 1, 2, 5]:  # Colunas clicáveis
                label.bind("<Button-1>", lambda e, c=col: self._handle_sort_click(c))
                label.configure(cursor="hand2")
                self.header_labels[col] = label
        
        # Container para o corpo da tabela
        body_container = ctk.CTkFrame(table_inner, fg_color="transparent")
        body_container.grid(row=1, column=0, sticky="nsew")
        body_container.grid_columnconfigure(0, weight=1)
        body_container.grid_rowconfigure(0, weight=1)
        
        # Canvas para scroll
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
        
        # Frame interno no canvas com EXATAMENTE as mesmas colunas do cabeçalho
        self.table_body_wrapper = ctk.CTkFrame(
            self.table_canvas,
            fg_color="transparent"
        )
        
        # Configura EXATAMENTE as mesmas 6 colunas do cabeçalho
        self.table_body_wrapper.grid_columnconfigure(0, weight=0, minsize=120)
        self.table_body_wrapper.grid_columnconfigure(1, weight=1)
        self.table_body_wrapper.grid_columnconfigure(2, weight=0, minsize=150)
        self.table_body_wrapper.grid_columnconfigure(3, weight=0, minsize=150)
        self.table_body_wrapper.grid_columnconfigure(4, weight=0, minsize=150)
        self.table_body_wrapper.grid_columnconfigure(5, weight=0, minsize=180)
        
        # Cria janela no canvas
        self.canvas_window = self.table_canvas.create_window(
            (0, 0),
            window=self.table_body_wrapper,
            anchor="nw"
        )
        
        # Configura scroll
        self.table_canvas.configure(yscrollcommand=self.table_scrollbar.set)
        
        # Função para sincronizar largura
        def sync_width(event=None):
            try:
                header_frame.update_idletasks()
                header_width = header_frame.winfo_width()
                
                if header_width > 1:
                    # Força o wrapper a ter exatamente a mesma largura do cabeçalho
                    self.table_canvas.itemconfig(self.canvas_window, width=header_width)
                    self.table_body_wrapper.configure(width=header_width)
                    self.table_body_wrapper.update_idletasks()
                    self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
            except:
                pass
        
        # Armazena função
        self._sync_width = sync_width
        
        # Layout canvas e scrollbar
        self.table_canvas.grid(row=0, column=0, sticky="nsew")
        self.table_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Mousewheel - bind em múltiplos widgets para melhor funcionalidade
        def on_mousewheel(event):
            try:
                if hasattr(self, 'table_canvas') and self.table_canvas.winfo_exists():
                    self.table_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except Exception:
                pass
        
        # Bind em múltiplos widgets para capturar scroll em toda a área da tabela
        self.table_canvas.bind("<MouseWheel>", on_mousewheel)
        body_container.bind("<MouseWheel>", on_mousewheel)
        if hasattr(self, 'table_body_wrapper'):
            self.table_body_wrapper.bind("<MouseWheel>", on_mousewheel)
        
        # Armazena função de scroll para usar nas linhas da tabela
        self._on_mousewheel = on_mousewheel
        
        # Bind para sincronizar largura
        header_frame.bind("<Configure>", sync_width)
        self.table_body_wrapper.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))
        
        # Guarda referência
        self.header_frame_ref = header_frame
    
    def _on_search_change(self, *args):
        """Callback quando busca muda"""
        self._apply_filters_and_sort()
    
    def _on_sort_combo_change(self, value):
        """Callback quando combo de ordenação muda"""
        sort_map = {"Código": "codigo", "Título": "titulo", "Prioridade": "prioridade", "Data Fechamento": "dataFechamento"}
        self.sort_by = sort_map.get(value, "dataFechamento")
        self._apply_filters_and_sort()
    
    def _on_order_combo_change(self, value):
        """Callback quando combo de ordem muda"""
        order_map = {"Crescente": "asc", "Decrescente": "desc"}
        self.sort_order = order_map.get(value, "desc")
        self._apply_filters_and_sort()
    
    def _handle_sort_click(self, column):
        """Handle clique na coluna do cabeçalho"""
        column_map = {0: "codigo", 1: "titulo", 2: "prioridade", 5: "dataFechamento"}
        column_name = column_map.get(column)
        
        if not column_name:
            return
        
        if self.sort_by == column_name:
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
        else:
            self.sort_by = column_name
            self.sort_order = "asc"
        
        # Atualiza combo boxes
        sort_map = {"codigo": "Código", "titulo": "Título", "prioridade": "Prioridade", "dataFechamento": "Data Fechamento"}
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
        status_num = int(status) if isinstance(status, (int, str)) and str(status).isdigit() else 0
        if status_num == 1:
            return '#ffc107'  # Amarelo - Aberto
        elif status_num == 2:
            return '#17a2b8'  # Azul - Em Atendimento
        elif status_num == 3:
            return '#28a745'  # Verde - Concluído
        return '#6c757d'  # Cinza - Default
    
    def _get_status_text(self, status):
        """Retorna texto do status"""
        status_num = int(status) if isinstance(status, (int, str)) and str(status).isdigit() else 0
        if status_num == 1:
            return 'ABERTO'
        elif status_num == 2:
            return 'EM ATENDIMENTO'
        elif status_num == 3:
            return 'CONCLUÍDO'
        return 'N/A'
    
    def _truncate_text(self, text, max_chars=10):
        """Trunca texto se exceder max_chars e adiciona '...'"""
        if not text:
            return ""
        text_str = str(text)
        if len(text_str) > max_chars:
            return text_str[:max_chars] + "..."
        return text_str
    
    def _load_tickets(self):
        """Carrega tickets"""
        self.loading = True
        threading.Thread(target=self._do_load_tickets, daemon=True).start()
    
    def _do_load_tickets(self):
        """Faz carregamento"""
        try:
            api_tickets = TicketService.get_tickets()
            
            if api_tickets:
                mapped = []
                for item in api_tickets:
                    if item.get('status') == 3:  # Status 3 = Fechado (concluído)
                        prioridade = item.get('prioridade', 2)
                        if isinstance(prioridade, int):
                            prioridade_text = 'ALTA' if prioridade == 3 else 'MÉDIA' if prioridade == 2 else 'BAIXA'
                        else:
                            prioridade_text = 'MÉDIA'
                        
                        status_text = 'CONCLUÍDO'
                        tecnico = item.get('tecnicoResponsavel', {}).get('nome', 'N/A') if isinstance(item.get('tecnicoResponsavel'), dict) else 'N/A'
                        solicitante = item.get('solicitante', {}).get('nome', 'N/A') if isinstance(item.get('solicitante'), dict) else 'N/A'
                        
                        mapped.append({
                            'id': item.get('id'),
                            'codigo': str(item.get('id', 0)).zfill(6),
                            'titulo': item.get('titulo', ''),
                            'prioridade': prioridade_text,
                            'status': item.get('status'),
                            'statusText': status_text,
                            'solicitante': solicitante,
                            'tecnico': tecnico,
                            'dataFechamento': item.get('dataFechamento', item.get('dataAbertura', ''))
                        })
                
                self.tickets = mapped
            else:
                self.tickets = []
        except Exception as e:
            print(f"Erro ao carregar tickets: {e}")
            self.tickets = []
        finally:
            self.loading = False
            self.after(0, self._apply_filters_and_sort)
    
    def _apply_filters_and_sort(self):
        """Aplica filtros e ordenação"""
        filtered = [t for t in self.tickets]
        
        search = self.search_term.get().lower()
        if search:
            filtered = [t for t in filtered if 
                       search in t['titulo'].lower() or 
                       search in t['codigo'].lower()]
        
        def sort_key(ticket):
            if self.sort_by == 'codigo':
                return int(ticket['codigo'])
            elif self.sort_by == 'titulo':
                return ticket['titulo'].lower()
            elif self.sort_by == 'prioridade':
                order = {'ALTA': 1, 'MÉDIA': 2, 'BAIXA': 3}
                return order.get(ticket['prioridade'], 4)
            elif self.sort_by == 'dataFechamento':
                try:
                    return datetime.fromisoformat(ticket['dataFechamento'].replace('Z', '+00:00'))
                except:
                    return datetime.now()
            return 0
        
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
        column_map = {0: "codigo", 1: "titulo", 2: "prioridade", 5: "dataFechamento"}
        header_texts = {
            0: "CÓDIGO",
            1: "TÍTULO",
            2: "PRIORIDADE",
            3: "SOLICITANTE",
            4: "TÉCNICO",
            5: "DATA FECHAMENTO"
        }
        for col, label in self.header_labels.items():
            if label:
                try:
                    column_name = column_map.get(col)
                    base_text = header_texts.get(col, "")
                    if column_name and self.sort_by == column_name:
                        arrow = "▲" if self.sort_order == "asc" else "▼"
                        label.configure(text=f"{base_text} {arrow}")
                    else:
                        label.configure(text=base_text)
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
            except Exception:
                pass
            return
        
        if not self.filtered_tickets:
            try:
                no_data_label = ctk.CTkLabel(
                    self.table_body_wrapper,
                text="Nenhum chamado concluído encontrado",
                    font=ctk.CTkFont(size=14),
                    text_color="#999999",
                    fg_color="transparent"
                )
                no_data_label.grid(row=0, column=0, columnspan=6, pady=48)
            except Exception:
                pass
            return
        
        # Cria linhas da tabela
        for i, ticket in enumerate(self.filtered_tickets):
            row_bg = "#FFFFFF" if i % 2 == 0 else "#FAFAFA"
            
            # Frame de fundo para a linha inteira
            bg_frame = ctk.CTkFrame(
                self.table_body_wrapper,
                fg_color=row_bg,
                corner_radius=0,
                height=60
            )
            bg_frame.grid(row=i, column=0, columnspan=6, sticky="ew", pady=0)
            bg_frame.grid_propagate(False)
            
            # Bind para clique na linha
            def make_click_handler(tid):
                def handler(event=None):
                    self._on_ticket_click(tid)
                return handler
            
            click_handler = make_click_handler(ticket['id'])
            bg_frame.bind("<Button-1>", click_handler)
            bg_frame.configure(cursor="hand2")
            
            # Código
            code_label = ctk.CTkLabel(
                self.table_body_wrapper,
                text=ticket['codigo'],
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#A93226",
                anchor="center",
                fg_color="transparent"
            )
            code_label.grid(row=i, column=0, sticky="ew", padx=(16, 8), pady=16)
            
            # Título
            title_label = ctk.CTkLabel(
                self.table_body_wrapper,
                text=ticket['titulo'],
                font=ctk.CTkFont(size=14),
                text_color="#262626",
                anchor="w",
                fg_color="transparent"
            )
            title_label.grid(row=i, column=1, sticky="ew", padx=8, pady=16)
            
            # Prioridade (badge)
            priority_color = self._get_priority_color(ticket['prioridade'])
            priority_badge = ctk.CTkLabel(
                self.table_body_wrapper,
                text=ticket['prioridade'],
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=priority_color,
                text_color="#FFFFFF",
                corner_radius=999,
                anchor="center"
            )
            priority_badge.grid(row=i, column=2, sticky="ew", padx=8, pady=16)
            
            # Solicitante (movido para coluna 3) - truncado
            solicitante_text = self._truncate_text(ticket.get('solicitante', 'N/A'), max_chars=10)
            solicitante_label = ctk.CTkLabel(
                self.table_body_wrapper,
                text=solicitante_text,
                font=ctk.CTkFont(size=14),
                text_color="#666666",
                anchor="w",
                fg_color="transparent"
            )
            solicitante_label.grid(row=i, column=3, sticky="ew", padx=8, pady=16)
            
            # Técnico (movido para coluna 4) - truncado
            tecnico_text = self._truncate_text(ticket.get('tecnico', 'N/A'), max_chars=10)
            tecnico_label = ctk.CTkLabel(
                self.table_body_wrapper,
                text=tecnico_text,
                font=ctk.CTkFont(size=14),
                text_color="#666666",
                anchor="w",
                fg_color="transparent"
            )
            tecnico_label.grid(row=i, column=4, sticky="ew", padx=8, pady=16)
            
            # Data Fechamento (movido para coluna 5)
            try:
                data = datetime.fromisoformat(ticket['dataFechamento'].replace('Z', '+00:00')).strftime('%d/%m/%Y')
            except:
                data = "N/A"
            date_label = ctk.CTkLabel(
                self.table_body_wrapper,
                text=data,
                font=ctk.CTkFont(size=14),
                text_color="#666666",
                anchor="e",
                fg_color="transparent"
            )
            date_label.grid(row=i, column=5, sticky="ew", padx=(8, 16), pady=16)
            
            # Bind clique em todos os widgets
            widgets_to_bind = [code_label, title_label, priority_badge, solicitante_label, tecnico_label, date_label, bg_frame]
            for widget in widgets_to_bind:
                widget.bind("<Button-1>", click_handler)
                widget.configure(cursor="hand2")
                # Adiciona bind de scroll também
                if hasattr(self, '_on_mousewheel'):
                    widget.bind("<MouseWheel>", self._on_mousewheel)
        
        # Força atualização e sincroniza larguras
        self.update_idletasks()
        self.table_body_wrapper.update_idletasks()
        self.table_canvas.update_idletasks()
        self.header_frame_ref.update_idletasks()
        
        # Sincroniza larguras após renderizar linhas
        self.after(10, self._sync_width)
        self.after(100, self._sync_width)
        
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
