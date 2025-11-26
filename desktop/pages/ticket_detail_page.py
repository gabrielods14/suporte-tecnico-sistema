"""
TicketDetailPage - Replica TicketDetailPage.jsx do web
"""
import tkinter as tk
from pages.base_page import BasePage
from api_client import TicketService, AIService
from components.toast import show_toast
from components.confirm_modal import ConfirmModal
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
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
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
                    TicketService.update_ticket(self.ticket_id, {'status': 2})
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
        desc_frame = tk.Frame(self.inner_content, bg="#F8F9FA")
        desc_frame.pack(fill=tk.X, pady=(0, 24))
        
        tk.Label(desc_frame, text="Descrição do Problema", font=("Inter", 16, "bold"),
                bg="#F8F9FA", fg="#000000", anchor="w").pack(fill=tk.X, pady=(0, 8))
        
        desc_text = tk.Text(desc_frame, font=("Inter", 14), bg="#FFFFFF", fg="#000000",
                           bd=1, relief=tk.SOLID, wrap=tk.WORD, height=6)
        desc_text.insert("1.0", self.ticket.get('descricao', 'N/A'))
        desc_text.config(state=tk.DISABLED)
        desc_text.pack(fill=tk.X)
        
        # Solução (se já existe)
        if self.ticket.get('solucao'):
            sol_frame = tk.Frame(self.inner_content, bg="#F8F9FA")
            sol_frame.pack(fill=tk.X, pady=(0, 24))
            
            tk.Label(sol_frame, text="Solução Registrada", font=("Inter", 16, "bold"),
                    bg="#F8F9FA", fg="#000000", anchor="w").pack(fill=tk.X, pady=(0, 8))
            
            sol_text = tk.Text(sol_frame, font=("Inter", 14), bg="#E8F5E9", fg="#000000",
                              bd=1, relief=tk.SOLID, wrap=tk.WORD, height=6)
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
        
        tk.Label(section_frame, text=title, font=("Inter", 16, "bold"),
                bg="#FFFFFF", fg="#000000", anchor="w").pack(fill=tk.X, padx=24, pady=(24, 16))
        
        for label, value in items:
            item_frame = tk.Frame(section_frame, bg="#FFFFFF")
            item_frame.pack(fill=tk.X, padx=24, pady=8)
            
            tk.Label(item_frame, text=label, font=("Inter", 12, "bold"),
                    bg="#FFFFFF", fg="#666666", width=20, anchor="w").pack(side=tk.LEFT)
            tk.Label(item_frame, text=str(value), font=("Inter", 12),
                    bg="#FFFFFF", fg="#000000", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(section_frame, text="", bg="#FFFFFF", height=1).pack()  # Espaço final
    
    def _create_solution_section(self):
        """Cria seção de solução"""
        section_frame = tk.Frame(self.inner_content, bg="#F8F9FA")
        section_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 24))
        
        # Header com botão de IA
        header_frame = tk.Frame(section_frame, bg="#F8F9FA")
        header_frame.pack(fill=tk.X, pady=(0, 16))
        
        tk.Label(header_frame, text="Registrar Solução", font=("Inter", 18, "bold"),
                bg="#F8F9FA", fg="#262626", anchor="w").pack(side=tk.LEFT)
        
        ai_btn = tk.Button(
            header_frame,
            text="🤖 Gerar Sugestão com IA" if not self.carregando_sugestao else "🔄 Gerando Sugestão...",
            font=("Inter", 14),
            bg="#17A2B8",
            fg="white",
            activebackground="#138496",
            activeforeground="white",
            bd=0,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2" if not self.carregando_sugestao else "wait",
            command=self._handle_gerar_sugestao,
            state=tk.NORMAL if not self.carregando_sugestao else tk.DISABLED
        )
        ai_btn.pack(side=tk.RIGHT)
        self.ai_button = ai_btn
        
        # Caixa de sugestão de IA (inicialmente oculta)
        self.suggestion_box = tk.Frame(section_frame, bg="#E3F2FD", bd=1, relief=tk.SOLID)
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
        
        self.suggestion_text = tk.Text(
            suggestion_inner,
            font=("Inter", 13),
            bg="#FFFFFF",
            fg="#262626",
            bd=0,
            relief=tk.FLAT,
            wrap=tk.WORD,
            height=4
        )
        self.suggestion_text.pack(fill=tk.X)
        self.suggestion_text.config(state=tk.DISABLED)
        
        # Textarea de solução
        self.solution_textarea = tk.Text(
            section_frame,
            font=("Inter", 14),
            bg="#FFFFFF",
            fg="#000000",
            bd=1,
            relief=tk.SOLID,
            wrap=tk.WORD,
            height=8,
            insertbackground="#262626"
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
        
        # Botão concluir
        conclude_btn = tk.Button(
            section_frame,
            text="Enviar Solução" if not self.saving else "Enviando...",
            font=("Inter", 14, "bold"),
            bg="#28A745",
            fg="white",
            activebackground="#218838",
            activeforeground="white",
            bd=0,
            relief=tk.FLAT,
            padx=40,
            pady=15,
            cursor="hand2" if not self.saving else "wait",
            command=self._handle_send_solution,
            state=tk.NORMAL if not self.saving else tk.DISABLED
        )
        conclude_btn.pack()
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
            self.ai_button.config(text="🔄 Gerando Sugestão...", state=tk.DISABLED)
        threading.Thread(target=self._do_gerar_sugestao, daemon=True).start()
    
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
                self.after(0, lambda: show_toast(self, 'Não foi possível gerar uma sugestão. Tente novamente.', 'error'))
        except Exception as e:
            error_msg = str(e)
            # Não mostra erro se for apenas problema de conexão (já está usando mock)
            if 'connection' not in error_msg.lower() and 'conectar' not in error_msg.lower():
                if 'erro' in error_msg.lower():
                    msg = error_msg
                else:
                    msg = 'Erro ao gerar sugestão. Usando sugestão padrão.'
                self.after(0, lambda: show_toast(self, msg, 'error'))
            # Se for erro de conexão, a sugestão mock já foi retornada, então não mostra erro
        finally:
            self.after(0, lambda: setattr(self, 'carregando_sugestao', False))
            if hasattr(self, 'ai_button'):
                self.after(0, lambda: self.ai_button.config(text="🤖 Gerar Sugestão com IA", state=tk.NORMAL))
    
    def _show_suggestion_box(self):
        """Mostra caixa de sugestão"""
        if hasattr(self, 'suggestion_text') and self.sugestao:
            self.suggestion_text.config(state=tk.NORMAL)
            self.suggestion_text.delete("1.0", tk.END)
            self.suggestion_text.insert("1.0", self.sugestao)
            self.suggestion_text.config(state=tk.DISABLED)
            self.suggestion_box.pack(fill=tk.X, pady=(0, 16))
    
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
            update_data = {
                'solucao': solution,
                'status': 3,  # Fechado (conforme enum StatusChamado na web)
                'tecnicoResponsavelId': self.ticket.get('tecnicoResponsavelId') or (int(self.user_info.get('id', 0)) if self.user_info.get('id') else None),
                'dataFechamento': datetime.now().isoformat()
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
