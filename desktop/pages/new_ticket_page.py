"""
NewTicketPage - Página de novo chamado
Mesma identidade visual da página de cadastro de funcionários
"""
import customtkinter as ctk
import tkinter as tk
from api_client import TicketService
from components.toast import show_toast
from components.confirm_modal import ConfirmModal
from components.form_validator import FormValidator, validate_required, validate_min_length
from config import COLORS
import threading


class NewTicketPage(ctk.CTkFrame):
    """Página de novo chamado - mesma identidade visual do cadastro de funcionários"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page, user_info):
        super().__init__(parent, fg_color="#F8F9FA")
        
        self.on_logout = on_logout
        self.on_navigate_to_home = on_navigate_to_home
        self.on_navigate_to_page = on_navigate_to_page
        self.user_info = user_info
        
        self.is_loading = False
        self.errors = {}
        self.form_data = {
            'tipoChamado': '',
            'titulo': '',
            'descricao': ''
        }
        
        # Inicializa validador
        self.validator = FormValidator()
        self.validator.add_validator('tipoChamado', validate_required, 'Tipo de chamado é obrigatório')
        self.validator.add_validator('titulo', validate_required, 'Título é obrigatório')
        self.validator.add_validator('titulo', validate_min_length(3), 'Título deve ter pelo menos 3 caracteres')
        self.validator.add_validator('descricao', validate_required, 'Descrição é obrigatória')
        self.validator.add_validator('descricao', validate_min_length(10), 'Descrição deve ter pelo menos 10 caracteres')
        
        self.tipos_chamado = [
            'Suporte',
            'Manutenção',
            'Instalação',
            'Consultoria',
            'Emergência'
        ]
        
        self._create_ui()
    
    def _create_ui(self):
        """Cria interface com mesma identidade visual do cadastro de funcionários"""
        # Container principal com scroll
        self.main_scrollable = ctk.CTkScrollableFrame(
            self,
            fg_color="#F8F9FA",
            corner_radius=0
        )
        self.main_scrollable.pack(fill="both", expand=True)
        self.main_scrollable.grid_columnconfigure(0, weight=1)
        
        # Container interno com padding
        main_container = ctk.CTkFrame(self.main_scrollable, fg_color="#F8F9FA")
        main_container.pack(fill="both", expand=True, padx=48, pady=48)
        main_container.grid_columnconfigure(0, weight=1)
        
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
        back_btn.pack(fill="x", anchor="w", pady=(0, 20))
        
        # === FORMULÁRIO (Card branco) ===
        form_card = ctk.CTkFrame(main_container, fg_color="#FFFFFF", corner_radius=16)
        form_card.pack(fill="both", expand=True)
        form_card.grid_columnconfigure(0, weight=1)
        
        # Padding interno
        form_inner = ctk.CTkFrame(form_card, fg_color="transparent")
        form_inner.pack(fill="both", expand=True, padx=48, pady=48)
        form_inner.grid_columnconfigure(0, weight=1)
        
        # Tipo de chamado
        self._create_tipo_field(form_inner, row=0)
        
        # Título do chamado
        self._create_text_field(form_inner, "Título do Chamado *", "titulo", row=1, max_length=100)
        
        # Descrição
        self._create_textarea_field(form_inner, "Descrição *", "descricao", row=2, max_length=1000, rows=8)
        
        # Botão enviar
        self.submit_btn = ctk.CTkButton(
            form_inner,
            text="ENVIAR",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#A93226",
            hover_color="#8B0000",
            height=50,
            command=self._handle_submit,
            state="normal"
        )
        self.submit_btn.grid(row=3, column=0, sticky="ew", pady=(24, 8))
        
        # Ajuda
        help_label = ctk.CTkLabel(
            form_inner,
            text="* Campos obrigatórios",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        )
        help_label.grid(row=4, column=0, sticky="w")
    
    def _create_tipo_field(self, parent, row):
        """Cria campo de tipo de chamado"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 24))
        frame.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(
            frame,
            text="Tipo de Chamado *",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333",
            anchor="w"
        )
        label.grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        self.tipoChamado_var = tk.StringVar(value="")
        tipo_combo = ctk.CTkComboBox(
            frame,
            values=[""] + self.tipos_chamado,
            variable=self.tipoChamado_var,
            command=self._on_tipo_change,
            font=ctk.CTkFont(size=16),
            height=50,
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
        # Acessibilidade: aria-label
        if hasattr(tipo_combo, 'configure'):
            try:
                tipo_combo.configure(tooltip="Selecione o tipo de chamado")
            except:
                pass
        tipo_combo.grid(row=1, column=0, sticky="ew")
        self.tipoChamado_combo = tipo_combo
        self.tipoChamado_var.trace('w', lambda *args: self._update_form_data('tipoChamado', self.tipoChamado_var.get()))
        
        # Label de erro
        error_label = ctk.CTkLabel(
            frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color="#DC3545",
            anchor="w"
        )
        error_label.grid(row=2, column=0, sticky="w", pady=(4, 0))
        setattr(self, "tipoChamado_error", error_label)
    
    def _on_tipo_change(self, value):
        """Callback quando tipo muda"""
        self.form_data['tipoChamado'] = value
        self._validate_field('tipoChamado', value)
    
    def _create_text_field(self, parent, label_text, field_name, row, max_length=None):
        """Cria campo de texto"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 24))
        frame.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333",
            anchor="w"
        )
        label.grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        entry = ctk.CTkEntry(
            frame,
            placeholder_text="Digite um título descritivo para o chamado" if field_name == 'titulo' else "",
            font=ctk.CTkFont(size=16),
            height=50,
            corner_radius=8,
            fg_color="#FFFFFF",
            text_color="#1A1A1A",
            border_width=2,
            border_color="#E5E5E5"
        )
        # Acessibilidade: aria-label
        if hasattr(entry, 'configure'):
            try:
                entry.configure(tooltip=f"Campo {label_text.lower()}")
            except:
                pass
        entry.grid(row=1, column=0, sticky="ew")
        entry.bind("<FocusIn>", lambda e: entry.configure(border_color="#A93226"))
        entry.bind("<FocusOut>", lambda e: entry.configure(border_color="#E5E5E5") if field_name not in self.errors else None)
        
        setattr(self, f"{field_name}_entry", entry)
        
        # Contador de caracteres
        if max_length:
            count_label = ctk.CTkLabel(
                frame,
                text=f"0/{max_length} caracteres",
                font=ctk.CTkFont(size=11),
                text_color="#666666",
                anchor="e"
            )
            count_label.grid(row=2, column=0, sticky="e", pady=(4, 0))
            
            def update_count(e=None):
                text = entry.get()
                count_label.configure(text=f"{len(text)}/{max_length} caracteres")
                # Também atualiza form_data e valida
                self._on_field_change(field_name, text, max_length)
            
            entry.bind("<KeyRelease>", update_count)
            setattr(self, f"{field_name}_count", count_label)
        else:
            # Se não tem contador, apenas valida
            entry.bind("<KeyRelease>", lambda e: self._on_field_change(field_name, entry.get(), max_length))
        
        # Label de erro
        error_label = ctk.CTkLabel(
            frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color="#DC3545",
            anchor="w"
        )
        error_row = 3 if max_length else 2
        error_label.grid(row=error_row, column=0, sticky="w", pady=(4, 0))
        setattr(self, f"{field_name}_error", error_label)
    
    def _create_textarea_field(self, parent, label_text, field_name, row, max_length=None, rows=8):
        """Cria campo de texto multilinha"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 24))
        frame.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#333333",
            anchor="w"
        )
        label.grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        textarea = ctk.CTkTextbox(
            frame,
            font=ctk.CTkFont(size=16),
            corner_radius=8,
            fg_color="#FFFFFF",
            text_color="#1A1A1A",
            border_width=2,
            border_color="#E5E5E5",
            height=rows * 20,
            wrap="word"
        )
        textarea.grid(row=1, column=0, sticky="ew")
        # Bind será feito no update_count para incluir validação e contador
        textarea.bind("<FocusIn>", lambda e: textarea.configure(border_color="#A93226"))
        textarea.bind("<FocusOut>", lambda e: textarea.configure(border_color="#E5E5E5") if field_name not in self.errors else None)
        
        # Placeholder
        placeholder_text = "Descreva detalhadamente o problema ou solicitação"
        textarea.insert("1.0", placeholder_text)
        textarea.configure(text_color="#666666")
        
        def on_focus_in(e):
            content = textarea.get("1.0", tk.END).strip()
            if content == placeholder_text:
                textarea.delete("1.0", tk.END)
                textarea.configure(text_color="#1A1A1A")
            textarea.configure(border_color="#A93226")
        
        def on_focus_out(e):
            content = textarea.get("1.0", tk.END).strip()
            if not content:
                textarea.insert("1.0", placeholder_text)
                textarea.configure(text_color="#666666")
            if field_name not in self.errors:
                textarea.configure(border_color="#E5E5E5")
        
        textarea.bind("<FocusIn>", on_focus_in)
        textarea.bind("<FocusOut>", on_focus_out)
        
        setattr(self, f"{field_name}_entry", textarea)
        
        # Contador de caracteres
        if max_length:
            count_label = ctk.CTkLabel(
                frame,
                text=f"0/{max_length} caracteres",
                font=ctk.CTkFont(size=11),
                text_color="#666666",
                anchor="e"
            )
            count_label.grid(row=2, column=0, sticky="e", pady=(4, 0))
            
            def update_count(e=None):
                content = textarea.get("1.0", tk.END).strip()
                is_placeholder = content == placeholder_text
                if is_placeholder:
                    content = ""
                count_label.configure(text=f"{len(content)}/{max_length} caracteres")
                # Também atualiza form_data e valida
                self._on_field_change(field_name, content, max_length)
            
            # Remove bind anterior e adiciona novo
            textarea.unbind("<KeyRelease>")
            textarea.bind("<KeyRelease>", update_count)
            setattr(self, f"{field_name}_count", count_label)
        
        # Label de erro
        error_label = ctk.CTkLabel(
            frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color="#DC3545",
            anchor="w"
        )
        error_row = 3 if max_length else 2
        error_label.grid(row=error_row, column=0, sticky="w", pady=(4, 0))
        setattr(self, f"{field_name}_error", error_label)
    
    def _update_form_data(self, field_name, value):
        """Atualiza form_data"""
        self.form_data[field_name] = value
    
    def _on_field_change(self, field_name, value, max_length=None):
        """Callback quando campo muda"""
        self._update_form_data(field_name, value)
        self._validate_field(field_name, value, max_length)
    
    def _validate_field(self, name, value, max_length=None):
        """Valida campo usando FormValidator"""
        # Valida usando o validator
        is_valid = self.validator.validate_field(name, value)
        error_msg = self.validator.get_error(name)
        
        # Validação adicional de comprimento máximo
        if is_valid and max_length and len(value.strip()) > max_length:
            is_valid = False
            error_msg = f'{name.capitalize()} deve ter no máximo {max_length} caracteres'
            self.validator.errors[name] = error_msg
        
        if error_msg:
            self.errors[name] = error_msg
        elif name in self.errors:
            del self.errors[name]
        
        # Atualiza UI
        error_label = getattr(self, f"{name}_error", None)
        if error_label:
            error_label.configure(text=error_msg if error_msg else "")
            # Acessibilidade: aria-describedby
            if hasattr(error_label, 'winfo_name'):
                widget_id = error_label.winfo_name()
        
        # Atualiza borda do campo (indicador visual de válido/inválido)
        if name == 'tipoChamado':
            combo = getattr(self, 'tipoChamado_combo', None)
            if combo:
                if error_msg:
                    combo.configure(border_color="#DC3545")
                elif value and value.strip():
                    combo.configure(border_color="#28a745")
                else:
                    combo.configure(border_color="#E5E5E5")
        elif name in ['titulo', 'descricao']:
            entry = getattr(self, f"{name}_entry", None)
            if entry:
                if error_msg:
                    entry.configure(border_color="#DC3545")
                elif value and value.strip() and not error_msg:
                    entry.configure(border_color="#28a745")
                else:
                    entry.configure(border_color="#E5E5E5")
    
    def _handle_submit(self):
        """Processa envio do formulário"""
        # Coleta dados
        tipo = self.tipoChamado_var.get()
        titulo = self.titulo_entry.get()
        descricao = self.descricao_entry.get("1.0", tk.END).strip()
        
        # Remove placeholder se presente
        placeholder_desc = "Descreva detalhadamente o problema ou solicitação"
        if descricao == placeholder_desc:
            descricao = ""
        
        self.form_data['tipoChamado'] = tipo
        self.form_data['titulo'] = titulo
        self.form_data['descricao'] = descricao
        
        # Valida todos os campos
        self._validate_field('tipoChamado', tipo)
        self._validate_field('titulo', titulo, 100)
        self._validate_field('descricao', descricao, 1000)
        
        # Verifica erros
        if self.errors or not all([tipo, titulo, descricao]):
            show_toast(self, 'Por favor, preencha todos os campos obrigatórios corretamente.', 'error')
            return
        
        if self.is_loading:
            return
        
        # Abre modal de confirmação
        self.confirm_modal = ConfirmModal(
            self,
            title="CONFIRMAR CHAMADO",
            message=f'Tem certeza que deseja enviar o chamado com o título "{titulo}"?',
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
        self.submit_btn.configure(state="disabled", text="ENVIANDO...")
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
                # Redireciona baseado na permissão do usuário
                user_permissao = self.user_info.get('permissao') or self.user_info.get('Permissao', 1)
                # permissao 1 = Colaborador (deve ir para Meus Chamados)
                # permissao 2 = Suporte Técnico, 3 = Administrador (podem ver todos os chamados)
                if user_permissao == 1:
                    self.after(1500, lambda: self.on_navigate_to_page('my-tickets'))
                else:
                    self.after(1500, lambda: self.on_navigate_to_page('pending-tickets'))
            else:
                self.after(0, lambda: show_toast(self, 'Erro ao criar chamado.', 'error'))
        except Exception as e:
            self.after(0, lambda: show_toast(self, f'Erro de conexão: {str(e)}', 'error'))
        finally:
            self.after(0, lambda: setattr(self, 'is_loading', False))
            self.after(0, lambda: self.submit_btn.configure(state="normal", text="ENVIAR"))
    
    def _clear_form(self):
        """Limpa formulário"""
        self.tipoChamado_var.set("")
        self.titulo_entry.delete(0, tk.END)
        self.descricao_entry.delete("1.0", tk.END)
        placeholder_desc = "Descreva detalhadamente o problema ou solicitação"
        self.descricao_entry.insert("1.0", placeholder_desc)
        self.descricao_entry.configure(text_color="#666666")
        self.errors = {}
        # Limpa labels de erro
        for field in ['tipoChamado', 'titulo', 'descricao']:
            error_label = getattr(self, f"{field}_error", None)
            if error_label:
                error_label.configure(text="")
            count_label = getattr(self, f"{field}_count", None)
            if count_label:
                if field == 'titulo':
                    count_label.configure(text="0/100 caracteres")
                elif field == 'descricao':
                    count_label.configure(text="0/1000 caracteres")
