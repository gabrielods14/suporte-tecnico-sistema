"""
UserProfilePage - Página de perfil do usuário
Mesma identidade visual das outras páginas modernas
"""
import customtkinter as ctk
import tkinter as tk
import re
import threading
from pages.base_page import BasePage
from api_client import UserService
from components.toast import show_toast
from components.confirm_save_modal import ConfirmSaveModal
from config import COLORS


class UserProfilePage(BasePage):
    """Página de perfil do usuário - mesma identidade visual das outras páginas"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page,
                 current_page, user_info, on_navigate_to_profile, on_update_user_info=None):
        super().__init__(parent, on_logout, on_navigate_to_page, current_page, user_info, page_title="MEU PERFIL", create_header_sidebar=False)
        
        self.on_navigate_to_home = on_navigate_to_home
        self.on_update_user_info = on_update_user_info
        
        self.is_editing = False
        self.is_loading = False
        self.errors = {}
        self.form_fields = {}
        self.form_widgets = {}
        
        # Lista de cargos corporativos pré-definidos (igual à web)
        self.cargos_corporativos = [
            'Diretor', 'Gerente', 'Coordenador', 'Supervisor', 'Analista',
            'Analista de TI', 'Analista de Sistemas', 'Desenvolvedor', 'Técnico',
            'Técnico de TI', 'Suporte Técnico', 'Especialista', 'Consultor',
            'Assistente', 'Assistente Administrativo', 'Auxiliar',
            'Coordenador de TI', 'Gerente de TI', 'Administrador de Sistemas',
            'Analista de Suporte', 'Analista de Negócios', 'Product Owner',
            'Scrum Master', 'Arquiteto de Software', 'DevOps', 'DBA',
            'Analista de Segurança', 'Analista de Qualidade', 'Analista de Dados',
            'Analista de Infraestrutura', 'Coordenador de Projetos',
            'Gerente de Projetos', 'Estagiário', 'Trainee'
        ]
        
        self.form_data = {
            'nome': '',
            'email': '',
            'telefone': '',
            'cargo': '',
            'id': '',
            'permissao': ''
        }
        
        # Inicializa com dados do user_info imediatamente
        self._initialize_with_user_info()
        
        self._create_ui()
        self._load_user_data()
    
    def _create_ui(self):
        """Cria interface com mesma identidade visual das outras páginas"""
        # Container principal com scroll
        self.main_scrollable = ctk.CTkScrollableFrame(
            self.main_content,
            fg_color=COLORS['neutral_50'],
            corner_radius=0
        )
        self.main_scrollable.pack(fill="both", expand=True)
        self.main_scrollable.grid_columnconfigure(0, weight=1)
        
        # Container interno com padding
        main_container = ctk.CTkFrame(self.main_scrollable, fg_color=COLORS['neutral_50'])
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
        
        # === CARD DE PERFIL (Card branco) ===
        profile_card = ctk.CTkFrame(main_container, fg_color="#FFFFFF", corner_radius=16)
        profile_card.pack(fill="both", expand=True)
        profile_card.grid_columnconfigure(0, weight=1)
        
        # Padding interno
        profile_inner = ctk.CTkFrame(profile_card, fg_color="transparent")
        profile_inner.pack(fill="both", expand=True, padx=48, pady=48)
        profile_inner.grid_columnconfigure(0, weight=1)
        
        # === SEÇÃO DE AVATAR E INFORMAÇÕES BÁSICAS ===
        avatar_section = ctk.CTkFrame(profile_inner, fg_color="transparent")
        avatar_section.pack(fill="x", pady=(0, 40))
        
        # Avatar circular vermelho
        avatar_container = ctk.CTkFrame(avatar_section, fg_color="transparent")
        avatar_container.pack()
        
        self.avatar_label = ctk.CTkLabel(
            avatar_container,
            text="U",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color="#FFFFFF",
            fg_color=COLORS['primary'],
            width=120,
            height=120,
            corner_radius=60
        )
        self.avatar_label.pack()
        
        # Nome e cargo
        self.name_label = ctk.CTkLabel(
            avatar_section,
            text="Usuário",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS['text_primary'],
            anchor="center"
        )
        self.name_label.pack(pady=(24, 8))
        
        self.role_label = ctk.CTkLabel(
            avatar_section,
            text="Cargo não informado",
            font=ctk.CTkFont(size=16),
            text_color=COLORS['text_secondary'],
            anchor="center"
        )
        self.role_label.pack()
        
        # === SEÇÃO DE INFORMAÇÕES INFORMATIVAS (somente leitura) ===
        info_section = ctk.CTkFrame(profile_inner, fg_color="#F8F9FA", corner_radius=8)
        info_section.pack(fill="x", pady=(0, 24))
        info_section.grid_columnconfigure(1, weight=1)
        
        # Título da seção
        info_title = ctk.CTkLabel(
            info_section,
            text="Informações do Usuário",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        info_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16, 12))
        
        # ID do Usuário (somente leitura)
        id_label = ctk.CTkLabel(
            info_section,
            text="ID:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        id_label.grid(row=1, column=0, sticky="w", padx=(16, 8), pady=(0, 8))
        
        self.id_value_label = ctk.CTkLabel(
            info_section,
            text="Carregando...",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        self.id_value_label.grid(row=1, column=1, sticky="w", padx=(0, 16), pady=(0, 8))
        
        # Permissão (somente leitura)
        permissao_label = ctk.CTkLabel(
            info_section,
            text="Permissão:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        permissao_label.grid(row=2, column=0, sticky="w", padx=(16, 8), pady=(0, 16))
        
        self.permissao_value_label = ctk.CTkLabel(
            info_section,
            text="Carregando...",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        self.permissao_value_label.grid(row=2, column=1, sticky="w", padx=(0, 16), pady=(0, 16))
        
        # === FORMULÁRIO (campos editáveis) ===
        form_title = ctk.CTkLabel(
            profile_inner,
            text="Dados Pessoais",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        form_title.pack(fill="x", pady=(0, 16))
        
        form_frame = ctk.CTkFrame(profile_inner, fg_color="transparent")
        form_frame.pack(fill="x", pady=(0, 32))
        form_frame.grid_columnconfigure(0, weight=1)
        
        # Nome
        self._create_form_field(form_frame, "Nome Completo *", "nome", field_type="text", row=0)
        
        # Email
        self._create_form_field(form_frame, "E-mail *", "email", field_type="email", row=1)
        
        # Cargo (select)
        self._create_form_field(form_frame, "Cargo *", "cargo", field_type="select", row=2, options=self.cargos_corporativos)
        
        # Telefone
        self._create_form_field(form_frame, "Telefone", "telefone", field_type="text", row=3, required=False)
        
        # Popula campos imediatamente com dados do user_info se disponíveis
        self._update_ui_with_data()
        
        # === BOTÕES DE AÇÃO ===
        actions_frame = ctk.CTkFrame(profile_inner, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(0, 0))
        
        self.edit_btn = ctk.CTkButton(
            actions_frame,
            text="EDITAR PERFIL",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_dark'],
            height=50,
            corner_radius=8,
            command=self._handle_edit
        )
        self.edit_btn.pack(side="left")
        
        self.cancel_btn = ctk.CTkButton(
            actions_frame,
            text="CANCELAR",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#6c757d",
            hover_color="#5a6268",
            height=50,
            corner_radius=8,
            command=self._handle_cancel
        )
        self.cancel_btn.pack(side="left", padx=(16, 0))
        self.cancel_btn.pack_forget()
        
        self.save_btn = ctk.CTkButton(
            actions_frame,
            text="SALVAR ALTERAÇÕES",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#28a745",
            hover_color="#218838",
            height=50,
            corner_radius=8,
            command=self._handle_submit
        )
        self.save_btn.pack(side="left", padx=(16, 0))
        self.save_btn.pack_forget()
    
    def _create_form_field(self, parent, label_text, field_name, field_type="text", row=0, required=True, options=None):
        """Cria um campo do formulário"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.grid(row=row, column=0, sticky="ew", pady=(0, 24))
        field_frame.grid_columnconfigure(0, weight=1)
        
        # Label
        label = ctk.CTkLabel(
            field_frame,
            text=label_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        label.grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        # Inicializa combo como None
        combo = None
        
        # Campo
        if field_type == "select":
            # Obtém valor inicial do form_data se disponível
            initial_value = self.form_data.get(field_name, '')
            widget = tk.StringVar(value=initial_value)
            combo = ctk.CTkComboBox(
                field_frame,
                values=[""] + options,
                variable=widget,
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
                dropdown_hover_color="#F0F0F0",
                state="normal"  # Cria como normal primeiro
            )
            combo.grid(row=1, column=0, sticky="ew")
            # Define o valor inicial
            if initial_value:
                widget.set(initial_value)
            # Agora desabilita
            combo.configure(state="disabled")
            widget.trace('w', lambda *args, name=field_name: self._on_field_change(name, widget.get()))
            self.form_fields[field_name] = widget
        else:
            # Obtém valor inicial do form_data se disponível
            initial_value = self.form_data.get(field_name, '')
            
            widget = ctk.CTkEntry(
                field_frame,
                font=ctk.CTkFont(size=16),
                height=50,
                corner_radius=8,
                fg_color="#FFFFFF",
                text_color="#1A1A1A",
                border_width=2,
                border_color="#E5E5E5",
                state="normal"  # Cria como normal para inserir valor
            )
            widget.grid(row=1, column=0, sticky="ew")
            # Insere valor inicial se houver
            if initial_value:
                widget.insert(0, initial_value)
            # Agora desabilita
            widget.configure(state="disabled")
            widget.bind("<KeyRelease>", lambda e, name=field_name: self._on_field_change(name, widget.get()))
            widget.bind("<FocusIn>", lambda e: widget.configure(border_color=COLORS['primary']))
            widget.bind("<FocusOut>", lambda e, name=field_name: self._handle_focus_out(name, widget))
            self.form_fields[field_name] = widget
        
        # Mensagem de erro
        error_label = ctk.CTkLabel(
            field_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#DC3545",
            anchor="w"
        )
        error_label.grid(row=2, column=0, sticky="w", pady=(4, 0))
        
        # Cria form_widgets
        widget_dict = {
            'widget': widget,
            'error_label': error_label,
            'required': required
        }
        # Se for select (combo), adiciona referência ao combo
        if combo is not None:
            widget_dict['combo'] = combo
        
        self.form_widgets[field_name] = widget_dict
    
    def _handle_focus_out(self, field_name, widget):
        """Lida com perda de foco do campo"""
        if field_name not in self.errors:
            widget.configure(border_color="#E5E5E5")
    
    def _on_field_change(self, field_name, value):
        """Valida campo em tempo real quando editando"""
        if self.is_editing:
            self._validate_field(field_name, value)
            self._update_form_data(field_name, value)
    
    def _update_form_data(self, field_name, value):
        """Atualiza dados do formulário"""
        self.form_data[field_name] = value
    
    def _validate_field(self, name, value):
        """Valida um campo"""
        new_errors = {**self.errors}
        widget_info = self.form_widgets.get(name, {})
        required = widget_info.get('required', True)
        error_label = widget_info.get('error_label')
        
        if name == 'nome':
            if not value.strip():
                new_errors[name] = 'Nome é obrigatório'
            elif len(value.strip()) < 2:
                new_errors[name] = 'Nome deve ter pelo menos 2 caracteres'
            else:
                new_errors.pop(name, None)
        elif name == 'email':
            email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not value.strip():
                new_errors[name] = 'E-mail é obrigatório'
            elif not re.match(email_regex, value):
                new_errors[name] = 'E-mail inválido'
            else:
                new_errors.pop(name, None)
        elif name == 'cargo':
            if not value.strip():
                new_errors[name] = 'Cargo é obrigatório'
            else:
                new_errors.pop(name, None)
        elif name == 'telefone':
            if value and not re.match(r'^[\d\s\-\(\)\+]+$', value):
                new_errors[name] = 'Telefone deve conter apenas números e símbolos válidos'
            else:
                new_errors.pop(name, None)
        
        self.errors = new_errors
        
        # Atualiza label de erro
        if error_label:
            if name in self.errors:
                error_label.configure(text=self.errors[name], text_color="#DC3545")
            else:
                error_label.configure(text="")
        
        # Atualiza borda do campo (indicador visual de válido/inválido)
        widget = widget_info.get('widget')
        if widget:
            if isinstance(widget, tk.StringVar):
                # Para ComboBox, atualiza o widget combobox
                combo = widget_info.get('combo')
                if combo:
                    if name in self.errors:
                        combo.configure(border_color="#DC3545")
                    elif value and value.strip():
                        combo.configure(border_color="#28a745")
                    else:
                        combo.configure(border_color="#E5E5E5")
            else:
                if name in self.errors:
                    widget.configure(border_color="#DC3545")
                elif value and value.strip():
                    widget.configure(border_color="#28a745")
                else:
                    widget.configure(border_color="#E5E5E5")
    
    def _initialize_with_user_info(self):
        """Inicializa form_data com dados do user_info se disponíveis"""
        if self.user_info:
            user_id = self.user_info.get('id') or self.user_info.get('Id') or ''
            permissao = self.user_info.get('permissao') or self.user_info.get('Permissao') or 1
            
            self.form_data = {
                'nome': self.user_info.get('nome', ''),
                'email': self.user_info.get('email', ''),
                'telefone': self.user_info.get('telefone', ''),
                'cargo': self.user_info.get('cargo', ''),
                'id': str(user_id),
                'permissao': str(permissao)
            }
    
    def _load_user_data(self):
        """Carrega dados do usuário"""
        self.is_loading = True
        threading.Thread(target=self._do_load_user_data, daemon=True).start()
    
    def _do_load_user_data(self):
        """Faz carregamento dos dados"""
        try:
            user_data = UserService.get_meu_perfil()
            
            if user_data:
                nome = user_data.get('nome') or user_data.get('Nome') or ''
                email = user_data.get('email') or user_data.get('Email') or ''
                telefone = user_data.get('telefone') or user_data.get('Telefone') or ''
                cargo = user_data.get('cargo') or user_data.get('Cargo') or ''
                
                user_id = user_data.get('id') or user_data.get('Id') or self.user_info.get('id') or self.user_info.get('Id') or ''
                permissao = user_data.get('permissao') or user_data.get('Permissao') or self.user_info.get('permissao') or self.user_info.get('Permissao') or 1
                
                self.form_data = {
                    'nome': nome,
                    'email': email,
                    'telefone': telefone,
                    'cargo': cargo,
                    'id': str(user_id),
                    'permissao': str(permissao)
                }
                
                self.after(0, lambda: self._update_ui_with_data())
                
                # Atualiza user_info se houver callback
                if self.on_update_user_info:
                    self.after(0, lambda: self.on_update_user_info({
                        **self.user_info,
                        'nome': nome,
                        'email': email,
                        'telefone': telefone,
                        'cargo': cargo,
                        'id': user_data.get('id') or user_data.get('Id') or self.user_info.get('id'),
                        'permissao': user_data.get('permissao') or user_data.get('Permissao') or self.user_info.get('permissao')
                    }))
        except Exception as e:
            print(f"Erro ao carregar dados do perfil: {e}")
            # Usa dados do user_info como fallback
            if self.user_info:
                user_id = self.user_info.get('id') or self.user_info.get('Id') or ''
                permissao = self.user_info.get('permissao') or self.user_info.get('Permissao') or 1
                
                self.form_data = {
                    'nome': self.user_info.get('nome', ''),
                    'email': self.user_info.get('email', ''),
                    'telefone': self.user_info.get('telefone', ''),
                    'cargo': self.user_info.get('cargo', ''),
                    'id': str(user_id),
                    'permissao': str(permissao)
                }
                self.after(0, lambda: self._update_ui_with_data())
        finally:
            self.is_loading = False
    
    def _update_ui_with_data(self):
        """Atualiza UI com os dados carregados"""
        # Atualiza avatar
        first_name = self.form_data.get('nome', 'Usuário').split()[0] if self.form_data.get('nome') else 'U'
        self.avatar_label.configure(text=first_name[0].upper())
        
        # Atualiza nome e cargo
        self.name_label.configure(text=self.form_data.get('nome', 'Usuário'))
        self.role_label.configure(text=self.form_data.get('cargo', 'Cargo não informado'))
        
        # Atualiza informações informativas (somente leitura)
        user_id = self.form_data.get('id') or self.user_info.get('id') or self.user_info.get('Id') or 'N/A'
        self.id_value_label.configure(text=str(user_id))
        
        permissao = self.form_data.get('permissao') or self.user_info.get('permissao') or self.user_info.get('Permissao') or 1
        permissao_map = {
            1: 'Colaborador',
            2: 'Suporte Técnico',
            3: 'Administrador'
        }
        permissao_text = permissao_map.get(int(permissao) if str(permissao).isdigit() else 1, 'Desconhecido')
        self.permissao_value_label.configure(text=permissao_text)
        
        # Atualiza campos do formulário
        for field_name, widget in self.form_fields.items():
            if isinstance(widget, tk.StringVar):
                # Para ComboBox, atualiza o StringVar
                widget.set(self.form_data.get(field_name, ''))
            else:
                # Para Entry, remove e insere o valor
                current_state = widget.cget("state")
                # Temporariamente habilita para inserir valor se estiver desabilitado
                if current_state == "disabled":
                    widget.configure(state="normal")
                widget.delete(0, tk.END)
                widget.insert(0, self.form_data.get(field_name, ''))
                # Restaura o estado original
                if current_state == "disabled":
                    widget.configure(state="disabled")
    
    def _handle_edit(self):
        """Habilita edição"""
        self.is_editing = True
        self.edit_btn.pack_forget()
        self.cancel_btn.pack(side="left")
        self.save_btn.pack(side="left", padx=(16, 0))
        
        # Habilita campos
        for field_name, widget_info in self.form_widgets.items():
            widget = widget_info['widget']
            if isinstance(widget, tk.StringVar):
                # Para ComboBox, habilita diretamente
                combo = widget_info.get('combo')
                if combo:
                    combo.configure(state="normal")
            else:
                widget.configure(state="normal")
    
    def _handle_cancel(self):
        """Cancela edição"""
        self.is_editing = False
        self.errors = {}
        
        # Fecha modal de confirmação se estiver aberto
        if hasattr(self, 'confirm_modal') and self.confirm_modal:
            try:
                self.confirm_modal.close()
            except:
                pass
            self.confirm_modal = None
        
        self.cancel_btn.pack_forget()
        self.save_btn.pack_forget()
        self.edit_btn.pack(side="left")
        
        # Restaura dados originais
        self._update_ui_with_data()
        
        # Desabilita campos e limpa erros
        for field_name, widget_info in self.form_widgets.items():
            widget = widget_info['widget']
            error_label = widget_info.get('error_label')
            if isinstance(widget, tk.StringVar):
                # Para ComboBox, desabilita diretamente
                combo = widget_info.get('combo')
                if combo:
                    combo.configure(state="disabled", border_color="#E5E5E5")
            else:
                widget.configure(state="disabled", border_color="#E5E5E5")
            if error_label:
                error_label.configure(text="")
    
    def _handle_submit(self):
        """Salva alterações"""
        # Valida todos os campos
        for field_name, widget_info in self.form_widgets.items():
            widget = widget_info['widget']
            value = widget.get() if isinstance(widget, tk.StringVar) else widget.get()
            self._validate_field(field_name, value)
        
        # Verifica se há erros
        has_errors = len(self.errors) > 0
        has_empty_required = any(
            not (self.form_data.get(name) or '').strip()
            for name, info in self.form_widgets.items()
            if info.get('required', True)
        )
        
        if has_errors or has_empty_required:
            show_toast(self, 'Por favor, corrija os erros antes de salvar.', 'error')
            return
        
        # Abre modal de confirmação
        self.confirm_modal = ConfirmSaveModal(
            self,
            is_open=True,
            title="Confirmar alterações",
            message="Tem certeza que deseja salvar as alterações do seu perfil?",
            on_confirm=self._perform_save,
            on_cancel=lambda: None
        )
    
    def _perform_save(self):
        """Executa salvamento"""
        if self.confirm_modal:
            try:
                self.confirm_modal.close()
            except:
                pass
            self.confirm_modal = None
        
        self.is_loading = True
        self.save_btn.configure(state="disabled", text="SALVANDO...")
        
        threading.Thread(target=self._do_save, daemon=True).start()
    
    def _do_save(self):
        """Faz salvamento"""
        try:
            update_data = {
                'nome': self.form_data['nome'],
                'email': self.form_data['email'],
                'telefone': self.form_data['telefone'],
                'cargo': self.form_data['cargo']
            }
            
            # Verifica se email já existe para outro usuário (igual ao web)
            try:
                all_users_data = UserService.get_users()
                users_array = []
                if isinstance(all_users_data, list):
                    users_array = all_users_data
                elif isinstance(all_users_data, dict):
                    users_array = all_users_data.get('usuarios', []) or all_users_data.get('items', []) or []
                
                email_lower = (update_data.get('email') or '').strip().lower()
                current_user_id = self.user_info.get('id') or self.user_info.get('Id')
                
                exists_other = any(
                    ((u.get('email') or u.get('Email') or '') + '').lower() == email_lower
                    and (current_user_id is None or int(u.get('id') or u.get('Id') or 0)) != int(current_user_id or 0)
                    for u in users_array
                )
                
                if exists_other:
                    self.after(0, lambda: show_toast(self, 'O e-mail informado já existe para outro usuário. Verifique e tente novamente.', 'error'))
                    self.after(0, lambda: setattr(self, 'is_loading', False))
                    self.after(0, lambda: self.save_btn.configure(state="normal", text="SALVAR ALTERAÇÕES"))
                    return
            except Exception as err:
                print(f'[UserProfilePage] Erro ao verificar emails: {err}')
                # Prossegue e confia na validação do backend
            
            result = UserService.update_meu_perfil(update_data)
            
            self.after(0, lambda: show_toast(self, 'Perfil atualizado com sucesso!', 'success'))
            self.after(0, self._handle_cancel)
            
            # Atualiza user_info
            if self.on_update_user_info:
                self.after(0, lambda: self.on_update_user_info({
                    **self.user_info,
                    **update_data
                }))
        except Exception as e:
            error_msg = str(e)
            if 'email' in error_msg.lower():
                self.after(0, lambda: show_toast(self, 'O e-mail informado já existe. Verifique e tente novamente.', 'error'))
            else:
                self.after(0, lambda: show_toast(self, 'Erro ao atualizar perfil. Tente novamente.', 'error'))
        finally:
            self.after(0, lambda: setattr(self, 'is_loading', False))
            self.after(0, lambda: self.save_btn.configure(state="normal", text="SALVAR ALTERAÇÕES"))
