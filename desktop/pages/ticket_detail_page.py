"""
TicketDetailPage - Replica TicketDetailPage.jsx do web
"""
import tkinter as tk
from pages.base_page import BasePage
from api_client import TicketService, AIService
from components.toast import show_toast
from components.confirm_modal import ConfirmModal
from config import COLORS
import customtkinter as ctk
import threading
from datetime import datetime

class TicketDetailPage(BasePage):
    """Página de detalhes do ticket - replica TicketDetailPage.jsx"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page,
                 user_info, ticket_id, previous_page=None):
        # Não cria Header e Sidebar próprios, pois já existem no HomePage
        super().__init__(parent, on_logout, on_navigate_to_page, 'pending-tickets', user_info, page_title="DETALHES DO CHAMADO", create_header_sidebar=False)
        
        self.on_navigate_to_home = on_navigate_to_home
        self.ticket_id = ticket_id
        self.previous_page = previous_page or 'pending-tickets'
        
        self.ticket = None
        self.loading = True
        self.saving = False
        self.solution = ""
        self.sugestao = ""
        self.carregando_sugestao = False
        self.animation_job = None  # Para controlar a animação
        self.confirm_modal = None
        
        self._create_ui()
        if ticket_id:
            self._load_ticket()
    
    def _create_ui(self):
        """Cria a interface"""
        # Frame interno para padding (evita frames aninhados desnecessários)
        self.content_frame = tk.Frame(self.main_content, bg="#F8F9FA")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=48, pady=48)
        
        # Canvas e Scrollbar para permitir scroll do conteúdo
        canvas = tk.Canvas(self.content_frame, bg="#F8F9FA", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F8F9FA")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def on_canvas_configure(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        canvas.bind("<Configure>", on_canvas_configure)
        
        # Habilita scroll do mouse no Canvas (Windows e Mac)
        def on_mousewheel(event):
            # Windows e Mac usam delta, Linux usa Button-4/Button-5
            if event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")
        
        def bind_mousewheel(event):
            # Windows e Mac
            canvas.bind_all("<MouseWheel>", on_mousewheel)
            # Linux
            canvas.bind_all("<Button-4>", on_mousewheel)
            canvas.bind_all("<Button-5>", on_mousewheel)
        
        def unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")
        
        # Bind quando o mouse entra no canvas
        canvas.bind("<Enter>", bind_mousewheel)
        canvas.bind("<Leave>", unbind_mousewheel)
        
        # Também permite scroll quando o mouse está sobre o frame scrollável
        scrollable_frame.bind("<Enter>", bind_mousewheel)
        scrollable_frame.bind("<Leave>", unbind_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botão voltar
        back_frame = tk.Frame(scrollable_frame, bg="#F8F9FA")
        back_frame.pack(fill="x", anchor="w", pady=(0, 20))
        
        def go_back():
            if self.previous_page:
                self.on_navigate_to_page(self.previous_page)
            else:
                self.on_navigate_to_home()
        
        back_btn = ctk.CTkButton(
            back_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color=COLORS['primary'],
            hover_color=COLORS['neutral_100'],
            anchor="w",
            command=go_back
        )
        back_btn.pack(side="left")
        
        # Container de conteúdo interno (será preenchido quando ticket carregar)
        self.inner_content = tk.Frame(scrollable_frame, bg="#F8F9FA")
        self.inner_content.pack(fill=tk.BOTH, expand=True)
    
    def _load_ticket(self):
        """Carrega ticket"""
        self.loading = True
        threading.Thread(target=self._do_load_ticket, daemon=True).start()
    
    def _do_load_ticket(self):
        """Faz carregamento"""
        try:
            ticket_data = TicketService.get_ticket(self.ticket_id)
            
            # Normaliza dados do solicitante e técnico
            solicitante = ticket_data.get('solicitante') or ticket_data.get('Solicitante') or {}
            if not isinstance(solicitante, dict):
                solicitante = {}
            
            tecnico = ticket_data.get('tecnicoResponsavel') or ticket_data.get('TecnicoResponsavel')
            if not isinstance(tecnico, dict):
                tecnico = None
            
            normalized_ticket = {
                **ticket_data,
                'status': int(ticket_data.get('status') or ticket_data.get('Status') or 1),
                'solicitante': {
                    'nome': solicitante.get('nome') or solicitante.get('Nome') or 'N/A',
                    'email': solicitante.get('email') or solicitante.get('Email') or 'N/A',
                    'cargo': solicitante.get('cargo') or solicitante.get('Cargo') or 'N/A',
                    'telefone': solicitante.get('telefone') or solicitante.get('Telefone') or 'N/A'
                },
                'tecnicoResponsavel': tecnico if tecnico else None,
                'titulo': ticket_data.get('titulo') or ticket_data.get('Titulo') or '',
                'descricao': ticket_data.get('descricao') or ticket_data.get('Descricao') or '',
                'tipo': ticket_data.get('tipo') or ticket_data.get('Tipo') or '',
                'prioridade': ticket_data.get('prioridade') or ticket_data.get('Prioridade') or 1,
                'dataAbertura': ticket_data.get('dataAbertura') or ticket_data.get('DataAbertura') or '',
                'dataFechamento': ticket_data.get('dataFechamento') or ticket_data.get('DataFechamento'),
                'solucao': ticket_data.get('solucao') or ticket_data.get('Solucao')
            }
            
            self.ticket = normalized_ticket
            self.solution = ""
            
            # Se o chamado está em status "Aberto" (1) e o usuário é um técnico, muda para "Em Atendimento" (2)
            # IMPORTANTE: Não altera status de chamados já fechados (status 3) ou em atendimento (status 2)
            ticket_status = normalized_ticket['status']
            permissao = self.user_info.get('permissao', 1)
            if ticket_status == 1 and permissao in [2, 3]:
                try:
                    # API .NET: Atribui técnico e atualiza status para EmAtendimento (2)
                    TicketService.update_ticket(self.ticket_id, {
                        'Status': 2,  # EmAtendimento
                        'TecnicoResponsavelId': int(self.user_info.get('id', 0))
                    })
                    self.ticket['status'] = 2
                    print('Chamado atualizado para "Em Atendimento"')
                except Exception as e:
                    print(f'Erro ao atualizar status do chamado: {e}')
            
            # Determina página de retorno baseada no status
            if ticket_status == 3:  # Fechado/Concluído
                self.previous_page = 'completed-tickets'
            else:
                self.previous_page = self.previous_page or 'pending-tickets'
                
        except Exception as e:
            print(f"Erro ao carregar ticket: {e}")
            self.ticket = None
        finally:
            self.loading = False
            self.after(0, self._update_ui)
    
    def _update_ui(self):
        """Atualiza UI com dados do ticket"""
        # Limpa conteúdo anterior (apenas o inner_content, mantém botão voltar)
        for widget in self.inner_content.winfo_children():
            widget.destroy()
        
        if self.loading:
            tk.Label(self.inner_content, text="Carregando detalhes do chamado...",
                    font=("Inter", 14), bg="#F8F9FA", fg="#666666").pack(pady=50)
            return
        
        if not self.ticket:
            tk.Label(self.inner_content, text="Chamado não encontrado.",
                    font=("Inter", 14), bg="#F8F9FA", fg="#DC3545").pack(pady=50)
            return
        
        # Atualiza título no header
        codigo = str(self.ticket.get('id', 0)).zfill(6)
        self.set_header_title(f"DETALHES DO CHAMADO #{codigo}")
        
        # Informações do chamado
        self._create_info_section("Informações do Chamado", [
            ("Título:", self.ticket.get('titulo', 'N/A')),
            ("Tipo:", self.ticket.get('tipo', 'N/A')),
            ("Prioridade:", self._get_priority_badge(self.ticket.get('prioridade'))),
            ("Status:", self._get_status_text(self.ticket.get('status'))),
            ("Data de Abertura:", self._format_date(self.ticket.get('dataAbertura'))),
            ("Data de Fechamento:", self._format_date(self.ticket.get('dataFechamento')))
        ])
        
        # Informações do solicitante
        solicitante = self.ticket.get('solicitante', {})
        if isinstance(solicitante, dict):
            self._create_info_section("Informações do Solicitante", [
                ("Nome:", solicitante.get('nome', 'N/A')),
                ("Email:", solicitante.get('email', 'N/A')),
                ("Cargo:", solicitante.get('cargo', 'N/A')),
                ("Telefone:", solicitante.get('telefone', 'N/A'))
            ])
        
        # Descrição
        desc_frame = tk.Frame(self.inner_content, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        desc_frame.pack(fill=tk.X, pady=(0, 24))
        
        # Título com linha azul
        title_frame = tk.Frame(desc_frame, bg="#FFFFFF")
        title_frame.pack(fill=tk.X, padx=24, pady=(24, 8))
        
        tk.Label(title_frame, text="Descrição do Problema", font=("Inter", 16, "bold"),
                bg="#FFFFFF", fg="#000000", anchor="w").pack(fill=tk.X)
        
        # Linha azul separadora
        separator = tk.Frame(title_frame, bg="#007BFF", height=2)
        separator.pack(fill=tk.X, pady=(8, 0))
        
        # Container para o campo de texto com linha azul vertical
        text_container = tk.Frame(desc_frame, bg="#FFFFFF")
        text_container.pack(fill=tk.X, padx=24, pady=(16, 24))
        
        # Linha azul vertical à esquerda
        left_border = tk.Frame(text_container, bg="#007BFF", width=4)
        left_border.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 0))
        
        # Campo de texto
        desc_text = tk.Text(text_container, font=("Inter", 14), bg="#FFFFFF", fg="#000000",
                           bd=0, relief=tk.FLAT, wrap=tk.WORD, height=6, padx=12, pady=12)
        desc_text.insert("1.0", self.ticket.get('descricao', 'N/A'))
        desc_text.config(state=tk.DISABLED)
        desc_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Força a linha azul a ter a mesma altura do texto
        def update_border_height():
            try:
                text_height = desc_text.winfo_reqheight()
                left_border.config(height=text_height)
            except:
                pass
        
        desc_text.after(100, update_border_height)
        
        # Solução (se já existe)
        if self.ticket.get('solucao'):
            sol_frame = tk.Frame(self.inner_content, bg="#FFFFFF", bd=1, relief=tk.SOLID)
            sol_frame.pack(fill=tk.X, pady=(0, 24))
            
            # Título com linha azul
            title_frame = tk.Frame(sol_frame, bg="#FFFFFF")
            title_frame.pack(fill=tk.X, padx=24, pady=(24, 8))
            
            tk.Label(title_frame, text="Solução Registrada", font=("Inter", 16, "bold"),
                    bg="#FFFFFF", fg="#000000", anchor="w").pack(fill=tk.X)
            
            # Linha azul separadora
            separator = tk.Frame(title_frame, bg="#007BFF", height=2)
            separator.pack(fill=tk.X, pady=(8, 0))
            
            # Container para o campo de texto
            text_container = tk.Frame(sol_frame, bg="#FFFFFF")
            text_container.pack(fill=tk.X, padx=24, pady=(16, 24))
            
            sol_text = tk.Text(text_container, font=("Inter", 14), bg="#E8F5E9", fg="#000000",
                              bd=0, relief=tk.FLAT, wrap=tk.WORD, height=6, padx=12, pady=12)
            sol_text.insert("1.0", self.ticket.get('solucao', ''))
            sol_text.config(state=tk.DISABLED)
            sol_text.pack(fill=tk.X)
        
        # Campo de solução (apenas para técnicos e se não fechado)
        permissao = self.user_info.get('permissao', 1)
        # Aceita tanto número quanto string para permissão
        if isinstance(permissao, str):
            try:
                permissao = int(permissao)
            except:
                permissao = 1
        status = self.ticket.get('status')
        if isinstance(status, str):
            try:
                status = int(status)
            except:
                status = 1
        
        # Debug: verificar permissões e status
        print(f"[DEBUG TicketDetail] Permissão do usuário: {permissao} (tipo: {type(permissao)}), Status do chamado: {status} (tipo: {type(status)})")
        print(f"[DEBUG TicketDetail] user_info completo: {self.user_info}")
        
        # Técnicos (permissão 2) e Administradores (permissão 3) podem atender chamados
        # Apenas não mostra se o chamado já está fechado (status 3)
        if permissao in [2, 3] and status != 3:  # Status 3 = Fechado
            print(f"[DEBUG TicketDetail] ✅ Criando seção de solução...")
            self._create_solution_section()
        else:
            print(f"[DEBUG TicketDetail] ❌ NÃO criando seção de solução - permissao={permissao} (deve ser 2 ou 3), status={status} (deve ser diferente de 3)")
    
    def _create_info_section(self, title, items):
        """Cria seção de informações"""
        section_frame = tk.Frame(self.inner_content, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        section_frame.pack(fill=tk.X, pady=(0, 24))
        
        # Título da seção
        title_frame = tk.Frame(section_frame, bg="#FFFFFF")
        title_frame.pack(fill=tk.X, padx=24, pady=(24, 8))
        
        tk.Label(title_frame, text=title, font=("Inter", 16, "bold"),
                bg="#FFFFFF", fg="#000000", anchor="w").pack(fill=tk.X)
        
        # Linha azul separadora
        separator = tk.Frame(title_frame, bg="#007BFF", height=2)
        separator.pack(fill=tk.X, pady=(8, 0))
        
        # Conteúdo da seção
        content_frame = tk.Frame(section_frame, bg="#FFFFFF")
        content_frame.pack(fill=tk.X, padx=24, pady=(16, 24))
        
        for label, value in items:
            item_frame = tk.Frame(content_frame, bg="#FFFFFF")
            item_frame.pack(fill=tk.X, pady=8)
            
            tk.Label(item_frame, text=label, font=("Inter", 12, "bold"),
                    bg="#FFFFFF", fg="#666666", width=20, anchor="w").pack(side=tk.LEFT)
            
            # Verifica se o valor é um badge (Status ou Prioridade)
            if label in ["Status:", "Prioridade:"]:
                badge_frame = tk.Frame(item_frame, bg="#FFFFFF")
                badge_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                if label == "Status:":
                    # Badge cinza para status
                    status_text = str(value).upper()
                    badge = tk.Label(badge_frame, text=status_text, font=("Inter", 11, "bold"),
                                    bg="#6C757D", fg="#FFFFFF", padx=12, pady=6,
                                    relief=tk.FLAT, bd=0)
                    badge.pack(side=tk.LEFT)
                elif label == "Prioridade:":
                    # Badge amarelo para prioridade
                    priority_text = str(value).upper()
                    badge = tk.Label(badge_frame, text=priority_text, font=("Inter", 11, "bold"),
                                    bg="#FFC107", fg="#000000", padx=12, pady=6,
                                    relief=tk.FLAT, bd=0)
                    badge.pack(side=tk.LEFT)
            else:
                tk.Label(item_frame, text=str(value), font=("Inter", 12),
                        bg="#FFFFFF", fg="#000000", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def _create_solution_section(self):
        """Cria seção de solução"""
        section_frame = tk.Frame(self.inner_content, bg="#FFFFFF", bd=2, relief=tk.SOLID, highlightbackground="#28A745", highlightthickness=2)
        section_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 24))
        
        # Header com título e botão de IA
        header_frame = tk.Frame(section_frame, bg="#FFFFFF")
        header_frame.pack(fill=tk.X, padx=24, pady=(24, 8))
        
        # Título com linha azul
        title_container = tk.Frame(header_frame, bg="#FFFFFF")
        title_container.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(title_container, text="Registrar Solução", font=("Inter", 16, "bold"),
                bg="#FFFFFF", fg="#000000", anchor="w").pack(fill=tk.X)
        
        # Linha azul separadora
        separator = tk.Frame(title_container, bg="#007BFF", height=2)
        separator.pack(fill=tk.X, pady=(8, 0))
        
        # Botão de IA roxo - com largura fixa para evitar mudanças durante animação
        button_text = "🤖 Gerar Sugestão com IA" if not self.carregando_sugestao else "🔄 Gerando Sugestão..."
        ai_btn = tk.Button(
            header_frame,
            text=button_text,
            font=("Inter", 14),
            bg="#6F42C1",
            fg="white",
            activebackground="#5A32A3",
            activeforeground="white",
            disabledforeground="white",  # Mantém texto branco quando desabilitado
            bd=0,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            width=25,  # Largura fixa em caracteres para manter tamanho constante
            cursor="hand2" if not self.carregando_sugestao else "wait",
            command=self._handle_gerar_sugestao,
            state=tk.NORMAL if not self.carregando_sugestao else tk.DISABLED
        )
        ai_btn.pack(side=tk.RIGHT, padx=(16, 0))
        self.ai_button = ai_btn
        
        # Container principal para sugestão e campo de solução
        main_content_frame = tk.Frame(section_frame, bg="#FFFFFF")
        main_content_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=(16, 24))
        
        # Caixa de sugestão de IA (inicialmente oculta, mas posicionada ANTES do campo)
        self.suggestion_box = tk.Frame(main_content_frame, bg="#E3F2FD", bd=1, relief=tk.SOLID)
        self.suggestion_box.pack_forget()
        
        suggestion_inner = tk.Frame(self.suggestion_box, bg="#E3F2FD")
        suggestion_inner.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
        
        suggestion_header = tk.Frame(suggestion_inner, bg="#E3F2FD")
        suggestion_header.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(suggestion_header, text="💡 Sugestão gerada pela IA:", 
                font=("Inter", 14, "bold"), bg="#E3F2FD", fg="#1565C0").pack(side=tk.LEFT)
        
        buttons_frame = tk.Frame(suggestion_header, bg="#E3F2FD")
        buttons_frame.pack(side=tk.RIGHT)
        
        usar_btn = tk.Button(
            buttons_frame,
            text="Usar Sugestão",
            font=("Inter", 12, "bold"),
            bg="#1565C0",
            fg="white",
            activebackground="#0D47A1",
            activeforeground="white",
            bd=0,
            relief=tk.FLAT,
            padx=16,
            pady=8,
            cursor="hand2",
            command=self._handle_usar_sugestao
        )
        usar_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        close_btn = tk.Button(
            buttons_frame,
            text="✕",
            font=("Inter", 14),
            bg="#E3F2FD",
            fg="#1565C0",
            activebackground="#BBDEFB",
            activeforeground="#0D47A1",
            bd=0,
            relief=tk.FLAT,
            padx=8,
            pady=4,
            cursor="hand2",
            command=lambda: self.suggestion_box.pack_forget()
        )
        close_btn.pack(side=tk.LEFT)
        
        # Frame para conter o Text e a Scrollbar
        text_frame = tk.Frame(suggestion_inner, bg="#E3F2FD")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para o texto de sugestão (armazenada como atributo)
        self.suggestion_scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, width=16)
        self.suggestion_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget para sugestão (maior e com scrollbar)
        self.suggestion_text = tk.Text(
            text_frame,
            font=("Inter", 13),
            bg="#FFFFFF",
            fg="#262626",
            bd=1,
            relief=tk.SOLID,
            wrap=tk.WORD,
            height=12,  # Aumentado para 12 linhas (maior área visível)
            yscrollcommand=self.suggestion_scrollbar.set,
            padx=12,
            pady=12
        )
        self.suggestion_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.suggestion_text.config(state=tk.DISABLED)
        
        # Configura a scrollbar para controlar o Text
        self.suggestion_scrollbar.config(command=self.suggestion_text.yview)
        
        # Container para textarea e botão (DEPOIS da sugestão)
        self.content_container = tk.Frame(main_content_frame, bg="#FFFFFF")
        self.content_container.pack(fill=tk.BOTH, expand=True)
        
        # Textarea de solução
        self.solution_textarea = tk.Text(
            self.content_container,
            font=("Inter", 14),
            bg="#FFFFFF",
            fg="#000000",
            bd=1,
            relief=tk.SOLID,
            wrap=tk.WORD,
            height=8,
            insertbackground="#262626",
            padx=12,
            pady=12
        )
        self.solution_textarea.pack(fill=tk.BOTH, expand=True, pady=(0, 16))
        self.solution_textarea.insert("1.0", "Descreva aqui a solução sugerida para o problema. Use o botão acima para gerar uma sugestão com IA...")
        self.solution_textarea.config(fg="#999999")
        
        def on_solution_focus_in(e):
            current = self.solution_textarea.get("1.0", tk.END).strip()
            if current == "Descreva aqui a solução sugerida para o problema. Use o botão acima para gerar uma sugestão com IA...":
                self.solution_textarea.delete("1.0", tk.END)
                self.solution_textarea.config(fg="#262626")
        
        def on_solution_focus_out(e):
            current = self.solution_textarea.get("1.0", tk.END).strip()
            if not current:
                self.solution_textarea.insert("1.0", "Descreva aqui a solução sugerida para o problema. Use o botão acima para gerar uma sugestão com IA...")
                self.solution_textarea.config(fg="#999999")
        
        self.solution_textarea.bind("<FocusIn>", on_solution_focus_in)
        self.solution_textarea.bind("<FocusOut>", on_solution_focus_out)
        self.solution_textarea.bind("<KeyRelease>", lambda e: self._update_solution())
        
        # Container para botão no canto inferior direito
        button_container = tk.Frame(self.content_container, bg="#FFFFFF")
        button_container.pack(fill=tk.X)
        
        # Botão concluir (cinza escuro no canto direito)
        conclude_btn = tk.Button(
            button_container,
            text="Enviar Solução" if not self.saving else "Enviando...",
            font=("Inter", 14, "bold"),
            bg="#495057",
            fg="white",
            activebackground="#343A40",
            activeforeground="white",
            bd=0,
            relief=tk.FLAT,
            padx=40,
            pady=15,
            cursor="hand2" if not self.saving else "wait",
            command=self._handle_send_solution,
            state=tk.NORMAL if not self.saving else tk.DISABLED
        )
        conclude_btn.pack(side=tk.RIGHT)
        self.conclude_button = conclude_btn
    
    def _update_solution(self):
        """Atualiza solução do textarea"""
        current = self.solution_textarea.get("1.0", tk.END).strip()
        if current != "Descreva aqui a solução sugerida para o problema. Use o botão acima para gerar uma sugestão com IA...":
            self.solution = current
    
    def _handle_usar_sugestao(self):
        """Usa a sugestão gerada"""
        if self.sugestao:
            self.solution_textarea.delete("1.0", tk.END)
            self.solution_textarea.insert("1.0", self.sugestao)
            self.solution_textarea.config(fg="#262626")
            self.solution = self.sugestao
            self.suggestion_box.pack_forget()
            show_toast(self, 'Sugestão aplicada ao campo de solução.', 'success')
    
    def _handle_gerar_sugestao(self):
        """Gera sugestão com IA"""
        if not self.ticket or not self.ticket.get('descricao'):
            show_toast(self, 'Não é possível gerar sugestão sem a descrição do problema.', 'error')
            return
        
        if self.carregando_sugestao:
            return
        
        self.carregando_sugestao = True
        if hasattr(self, 'ai_button'):
            self.ai_button.config(text="🔄 Gerando Sugestão", state=tk.DISABLED, fg="white", disabledforeground="white")
        # Inicia animação
        self._start_loading_animation()
        threading.Thread(target=self._do_gerar_sugestao, daemon=True).start()
    
    def _start_loading_animation(self):
        """Inicia animação de loading no botão"""
        if not self.carregando_sugestao or not hasattr(self, 'ai_button'):
            return
        
        # Estados da animação: pontos que aparecem e desaparecem
        # Usa espaços para manter a mesma largura do texto
        animation_states = [
            "🔄 Gerando Sugestão   ",  # 3 espaços
            "🔄 Gerando Sugestão.  ",  # 2 espaços
            "🔄 Gerando Sugestão.. ",  # 1 espaço
            "🔄 Gerando Sugestão..."   # 0 espaços
        ]
        
        # Contador para ciclo da animação
        if not hasattr(self, '_animation_counter'):
            self._animation_counter = 0
        
        # Atualiza o texto do botão
        state_index = self._animation_counter % len(animation_states)
        self.ai_button.config(text=animation_states[state_index], fg="white", disabledforeground="white")
        
        # Incrementa contador
        self._animation_counter += 1
        
        # Agenda próxima atualização (500ms)
        if self.carregando_sugestao:
            self.animation_job = self.after(500, self._start_loading_animation)
    
    def _stop_loading_animation(self):
        """Para a animação de loading"""
        if self.animation_job:
            self.after_cancel(self.animation_job)
            self.animation_job = None
        if hasattr(self, '_animation_counter'):
            self._animation_counter = 0
    
    def _do_gerar_sugestao(self):
        """Faz geração de sugestão"""
        try:
            response = AIService.gerar_sugestao(
                self.ticket.get('titulo', ''),
                self.ticket.get('descricao', '')
            )
            
            if response and response.get('sugestao'):
                self.sugestao = response['sugestao']
                self.after(0, lambda: self._show_suggestion_box())
                self.after(0, lambda: show_toast(self, 'Sugestão gerada com sucesso! Clique em "Usar Sugestão" para aplicá-la.', 'success'))
            else:
                self.after(0, lambda: show_toast(self, 'Não foi possível gerar uma sugestão. A resposta da API não contém sugestão.', 'error'))
        except Exception as e:
            # Log detalhado para debug
            print(f"[AIService] Erro ao gerar sugestão: {e}")
            print(f"[AIService] Tipo do erro: {type(e)}")
            if hasattr(e, 'status_code'):
                print(f"[AIService] Status code: {e.status_code}")
            if hasattr(e, 'data'):
                print(f"[AIService] Dados do erro: {e.data}")
            
            # Extrai mensagem de erro igual ao web TicketDetailPage.jsx (linha 138)
            # error.data?.erro || error.message || 'Erro ao gerar sugestão. Verifique se a API do Gemini está configurada.'
            if hasattr(e, 'data') and e.data:
                error_detail = e.data.get('erro') or e.data.get('message', '')
            else:
                error_detail = ''
            
            # Usa error.message se não tiver error.data.erro
            if not error_detail:
                error_detail = str(e) if hasattr(e, '__str__') else 'Erro desconhecido'
            
            # Fallback para mensagem padrão se ainda estiver vazio
            if not error_detail:
                error_detail = 'Erro ao gerar sugestão. Verifique se a API do Gemini está configurada.'
            
            # Mostra mensagem de erro (igual ao web)
            self.after(0, lambda msg=error_detail: show_toast(self, msg, 'error'))
        finally:
            self.after(0, lambda: setattr(self, 'carregando_sugestao', False))
            self.after(0, self._stop_loading_animation)
            if hasattr(self, 'ai_button'):
                self.after(0, lambda: self.ai_button.config(
                    text="🤖 Gerar Sugestão com IA", 
                    state=tk.NORMAL,
                    fg="white"
                ))
    
    def _show_suggestion_box(self):
        """Mostra caixa de sugestão"""
        if hasattr(self, 'suggestion_text') and self.sugestao:
            self.suggestion_text.config(state=tk.NORMAL)
            self.suggestion_text.delete("1.0", tk.END)
            self.suggestion_text.insert("1.0", self.sugestao)
            self.suggestion_text.config(state=tk.DISABLED)
            # Atualiza a scrollbar após inserir o texto
            self.suggestion_text.update_idletasks()
            # Empacota ANTES do content_container para aparecer antes do campo de descrição
            # Define altura máxima para que a scrollbar apareça quando necessário
            if hasattr(self, 'content_container'):
                self.suggestion_box.pack(fill=tk.BOTH, pady=(0, 16), before=self.content_container)
            else:
                self.suggestion_box.pack(fill=tk.BOTH, pady=(0, 16))
            
            # Força atualização da scrollbar após mostrar a caixa
            self.suggestion_text.see("1.0")
            self.suggestion_text.update_idletasks()
            
            # Atualiza a configuração da scrollbar para garantir que apareça
            if hasattr(self, 'suggestion_scrollbar'):
                # Verifica se o conteúdo excede a altura visível
                line_count = int(self.suggestion_text.index('end-1c').split('.')[0])
                visible_lines = self.suggestion_text['height']
                if line_count > visible_lines:
                    # Força a scrollbar a aparecer
                    self.suggestion_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                else:
                    # Remove a scrollbar se não for necessária (opcional)
                    pass  # Mantém sempre visível para consistência visual
    
    def _handle_send_solution(self):
        """Abre modal de confirmação antes de enviar solução"""
        solution = self.solution_textarea.get("1.0", tk.END).strip()
        
        # Remove placeholder
        if solution == "Descreva aqui a solução sugerida para o problema. Use o botão acima para gerar uma sugestão com IA...":
            solution = ""
        
        if not solution:
            show_toast(self, 'Por favor, descreva a solução antes de enviar.', 'error')
            return
        
        if self.saving:
            return
        
        # Abre modal de confirmação
        self.confirm_modal = ConfirmModal(
            self,
            title="CONFIRMAR ENVIO DA SOLUÇÃO",
            message=f"Tem certeza que deseja enviar esta solução e fechar o chamado?\n\nO chamado será marcado como \"Fechado\" e o usuário receberá a solução sugerida.",
            confirm_text="Confirmar",
            cancel_text="Cancelar",
            on_confirm=lambda: self._on_confirm_solution(solution),
            on_cancel=lambda: setattr(self, 'confirm_modal', None)
        )
    
    def _on_confirm_solution(self, solution):
        """Callback do modal de confirmação"""
        if self.confirm_modal:
            try:
                self.confirm_modal.close()
            except:
                pass
            self.confirm_modal = None
        self._perform_send_solution(solution)
    
    def _perform_send_solution(self, solution):
        """Executa envio da solução"""
        self.saving = True
        if hasattr(self, 'conclude_button'):
            self.conclude_button.config(text="Enviando...", state=tk.DISABLED)
        threading.Thread(target=self._do_send_solution, args=(solution,), daemon=True).start()
    
    def _do_send_solution(self, solution):
        """Faz envio da solução"""
        try:
            # API .NET: Quando tem Solução, fecha automaticamente (status 3 = Fechado)
            update_data = {
                'Solucao': solution,
                'Status': 3,  # Fechado (conforme enum StatusChamado na API .NET)
                'TecnicoResponsavelId': self.ticket.get('tecnicoResponsavelId') or self.ticket.get('TecnicoResponsavelId') or (int(self.user_info.get('id', 0)) if self.user_info.get('id') else None),
                'DataFechamento': datetime.now().isoformat()
            }
            
            TicketService.update_ticket(self.ticket_id, update_data)
            
            self.after(0, lambda: show_toast(self, 'Solução enviada e chamado fechado com sucesso!', 'success'))
            
            # Aguarda um pouco para a toast ser exibida e depois navega
            self.after(1500, lambda: self.on_navigate_to_page('completed-tickets'))
        except Exception as e:
            self.after(0, lambda: show_toast(self, f'Erro ao enviar solução. Tente novamente. {str(e)}', 'error'))
        finally:
            self.after(0, lambda: setattr(self, 'saving', False))
            if hasattr(self, 'conclude_button'):
                self.after(0, lambda: self.conclude_button.config(text="Enviar Solução", state=tk.NORMAL))
    
    def _get_priority_text(self, priority):
        """Obtém texto da prioridade"""
        if isinstance(priority, int):
            return {3: 'ALTA', 2: 'MÉDIA', 1: 'BAIXA'}.get(priority, 'N/A')
        return str(priority) if priority else 'N/A'
    
    def _get_priority_badge(self, priority):
        """Retorna widget de badge de prioridade para exibição na seção de info"""
        # Retorna apenas texto por enquanto, pode ser melhorado depois
        return self._get_priority_text(priority)
    
    def _get_priority_color(self, priority):
        """Retorna cor da prioridade"""
        if isinstance(priority, int):
            return {3: '#dc3545', 2: '#ffc107', 1: '#28a745'}.get(priority, '#6c757d')
        return '#6c757d'
    
    def _get_status_text(self, status):
        """Obtém texto do status"""
        if isinstance(status, int):
            # StatusChamado enum: 1=Aberto, 2=EmAtendimento, 3=Fechado
            return {1: 'ABERTO', 2: 'EM ATENDIMENTO', 3: 'CONCLUÍDO'}.get(status, 'N/A')
        return str(status) if status else 'N/A'
    
    def _format_date(self, date_string):
        """Formata data"""
        if not date_string:
            return 'N/A'
        try:
            date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return date.strftime('%d/%m/%Y %H:%M')
        except:
            return str(date_string)
