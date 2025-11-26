"""
FAQPage - Replica FAQPage.jsx do web
Versão simplificada com as principais seções
"""
import tkinter as tk
from pages.base_page import BasePage

class FAQPage(BasePage):
    """Página FAQ - replica FAQPage.jsx"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page,
                 current_page, user_info, on_navigate_to_profile):
        super().__init__(parent, on_logout, on_navigate_to_page, current_page, user_info, page_title="MANUAL DO SISTEMA", create_header_sidebar=False)
        
        self.on_navigate_to_home = on_navigate_to_home
        self.open_section = None
        self.permissao = user_info.get('permissao', 1) if user_info else 1
        self.is_colaborador = self.permissao == 1
        
        self._create_ui()
    
    def _create_ui(self):
        """Cria interface igual à versão web"""
        # Container principal com scroll
        canvas = tk.Canvas(self.main_content, bg="#F8F9FA", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.main_content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F8F9FA")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        container = tk.Frame(scrollable_frame, bg="#F8F9FA")
        container.pack(fill=tk.BOTH, expand=True, padx=48, pady=48)
        
        
        # Header
        header_frame = tk.Frame(container, bg="#F8F9FA")
        header_frame.pack(fill=tk.X, pady=(0, 32))
        
        title_frame = tk.Frame(header_frame, bg="#F8F9FA")
        title_frame.pack()
        
        title_icon = tk.Label(title_frame, text="❓", font=("Inter", 24), bg="#F8F9FA", fg="#A93226")
        title_icon.pack(side=tk.LEFT, padx=(0, 12))
        
        title_label = tk.Label(
            title_frame,
            text="Manual do Sistema HelpWave",
            font=("Inter", 32, "bold"),
            bg="#F8F9FA",
            fg="#262626"
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle = tk.Label(
            header_frame,
            text="Guia completo para uso do sistema de gestão de chamados técnicos",
            font=("Inter", 16),
            bg="#F8F9FA",
            fg="#737373"
        )
        subtitle.pack(pady=(12, 0))
        
        # Seções FAQ
        self.sections_frame = tk.Frame(container, bg="#F8F9FA")
        self.sections_frame.pack(fill=tk.BOTH, expand=True)
        
        self._create_sections()
        
        # Footer
        footer_frame = tk.Frame(container, bg="#F8F9FA")
        footer_frame.pack(fill=tk.X, pady=(32, 0))
        
        footer_text = tk.Label(
            footer_frame,
            text="Não encontrou o que procura? Entre em contato através do menu CONTATO.",
            font=("Inter", 14),
            bg="#F8F9FA",
            fg="#737373",
            wraplength=800,
            justify="center"
        )
        footer_text.pack(pady=(0, 8))
        
        copyright_text = tk.Label(
            footer_frame,
            text="© 2025 HelpWave - Simplificando o seu suporte",
            font=("Inter", 12),
            bg="#F8F9FA",
            fg="#999999"
        )
        copyright_text.pack()
    
    def _create_sections(self):
        """Cria seções FAQ baseadas nas permissões do usuário"""
        sections = []
        
        # Visão Geral
        sections.append({
            'id': 'visao-geral',
            'title': 'Visão Geral do Sistema',
            'icon': 'ℹ️',
            'visible_for': None,  # Todos
            'content': self._get_visao_geral_content()
        })
        
        # Navegação
        sections.append({
            'id': 'navegacao',
            'title': 'Navegação no Sistema',
            'icon': '🏠',
            'visible_for': None,
            'content': self._get_navegacao_content()
        })
        
        # Home
        sections.append({
            'id': 'home',
            'title': 'Página Inicial (Home)',
            'icon': '🏠',
            'visible_for': None,
            'content': self._get_home_content()
        })
        
        # Criar Chamado
        sections.append({
            'id': 'criar-chamado',
            'title': 'Como Criar um Chamado',
            'icon': '✏️',
            'visible_for': None,
            'content': self._get_criar_chamado_content()
        })
        
        # Gerenciar Chamados (apenas Suporte/Admin)
        if not self.is_colaborador:
            sections.append({
                'id': 'gerenciar-chamados',
                'title': 'Gerenciar Chamados (Suporte/Admin)',
                'icon': '📋',
                'visible_for': [2, 3],
                'content': self._get_gerenciar_chamados_content()
            })
            
            sections.append({
                'id': 'relatorios',
                'title': 'Relatórios e Estatísticas',
                'icon': '📊',
                'visible_for': [2, 3],
                'content': self._get_relatorios_content()
            })
        
        # Perfil
        sections.append({
            'id': 'perfil',
            'title': 'Gerenciar Perfil',
            'icon': '👤',
            'visible_for': None,
            'content': self._get_perfil_content()
        })
        
        # Perguntas Frequentes
        sections.append({
            'id': 'perguntas-frequentes',
            'title': 'Perguntas Frequentes',
            'icon': '❓',
            'visible_for': None,
            'content': self._get_perguntas_frequentes_content()
        })
        
        # Cria seções visíveis
        for section in sections:
            if section['visible_for'] is None or self.permissao in section['visible_for']:
                self._create_section_item(section)
    
    def _create_section_item(self, section):
        """Cria um item de seção expansível"""
        section_frame = tk.Frame(self.sections_frame, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        section_frame.pack(fill=tk.X, pady=(0, 16))
        
        # Header clicável
        header_btn = tk.Frame(section_frame, bg="#FFFFFF", cursor="hand2")
        header_btn.pack(fill=tk.X)
        header_btn.bind("<Button-1>", lambda e: self._toggle_section(section['id'], content_frame))
        
        header_inner = tk.Frame(header_btn, bg="#FFFFFF")
        header_inner.pack(fill=tk.X, padx=24, pady=16)
        
        # Ícone e título
        title_frame = tk.Frame(header_inner, bg="#FFFFFF")
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        icon_label = tk.Label(title_frame, text=section['icon'], font=("Inter", 18), bg="#FFFFFF", fg="#A93226")
        icon_label.pack(side=tk.LEFT, padx=(0, 12))
        icon_label.bind("<Button-1>", lambda e: self._toggle_section(section['id'], content_frame))
        
        title_label = tk.Label(
            title_frame,
            text=section['title'],
            font=("Inter", 18, "bold"),
            bg="#FFFFFF",
            fg="#262626"
        )
        title_label.pack(side=tk.LEFT)
        title_label.bind("<Button-1>", lambda e: self._toggle_section(section['id'], content_frame))
        
        # Seta
        arrow_label = tk.Label(
            header_inner,
            text="▼" if self.open_section != section['id'] else "▲",
            font=("Inter", 14),
            bg="#FFFFFF",
            fg="#737373"
        )
        arrow_label.pack(side=tk.RIGHT)
        arrow_label.bind("<Button-1>", lambda e: self._toggle_section(section['id'], content_frame))
        
        # Conteúdo (inicialmente oculto)
        content_frame = tk.Frame(section_frame, bg="#FFFFFF")
        if self.open_section == section['id']:
            content_frame.pack(fill=tk.X, padx=24, pady=(0, 24))
        
        content_inner = tk.Frame(content_frame, bg="#FFFFFF")
        content_inner.pack(fill=tk.X, padx=0, pady=16)
        
        # Adiciona conteúdo
        if isinstance(section['content'], str):
            content_label = tk.Label(
                content_inner,
                text=section['content'],
                font=("Inter", 14),
                bg="#FFFFFF",
                fg="#262626",
                wraplength=1000,
                justify="left",
                anchor="w"
            )
            content_label.pack(anchor="w", pady=8)
        else:
            # Se for uma lista de widgets, adiciona todos
            for widget in section['content']:
                widget.pack(anchor="w", pady=4, in_=content_inner)
        
        # Guarda referências
        section_frame.section_id = section['id']
        section_frame.content_frame = content_frame
        section_frame.arrow_label = arrow_label
    
    def _toggle_section(self, section_id, content_frame):
        """Abre/fecha uma seção"""
        if self.open_section == section_id:
            self.open_section = None
            content_frame.pack_forget()
        else:
            # Fecha outras seções
            for widget in self.sections_frame.winfo_children():
                if hasattr(widget, 'section_id') and widget.section_id != section_id:
                    if hasattr(widget, 'content_frame'):
                        widget.content_frame.pack_forget()
                    if hasattr(widget, 'arrow_label'):
                        widget.arrow_label.config(text="▼")
            
            self.open_section = section_id
            content_frame.pack(fill=tk.X, padx=24, pady=(0, 24))
            
            # Atualiza seta
            for widget in self.sections_frame.winfo_children():
                if hasattr(widget, 'section_id') and widget.section_id == section_id:
                    if hasattr(widget, 'arrow_label'):
                        widget.arrow_label.config(text="▲")
    
    def _get_visao_geral_content(self):
        """Retorna conteúdo da seção Visão Geral"""
        content = """O HelpWave é um sistema de gestão de chamados técnicos desenvolvido para facilitar 
