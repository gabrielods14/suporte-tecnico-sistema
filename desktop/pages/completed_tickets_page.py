"""
CompletedTicketsPage - Layout moderno igual à versão web
"""
import tkinter as tk
from tkinter import ttk
from pages.base_page import BasePage
from api_client import TicketService
import threading
from datetime import datetime
from PIL import Image, ImageDraw, ImageTk

def create_rounded_badge(parent, text, bg_color, fg_color="white", font=("Inter", 10, "bold"), padx=12, pady=4, radius=12):
    """Cria um badge com bordas arredondadas usando PIL"""
    # Calcula tamanho do texto
    temp_label = tk.Label(parent, text=text, font=font)
    temp_label.update()
    text_width = temp_label.winfo_reqwidth()
    text_height = temp_label.winfo_reqheight()
    temp_label.destroy()
    
    # Dimensões do badge
    width = text_width + (padx * 2)
    height = text_height + (pady * 2)
    
    # Cria imagem com bordas arredondadas
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Converte cor hex para RGB
    if bg_color.startswith('#'):
        bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
    else:
        bg_rgb = (220, 53, 69)  # Vermelho padrão
    
    # Desenha retângulo arredondado (compatível com versões antigas do PIL)
    try:
        # PIL 9.0.0+ tem rounded_rectangle
        draw.rounded_rectangle([(0, 0), (width-1, height-1)], radius=radius, fill=bg_rgb)
    except AttributeError:
        # Fallback para versões antigas: desenha retângulo normal
        draw.rectangle([(0, 0), (width-1, height-1)], fill=bg_rgb)
    
    # Converte para PhotoImage
    photo = ImageTk.PhotoImage(img)
    
    # Cria label com a imagem
    badge = tk.Label(parent, image=photo, text=text, compound=tk.CENTER,
                    font=font, fg=fg_color, bg=parent.cget('bg'))
    badge.image = photo  # Mantém referência
    
    return badge

