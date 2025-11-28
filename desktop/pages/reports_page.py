"""
ReportsPage - Replica ReportsPage.jsx do web
"""
import tkinter as tk
import customtkinter as ctk
from pages.base_page import BasePage
from api_client import TicketService, UserService, AIService, api_client
from config import COLORS
import threading
import requests

class ReportsPage(BasePage):
    """Página de relatórios - replica ReportsPage.jsx"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page,
                 current_page, user_info):
        super().__init__(parent, on_logout, on_navigate_to_page, current_page, user_info, page_title="RELATÓRIOS DO SISTEMA", create_header_sidebar=False)
        
        self.on_navigate_to_home = on_navigate_to_home
        
        self.reports = {
            'totalUsuarios': 0,
            'totalChamados': 0,
            'chamadosResolvidos': 0,
            'chamadosEmAndamento': 0,
            'usuariosPorNivel': {
                'colaboradores': 0,
                'suporteTecnico': 0,
                'administradores': 0
            }
        }
        self.loading = True
        
        self._create_ui()
        self._load_reports()
    
    def _create_ui(self):
        """Cria a interface - layout idêntico ao web"""
        container = tk.Frame(self.main_content, bg="#F8F9FA")
        container.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)
        
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
        
        # Cards de estatísticas - layout horizontal (ícone à esquerda, conteúdo à direita)
        stats_frame = tk.Frame(container, bg="#F8F9FA")
        stats_frame.pack(fill=tk.X, pady=(0, 32))
        
        # Grid com 4 colunas, cada uma com weight=1 para distribuir igualmente
        stats_frame.grid_columnconfigure(0, weight=1, minsize=250)
        stats_frame.grid_columnconfigure(1, weight=1, minsize=250)
        stats_frame.grid_columnconfigure(2, weight=1, minsize=250)
        stats_frame.grid_columnconfigure(3, weight=1, minsize=250)
        
        self.stats_cards = {}
        stats = [
            ('totalUsuarios', 'Usuários Cadastrados', '👥'),
            ('totalChamados', 'Total de Chamados', '✅'),
            ('chamadosResolvidos', 'Chamados Resolvidos', '✅'),
            ('chamadosEmAndamento', 'Em Andamento', '⏳')
        ]
        
        for i, (key, label, icon) in enumerate(stats):
            # Card branco com bordas arredondadas simuladas e sombra
            card = tk.Frame(stats_frame, bg="#FFFFFF", bd=0, relief=tk.FLAT)
            card.grid(row=0, column=i, padx=12, pady=0, sticky="nsew")
            
            # Container interno com padding
            card_inner = tk.Frame(card, bg="#FFFFFF")
            card_inner.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)
            
            # Layout horizontal: ícone à esquerda, conteúdo à direita
            icon_frame = tk.Frame(card_inner, bg="#FFFFFF", width=60, height=60)
            icon_frame.pack(side=tk.LEFT, padx=(0, 24))
            icon_frame.pack_propagate(False)
            
            # Ícone circular (simulado com label)
            icon_label = tk.Label(
                icon_frame, 
                text=icon, 
                font=("Inter", 24), 
                bg="#FFFFFF", 
                fg="#A93226"
            )
            icon_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Conteúdo à direita
            content_frame = tk.Frame(card_inner, bg="#FFFFFF")
            content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            value_label = tk.Label(
                content_frame, 
                text="0", 
                font=("Inter", 40, "bold"), 
                bg="#FFFFFF", 
                fg="#2d3748",
                anchor="w"
            )
            value_label.pack(anchor="w")
            
            text_label = tk.Label(
                content_frame, 
                text=label, 
                font=("Inter", 14), 
                bg="#FFFFFF", 
                fg="#718096",
                anchor="w"
            )
            text_label.pack(anchor="w", pady=(4, 0))
            
            self.stats_cards[key] = value_label
        
        # Seção de usuários por nível - card branco
        users_frame = tk.Frame(container, bg="#FFFFFF", bd=0, relief=tk.FLAT)
        users_frame.pack(fill=tk.X, pady=(0, 32))
        
        users_inner = tk.Frame(users_frame, bg="#FFFFFF")
        users_inner.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)
        
        # Título da seção com borda inferior
        title_frame = tk.Frame(users_inner, bg="#FFFFFF")
        title_frame.pack(fill=tk.X, pady=(0, 24))
        
        title_text = tk.Label(
            title_frame,
            text="USUÁRIOS POR NÍVEL DE ACESSO",
            font=("Inter", 20, "bold"),
            bg="#FFFFFF",
            fg="#2d3748"
        )
        title_text.pack(anchor="w")
        
        # Linha divisória vermelha
        divider = tk.Frame(title_frame, bg="#A93226", height=2)
        divider.pack(fill=tk.X, pady=(8, 0))
        
        # Grid para os níveis de usuário
        levels_frame = tk.Frame(users_inner, bg="#FFFFFF")
        levels_frame.pack(fill=tk.X)
        levels_frame.grid_columnconfigure(0, weight=1, minsize=200)
        levels_frame.grid_columnconfigure(1, weight=1, minsize=200)
        levels_frame.grid_columnconfigure(2, weight=1, minsize=200)
        
        self.users_labels = {}
        levels = [
            ('colaboradores', 'Colaboradores', '#4299e1'),
            ('suporteTecnico', 'Suporte Técnico', '#f6ad55'),
            ('administradores', 'Administradores', '#48bb78')
        ]
        
        for i, (nivel, label_text, color) in enumerate(levels):
            item_frame = tk.Frame(levels_frame, bg="#f7fafc")
            item_frame.grid(row=0, column=i, padx=8, pady=0, sticky="nsew")
            
            item_inner = tk.Frame(item_frame, bg="#f7fafc")
            item_inner.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
            
            # Indicador circular colorido
            indicator_frame = tk.Frame(item_inner, bg="#f7fafc")
            indicator_frame.pack(side=tk.LEFT, padx=(0, 16))
            
            indicator = tk.Frame(indicator_frame, bg=color, width=12, height=12)
            indicator.pack()
            indicator.pack_propagate(False)
            
            # Conteúdo
            content_frame = tk.Frame(item_inner, bg="#f7fafc")
            content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            name_label = tk.Label(
                content_frame,
                text=label_text,
                font=("Inter", 14),
                bg="#f7fafc",
                fg="#718096",
                anchor="w"
            )
            name_label.pack(anchor="w")
            
            count_label = tk.Label(
                content_frame,
                text="0",
                font=("Inter", 24, "bold"),
                bg="#f7fafc",
                fg="#2d3748",
                anchor="w"
            )
            count_label.pack(anchor="w", pady=(4, 0))
            
            self.users_labels[nivel] = count_label
        
        # Seção de Estatísticas de Chamados (barras de progresso)
        stats_section = tk.Frame(container, bg="#FFFFFF", bd=0, relief=tk.FLAT)
        stats_section.pack(fill=tk.X, pady=(0, 32))
        
        stats_inner = tk.Frame(stats_section, bg="#FFFFFF")
        stats_inner.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)
        
        # Título da seção
        stats_title_frame = tk.Frame(stats_inner, bg="#FFFFFF")
        stats_title_frame.pack(fill=tk.X, pady=(0, 24))
        
        stats_title = tk.Label(
            stats_title_frame,
            text="ESTATÍSTICAS DE CHAMADOS",
            font=("Inter", 20, "bold"),
            bg="#FFFFFF",
            fg="#2d3748"
        )
        stats_title.pack(anchor="w")
        
        # Linha divisória vermelha
        divider2 = tk.Frame(stats_title_frame, bg="#A93226", height=2)
        divider2.pack(fill=tk.X, pady=(8, 0))
        
        # Container para barras de progresso
        bars_frame = tk.Frame(stats_inner, bg="#FFFFFF")
        bars_frame.pack(fill=tk.X)
        
        # Barra para Resolvidos
        self.resolved_bar_container = tk.Frame(bars_frame, bg="#FFFFFF")
        self.resolved_bar_container.pack(fill=tk.X, pady=(0, 24))
        
        resolved_bar_bg = tk.Frame(self.resolved_bar_container, bg="#e2e8f0", height=24)
        resolved_bar_bg.pack(fill=tk.X)
        
        self.resolved_bar_fill = tk.Frame(resolved_bar_bg, bg="#28a745", height=24)
        self.resolved_bar_fill.pack(side=tk.LEFT, fill=tk.Y)
        
        resolved_info = tk.Frame(self.resolved_bar_container, bg="#FFFFFF")
        resolved_info.pack(fill=tk.X, pady=(8, 0))
        
        self.resolved_label = tk.Label(
            resolved_info,
            text="Resolvidos: 0 (0%)",
            font=("Inter", 14),
            bg="#FFFFFF",
            fg="#2d3748",
            anchor="w"
        )
        self.resolved_label.pack(anchor="w")
        
        # Barra para Em Andamento
        self.in_progress_bar_container = tk.Frame(bars_frame, bg="#FFFFFF")
        self.in_progress_bar_container.pack(fill=tk.X)
        
        in_progress_bar_bg = tk.Frame(self.in_progress_bar_container, bg="#e2e8f0", height=24)
        in_progress_bar_bg.pack(fill=tk.X)
        
        self.in_progress_bar_fill = tk.Frame(in_progress_bar_bg, bg="#ffc107", height=24)
        self.in_progress_bar_fill.pack(side=tk.LEFT, fill=tk.Y)
        
        in_progress_info = tk.Frame(self.in_progress_bar_container, bg="#FFFFFF")
        in_progress_info.pack(fill=tk.X, pady=(8, 0))
        
        self.in_progress_label = tk.Label(
            in_progress_info,
            text="Em Andamento: 0 (0%)",
            font=("Inter", 14),
            bg="#FFFFFF",
            fg="#2d3748",
            anchor="w"
        )
        self.in_progress_label.pack(anchor="w")
        
        # Seção de Status das APIs
        api_section = tk.Frame(container, bg="#FFFFFF", bd=0, relief=tk.FLAT)
        api_section.pack(fill=tk.X)
        
        api_inner = tk.Frame(api_section, bg="#FFFFFF")
        api_inner.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)
        
        # Título da seção
        api_title_frame = tk.Frame(api_inner, bg="#FFFFFF")
        api_title_frame.pack(fill=tk.X, pady=(0, 24))
        
        api_title = tk.Label(
            api_title_frame,
            text="STATUS DOS SERVIÇOS",
            font=("Inter", 20, "bold"),
            bg="#FFFFFF",
            fg="#2d3748"
        )
        api_title.pack(anchor="w")
        
        # Linha divisória vermelha
        divider3 = tk.Frame(api_title_frame, bg="#A93226", height=2)
        divider3.pack(fill=tk.X, pady=(8, 0))
        
        # Grid para cards de API
        api_grid = tk.Frame(api_inner, bg="#FFFFFF")
        api_grid.pack(fill=tk.X)
        api_grid.grid_columnconfigure(0, weight=1, minsize=300)
        api_grid.grid_columnconfigure(1, weight=1, minsize=300)
        
        # Card API Database
        db_card = tk.Frame(api_grid, bg="#f7fafc", bd=1, relief=tk.SOLID)
        db_card.grid(row=0, column=0, padx=12, pady=0, sticky="nsew")
        
        db_inner = tk.Frame(db_card, bg="#f7fafc")
        db_inner.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)
        
        db_icon = tk.Label(db_inner, text="🗄️", font=("Inter", 32), bg="#f7fafc", fg="#A93226")
        db_icon.pack(side=tk.LEFT, padx=(0, 16))
        
        db_info = tk.Frame(db_inner, bg="#f7fafc")
        db_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        db_title = tk.Label(db_info, text="API Banco de Dados", font=("Inter", 16, "bold"), 
                           bg="#f7fafc", fg="#2d3748", anchor="w")
        db_title.pack(anchor="w")
        
        self.db_status_frame = tk.Frame(db_info, bg="#f7fafc")
        self.db_status_frame.pack(anchor="w", pady=(8, 0))
        
        self.db_status_icon = tk.Label(self.db_status_frame, text="🔄", font=("Inter", 14), 
                                       bg="#f7fafc", fg="#ffc107")
        self.db_status_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        self.db_status_label = tk.Label(self.db_status_frame, text="Verificando...", 
                                       font=("Inter", 14), bg="#f7fafc", fg="#ffc107", anchor="w")
        self.db_status_label.pack(side=tk.LEFT)
        
        self.db_response_label = tk.Label(db_info, text="", font=("Inter", 12), 
                                         bg="#f7fafc", fg="#718096", anchor="w")
        self.db_response_label.pack(anchor="w", pady=(4, 0))
        
        # Card API IA
        ai_card = tk.Frame(api_grid, bg="#f7fafc", bd=1, relief=tk.SOLID)
        ai_card.grid(row=0, column=1, padx=12, pady=0, sticky="nsew")
        
        ai_inner = tk.Frame(ai_card, bg="#f7fafc")
        ai_inner.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)
        
        ai_icon = tk.Label(ai_inner, text="🤖", font=("Inter", 32), bg="#f7fafc", fg="#A93226")
        ai_icon.pack(side=tk.LEFT, padx=(0, 16))
        
        ai_info = tk.Frame(ai_inner, bg="#f7fafc")
        ai_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ai_title = tk.Label(ai_info, text="API de IA", font=("Inter", 16, "bold"), 
                           bg="#f7fafc", fg="#2d3748", anchor="w")
        ai_title.pack(anchor="w")
        
        self.ai_status_frame = tk.Frame(ai_info, bg="#f7fafc")
        self.ai_status_frame.pack(anchor="w", pady=(8, 0))
        
        self.ai_status_icon = tk.Label(self.ai_status_frame, text="🔄", font=("Inter", 14), 
                                  bg="#f7fafc", fg="#ffc107")
        self.ai_status_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        self.ai_status_label = tk.Label(self.ai_status_frame, text="Verificando...", 
                                   font=("Inter", 14), bg="#f7fafc", fg="#ffc107", anchor="w")
        self.ai_status_label.pack(side=tk.LEFT)
        
        self.ai_response_label = tk.Label(ai_info, text="", font=("Inter", 12), 
                                    bg="#f7fafc", fg="#718096", anchor="w")
        self.ai_response_label.pack(anchor="w", pady=(4, 0))
    
    def _load_reports(self):
        """Carrega relatórios"""
        self.loading = True
        threading.Thread(target=self._do_load_reports, daemon=True).start()
    
    def _do_load_reports(self):
        """Faz carregamento"""
        try:
            # Busca tickets
            tickets = TicketService.get_tickets()
            
            total_chamados = len(tickets) if tickets else 0
            # Status 3 = Fechado (concluído/resolvido) - como na versão web
            chamados_resolvidos = len([t for t in (tickets or []) if t.get('status') == 3])
            # Status 1 e 2 = Aberto e Em Atendimento (em andamento) - como na versão web
            chamados_em_andamento = len([t for t in (tickets or []) if t.get('status') in [1, 2]])
            
            # Busca usuários
            usuarios_por_nivel = {
                'colaboradores': 0,
                'suporteTecnico': 0,
                'administradores': 0
            }
            total_usuarios = 0
            
            try:
                users = UserService.get_users()
                if users:
                    total_usuarios = len(users)
                    for user in users:
                        permissao = user.get('permissao', 1)
                        if permissao == 1:
                            usuarios_por_nivel['colaboradores'] += 1
                        elif permissao == 2:
                            usuarios_por_nivel['suporteTecnico'] += 1
                        elif permissao == 3:
                            usuarios_por_nivel['administradores'] += 1
            except Exception as e:
                print(f"Erro ao carregar usuários: {e}")
            
            # Verifica status da API de banco de dados
            api_status = {'database': {'status': 'checking', 'responseTime': None}, 
                         'ai': {'status': 'checking', 'responseTime': None}}
            try:
                import time
                start_time = time.time()
                TicketService.get_tickets()
                end_time = time.time()
                response_time = int((end_time - start_time) * 1000)
                api_status['database'] = {'status': 'online', 'responseTime': response_time}
            except:
                api_status['database'] = {'status': 'offline', 'responseTime': None}
            
            # Verifica status da API de IA
            try:
                import time
                from config import FLASK_BASE_URL
                import requests
                
                start_time = time.time()
                # Tenta fazer uma requisição de teste ao endpoint de IA
                flask_url = FLASK_BASE_URL or 'http://localhost:5000'
                test_url = f'{flask_url}/api/gemini/sugerir-resposta'
                
                token = api_client.get_auth_token()
                headers = {'Content-Type': 'application/json'}
                if token:
                    headers['Authorization'] = f'Bearer {token}'
                
                response = requests.post(
                    test_url,
                    json={'descricaoChamado': 'Test'},
                    headers=headers,
                    timeout=5
                )
                
                end_time = time.time()
                response_time = int((end_time - start_time) * 1000)
                
                if response.status_code == 200:
                    api_status['ai'] = {'status': 'online', 'responseTime': response_time}
                elif response.status_code == 501 or response.status_code == 404:
                    api_status['ai'] = {'status': 'not-implemented', 'responseTime': None}
                else:
                    api_status['ai'] = {'status': 'offline', 'responseTime': None}
            except requests.exceptions.RequestException:
                # Erro de conexão
                api_status['ai'] = {'status': 'offline', 'responseTime': None}
            except Exception as e:
                # Outros erros - assume não implementado
                api_status['ai'] = {'status': 'not-implemented', 'responseTime': None}
            
            self.reports = {
                'totalUsuarios': total_usuarios,
                'totalChamados': total_chamados,
                'chamadosResolvidos': chamados_resolvidos,
                'chamadosEmAndamento': chamados_em_andamento,
                'usuariosPorNivel': usuarios_por_nivel,
                'apiStatus': api_status
            }
        except Exception as e:
            print(f"Erro ao carregar relatórios: {e}")
        finally:
            self.loading = False
            self.after(0, self._update_ui)
    
    def _update_ui(self):
        """Atualiza UI"""
        # Verifica se a página ainda existe
        try:
            if not self.winfo_exists():
                return
        except tk.TclError:
            return
        
        # Atualiza cards
        try:
            for key in ['totalUsuarios', 'totalChamados', 'chamadosResolvidos', 'chamadosEmAndamento']:
                if key in self.stats_cards:
                    card = self.stats_cards[key]
                    if card and card.winfo_exists():
                        card.config(text=str(self.reports.get(key, 0)))
        except tk.TclError:
            # Widgets foram destruídos
            return
        
        # Atualiza usuários por nível
        try:
            for nivel, label in self.users_labels.items():
                if label and label.winfo_exists():
                    count = self.reports['usuariosPorNivel'].get(nivel, 0)
                    label.config(text=str(count))
        except tk.TclError:
            # Widgets foram destruídos
            pass
        
        # Atualiza barras de progresso de estatísticas
        try:
            total = self.reports.get('totalChamados', 0)
            if total > 0:
                resolved_pct = int((self.reports.get('chamadosResolvidos', 0) / total) * 100)
                in_progress_pct = int((self.reports.get('chamadosEmAndamento', 0) / total) * 100)
                
                # Atualiza largura das barras
                if hasattr(self, 'resolved_bar_fill') and self.resolved_bar_fill and self.resolved_bar_fill.winfo_exists():
                    resolved_bar_container = self.resolved_bar_fill.master
                    if resolved_bar_container.winfo_exists() and resolved_bar_container.winfo_width() > 1:
                        resolved_width = int((resolved_pct / 100) * resolved_bar_container.winfo_width())
                        self.resolved_bar_fill.config(width=resolved_width)
                
                if hasattr(self, 'in_progress_bar_fill') and self.in_progress_bar_fill and self.in_progress_bar_fill.winfo_exists():
                    in_progress_bar_container = self.in_progress_bar_fill.master
                    if in_progress_bar_container.winfo_exists() and in_progress_bar_container.winfo_width() > 1:
                        in_progress_width = int((in_progress_pct / 100) * in_progress_bar_container.winfo_width())
                        self.in_progress_bar_fill.config(width=in_progress_width)
                
                if hasattr(self, 'resolved_label') and self.resolved_label and self.resolved_label.winfo_exists():
                    self.resolved_label.config(
                        text=f"Resolvidos: {self.reports.get('chamadosResolvidos', 0)} ({resolved_pct}%)"
                    )
                if hasattr(self, 'in_progress_label') and self.in_progress_label and self.in_progress_label.winfo_exists():
                    self.in_progress_label.config(
                        text=f"Em Andamento: {self.reports.get('chamadosEmAndamento', 0)} ({in_progress_pct}%)"
                    )
            else:
                if hasattr(self, 'resolved_label') and self.resolved_label and self.resolved_label.winfo_exists():
                    self.resolved_label.config(text="Resolvidos: 0 (0%)")
                if hasattr(self, 'in_progress_label') and self.in_progress_label and self.in_progress_label.winfo_exists():
                    self.in_progress_label.config(text="Em Andamento: 0 (0%)")
        except tk.TclError:
            # Widgets foram destruídos
            pass
        
        # Atualiza status da API
        try:
            db_status = self.reports.get('apiStatus', {}).get('database', {})
            db_status_text = db_status.get('status', 'checking')
            db_response_time = db_status.get('responseTime')
            
            status_configs = {
                'online': ('✅', 'Online', '#28a745'),
                'offline': ('❌', 'Offline', '#dc3545'),
                'checking': ('🔄', 'Verificando...', '#ffc107')
            }
            
            icon, text, color = status_configs.get(db_status_text, ('🔄', 'Verificando...', '#ffc107'))
            
            if hasattr(self, 'db_status_icon') and self.db_status_icon and self.db_status_icon.winfo_exists():
                self.db_status_icon.config(text=icon, fg=color)
            if hasattr(self, 'db_status_label') and self.db_status_label and self.db_status_label.winfo_exists():
                self.db_status_label.config(text=text, fg=color)
            
            if hasattr(self, 'db_response_label') and self.db_response_label and self.db_response_label.winfo_exists():
                if db_response_time is not None:
                    self.db_response_label.config(text=f"Tempo de Resposta: {db_response_time}ms")
                else:
                    self.db_response_label.config(text="")
            
            # Atualiza status da API de IA
            ai_status = self.reports.get('apiStatus', {}).get('ai', {})
            ai_status_text = ai_status.get('status', 'checking')
            ai_response_time = ai_status.get('responseTime')
            
            ai_status_configs = {
                'online': ('✅', 'Online', '#28a745'),
                'offline': ('❌', 'Offline', '#dc3545'),
                'checking': ('🔄', 'Verificando...', '#ffc107'),
                'not-implemented': ('🚫', 'Não Implementado', '#6c757d')
            }
            
            ai_icon, ai_text, ai_color = ai_status_configs.get(ai_status_text, ('🔄', 'Verificando...', '#ffc107'))
            
            if hasattr(self, 'ai_status_icon') and self.ai_status_icon and self.ai_status_icon.winfo_exists():
                self.ai_status_icon.config(text=ai_icon, fg=ai_color)
            if hasattr(self, 'ai_status_label') and self.ai_status_label and self.ai_status_label.winfo_exists():
                self.ai_status_label.config(text=ai_text, fg=ai_color)
            
            if hasattr(self, 'ai_response_label') and self.ai_response_label and self.ai_response_label.winfo_exists():
                if ai_response_time is not None:
                    self.ai_response_label.config(text=f"Tempo de Resposta: {ai_response_time}ms")
                elif ai_status_text == 'not-implemented':
                    self.ai_response_label.config(text="Implementação Futura")
                else:
                    self.ai_response_label.config(text="")
        except tk.TclError:
            # Widgets foram destruídos
            pass
