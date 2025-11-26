"""
NewTicketPage - Replica EXATAMENTE NewTicketPage.jsx do web
"""
import tkinter as tk
from tkinter import ttk
from pages.base_page import BasePage
from api_client import TicketService
from components.toast import show_toast
from components.confirm_modal import ConfirmModal
import threading

class NewTicketPage(BasePage):
    """Página de novo ticket - layout IDÊNTICO ao web"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page, user_info):
        super().__init__(parent, on_logout, on_navigate_to_page, 'newticket', user_info, page_title="NOVO CHAMADO", create_header_sidebar=False)
        
        self.on_navigate_to_home = on_navigate_to_home
        self.is_loading = False
        self.errors = {}
        self.form_data = {
            'tipoChamado': '',
            'titulo': '',
            'descricao': ''
        }
        
        self.tipos_chamado = [
            ('', 'Selecione o tipo de chamado'),
            ('Suporte', 'Suporte'),
            ('Manutenção', 'Manutenção'),
            ('Instalação', 'Instalação'),
            ('Consultoria', 'Consultoria'),
            ('Emergência', 'Emergência')
        ]
        
        self._create_ui()
    
    def _create_ui(self):
        """Cria interface moderna e elegante - estilo web melhorado"""
        # Container principal com scroll
        scroll_container = tk.Frame(self.main_content, bg="#F8F9FA")
        scroll_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para scroll suave
        canvas = tk.Canvas(scroll_container, bg="#F8F9FA", highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F8F9FA")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configurar canvas para atualizar largura do frame interno
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Ajustar largura do frame interno para corresponder ao canvas
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        canvas.bind('<Configure>', configure_scroll_region)
        scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Container principal - padding reduzido apenas nas laterais
        container = tk.Frame(scrollable_frame, bg="#F8F9FA")
        container.pack(fill=tk.BOTH, expand=True, padx=24, pady=32)
        
        # Bind mousewheel para scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        
        # Container do formulário - ocupa toda largura disponível
        form_wrapper = tk.Frame(container, bg="#F8F9FA")
        form_wrapper.pack(fill=tk.BOTH, expand=True)
        form_wrapper.grid_columnconfigure(0, weight=1)
        
        # Formulário branco moderno - ocupa toda largura
        form_frame = tk.Frame(form_wrapper, bg="#FFFFFF", bd=2, relief=tk.SOLID, highlightbackground="#E5E5E5")
        form_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 24))
        
        # Frame interno para padding - reduzido nas laterais
        form_inner = tk.Frame(form_frame, bg="#FFFFFF")
        form_inner.pack(fill=tk.BOTH, expand=True, padx=24, pady=32)
        
        # Frame central para conter o formulário - ocupa toda largura
        form_content = tk.Frame(form_inner, bg="#FFFFFF")
        form_content.pack(fill=tk.BOTH, expand=True)
        
        # Tipo de chamado
        self._create_select_field(form_content, "TIPO DE CHAMADO *", "tipoChamado", 
                                  self.tipos_chamado, row=0)
        
        # Título
        self._create_text_field(form_content, "TÍTULO DO CHAMADO *", "titulo", 
                               row=1, max_length=100)
        
        # Descrição
        self._create_textarea_field(form_content, "DESCRIÇÃO *", "descricao", 
                                   row=2, max_length=1000, rows=8)
        
        # Botão enviar - moderno com hover effect
        submit_btn = tk.Button(
            form_content,
            text="ENVIAR",
            font=("Inter", 18, "bold"),
            bg="#A93226",
            fg="white",
            activebackground="#8B0000",
            activeforeground="white",
            bd=0,
            relief=tk.FLAT,
            padx=24,
            pady=18,
            cursor="hand2",
            command=self._handle_submit
        )
        submit_btn.pack(fill=tk.X, pady=(32, 0))
        
        # Ajuda - centralizado
        help_label = tk.Label(
            form_content,
            text="* Campos obrigatórios",
            font=("Inter", 14),
            fg="#666666",
            bg="#FFFFFF"
        )
        help_label.pack(pady=(16, 0))
        
        # Atualizar scrollregion após todos os widgets serem criados
        def update_scroll():
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
        
        scrollable_frame.after(100, update_scroll)
    
    def _create_select_field(self, parent, label_text, field_name, options, row):
        """Cria campo de seleção moderno com sombras e bordas arredondadas"""
        frame = tk.Frame(parent, bg="#FFFFFF")
        frame.pack(fill=tk.X, pady=(0, 32))
        
        # Label moderno
        label = tk.Label(
            frame,
            text=label_text,
            font=("Inter", 13, "bold"),
            fg="#333333",
            bg="#FFFFFF",
            anchor="w"
        )
        label.pack(fill=tk.X, pady=(0, 12))
        
        # Container do select - simplificado
        select_container = tk.Frame(frame, bg="#FFFFFF")
        select_container.pack(fill=tk.X)
        
        var = tk.StringVar(value=options[0][0] if options else '')
        var.trace('w', lambda *args: self._update_form_data(field_name, var.get()))
        
        # Select com estilo moderno - ocupa toda largura
        option_menu = tk.OptionMenu(select_container, var, *[opt[0] for opt in options],
                                   command=lambda v: self._update_form_data(field_name, v))
        
        # Estilização moderna do select
        option_menu.config(
            font=("Inter", 15),
            bg="#FFFFFF",
            fg="#1A1A1A",
            activebackground="#F0F0F0",
            activeforeground="#1A1A1A",
            bd=2,
            relief=tk.SOLID,
            highlightthickness=1,
            highlightbackground="#E5E5E5",
            highlightcolor="#A93226",
            padx=16,
            pady=14,
            anchor="w",
            cursor="hand2",
            direction="below"  # Abre para baixo
        )
        # Usar pack para garantir que ocupe toda largura
        option_menu.pack(fill=tk.X, expand=True)
        
        # Bind para hover effect
        def on_enter(e):
            option_menu.config(highlightbackground="#A93226")
        def on_leave(e):
            option_menu.config(highlightbackground="#E5E5E5")
        option_menu.bind("<Enter>", on_enter)
        option_menu.bind("<Leave>", on_leave)
        
        setattr(self, f"{field_name}_var", var)
        
        # Mensagem de erro
        error_label = tk.Label(
            frame,
            text="",
            font=("Inter", 12),
            fg="#DC3545",
            bg="#FFFFFF",
            anchor="w"
        )
        error_label.pack(fill=tk.X, pady=(6, 0))
        setattr(self, f"{field_name}_error", error_label)
    
    def _create_text_field(self, parent, label_text, field_name, row, max_length=None):
        """Cria campo de texto moderno com sombras e bordas arredondadas"""
        frame = tk.Frame(parent, bg="#FFFFFF")
        frame.pack(fill=tk.X, pady=(0, 32))
        
        # Label moderno
        label = tk.Label(
            frame,
            text=label_text,
            font=("Inter", 13, "bold"),
            fg="#333333",
            bg="#FFFFFF",
            anchor="w"
        )
        label.pack(fill=tk.X, pady=(0, 12))
        
        # Input moderno com estilo melhorado
        entry = tk.Entry(
            frame,
            font=("Inter", 15),
            bg="#FFFFFF",
            fg="#1A1A1A",
            bd=2,
            relief=tk.SOLID,
            highlightthickness=1,
            insertbackground="#000000",
            highlightbackground="#E5E5E5",
            highlightcolor="#A93226"
        )
        entry.pack(fill=tk.X, ipady=14, padx=0)
        
        # Placeholder (simulado com bind)
        placeholder_text = "Digite um título descritivo para o chamado"
        entry.insert(0, placeholder_text)
        entry.config(fg="#666666")
        
        def on_focus_in(e):
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry.config(fg="#1A1A1A", highlightbackground="#A93226")
            else:
                entry.config(highlightbackground="#A93226")
        
        def on_focus_out(e):
            if not entry.get():
                entry.insert(0, placeholder_text)
                entry.config(fg="#666666", highlightbackground="#E5E5E5")
            else:
                entry.config(highlightbackground="#E5E5E5")
        
        # Hover effect
        def on_enter(e):
            if entry.get() != placeholder_text:
                entry.config(highlightbackground="#A93226")
        def on_leave(e):
            if entry.get() != placeholder_text:
                entry.config(highlightbackground="#E5E5E5")
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry.bind("<Enter>", on_enter)
        entry.bind("<Leave>", on_leave)
        entry.bind("<KeyRelease>", lambda e: self._validate_field(field_name, entry.get(), max_length))
        
        setattr(self, f"{field_name}_entry", entry)
        
        # Contador de caracteres moderno
        if max_length:
            count_label = tk.Label(
                frame,
                text=f"0/{max_length} caracteres",
                font=("Inter", 11),
                fg="#666666",
                bg="#FFFFFF",
                anchor="e"
            )
            count_label.pack(fill=tk.X, pady=(6, 0))
            setattr(self, f"{field_name}_count", count_label)
            
            def update_count(e):
                text = entry.get()
                if text == placeholder_text:
                    text = ""
                count_label.config(text=f"{len(text)}/{max_length} caracteres")
            entry.bind("<KeyRelease>", update_count)
        
        # Mensagem de erro
        error_label = tk.Label(
            frame,
            text="",
            font=("Inter", 12),
            fg="#DC3545",
            bg="#FFFFFF",
            anchor="w"
        )
        error_label.pack(fill=tk.X, pady=(6, 0))
        setattr(self, f"{field_name}_error", error_label)
    
    def _create_textarea_field(self, parent, label_text, field_name, row, max_length=None, rows=8):
        """Cria textarea moderno com sombras e bordas arredondadas"""
        frame = tk.Frame(parent, bg="#FFFFFF")
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 32))
        
        # Label moderno
        label = tk.Label(
            frame,
            text=label_text,
            font=("Inter", 13, "bold"),
            fg="#333333",
            bg="#FFFFFF",
            anchor="w"
        )
        label.pack(fill=tk.X, pady=(0, 12))
        
        # Textarea moderno
        textarea = tk.Text(
            frame,
            font=("Inter", 15),
            bg="#FFFFFF",
            fg="#1A1A1A",
            bd=2,
            relief=tk.SOLID,
            insertbackground="#000000",
            wrap=tk.WORD,
            height=rows,
            highlightthickness=1,
            highlightbackground="#E5E5E5",
            highlightcolor="#A93226"
        )
        textarea.pack(fill=tk.BOTH, expand=True, ipady=14, padx=0)
        
        # Placeholder (simulado)
        placeholder_text = "Descreva detalhadamente o problema ou solicitação"
        textarea.insert("1.0", placeholder_text)
        textarea.config(fg="#666666")
        
        def on_focus_in(e):
            if textarea.get("1.0", tk.END).strip() == placeholder_text:
                textarea.delete("1.0", tk.END)
                textarea.config(fg="#1A1A1A", highlightbackground="#A93226")
            else:
                textarea.config(highlightbackground="#A93226")
        
        def on_focus_out(e):
            if not textarea.get("1.0", tk.END).strip():
                textarea.insert("1.0", placeholder_text)
                textarea.config(fg="#666666", highlightbackground="#E5E5E5")
            else:
                textarea.config(highlightbackground="#E5E5E5")
        
        # Hover effect
        def on_enter(e):
            if textarea.get("1.0", tk.END).strip() != placeholder_text:
                textarea.config(highlightbackground="#A93226")
        def on_leave(e):
            if textarea.get("1.0", tk.END).strip() != placeholder_text:
                textarea.config(highlightbackground="#E5E5E5")
        
        textarea.bind("<FocusIn>", on_focus_in)
        textarea.bind("<FocusOut>", on_focus_out)
        textarea.bind("<Enter>", on_enter)
        textarea.bind("<Leave>", on_leave)
        textarea.bind("<KeyRelease>", lambda e: self._validate_field(field_name, textarea.get("1.0", tk.END).strip(), max_length))
        
        setattr(self, f"{field_name}_entry", textarea)
        
        # Contador de caracteres moderno
        if max_length:
            count_label = tk.Label(
                frame,
                text=f"0/{max_length} caracteres",
                font=("Inter", 11),
                fg="#666666",
                bg="#FFFFFF",
                anchor="e"
            )
            count_label.pack(fill=tk.X, pady=(6, 0))
            setattr(self, f"{field_name}_count", count_label)
            
            def update_count(e):
                content = textarea.get("1.0", tk.END).strip()
                if content == placeholder_text:
                    content = ""
                count_label.config(text=f"{len(content)}/{max_length} caracteres")
            textarea.bind("<KeyRelease>", update_count)
        
        # Mensagem de erro
        error_label = tk.Label(
            frame,
            text="",
            font=("Inter", 12),
            fg="#DC3545",
            bg="#FFFFFF",
            anchor="w"
        )
        error_label.pack(fill=tk.X, pady=(6, 0))
        setattr(self, f"{field_name}_error", error_label)
    
    def _update_form_data(self, field_name, value):
        """Atualiza form_data"""
        self.form_data[field_name] = value
    
    def _validate_field(self, name, value, max_length=None):
        """Valida campo"""
        # Remove placeholder se presente
        if name == 'titulo' and value == "Digite um título descritivo para o chamado":
            value = ""
        elif name == 'descricao' and value == "Descreva detalhadamente o problema ou solicitação":
            value = ""
        
        error_msg = ""
        
        if name == 'tipoChamado':
            if not value.strip():
                error_msg = 'Tipo de chamado é obrigatório'
        elif name == 'titulo':
            if not value.strip():
                error_msg = 'Título é obrigatório'
            elif len(value.strip()) < 5:
                error_msg = 'Título deve ter pelo menos 5 caracteres'
            elif max_length and len(value.strip()) > max_length:
                error_msg = f'Título deve ter no máximo {max_length} caracteres'
        elif name == 'descricao':
            if not value.strip():
                error_msg = 'Descrição é obrigatória'
            elif len(value.strip()) < 10:
                error_msg = 'Descrição deve ter pelo menos 10 caracteres'
            elif max_length and len(value.strip()) > max_length:
                error_msg = f'Descrição deve ter no máximo {max_length} caracteres'
        
        if name in self.errors:
            if not error_msg:
                del self.errors[name]
        else:
            if error_msg:
                self.errors[name] = error_msg
        
        error_label = getattr(self, f"{name}_error", None)
        if error_label:
            error_label.config(text=error_msg)
    
    def _handle_submit(self):
        """Processa envio"""
        # Obtém valores reais (sem placeholder)
        tipo = self.tipoChamado_var.get()
        titulo = self.titulo_entry.get()
        if titulo == "Digite um título descritivo para o chamado":
            titulo = ""
        descricao = self.descricao_entry.get("1.0", tk.END).strip()
        if descricao == "Descreva detalhadamente o problema ou solicitação":
            descricao = ""
        
        self.form_data['tipoChamado'] = tipo
        self.form_data['titulo'] = titulo
        self.form_data['descricao'] = descricao
        
        self._validate_field('tipoChamado', self.form_data['tipoChamado'])
        self._validate_field('titulo', self.form_data['titulo'], 100)
        self._validate_field('descricao', self.form_data['descricao'], 1000)
        
        if self.errors or not all([self.form_data['tipoChamado'], 
                                   self.form_data['titulo'], 
                                   self.form_data['descricao']]):
            show_toast(self, 'Por favor, preencha todos os campos obrigatórios corretamente.', 'error')
            return
        
        if self.is_loading:
            return
        
        # Abre modal de confirmação (igual à versão web)
        ConfirmModal(
            self,
            title="CONFIRMAR CHAMADO",
            message=f'Tem certeza que deseja enviar o chamado com o título "{self.form_data["titulo"]}"?',
            confirm_text="Confirmar",
            cancel_text="Cancelar",
            on_confirm=self._perform_submit,
            on_cancel=lambda: None
        )
    
    def _perform_submit(self):
        """Executa envio após confirmação"""
        if self.is_loading:
            return
        
        self.is_loading = True
        threading.Thread(target=self._do_submit, daemon=True).start()
    
    def _do_submit(self):
        """Faz envio"""
        try:
            solicitante_id = self.user_info.get('id')
            if solicitante_id:
                solicitante_id = int(solicitante_id)
            
            payload = {
                'tipo': self.form_data['tipoChamado'],
                'titulo': self.form_data['titulo'],
                'descricao': self.form_data['descricao'],
                'prioridade': 2,
                'solicitanteId': solicitante_id
            }
            
            response = TicketService.create_ticket(payload)
            
            if response:
                self.after(0, lambda: show_toast(self, 'Chamado criado com sucesso!', 'success'))
                self.after(0, self._clear_form)
                self.after(1500, lambda: self.on_navigate_to_page('pending-tickets'))
            else:
                self.after(0, lambda: show_toast(self, 'Erro ao criar chamado.', 'error'))
        except Exception as e:
            self.after(0, lambda: show_toast(self, f'Erro de conexão: {str(e)}', 'error'))
        finally:
            self.after(0, lambda: setattr(self, 'is_loading', False))
    
    def _clear_form(self):
        """Limpa formulário"""
        self.tipoChamado_var.set('')
        self.titulo_entry.delete(0, tk.END)
        self.titulo_entry.insert(0, "Digite um título descritivo para o chamado")
        self.titulo_entry.config(fg="#666666")
        self.descricao_entry.delete("1.0", tk.END)
        self.descricao_entry.insert("1.0", "Descreva detalhadamente o problema ou solicitação")
        self.descricao_entry.config(fg="#666666")
        self.errors = {}
        for field in ['tipoChamado', 'titulo', 'descricao']:
            error_label = getattr(self, f"{field}_error", None)
            if error_label:
                error_label.config(text="")
            count_label = getattr(self, f"{field}_count", None)
            if count_label:
                if field == 'titulo':
                    count_label.config(text="0/100 caracteres")
                elif field == 'descricao':
                    count_label.config(text="0/1000 caracteres")