class ScrollableFrame(tk.Frame):
    """Frame com scrollbar moderna"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
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

class CompletedTicketsPage(BasePage):
    """Página de chamados concluídos - layout moderno igual à versão web"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page,
                 current_page, user_info, on_navigate_to_ticket_detail):
        super().__init__(parent, on_logout, on_navigate_to_page, current_page, user_info, page_title="CHAMADOS CONCLUÍDOS", create_header_sidebar=False)
        
        self.on_navigate_to_home = on_navigate_to_home
        self.on_navigate_to_ticket_detail = on_navigate_to_ticket_detail
        
        self.tickets = []
        self.filtered_tickets = []
        self.loading = True
        self.search_term = ""
        self.sort_by = "dataFechamento"
        self.sort_order = "desc"
        
        self._create_ui()
        self._load_tickets()
    
    def _create_ui(self):
        """Cria interface moderna igual à versão web"""
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
        
        def on_focus_in(e):
            if self.search_entry.get() == "Buscar por código ou título...":
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg="#262626")
        
        def on_focus_out(e):
            if not self.search_entry.get():
                self.search_entry.insert(0, "Buscar por código ou título...")
                self.search_entry.config(fg="#737373")
        
        self.search_entry.bind("<FocusIn>", on_focus_in)
        self.search_entry.bind("<FocusOut>", on_focus_out)
        self.search_entry.bind("<KeyRelease>", lambda e: self._on_search_change(
            self.search_entry.get() if self.search_entry.get() != "Buscar por código ou título..." else ""
        ))
        
        # Ordenação
        sort_frame = tk.Frame(filters_inner, bg="#FFFFFF")
        sort_frame.pack(side=tk.RIGHT)
        
        tk.Label(sort_frame, text="🔽 Ordenar por:", font=("Inter", 14, "bold"), 
                bg="#FFFFFF", fg="#262626").pack(side=tk.LEFT, padx=(0, 8))
        
        self.sort_var = tk.StringVar(value="dataFechamento")
        sort_menu = tk.OptionMenu(sort_frame, self.sort_var, "codigo", "titulo", "prioridade", "dataFechamento",
                                  command=lambda v: self._on_sort_change(v, self.sort_order))
        sort_menu.config(font=("Inter", 14), bg="#F5F5F5", fg="#262626", bd=1, relief=tk.SOLID, padx=16, pady=16)
        sort_menu.pack(side=tk.LEFT, padx=(0, 8))
        
        self.order_var = tk.StringVar(value="desc")
        order_menu = tk.OptionMenu(sort_frame, self.order_var, "asc", "desc",
                                   command=lambda v: self._on_sort_change(self.sort_by, v))
        order_menu.config(font=("Inter", 14), bg="#F5F5F5", fg="#262626", bd=1, relief=tk.SOLID, padx=16, pady=16)
        order_menu.pack(side=tk.LEFT)
        
        # Tabela - card branco com largura mínima
        table_frame = tk.Frame(container, bg="#FFFFFF", bd=0, relief=tk.FLAT)
        table_frame.pack(fill=tk.BOTH, expand=True)
        table_frame.config(width=1000)  # Largura mínima para evitar quebra
        
        # Container interno para garantir largura mínima
        table_inner = tk.Frame(table_frame, bg="#FFFFFF")
        table_inner.pack(fill=tk.BOTH, expand=True)
        
        # Container para cabeçalho que reserva espaço para scrollbar
        header_container = tk.Frame(table_inner, bg="#FFFFFF")
        header_container.pack(fill=tk.X)
        
        # Cabeçalho da tabela - usa frames com larguras fixas em pixels
        header_frame = tk.Frame(header_container, bg="#A93226", height=50)
        header_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        header_frame.pack_propagate(False)
        
        # CÓDIGO
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
        self.header_labels = {"codigo": code_label}
        
        # TÍTULO
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
        
        # PRIORIDADE (ajustado para esquerda)
        priority_header_frame = tk.Frame(header_frame, bg="#A93226", width=150)
        priority_header_frame.pack(side=tk.LEFT, fill=tk.Y)
        priority_header_frame.pack_propagate(False)
        priority_label = tk.Label(
            priority_header_frame,
            text="PRIORIDADE",
            font=("Inter", 12, "bold"),
            bg="#A93226",
            fg="white",
            anchor="w",  # Alinha à esquerda
            pady=16,
            padx=8
        )
        priority_label.pack(fill=tk.Y, expand=True, anchor="w", padx=8)
        priority_label.bind("<Button-1>", lambda e: self._handle_sort_click("prioridade"))
        priority_label.config(cursor="hand2")
        self.header_labels["prioridade"] = priority_label
        
        # STATUS (ajustado para esquerda)
        status_header_frame = tk.Frame(header_frame, bg="#A93226", width=120)
        status_header_frame.pack(side=tk.LEFT, fill=tk.Y)
        status_header_frame.pack_propagate(False)
        status_label = tk.Label(
            status_header_frame,
            text="STATUS",
            font=("Inter", 12, "bold"),
            bg="#A93226",
            fg="white",
            anchor="w",  # Alinha à esquerda
            pady=16,
            padx=8
        )
        status_label.pack(fill=tk.Y, expand=True, anchor="w", padx=8)
        self.header_labels[None] = None
        
        # SOLICITANTE (igual à versão web)
        solicitante_header_frame = tk.Frame(header_frame, bg="#A93226", width=150)
        solicitante_header_frame.pack(side=tk.LEFT, fill=tk.Y)
        solicitante_header_frame.pack_propagate(False)
        solicitante_label = tk.Label(
            solicitante_header_frame,
            text="SOLICITANTE",
            font=("Inter", 12, "bold"),
            bg="#A93226",
            fg="white",
            anchor="w",
            pady=16,
            padx=8
        )
        solicitante_label.pack(fill=tk.Y, expand=True, anchor="w", padx=8)
        self.header_labels[None] = None
        
        # TÉCNICO (ajustado para esquerda)
        tecnico_header_frame = tk.Frame(header_frame, bg="#A93226", width=150)
        tecnico_header_frame.pack(side=tk.LEFT, fill=tk.Y)
        tecnico_header_frame.pack_propagate(False)
        tecnico_label = tk.Label(
            tecnico_header_frame,
            text="TÉCNICO",
            font=("Inter", 12, "bold"),
            bg="#A93226",
            fg="white",
            anchor="w",  # Alinha à esquerda
            pady=16,
            padx=8
        )
        tecnico_label.pack(fill=tk.Y, expand=True, anchor="w", padx=8)
        
        # DATA FECHAMENTO (ajustado para esquerda)
        date_header_frame = tk.Frame(header_frame, bg="#A93226", width=180)
        date_header_frame.pack(side=tk.LEFT, fill=tk.Y)
        date_header_frame.pack_propagate(False)
        date_label = tk.Label(
            date_header_frame,
            text="DATA FECHAMENTO",
            font=("Inter", 12, "bold"),
            bg="#A93226",
            fg="white",
            anchor="w",  # Alinha à esquerda
            pady=16,
            padx=8
        )
        date_label.pack(fill=tk.Y, expand=True, anchor="w", padx=8)
        date_label.bind("<Button-1>", lambda e: self._handle_sort_click("dataFechamento"))
        date_label.config(cursor="hand2")
        self.header_labels["dataFechamento"] = date_label
        
        # Guarda referências dos frames do cabeçalho para usar nas linhas
        self.header_frames = {
            'codigo': code_header_frame,
            'titulo': title_header_frame,
            'prioridade': priority_header_frame,
            'status': status_header_frame,
            'solicitante': solicitante_header_frame,
            'tecnico': tecnico_header_frame,
            'data': date_header_frame
        }
        self.header_frame_ref = header_frame  # Guarda referência do cabeçalho completo
        
        # Frame scrollável para o corpo da tabela (ao lado do cabeçalho)
        scrollable_container = tk.Frame(table_inner, bg="#FFFFFF")
        scrollable_container.pack(fill=tk.BOTH, expand=True)
        
        self.scrollable_frame = ScrollableFrame(scrollable_container)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)
        
        self.table_body = self.scrollable_frame.scrollable_frame
        self.header_container = header_container  # Guarda referência
        self.scrollable_container = scrollable_container  # Guarda referência
        
        # Garante que o cabeçalho e o corpo tenham a mesma largura (considerando scrollbar)
        def sync_table_width(event=None):
            try:
                # Largura disponível do container interno
                container_width = table_inner.winfo_width()
                if container_width > 1:
                    # Verifica se a scrollbar está visível
                    scrollbar_width = 0
                    try:
                        if self.scrollable_frame.scrollbar.winfo_ismapped():
                            scrollbar_width = self.scrollable_frame.scrollbar.winfo_width()
                    except:
                        pass
                    
                    # Largura do conteúdo (sem scrollbar)
                    content_width = container_width - scrollbar_width
                    if content_width > 0:
                        # Atualiza largura do cabeçalho
                        header_frame.config(width=content_width)
                        
                        # Atualiza largura do canvas window
                        self.scrollable_frame.canvas.itemconfig(
                            self.scrollable_frame.canvas_window,
                            width=content_width
                        )
                        # Força atualização do scrollregion
                        self.scrollable_frame.update_scroll()
            except:
                pass
        
        # Sincroniza quando o container ou a janela mudarem de tamanho
        table_inner.bind("<Configure>", sync_table_width)
        header_container.bind("<Configure>", sync_table_width)
        scrollable_container.bind("<Configure>", sync_table_width)
        
        # Atualiza quando a scrollbar aparecer ou desaparecer
        def on_scrollbar_change(event=None):
            self.after(10, sync_table_width)
        
        try:
            self.scrollable_frame.scrollbar.bind("<Map>", on_scrollbar_change)
            self.scrollable_frame.scrollbar.bind("<Unmap>", on_scrollbar_change)
        except:
            pass
        
        self.after(100, sync_table_width)
        
        # Atualiza quando a janela principal for redimensionada
        def on_window_resize(event=None):
            sync_table_width()
        
        # Bind no root para detectar redimensionamento da janela
        root = self.winfo_toplevel()
        root.bind("<Configure>", lambda e: sync_table_width() if e.widget == root else None)
    
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
        # StatusChamado enum: 1=Aberto, 2=EmAtendimento, 3=Fechado
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
        # StatusChamado enum: 1=Aberto, 2=EmAtendimento, 3=Fechado
        status_num = int(status) if isinstance(status, (int, str)) and str(status).isdigit() else 0
        if status_num == 1:
            return 'ABERTO'
        elif status_num == 2:
            return 'EM ATENDIMENTO'
        elif status_num == 3:
            return 'CONCLUÍDO'
        return 'N/A'
    
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
                    if item.get('status') == 3:  # Status 3 = Fechado (concluído) - como na versão web
                        prioridade = item.get('prioridade', 2)
                        if isinstance(prioridade, int):
                            prioridade_text = 'ALTA' if prioridade == 3 else 'MÉDIA' if prioridade == 2 else 'BAIXA'
                        else:
                            prioridade_text = 'MÉDIA'
                        
                        status_text = 'CONCLUÍDO'  # Status 3 = Fechado/Concluído
                        tecnico = item.get('tecnicoResponsavel', {}).get('nome', 'N/A') if isinstance(item.get('tecnicoResponsavel'), dict) else 'N/A'
                        solicitante = item.get('solicitante', {}).get('nome', 'N/A') if isinstance(item.get('solicitante'), dict) else 'N/A'
                        
                        mapped.append({
                            'id': item.get('id'),
                            'codigo': str(item.get('id', 0)).zfill(6),
                            'titulo': item.get('titulo', ''),
                            'prioridade': prioridade_text,
                            'status': item.get('status'),  # Mantém status numérico
                            'statusText': status_text,  # Texto do status
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
    
    def _on_search_change(self, term):
        """Atualiza busca"""
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
    
    def _apply_filters_and_sort(self):
        """Aplica filtros e ordenação"""
        filtered = [t for t in self.tickets]
        
        if self.search_term:
            filtered = [t for t in filtered if 
                       self.search_term in t['titulo'].lower() or 
                       self.search_term in t['codigo'].lower()]
        
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
        """Atualiza tabela com layout moderno"""
        # Verifica se o widget ainda existe
        try:
            if not self.table_body.winfo_exists():
                return
        except tk.TclError:
            return
        
        # Limpa tabela
        try:
            for widget in self.table_body.winfo_children():
                widget.destroy()
        except tk.TclError:
            # Widget foi destruído durante a iteração
            return
        
        # Atualiza indicadores de ordenação no cabeçalho
        for key, label in self.header_labels.items():
            if label and key:
                try:
                    if not label.winfo_exists():
                        continue
                    if self.sort_by == key:
                        arrow = "▲" if self.sort_order == "asc" else "▼"
                        text = label.cget("text").split()[0]  # Remove arrow se existir
                        label.config(text=f"{text} {arrow}")
                    else:
                        text = label.cget("text").split()[0]
                        label.config(text=text)
                except tk.TclError:
                    # Widget foi destruído
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
            return
        
        if not self.filtered_tickets:
            no_data_label = tk.Label(
                self.table_body,
                text="Nenhum chamado concluído encontrado",
                font=("Inter", 14),
                bg="#FFFFFF",
                fg="#737373",
                pady=48
            )
            no_data_label.pack(pady=48)
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
                status_width = self.header_frames['status'].winfo_width()
                solicitante_width = self.header_frames['solicitante'].winfo_width()
                tecnico_width = self.header_frames['tecnico'].winfo_width()
                date_width = self.header_frames['data'].winfo_width()
            except:
                # Fallback para larguras fixas se não conseguir obter
                code_width = 120
                priority_width = 150
                status_width = 120
                solicitante_width = 150
                tecnico_width = 150
                date_width = 180
            
            # Código - usa largura EXATA do cabeçalho
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
            
            # Título - frame que expande (igual ao cabeçalho)
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
            
            # Prioridade (badge colorido) - usa largura EXATA do cabeçalho
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
            
            # Status (badge colorido) - usa largura EXATA do cabeçalho
            status_cell = tk.Frame(row_frame, bg=row_bg, width=status_width)
            status_cell.pack(side=tk.LEFT, fill=tk.Y)
            status_cell.pack_propagate(False)
            status_val = ticket.get('status', ticket.get('status_num', 3))
            status_color = self._get_status_color(status_val)
            status_text = self._get_status_text(status_val)
            status_badge = tk.Label(
                status_cell,
                text=status_text,
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
            
            # Solicitante - usa largura EXATA do cabeçalho
            solicitante_cell = tk.Frame(row_frame, bg=row_bg, width=solicitante_width)
            solicitante_cell.pack(side=tk.LEFT, fill=tk.Y)
            solicitante_cell.pack_propagate(False)
            solicitante_label = tk.Label(
                solicitante_cell,
                text=ticket.get('solicitante', 'N/A'),
                font=("Inter", 14),
                bg=row_bg,
                fg="#737373",
                anchor="center"
            )
            solicitante_label.pack(fill=tk.BOTH, expand=True)
            solicitante_label.bind("<Button-1>", lambda e, tid=ticket['id']: self._on_ticket_click(tid))
            
            # Técnico - usa largura EXATA do cabeçalho
            tecnico_cell = tk.Frame(row_frame, bg=row_bg, width=tecnico_width)
            tecnico_cell.pack(side=tk.LEFT, fill=tk.Y)
            tecnico_cell.pack_propagate(False)
            tecnico_label = tk.Label(
                tecnico_cell,
                text=ticket['tecnico'],
                font=("Inter", 14, "italic"),
                bg=row_bg,
                fg="#737373",
                anchor="center"
            )
            tecnico_label.pack(fill=tk.BOTH, expand=True)
            tecnico_label.bind("<Button-1>", lambda e, tid=ticket['id']: self._on_ticket_click(tid))
            
            # Data Fechamento - usa largura EXATA do cabeçalho
            date_cell = tk.Frame(row_frame, bg=row_bg, width=date_width)
            date_cell.pack(side=tk.LEFT, fill=tk.Y)
            date_cell.pack_propagate(False)
            try:
                data = datetime.fromisoformat(ticket['dataFechamento'].replace('Z', '+00:00')).strftime('%d/%m/%Y')
            except:
                data = "N/A"
            date_label = tk.Label(
                date_cell,
                text=data,
                font=("Inter", 14),
                bg=row_bg,
                fg="#737373",
                anchor="center"
            )
            date_label.pack(fill=tk.BOTH, expand=True)
            date_label.bind("<Button-1>", lambda e, tid=ticket['id']: self._on_ticket_click(tid))
        
        # Atualiza scrollregion após adicionar todos os widgets
        # Também força atualização das larguras após renderização
        def update_after_render():
            self.scrollable_frame.update_scroll()
            # Força atualização das larguras das células após renderização completa
            self.after(50, self._update_row_widths)
        
        self.after(10, update_after_render)
    
    def _update_row_widths(self):
        """Atualiza larguras das células das linhas para corresponder ao cabeçalho"""
        try:
            # Obtém larguras reais dos frames do cabeçalho
            code_width = self.header_frames['codigo'].winfo_width()
            priority_width = self.header_frames['prioridade'].winfo_width()
            status_width = self.header_frames['status'].winfo_width()
            solicitante_width = self.header_frames['solicitante'].winfo_width()
            tecnico_width = self.header_frames['tecnico'].winfo_width()
            date_width = self.header_frames['data'].winfo_width()
            
            # Atualiza todas as células das linhas
            for row_frame in self.table_body.winfo_children():
                if isinstance(row_frame, tk.Frame):
                    cells = row_frame.winfo_children()
                    if len(cells) >= 7:  # Atualizado para 7 células (incluindo solicitante)
                        # Código
                        if cells[0].winfo_width() != code_width:
                            cells[0].config(width=code_width)
                        # Prioridade
                        if cells[2].winfo_width() != priority_width:
                            cells[2].config(width=priority_width)
                        # Status
                        if cells[3].winfo_width() != status_width:
                            cells[3].config(width=status_width)
                        # Solicitante
                        if cells[4].winfo_width() != solicitante_width:
                            cells[4].config(width=solicitante_width)
                        # Técnico
                        if cells[5].winfo_width() != tecnico_width:
                            cells[5].config(width=tecnico_width)
                        # Data
                        if cells[6].winfo_width() != date_width:
                            cells[6].config(width=date_width)
        except:
            pass
    
    def _on_ticket_click(self, ticket_id):
        """Handle clique no ticket"""
        if self.on_navigate_to_ticket_detail:
            self.on_navigate_to_ticket_detail(ticket_id)