a comunicação entre colaboradores e a equipe de suporte técnico. Este manual irá guiá-lo através 
de todas as funcionalidades disponíveis."""
        
        if not self.is_colaborador:
            content += "\n\nTipos de Usuário:\n"
            content += "• Colaborador (Permissão 1): Pode criar chamados e visualizar seus próprios chamados.\n"
            content += "• Suporte Técnico (Permissão 2): Pode visualizar, gerenciar e resolver chamados de todos os usuários.\n"
            content += "• Administrador (Permissão 3): Tem acesso completo, incluindo cadastro de funcionários e relatórios detalhados."
        else:
            content += "\n\nSua Conta:\n"
            content += "Você está logado como Colaborador. Com essa permissão, você pode:\n"
            content += "• Criar novos chamados técnicos quando precisar de assistência\n"
            content += "• Visualizar e acompanhar seus chamados\n"
            content += "• Gerenciar suas informações de perfil"
        
        return content
    
    def _get_navegacao_content(self):
        """Retorna conteúdo da seção Navegação"""
        content = "Menu Lateral (Sidebar)\n"
        content += "O menu lateral está sempre visível e permite acesso rápido às principais áreas do sistema:\n\n"
        content += "• HOME: Retorna à página inicial com os cards de acesso rápido\n"
        
        if self.is_colaborador:
            content += "• MEUS CHAMADOS: Visualiza todos os seus chamados criados\n"
        else:
            content += "• CHAMADO: Visualiza chamados em andamento\n"
            content += "• RELATÓRIOS: Acessa estatísticas e relatórios\n"
        
        content += "• FQA: Esta página de ajuda e manual do sistema\n"
        content += "• CONTATO: Informações de contato para suporte adicional\n\n"
        content += "Header (Cabeçalho)\n"
        content += "• Ícone de Usuário: Clique para acessar seu perfil\n"
        content += "• Ícone de Engrenagem: Menu com opções de Perfil e Logout"
        return content
    
    def _get_home_content(self):
        """Retorna conteúdo da seção Home"""
        content = "A página inicial exibe cards clicáveis que levam às principais funcionalidades:\n\n"
        content += "NOVO CHAMADO\n"
        content += "Permite criar um novo chamado técnico. Você precisa informar:\n"
        content += "• Tipo de chamado (Suporte, Manutenção, Instalação, Consultoria, Emergência)\n"
        content += "• Título do chamado\n"
        content += "• Descrição detalhada do problema\n\n"
        
        if self.is_colaborador:
            content += "MEUS CHAMADOS\n"
            content += "Permite visualizar todos os seus chamados criados."
        else:
            content += "CHAMADOS EM ANDAMENTO\n"
            content += "Lista todos os chamados que estão abertos ou em andamento.\n\n"
            content += "CHAMADOS CONCLUÍDOS\n"
            content += "Histórico de todos os chamados já resolvidos.\n\n"
            content += "RELATÓRIOS\n"
            content += "Visualiza estatísticas e métricas do sistema."
        
        return content
    
    def _get_criar_chamado_content(self):
        """Retorna conteúdo da seção Criar Chamado"""
        content = "1. Na página inicial, clique no card 'NOVO CHAMADO'\n"
        content += "2. Selecione o Tipo de Chamado no dropdown\n"
        content += "3. Digite um Título descritivo para o chamado (mínimo 5 caracteres)\n"
        content += "4. Escreva uma Descrição detalhada do problema (mínimo 10 caracteres)\n"
        content += "5. Clique em 'ENVIAR'\n\n"
        content += "Atenção: Certifique-se de preencher todos os campos obrigatórios antes de enviar."
        return content
    
    def _get_gerenciar_chamados_content(self):
        """Retorna conteúdo da seção Gerenciar Chamados"""
        content = "Visualizar Chamados em Andamento\n"
        content += "1. Acesse 'CHAMADOS EM ANDAMENTO' pelo menu lateral\n"
        content += "2. Use a barra de pesquisa para buscar por título ou código\n"
        content += "3. Use os filtros para ordenar por diferentes critérios\n"
        content += "4. Clique em um chamado para ver detalhes completos\n\n"
        content += "Atualizar um Chamado\n"
        content += "1. Ao abrir um chamado, você verá todas as informações\n"
        content += "2. Na seção de 'Solução', você pode escrever a descrição da solução aplicada\n"
        content += "3. Clique em 'ENVIAR SOLUÇÃO' para fechar o chamado"
        return content
    
    def _get_relatorios_content(self):
        """Retorna conteúdo da seção Relatórios"""
        content = "Os relatórios fornecem uma visão geral do desempenho do sistema:\n"
        content += "• Total de Usuários: Número total de usuários cadastrados\n"
        content += "• Total de Chamados: Todos os chamados já criados\n"
        content += "• Chamados Resolvidos: Quantidade de chamados já concluídos\n"
        content += "• Chamados Em Andamento: Chamados abertos que estão sendo trabalhados"
        return content
    
    def _get_perfil_content(self):
        """Retorna conteúdo da seção Perfil"""
        content = "Como Acessar Seu Perfil\n"
        content += "1. Clique no ícone de usuário no header, OU\n"
        content += "2. Clique no ícone de engrenagem e selecione 'Perfil' no menu\n\n"
        content += "Editar Informações do Perfil\n"
        content += "1. Na página de perfil, clique no botão 'EDITAR PERFIL'\n"
        content += "2. Os campos editáveis serão habilitados\n"
        content += "3. Faça as alterações desejadas\n"
        content += "4. Clique em 'SALVAR ALTERAÇÕES' para confirmar"
        return content
    
    def _get_perguntas_frequentes_content(self):
        """Retorna conteúdo da seção Perguntas Frequentes"""
        content = "Como faço login no sistema?\n"
        content += "Use seu e-mail e senha cadastrados. Se você não tem acesso, entre em contato com um administrador.\n\n"
        content += "Esqueci minha senha. O que fazer?\n"
        content += "Entre em contato com o administrador do sistema ou com a equipe de TI para redefinir sua senha.\n\n"
        content += "Posso cancelar um chamado que criei?\n"
        content += "Chamados abertos podem ser atualizados apenas pela equipe de suporte. Se precisar cancelar, entre em contato com a equipe.\n\n"
        content += "Como sei quando meu chamado foi resolvido?\n"
        content += "O status do chamado será atualizado para 'Resolvido' quando o técnico finalizar o atendimento."
        return content


