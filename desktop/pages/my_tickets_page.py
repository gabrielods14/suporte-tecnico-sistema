"""
MyTicketsPage - Página de Meus Chamados (para Colaboradores)
Replica MyTicketsPage.jsx do web
"""
import tkinter as tk
from tkinter import ttk
from pages.base_page import BasePage
from api_client import TicketService
from components.loading_screen import LoadingScreen
from components.toast import show_toast
import threading
from datetime import datetime, timedelta

class ScrollableFrame(tk.Frame):
    """Frame com scrollbar moderna"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Canvas para scroll
        self.canvas = tk.Canvas(self, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        
        def update_scrollregion(event=None):
            self.canvas.update_idletasks()
            bbox = self.canvas.bbox("all")
            if bbox:
                self.canvas.configure(scrollregion=bbox)
        
        self.scrollable_frame.bind("<Configure>", update_scrollregion)
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Atualiza largura do frame interno quando canvas muda de tamanho
        def on_canvas_configure(event):
            canvas_width = event.width
            # Verifica se a scrollbar está visível e subtrai sua largura
            try:
                if self.scrollbar.winfo_ismapped():
                    scrollbar_width = self.scrollbar.winfo_width()
                    canvas_width = canvas_width - scrollbar_width
            except:
                pass
            if canvas_width > 0:
                self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        self.canvas.bind("<Configure>", on_canvas_configure)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel apenas quando o mouse está sobre o canvas
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))
        
        # Guarda função de atualização
        self.update_scroll = update_scrollregion
    
    def _on_mousewheel(self, event):
        try:
            # Verifica se o canvas ainda existe antes de tentar fazer scroll
            if self.canvas.winfo_exists():
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            # Widget foi destruído, ignora o evento
            pass

class MyTicketsPage(BasePage):
    """Página de meus chamados - apenas para colaboradores"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page, 
                 current_page, user_info, on_navigate_to_ticket_detail, on_navigate_to_profile):
        super().__init__(parent, on_logout, on_navigate_to_page, current_page, user_info, page_title="MEUS CHAMADOS", create_header_sidebar=False)
        
        self.on_navigate_to_home = on_navigate_to_home
        self.on_navigate_to_ticket_detail = on_navigate_to_ticket_detail
        self.tickets = []
        self.filtered_tickets = []
        self.loading = True
        self.search_term = ""
        self.sort_by = "dataAbertura"
        self.sort_order = "desc"
        
        self._create_ui()
        self._load_tickets()
    
    def _create_ui(self):
        """Cria interface"""
        # Container principal
        container = tk.Frame(self.main_content, bg="#F8F9FA")
        container.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)
        
        # Filtros - card branco
        filters_frame = tk.Frame(container, bg="#FFFFFF", bd=0, relief=tk.FLAT)
        filters_frame.pack(fill=tk.X, pady=(0, 32))
        
        filters_inner = tk.Frame(filters_frame, bg="#FFFFFF")
        filters_inner.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)
        
        # Busca com ícone
        search_container = tk.Frame(filters_inner, bg="#F5F5F5", bd=1, relief=tk.SOLID)
        search_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 24))
        
        search_icon = tk.Label(search_container, text="🔍", font=("Inter", 16), bg="#F5F5F5", fg="#737373")
        search_icon.pack(side=tk.LEFT, padx=16)
        
        self.search_entry = tk.Entry(
            search_container,
            font=("Inter", 16),
            bg="#F5F5F5",
            fg="#262626",
            bd=0,
            relief=tk.FLAT
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 16), pady=16)
        self.search_entry.insert(0, "Buscar por código ou título...")
        self.search_entry.config(fg="#737373")
        
        self.search_entry.bind("<FocusIn>", self._on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self._on_search_focus_out)
        self.search_entry.bind("<KeyRelease>", lambda e: self._on_search_change(
            self.search_entry.get() if self.search_entry.get() != "Buscar por código ou título..." else ""
        ))
        
        # Ordenação
        sort_frame = tk.Frame(filters_inner, bg="#FFFFFF")
        sort_frame.pack(side=tk.RIGHT)
        
        tk.Label(sort_frame, text="🔽 Ordenar por:", font=("Inter", 14, "bold"), 
                bg="#FFFFFF", fg="#262626").pack(side=tk.LEFT, padx=(0, 8))
        
        self.sort_var = tk.StringVar(value="dataAbertura")
        sort_menu = tk.OptionMenu(sort_frame, self.sort_var, "codigo", "titulo", "prioridade", "dataAbertura",
                                  command=lambda v: self._on_sort_change(v, self.sort_order))
        sort_menu.config(font=("Inter", 14), bg="#F5F5F5", fg="#262626", bd=1, relief=tk.SOLID, padx=16, pady=16)
        sort_menu.pack(side=tk.LEFT, padx=(0, 8))
        
        self.order_var = tk.StringVar(value="desc")
        order_menu = tk.OptionMenu(sort_frame, self.order_var, "asc", "desc",
                                   command=lambda v: self._on_sort_change(self.sort_by, v))
        order_menu.config(font=("Inter", 14), bg="#F5F5F5", fg="#262626", bd=1, relief=tk.SOLID, padx=16, pady=16)
        order_menu.pack(side=tk.LEFT)
        
        # Tabela - card branco
        table_frame = tk.Frame(container, bg="#FFFFFF", bd=0, relief=tk.FLAT)
        table_frame.pack(fill=tk.BOTH, expand=True)
        table_frame.config(width=900)
        
        # Container interno
        table_inner = tk.Frame(table_frame, bg="#FFFFFF")
        table_inner.pack(fill=tk.BOTH, expand=True)
        
        # Container para cabeçalho que reserva espaço para scrollbar
        header_container = tk.Frame(table_inner, bg="#FFFFFF")
        header_container.pack(fill=tk.X)
        
        # Cabeçalho da tabela
        header_frame = tk.Frame(header_container, bg="#A93226", height=50)
        header_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        header_frame.pack_propagate(False)
        
        # Inicializa header_labels
        self.header_labels = {}
        
        # Colunas do cabeçalho - frames com larguras fixas
        # CÓDIGO - 120px
        code_header_frame = tk.Frame(header_frame, bg="#A93226", width=120)
        code_header_frame.pack(side=tk.LEFT, fill=tk.Y)
        code_header_frame.pack_propagate(False)
        code_label = tk.Label(
            code_header_frame,
            text="CÓDIGO",
            font=("Inter", 12, "bold"),
            bg="#A93226",
            fg="white",
            anchor="center",
            pady=16
        )
        code_label.pack(fill=tk.BOTH, expand=True)
        code_label.bind("<Button-1>", lambda e: self._handle_sort_click("codigo"))
        code_label.config(cursor="hand2")
        self.header_labels["codigo"] = code_label
        
        # TÍTULO - expande
        title_header_frame = tk.Frame(header_frame, bg="#A93226")
        title_header_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        title_label = tk.Label(
            title_header_frame,
            text="TÍTULO",
            font=("Inter", 12, "bold"),
            bg="#A93226",
            fg="white",
            anchor="w",
            padx=16,
            pady=16
        )
        title_label.pack(fill=tk.BOTH, expand=True)
        title_label.bind("<Button-1>", lambda e: self._handle_sort_click("titulo"))
        title_label.config(cursor="hand2")
        self.header_labels["titulo"] = title_label
        
        # PRIORIDADE - 150px fixo
        priority_header_frame = tk.Frame(header_frame, bg="#A93226", width=150)
        priority_header_frame.pack(side=tk.LEFT, fill=tk.Y)
        priority_header_frame.pack_propagate(False)
        priority_label = tk.Label(
            priority_header_frame,
            text="PRIORIDADE",
            font=("Inter", 12, "bold"),
            bg="#A93226",
            fg="white",
            anchor="w",
            pady=16,
            padx=8
        )
        priority_label.pack(fill=tk.Y, expand=True, anchor="w", padx=8)
        priority_label.bind("<Button-1>", lambda e: self._handle_sort_click("prioridade"))
        priority_label.config(cursor="hand2")
        self.header_labels["prioridade"] = priority_label
        
        # DATA LIMITE - 150px fixo
        date_header_frame = tk.Frame(header_frame, bg="#A93226", width=150)
        date_header_frame.pack(side=tk.LEFT, fill=tk.Y)
        date_header_frame.pack_propagate(False)
        date_label = tk.Label(
            date_header_frame,
            text="DATA LIMITE",
            font=("Inter", 12, "bold"),
            bg="#A93226",
            fg="white",
            anchor="w",
            pady=16,
            padx=8
        )
        date_label.pack(fill=tk.Y, expand=True, anchor="w", padx=8)
        date_label.bind("<Button-1>", lambda e: self._handle_sort_click("dataAbertura"))
        date_label.config(cursor="hand2")
        self.header_labels["dataAbertura"] = date_label
        
        # STATUS - 150px fixo
        status_header_frame = tk.Frame(header_frame, bg="#A93226", width=150)
        status_header_frame.pack(side=tk.LEFT, fill=tk.Y)
        status_header_frame.pack_propagate(False)
        status_label = tk.Label(
            status_header_frame,
            text="STATUS",
            font=("Inter", 12, "bold"),
            bg="#A93226",
            fg="white",
            anchor="w",
            pady=16,
            padx=8
        )
        status_label.pack(fill=tk.Y, expand=True, anchor="w", padx=8)
        self.header_labels[None] = None
        
        # TÉCNICO RESPONSÁVEL - 200px fixo
        tecnico_header_frame = tk.Frame(header_frame, bg="#A93226", width=200)
        tecnico_header_frame.pack(side=tk.LEFT, fill=tk.Y)
        tecnico_header_frame.pack_propagate(False)
        tecnico_label = tk.Label(
            tecnico_header_frame,
            text="TÉCNICO RESPONSÁVEL",
            font=("Inter", 12, "bold"),
            bg="#A93226",
            fg="white",
            anchor="w",
            pady=16,
            padx=8
        )
        tecnico_label.pack(fill=tk.Y, expand=True, anchor="w", padx=8)
        self.header_labels[None] = None
        
        # Guarda referências dos frames do cabeçalho
        self.header_frames = {
            'codigo': code_header_frame,
            'titulo': title_header_frame,
            'prioridade': priority_header_frame,
            'data': date_header_frame,
            'status': status_header_frame,
            'tecnico': tecnico_header_frame
        }
        self.header_frame_ref = header_frame
        
        # Frame scrollável para o corpo da tabela
        scrollable_container = tk.Frame(table_inner, bg="#FFFFFF")
        scrollable_container.pack(fill=tk.BOTH, expand=True)
        
        self.scrollable_frame = ScrollableFrame(scrollable_container)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)
        
        self.table_body = self.scrollable_frame.scrollable_frame
        self.header_container = header_container
        self.scrollable_container = scrollable_container
        self.table_frame = table_frame
        self.table_inner = table_inner
        
        # Força atualização inicial da tabela para mostrar estado de carregamento
        def init_table():
            if hasattr(self, 'table_body') and self.table_body:
                self._update_table()
        self.after(200, init_table)
        
        # Função para sincronizar larguras
        def sync_table_width(event=None):
            try:
                container_width = table_inner.winfo_width()
                if container_width > 1:
                    scrollbar_width = 0
                    try:
                        if self.scrollable_frame.scrollbar.winfo_ismapped():
                            scrollbar_width = self.scrollable_frame.scrollbar.winfo_width()
                    except:
                        pass
                    
                    content_width = container_width - scrollbar_width
                    if content_width > 0:
                        header_frame.config(width=content_width)
                        self.scrollable_frame.canvas.itemconfig(
                            self.scrollable_frame.canvas_window,
                            width=content_width
                        )
                        self.scrollable_frame.update_scroll()
            except:
                pass
        
        table_inner.bind("<Configure>", sync_table_width)
        header_container.bind("<Configure>", sync_table_width)
        scrollable_container.bind("<Configure>", sync_table_width)
        
        def on_scrollbar_change(event=None):
            self.after(10, sync_table_width)
        
        try:
            self.scrollable_frame.scrollbar.bind("<Map>", on_scrollbar_change)
            self.scrollable_frame.scrollbar.bind("<Unmap>", on_scrollbar_change)
        except:
            pass
        
        self.after(100, sync_table_width)
        
        root = self.winfo_toplevel()
        root.bind("<Configure>", lambda e: sync_table_width() if e.widget == root else None)
    
    def _on_search_focus_in(self, event):
        """Quando foca no campo de busca"""
        if self.search_entry.get() == "Buscar por código ou título...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="#262626")
    
    def _on_search_focus_out(self, event):
        """Quando perde foco no campo de busca"""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Buscar por código ou título...")
            self.search_entry.config(fg="#737373")
    
    def _on_search_change(self, term):
        """Quando o texto de busca muda"""
        self.search_term = term.lower()
        self._apply_filters_and_sort()
    
    def _on_sort_change(self, sort_by, sort_order):
        """Atualiza ordenação"""
        self.sort_by = sort_by
        self.sort_order = sort_order
        self._apply_filters_and_sort()
    
    def _handle_sort_click(self, column):
        """Handle clique na coluna"""
        if self.sort_by == column:
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
        else:
            self.sort_by = column
            self.sort_order = "asc"
        self._apply_filters_and_sort()
    
    def _load_tickets(self):
        """Carrega tickets do usuário"""
        self.loading = True
        threading.Thread(target=self._do_load_tickets, daemon=True).start()
    
    def _do_load_tickets(self):
        """Faz carregamento dos tickets"""
        try:
            user_id = self.user_info.get('id')
            if not user_id:
                self.after(0, lambda: setattr(self, 'loading', False))
                return
            
            filters = {'solicitanteId': int(user_id)}
            tickets = TicketService.get_tickets(filters)
            
            if tickets:
                mapped = []
                for t in tickets:
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
        
        # Filtro de busca
        if self.search_term:
            filtered = [t for t in filtered if 
                       self.search_term in t['titulo'].lower() or 
                       self.search_term in t['codigo'].lower()]
        
        # Ordenação
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
                    return t['dataAbertura'] or ''
                except:
                    return ''
            return ''
        
        filtered.sort(key=sort_key, reverse=(self.sort_order == 'desc'))
        self.filtered_tickets = filtered
        self._update_table()
    
    def _update_table(self):
        """Atualiza tabela com layout moderno"""
        # Verifica se o widget ainda existe
        try:
            if not hasattr(self, 'table_body'):
                return
            if not self.table_body:
                return
            if not hasattr(self.table_body, 'winfo_exists') or not self.table_body.winfo_exists():
                return
        except (tk.TclError, AttributeError):
            return
        
        # Limpa tabela
        try:
            for widget in self.table_body.winfo_children():
                widget.destroy()
        except tk.TclError:
            return
        
        # Atualiza indicadores de ordenação no cabeçalho
        for key, label in self.header_labels.items():
            if label and key:
                try:
                    if not label.winfo_exists():
                        continue
                    if self.sort_by == key:
                        arrow = "▲" if self.sort_order == "asc" else "▼"
                        text = label.cget("text").split()[0]
                        label.config(text=f"{text} {arrow}")
                    else:
                        text = label.cget("text").split()[0]
                        label.config(text=text)
                except tk.TclError:
                    continue
        
        if self.loading:
            loading_label = tk.Label(
                self.table_body,
                text="Carregando...",
                font=("Inter", 14),
                bg="#FFFFFF",
                fg="#737373",
                pady=48
            )
            loading_label.pack(pady=48)
            self.after(10, lambda: self.scrollable_frame.update_scroll())
            return
        
        if not self.filtered_tickets:
            no_data_label = tk.Label(
                self.table_body,
                text="Nenhum chamado encontrado",
                font=("Inter", 14),
                bg="#FFFFFF",
                fg="#737373",
                pady=48
            )
            no_data_label.pack(pady=48)
            self.after(10, lambda: self.scrollable_frame.update_scroll())
            return
        
        # Cria linhas da tabela - usa EXATAMENTE as mesmas larguras do cabeçalho
        for i, ticket in enumerate(self.filtered_tickets):
            row_bg = "#FFFFFF" if i % 2 == 0 else "#FAFAFA"
            row_frame = tk.Frame(self.table_body, bg=row_bg, cursor="hand2", height=60)
            row_frame.pack(fill=tk.X, pady=0)
            row_frame.pack_propagate(False)
            row_frame.bind("<Button-1>", lambda e, tid=ticket['id']: self._on_ticket_click(tid))
            
            # Obtém larguras reais dos frames do cabeçalho
            try:
                code_width = self.header_frames['codigo'].winfo_width()
                priority_width = self.header_frames['prioridade'].winfo_width()
                date_width = self.header_frames['data'].winfo_width()
                status_width = self.header_frames['status'].winfo_width()
                tecnico_width = self.header_frames['tecnico'].winfo_width()
            except:
                code_width = 120
                priority_width = 150
                date_width = 150
                status_width = 150
                tecnico_width = 200
            
            # Código
            code_cell = tk.Frame(row_frame, bg=row_bg, width=code_width)
            code_cell.pack(side=tk.LEFT, fill=tk.Y)
            code_cell.pack_propagate(False)
            code_label = tk.Label(
                code_cell,
                text=ticket['codigo'],
                font=("Inter", 14, "bold"),
                bg=row_bg,
                fg="#A93226",
                anchor="center"
            )
            code_label.pack(fill=tk.BOTH, expand=True)
            code_label.bind("<Button-1>", lambda e, tid=ticket['id']: self._on_ticket_click(tid))
            
            # Título - expande
            title_cell = tk.Frame(row_frame, bg=row_bg)
            title_cell.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            title_label = tk.Label(
                title_cell,
                text=ticket['titulo'],
                font=("Inter", 14),
                bg=row_bg,
                fg="#262626",
                anchor="w",
                padx=16
            )
            title_label.pack(fill=tk.BOTH, expand=True)
            title_label.bind("<Button-1>", lambda e, tid=ticket['id']: self._on_ticket_click(tid))
            
            # Prioridade (badge colorido)
            priority_cell = tk.Frame(row_frame, bg=row_bg, width=priority_width)
            priority_cell.pack(side=tk.LEFT, fill=tk.Y)
            priority_cell.pack_propagate(False)
            priority_color = self._get_priority_color(ticket['prioridade'])
            priority_badge = tk.Label(
                priority_cell,
                text=ticket['prioridade'],
                font=("Inter", 10, "bold"),
                bg=priority_color,
                fg="white",
                padx=12,
                pady=4,
                relief=tk.FLAT,
                anchor="center"
            )
            priority_badge.pack(expand=True)
            priority_badge.bind("<Button-1>", lambda e, tid=ticket['id']: self._on_ticket_click(tid))
            
            # Data Limite
            date_cell = tk.Frame(row_frame, bg=row_bg, width=date_width)
            date_cell.pack(side=tk.LEFT, fill=tk.Y)
            date_cell.pack_propagate(False)
            date_text = self._format_date(ticket.get('dataLimite') or ticket.get('dataAbertura')) if (ticket.get('dataLimite') or ticket.get('dataAbertura')) else 'N/A'
            date_label = tk.Label(
                date_cell,
                text=date_text,
                font=("Inter", 14),
                bg=row_bg,
                fg="#737373",
                anchor="center"
            )
            date_label.pack(fill=tk.BOTH, expand=True)
            date_label.bind("<Button-1>", lambda e, tid=ticket['id']: self._on_ticket_click(tid))
            
            # Status (badge colorido)
            status_cell = tk.Frame(row_frame, bg=row_bg, width=status_width)
            status_cell.pack(side=tk.LEFT, fill=tk.Y)
            status_cell.pack_propagate(False)
            status_color = self._get_status_color(ticket['status'])
            status_badge = tk.Label(
                status_cell,
                text=ticket['statusText'],
                font=("Inter", 10, "bold"),
                bg=status_color,
                fg="white",
                padx=12,
                pady=4,
                relief=tk.FLAT,
                anchor="center"
            )
            status_badge.pack(expand=True)
            status_badge.bind("<Button-1>", lambda e, tid=ticket['id']: self._on_ticket_click(tid))
            
            # Técnico Responsável
            tecnico_cell = tk.Frame(row_frame, bg=row_bg, width=tecnico_width)
            tecnico_cell.pack(side=tk.LEFT, fill=tk.Y)
            tecnico_cell.pack_propagate(False)
            tecnico_label = tk.Label(
                tecnico_cell,
                text=ticket['tecnico'],
                font=("Inter", 14),
                bg=row_bg,
                fg="#737373",
                anchor="w",
                padx=8
            )
            tecnico_label.pack(fill=tk.BOTH, expand=True)
            tecnico_label.bind("<Button-1>", lambda e, tid=ticket['id']: self._on_ticket_click(tid))
        
        # Atualiza scrollregion após adicionar todos os widgets
        def update_after_render():
            self.scrollable_frame.update_scroll()
            self.after(50, self._update_row_widths)
        
        self.after(10, update_after_render)
    
    def _update_row_widths(self):
        """Atualiza larguras das células das linhas para corresponder ao cabeçalho"""
        try:
            code_width = self.header_frames['codigo'].winfo_width()
            priority_width = self.header_frames['prioridade'].winfo_width()
            date_width = self.header_frames['data'].winfo_width()
            status_width = self.header_frames['status'].winfo_width()
            tecnico_width = self.header_frames['tecnico'].winfo_width()
            
            for row_frame in self.table_body.winfo_children():
                if isinstance(row_frame, tk.Frame):
                    cells = row_frame.winfo_children()
                    if len(cells) >= 6:
                        if cells[0].winfo_width() != code_width:
                            cells[0].config(width=code_width)
                        if cells[2].winfo_width() != priority_width:
                            cells[2].config(width=priority_width)
                        if cells[3].winfo_width() != date_width:
                            cells[3].config(width=date_width)
                        if cells[4].winfo_width() != status_width:
                            cells[4].config(width=status_width)
                        if cells[5].winfo_width() != tecnico_width:
                            cells[5].config(width=tecnico_width)
        except:
            pass
    
    def _on_ticket_click(self, ticket_id):
        """Lida com clique em ticket"""
        if self.on_navigate_to_ticket_detail:
            # A função já tem previous_page='my-tickets' hardcoded, então passa apenas ticket_id
            self.on_navigate_to_ticket_detail(ticket_id)
    
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
    
    def _get_priority_color(self, priority):
        """Retorna cor da prioridade"""
        return {'ALTA': '#dc3545', 'MÉDIA': '#ffc107', 'BAIXA': '#28a745'}.get(priority, '#6c757d')
    
    def _get_status_color(self, status):
        """Retorna cor do status"""
        return {1: '#007bff', 2: '#ffc107', 3: '#6c757d'}.get(status, '#6c757d')
    
    def _format_date(self, date_string):
        """Formata data"""
        try:
            date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return date.strftime('%d/%m/%Y')
        except:
            return date_string if date_string else 'N/A'
