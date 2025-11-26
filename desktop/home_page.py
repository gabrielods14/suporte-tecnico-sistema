"""
Página Home/Dashboard Principal
Baseada no HomePage.jsx do projeto web
Gerencia navegação entre diferentes páginas
"""
import customtkinter as ctk
from config import COLORS
from components.sidebar import Sidebar
from components.header import Header
from pages.new_ticket_page import NewTicketPage
from pages.pending_tickets_page import PendingTicketsPage
from pages.completed_tickets_page import CompletedTicketsPage
from pages.my_tickets_page import MyTicketsPage
from pages.ticket_detail_page import TicketDetailPage
from pages.register_employee_page import RegisterEmployeePage
from pages.reports_page import ReportsPage
from pages.users_report_page import UsersReportPage
from pages.user_activity_page import UserActivityPage
from pages.contact_page import ContactPage
from pages.faq_page import FAQPage
from pages.user_profile_page import UserProfilePage


class HomePage(ctk.CTkFrame):
    """Página principal que gerencia o dashboard e navegação"""
    
    def __init__(self, parent, user_info=None, on_logout=None, on_navigate=None, 
                 current_page='home', on_navigate_to_register=None, 
                 on_navigate_to_new_ticket=None, on_navigate_to_page=None,
                 on_navigate_to_profile=None):
        print("[HomePage.__init__] Iniciando...")
        print(f"[HomePage.__init__] parent: {parent}")
        print(f"[HomePage.__init__] user_info: {user_info}")
        
        super().__init__(parent)
        print("[HomePage.__init__] super() chamado")
        
        self.user_info = user_info or {}
        self.on_logout = on_logout
        self.current_page = current_page
        
        # Armazena os callbacks separados para uso direto
        self.on_navigate_to_register = on_navigate_to_register
        self.on_navigate_to_new_ticket = on_navigate_to_new_ticket
        self.on_navigate_to_page = on_navigate_to_page
        self.on_navigate_to_profile = on_navigate_to_profile
        
        # Suporta tanto o formato antigo (on_navigate) quanto o novo (callbacks separados)
        if on_navigate:
            self.on_navigate = on_navigate
        else:
            # Cria um wrapper que converte os callbacks separados
            def navigate_wrapper(page_id, **kwargs):
                if page_id == 'logout':
                    if on_logout:
                        on_logout()
                elif page_id == 'register':
                    if on_navigate_to_register:
                        on_navigate_to_register()
                elif page_id == 'newticket':
                    if on_navigate_to_new_ticket:
                        on_navigate_to_new_ticket()
                else:
                    if on_navigate_to_page:
                        on_navigate_to_page(page_id)
            self.on_navigate = navigate_wrapper
        
        # IMPORTANTE: Configura o frame para ocupar todo o espaço
        self.configure(fg_color="#F8F9FA")
        print("[HomePage.__init__] Frame configurado")
        
        # Grid layout igual ao web: "sidebar header" / "sidebar main"
        self.grid_columnconfigure(0, weight=0, minsize=280)  # Sidebar
        self.grid_columnconfigure(1, weight=1)  # Conteúdo principal
        self.grid_rowconfigure(0, weight=0, minsize=70)  # Header
        self.grid_rowconfigure(1, weight=1)  # Conteúdo
        print("[HomePage.__init__] Grid configurado")
        
        # Sidebar (esquerda, ocupa 2 linhas)
        print("[HomePage.__init__] Criando Sidebar...")
        try:
            self.sidebar = Sidebar(self, current_page, self.navigate)
            self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=0, pady=0)
            print("[HomePage.__init__] Sidebar criada")
        except Exception as e:
            print(f"[HomePage.__init__] ERRO ao criar Sidebar: {e}")
            raise
        
        # Header (topo, coluna 1)
        print("[HomePage.__init__] Criando Header...")
        try:
            # Extrai o primeiro nome do user_info
            first_name = ""
            if user_info and user_info.get('nome'):
                name_parts = user_info['nome'].strip().split()
                first_name = name_parts[0] if name_parts else ""
            elif user_info and user_info.get('email'):
                first_name = user_info['email'].split('@')[0]
            
            self.header = Header(
                self, 
                on_logout, 
                first_name,
                user_info=user_info,
                on_navigate_to_profile=self.on_navigate_to_profile,
                page_title=""  # Título inicial vazio, será atualizado quando navegar
            )
            self.header.grid(row=0, column=1, sticky="ew", padx=0, pady=0)
            print("[HomePage.__init__] Header criado")
        except Exception as e:
            print(f"[HomePage.__init__] ERRO ao criar Header: {e}")
            raise
        
        # Container para conteúdo principal (coluna 1, linha 1)
        print("[HomePage.__init__] Criando content_frame...")
        try:
            self.content_frame = ctk.CTkFrame(self, fg_color="#F8F9FA")
            self.content_frame.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_rowconfigure(0, weight=1)
            print("[HomePage.__init__] content_frame criado")
        except Exception as e:
            print(f"[HomePage.__init__] ERRO ao criar content_frame: {e}")
            raise
        
        # Frame atual do conteúdo
        self.current_content = None
        
        # Define título inicial
        page_titles = {
            'home': '',
            'newticket': 'NOVO CHAMADO',
            'pending-tickets': 'CHAMADOS ABERTOS',
            'completed-tickets': 'CHAMADOS CONCLUÍDOS',
            'my-tickets': 'MEUS CHAMADOS',
            'reports': 'RELATÓRIOS DO SISTEMA',
            'dashboard': 'DASHBOARD',
            'register': 'CADASTRO DE FUNCIONÁRIO',
            'ticket-detail': 'DETALHES DO CHAMADO',
            'faq': 'FQA',
            'contact': 'CONTATO'
        }
        initial_title = page_titles.get(current_page, '')
        if hasattr(self, 'header') and hasattr(self.header, 'set_title'):
            self.header.set_title(initial_title)
        
        # Mostra a página apropriada
        print("[HomePage.__init__] Chamando show_page...")
        try:
            self.show_page(current_page)
            print("[HomePage.__init__] show_page concluído")
        except Exception as e:
            print(f"[HomePage.__init__] ERRO ao chamar show_page: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        print("[HomePage.__init__] HomePage inicializado com sucesso!")
    
    def navigate(self, page_id, **kwargs):
        """Navega para uma página específica"""
        if page_id == 'logout':
            self.on_logout()
        elif page_id == 'home':
            self.show_page('home')
        else:
            self.show_page(page_id, **kwargs)
    
    def set_header_title(self, title):
        """Atualiza o título no header"""
        if hasattr(self, 'header') and hasattr(self.header, 'set_title'):
            self.header.set_title(title)
    
    def _update_user_info(self, updated_info):
        """Atualiza informações do usuário"""
        if self.user_info:
            self.user_info.update(updated_info)
        # Atualiza header se necessário
        if hasattr(self, 'header'):
            display_name = self.user_info.get('nome', 'Usuário') if self.user_info else 'Usuário'
            # Pode atualizar nome no header aqui se necessário
    
    def show_page(self, page_id, **kwargs):
        """Mostra uma página específica"""
        self.current_page = page_id
        
        # Atualiza sidebar
        if hasattr(self, 'sidebar'):
            self.sidebar.set_current_page(page_id)
        
        # Remove conteúdo anterior
        if self.current_content:
            self.current_content.destroy()
            self.current_content = None
        
        # Define títulos das páginas no header
        page_titles = {
            'home': '',
            'newticket': 'NOVO CHAMADO',
            'pending-tickets': 'CHAMADOS ABERTOS',
            'completed-tickets': 'CHAMADOS CONCLUÍDOS',
            'my-tickets': 'MEUS CHAMADOS',
            'reports': 'RELATÓRIO DE USUÁRIOS',
            'dashboard': 'RELATÓRIOS DO SISTEMA',
            'register': 'CADASTRO DE FUNCIONÁRIO',
            'ticket-detail': 'DETALHES DO CHAMADO',
            'user-activity': 'ATIVIDADE DO USUÁRIO',
            'faq': 'FQA',
            'contact': 'CONTATO'
        }
        title = page_titles.get(page_id, '')
        self.set_header_title(title)
        
        # Cria novo conteúdo baseado na página
        if page_id == 'home':
            self.current_content = self._create_home_content()
            if self.current_content:
                self.current_content.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
                self.content_frame.grid_columnconfigure(0, weight=1)
                self.content_frame.grid_rowconfigure(0, weight=1)
        elif page_id == 'newticket':
            self.current_content = NewTicketPage(
                self.content_frame,
                self.on_logout,
                lambda: self.navigate('home'),
                self.on_navigate,
                self.user_info
            )
        elif page_id == 'pending-tickets':
            self.current_content = PendingTicketsPage(
                self.content_frame,
                self.on_logout,
                lambda: self.navigate('home'),
                self.on_navigate,
                page_id,
                self.user_info,
                lambda ticket_id: self.navigate('ticket-detail', ticket_id=ticket_id, previous_page='pending-tickets')
            )
        elif page_id == 'completed-tickets':
            self.current_content = CompletedTicketsPage(
                self.content_frame,
                self.on_logout,
                lambda: self.navigate('home'),
                self.on_navigate,
                page_id,
                self.user_info,
                lambda ticket_id: self.navigate('ticket-detail', ticket_id=ticket_id, previous_page='completed-tickets')
            )
        elif page_id == 'my-tickets':
            self.current_content = MyTicketsPage(
                self.content_frame,
                self.on_logout,
                lambda: self.navigate('home'),
                self.on_navigate,
                page_id,
                self.user_info,
                lambda ticket_id: self.navigate('ticket-detail', ticket_id=ticket_id, previous_page='my-tickets'),
                self.on_navigate_to_profile
            )
        elif page_id == 'ticket-detail':
            ticket_id = kwargs.get('ticket_id')
            previous_page = kwargs.get('previous_page') or kwargs.get('from_page')
            if ticket_id:
                self.current_content = TicketDetailPage(
                    self.content_frame,
                    self.on_logout,
                    lambda: self.navigate('home'),
                    self.on_navigate,
                    self.user_info,
                    ticket_id,
                    previous_page=previous_page
                )
            else:
                self.current_content = self._create_home_content()
        elif page_id == 'register':
            self.current_content = RegisterEmployeePage(
                self.content_frame,
                self.on_logout,
                lambda: self.navigate('home'),
                self.user_info
            )
        elif page_id == 'reports':
            # Reports mostra UsersReportPage (relatório de usuários)
            self.current_content = UsersReportPage(
                self.content_frame,
                self.on_logout,
                lambda: self.navigate('home'),
                self.on_navigate,
                page_id,
                self.user_info,
                self.on_navigate_to_profile,
                on_view_user=lambda uid: self.navigate('user-activity', userId=uid)
            )
        elif page_id == 'dashboard':
            # Dashboard mostra ReportsPage (relatórios do sistema)
            self.current_content = ReportsPage(
                self.content_frame,
                self.on_logout,
                lambda: self.navigate('home'),
                self.on_navigate,
                page_id,
                self.user_info
            )
        elif page_id == 'user-activity':
            userId = kwargs.get('userId')
            self.current_content = UserActivityPage(
                self.content_frame,
                self.on_logout,
                lambda: self.navigate('home'),
                self.on_navigate,
                page_id,
                self.user_info,
                self.on_navigate_to_profile,
                userId=userId,
                on_back=lambda: self.navigate('reports')
            )
        elif page_id == 'faq':
            self.current_content = FAQPage(
                self.content_frame,
                self.on_logout,
                lambda: self.navigate('home'),
                self.on_navigate,
                page_id,
                self.user_info,
                self.on_navigate_to_profile
            )
        elif page_id == 'contact':
            self.current_content = ContactPage(
                self.content_frame,
                self.on_logout,
                lambda: self.navigate('home'),
                self.on_navigate,
                page_id,
                self.user_info,
                self.on_navigate_to_profile
            )
        elif page_id == 'profile':
            self.current_content = UserProfilePage(
                self.content_frame,
                self.on_logout,
                lambda: self.navigate('home'),
                self.on_navigate,
                page_id,
                self.user_info,
                self.on_navigate_to_profile,
                self._update_user_info
            )
        else:
            self.current_content = self._create_home_content()
        
        # Garante que o conteúdo seja exibido usando grid
        if self.current_content:
            self.current_content.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_rowconfigure(0, weight=1)
            # Força atualização
            self.content_frame.update_idletasks()
    
    def _create_home_content(self):
        """Cria o conteúdo da página inicial com os cards - idêntico à versão web"""
        # Frame principal - usa scrollable para não cortar quando maximizar
        frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="#F8F9FA")
        frame.grid_columnconfigure(0, weight=1)
        
        # Container interno para organizar conteúdo
        content_inner = ctk.CTkFrame(frame, fg_color="transparent")
        content_inner.pack(fill="both", expand=True, padx=32, pady=32)
        content_inner.grid_columnconfigure(0, weight=1)
        
        # Título de boas-vindas - formato exato da web: "BEM-VINDO (A), {firstName}"
        first_name = ""
        if self.user_info and self.user_info.get('nome'):
            name_parts = self.user_info['nome'].strip().split()
            first_name = name_parts[0] if name_parts else ""
        elif self.user_info and self.user_info.get('email'):
            first_name = self.user_info['email'].split('@')[0]
        
        welcome_text = f"BEM-VINDO (A){', ' + first_name.upper() if first_name else ''}"
        content_inner.grid_columnconfigure(0, weight=1)
        content_inner.grid_rowconfigure(0, weight=0)  # Título
        content_inner.grid_rowconfigure(1, weight=1)  # Cards
        content_inner.grid_rowconfigure(2, weight=0)  # Footer
        
        welcome_label = ctk.CTkLabel(
            content_inner,
            text=welcome_text,
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#000000"
        )
        welcome_label.pack(pady=(0, 32))
        
        # Container para os cards - grid responsivo como na web
        cards_container = ctk.CTkFrame(content_inner, fg_color="transparent")
        cards_container.pack(fill="both", expand=True, pady=(0, 32))
        
        # Grid responsivo: mínimo 280px por card, adapta-se automaticamente
        # Usa uniform para garantir que todas as colunas tenham a mesma largura
        cards_container.grid_columnconfigure(0, weight=1, minsize=280, uniform="card_col")
        cards_container.grid_columnconfigure(1, weight=1, minsize=280, uniform="card_col")
        cards_container.grid_columnconfigure(2, weight=1, minsize=280, uniform="card_col")
        
        # Configura linhas do grid para altura uniforme - todas com mesma altura
        # Altura maior para cards mais quadrados (aspect ratio ~1:1)
        # Com largura mínima de 280px, altura de 280px cria cards quadrados
        max_rows = 3
        for r in range(max_rows):
            cards_container.grid_rowconfigure(r, weight=1, minsize=280, uniform="card_row")
        
        permissao = self.user_info.get('permissao') if self.user_info else None
        card_count = 0
        
        # Card: Novo Chamado (todos podem ver)
        if permissao in [1, 2, 3] or permissao is None:
            row = card_count // 3
            col = card_count % 3
            # Usa callback direto se disponível, senão usa navigate interno
            def new_ticket_command():
                print(f"[HomePage] Card NOVO CHAMADO clicado")
                print(f"[HomePage] on_navigate_to_new_ticket: {self.on_navigate_to_new_ticket}")
                if self.on_navigate_to_new_ticket:
                    self.on_navigate_to_new_ticket()
                else:
                    self.navigate('newticket')
            self._create_card(
                cards_container,
                "✏️",
                "NOVO CHAMADO",
                new_ticket_command,
                row=row,
                col=col
            )
            card_count += 1
        
        # Card "MEUS CHAMADOS" apenas para Colaborador (1)
        if permissao == 1:
            row = card_count // 3
            col = card_count % 3
            def my_tickets_command():
                print(f"[HomePage] Card MEUS CHAMADOS clicado")
                if self.on_navigate_to_page:
                    self.on_navigate_to_page('my-tickets')
                else:
                    self.navigate('my-tickets')
            self._create_card(
                cards_container,
                "📋",
                "MEUS CHAMADOS",
                my_tickets_command,
                row=row,
                col=col
            )
            card_count += 1
        
        # Cards apenas para Suporte (2) e Admin (3)
        if permissao in [2, 3]:
            row = card_count // 3
            col = card_count % 3
            # Usa callback direto se disponível
            def pending_command():
                print(f"[HomePage] Card CHAMADOS EM ANDAMENTO clicado")
                print(f"[HomePage] on_navigate_to_page: {self.on_navigate_to_page}")
                if self.on_navigate_to_page:
                    self.on_navigate_to_page('pending-tickets')
                else:
                    self.navigate('pending-tickets')
            self._create_card(
                cards_container,
                "📋",
                "CHAMADOS EM ANDAMENTO",
                pending_command,
                row=row,
                col=col
            )
            card_count += 1
            
            row = card_count // 3
            col = card_count % 3
            # Usa callback direto se disponível
            def completed_command():
                print(f"[HomePage] Card CHAMADOS CONCLUÍDOS clicado")
                print(f"[HomePage] on_navigate_to_page: {self.on_navigate_to_page}")
                if self.on_navigate_to_page:
                    self.on_navigate_to_page('completed-tickets')
                else:
                    self.navigate('completed-tickets')
            self._create_card(
                cards_container,
                "✅",
                "CHAMADOS CONCLUÍDOS",
                completed_command,
                row=row,
                col=col
            )
            card_count += 1
            
            row = card_count // 3
            col = card_count % 3
            # Usa callback direto se disponível
            def reports_command():
                print(f"[HomePage] Card RELATÓRIOS clicado")
                print(f"[HomePage] on_navigate_to_page: {self.on_navigate_to_page}")
                if self.on_navigate_to_page:
                    self.on_navigate_to_page('reports')
                else:
                    self.navigate('reports')
            self._create_card(
                cards_container,
                "📊",
                "RELATÓRIOS",
                reports_command,
                row=row,
                col=col
            )
            card_count += 1
        
        # Card apenas para Admin (3)
        if permissao == 3:
            row = card_count // 3
            col = card_count % 3
            # Usa callback direto se disponível
            def register_command():
                print(f"[HomePage] Card CADASTRO DE FUNCIONÁRIO clicado")
                print(f"[HomePage] on_navigate_to_register: {self.on_navigate_to_register}")
                if self.on_navigate_to_register:
                    self.on_navigate_to_register()
                else:
                    self.navigate('register')
            self._create_card(
                cards_container,
                "👥",
                "CADASTRO DE FUNCIONÁRIO",
                register_command,
                row=row,
                col=col
            )
            card_count += 1
        
        # Configura as linhas do grid conforme necessário
        max_row = (card_count - 1) // 3
        for r in range(max_row + 1):
            cards_container.grid_rowconfigure(r, weight=1)
        
        # Footer - formato exato da web com duas linhas separadas
        footer_frame = ctk.CTkFrame(content_inner, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(32, 0))
        
        # Linha divisória
        separator = ctk.CTkFrame(footer_frame, fg_color="#E5E5E5", height=2)
        separator.pack(fill="x", pady=(0, 16))
        
        footer_text1 = ctk.CTkLabel(
            footer_frame,
            text="HelpWave — Simplificando o seu suporte.",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        )
        footer_text1.pack(pady=(0, 4))
        
        footer_text2 = ctk.CTkLabel(
            footer_frame,
            text="© 2025 HelpWave",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        )
        footer_text2.pack()
        
        return frame
    
    def _create_card(self, parent, icon, text, command, row, col):
        """Cria um card clicável para o dashboard - visual idêntico ao web"""
        # Card vermelho usando a cor primária do sistema
        card = ctk.CTkFrame(
            parent,
            corner_radius=16,  # Bordas arredondadas
            fg_color=COLORS['primary'],  # Vermelho do sistema (#A93226)
            border_width=0  # Sem borda para visual mais limpo
        )
        # Configura o card no grid com gap de 24px (var(--space-xl))
        card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
        
        # Container interno para centralizar conteúdo - usa pack para centralização perfeita
        card_inner = ctk.CTkFrame(card, fg_color="transparent")
        card_inner.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Container para ícone e texto centralizados - usa grid para controle preciso
        content_container = ctk.CTkFrame(card_inner, fg_color="transparent")
        content_container.place(relx=0.5, rely=0.5, anchor="center")
        content_container.grid_columnconfigure(0, weight=1)
        
        # Ícone - branco, tamanho 3rem (48px), perfeitamente centralizado
        icon_label = ctk.CTkLabel(
            content_container,
            text=icon,
            font=ctk.CTkFont(size=48),
            fg_color="transparent",
            text_color="#FFFFFF",
            anchor="center",
            width=80,
            height=60
        )
        icon_label.grid(row=0, column=0, pady=(0, 16), sticky="")
        
        # Texto - branco, bold, uppercase, centralizado
        text_label = ctk.CTkLabel(
            content_container,
            text=text,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF",
            fg_color="transparent",
            anchor="center",
            wraplength=200,
            justify="center"
        )
        text_label.grid(row=1, column=0, sticky="")
        
        # Efeito hover e clique - aplicado diretamente no card
        original_color = COLORS['primary']
        hover_color = COLORS['neutral_900']  # Preto no hover
        
        def on_enter(event):
            # Muda cor para preto - SEM mudar tamanho para evitar movimento
            card.configure(fg_color=hover_color)
            card.configure(cursor="hand2")
        
        def on_leave(event):
            # Volta ao vermelho original
            card.configure(fg_color=original_color)
            card.configure(cursor="")
        
        def on_click(event=None):
            print(f"[HomePage._create_card] Card clicado: {text}")
            print(f"[HomePage._create_card] command: {command}")
            if command:
                try:
                    command()
                    print(f"[HomePage._create_card] Comando executado com sucesso")
                except Exception as e:
                    print(f"[HomePage._create_card] ERRO ao executar comando: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print(f"[HomePage._create_card] AVISO: command é None!")
        
        # Aplica hover e clique diretamente no card (não nos filhos)
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", on_click)
        card.configure(cursor="hand2")
        
        # Também aplica nos filhos para garantir que funcione em qualquer lugar
        for widget in [card_inner, content_container, icon_label, text_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
            try:
                widget.configure(cursor="hand2")
            except:
                pass
        
        return card
