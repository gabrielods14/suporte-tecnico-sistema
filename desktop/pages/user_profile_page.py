"""
UserProfilePage - Replica UserProfilePage.jsx do web
"""
import tkinter as tk
import re
import threading
from pages.base_page import BasePage
from api_client import UserService
from components.toast import show_toast
from components.confirm_modal import ConfirmModal

class UserProfilePage(BasePage):
    """Página de perfil do usuário - replica UserProfilePage.jsx"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page,
                 current_page, user_info, on_navigate_to_profile, on_update_user_info=None):
        super().__init__(parent, on_logout, on_navigate_to_page, current_page, user_info, page_title="MEU PERFIL", create_header_sidebar=False)
        
        self.on_navigate_to_home = on_navigate_to_home
        self.on_update_user_info = on_update_user_info
        
        self.is_editing = False
        self.is_loading = False
        self.errors = {}
        
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
            'cargo': ''
        }
        
        self._create_ui()
        self._load_user_data()
    
    def _create_ui(self):
        """Cria interface igual à versão web"""
        container = tk.Frame(self.main_content, bg="#F8F9FA")
        container.pack(fill=tk.BOTH, expand=True, padx=48, pady=48)
        
        
        # Header
        header_frame = tk.Frame(container, bg="#F8F9FA")
        header_frame.pack(fill=tk.X, pady=(0, 32))
        
        header_label = tk.Label(
            header_frame,
            text="MEU PERFIL",
            font=("Inter", 32, "bold"),
            bg="#F8F9FA",
            fg="#262626"
        )
        header_label.pack(anchor="w")
        
        # Card de perfil
        profile_card = tk.Frame(container, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        profile_card.pack(fill=tk.BOTH, expand=True)
        
        profile_inner = tk.Frame(profile_card, bg="#FFFFFF")
        profile_inner.pack(fill=tk.BOTH, expand=True, padx=48, pady=48)
        
        # Avatar e informações básicas
        avatar_section = tk.Frame(profile_inner, bg="#FFFFFF")
        avatar_section.pack(pady=(0, 32))
        
        # Avatar circular
        avatar_frame = tk.Frame(avatar_section, bg="#A93226", width=80, height=80)
        avatar_frame.pack()
        avatar_frame.pack_propagate(False)
        
        self.avatar_label = tk.Label(
            avatar_frame,
            text="U",
            font=("Inter", 32, "bold"),
            bg="#A93226",
            fg="white"
        )
        self.avatar_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Nome e cargo
        self.name_label = tk.Label(
            avatar_section,
            text="Usuário",
            font=("Inter", 24, "bold"),
            bg="#FFFFFF",
            fg="#262626"
        )
        self.name_label.pack(pady=(16, 8))
        
        self.role_label = tk.Label(
            avatar_section,
            text="Cargo não informado",
            font=("Inter", 16),
            bg="#FFFFFF",
            fg="#737373"
        )
        self.role_label.pack()
        
        # Formulário
        form_frame = tk.Frame(profile_inner, bg="#FFFFFF")
        form_frame.pack(fill=tk.X)
        
        # Nome
        self._create_form_field(form_frame, "Nome Completo *", "nome", field_type="text", row=0)
        
        # Email
        self._create_form_field(form_frame, "E-mail *", "email", field_type="email", row=1)
        
        # Cargo (select)
        self._create_form_field(form_frame, "Cargo *", "cargo", field_type="select", row=2, options=self.cargos_corporativos)
        
        # Telefone
        self._create_form_field(form_frame, "Telefone", "telefone", field_type="text", row=3, required=False)
        
        # Botões de ação
        actions_frame = tk.Frame(profile_inner, bg="#FFFFFF")
        actions_frame.pack(fill=tk.X, pady=(32, 0))
        
        self.edit_btn = tk.Button(
            actions_frame,
            text="EDITAR PERFIL",
            font=("Inter", 14, "bold"),
            bg="#A93226",
            fg="white",
            activebackground="#8B0000",
            activeforeground="white",
            bd=0,
            relief=tk.FLAT,
            padx=32,
            pady=12,
            cursor="hand2",
            command=self._handle_edit
        )
        self.edit_btn.pack(side=tk.LEFT)
        
        self.cancel_btn = tk.Button(
            actions_frame,
            text="CANCELAR",
            font=("Inter", 14, "bold"),
            bg="#6c757d",
            fg="white",
            activebackground="#5a6268",
            activeforeground="white",
            bd=0,
            relief=tk.FLAT,
            padx=32,
            pady=12,
            cursor="hand2",
            command=self._handle_cancel
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=(16, 0))
        self.cancel_btn.pack_forget()
        
        self.save_btn = tk.Button(
            actions_frame,
            text="SALVAR ALTERAÇÕES",
            font=("Inter", 14, "bold"),
            bg="#28a745",
            fg="white",
            activebackground="#218838",
            activeforeground="white",
            bd=0,
            relief=tk.FLAT,
            padx=32,
            pady=12,
            cursor="hand2",
            command=self._handle_submit
        )
        self.save_btn.pack(side=tk.LEFT, padx=(16, 0))
        self.save_btn.pack_forget()
        
        # Guarda referências dos campos
        self.form_fields = {}
        self.form_widgets = {}
    
    def _create_form_field(self, parent, label_text, field_name, field_type="text", row=0, required=True, options=None):
        """Cria um campo do formulário"""
        field_frame = tk.Frame(parent, bg="#FFFFFF")
        field_frame.grid(row=row, column=0, sticky="ew", pady=(0, 24))
        field_frame.grid_columnconfigure(1, weight=1)
        
        # Label
        label = tk.Label(
            field_frame,
            text=label_text,
            font=("Inter", 14, "bold"),
            bg="#FFFFFF",
            fg="#262626",
            anchor="w"
        )
        label.grid(row=0, column=0, sticky="w", padx=(0, 16))
        
        # Campo
        if field_type == "select":
            widget = tk.StringVar(value="")
            select = tk.OptionMenu(field_frame, widget, "", *options)
            select.config(font=("Inter", 14), bg="#FFFFFF", fg="#262626", bd=1, relief=tk.SOLID, 
                         highlightthickness=0, width=30, anchor="w", state="disabled")
            select.grid(row=0, column=1, sticky="ew")
            widget.trace('w', lambda *args, name=field_name: self._on_field_change(name, widget.get()))
        else:
            widget = tk.Entry(
                field_frame,
                font=("Inter", 14),
                bg="#FFFFFF",
                fg="#262626",
                bd=1,
                relief=tk.SOLID,
                highlightthickness=0,
                state="disabled"
            )
            widget.grid(row=0, column=1, sticky="ew", ipady=8)
            widget.bind("<KeyRelease>", lambda e, name=field_name: self._on_field_change(name, widget.get()))
        
        # Mensagem de erro
        error_label = tk.Label(
            field_frame,
            text="",
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#dc3545",
            anchor="w"
        )
        error_label.grid(row=1, column=1, sticky="w", pady=(4, 0))
        
        self.form_fields[field_name] = widget
        self.form_widgets[field_name] = {
            'widget': widget,
            'error_label': error_label,
            'required': required
        }
    
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
                error_label.config(text=self.errors[name], fg="#dc3545")
            else:
                error_label.config(text="")
    
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
                
                self.form_data = {
                    'nome': nome,
                    'email': email,
                    'telefone': telefone,
                    'cargo': cargo
                }
                
                self.after(0, lambda: self._update_ui_with_data())
                
                # Atualiza user_info se houver callback
                if self.on_update_user_info:
                    self.after(0, lambda: self.on_update_user_info({
                        **self.user_info,
                        'nome': nome,
                        'email': email,
                        'telefone': telefone,
                        'cargo': cargo
                    }))
        except Exception as e:
            print(f"Erro ao carregar dados do perfil: {e}")
            # Usa dados do user_info como fallback
            if self.user_info:
                self.form_data = {
                    'nome': self.user_info.get('nome', ''),
                    'email': self.user_info.get('email', ''),
                    'telefone': self.user_info.get('telefone', ''),
                    'cargo': self.user_info.get('cargo', '')
                }
                self.after(0, lambda: self._update_ui_with_data())
        finally:
            self.is_loading = False
    
    def _update_ui_with_data(self):
        """Atualiza UI com os dados carregados"""
        # Atualiza avatar
        first_name = self.form_data.get('nome', 'Usuário').split()[0] if self.form_data.get('nome') else 'U'
        self.avatar_label.config(text=first_name[0].upper())
        
        # Atualiza nome e cargo
        self.name_label.config(text=self.form_data.get('nome', 'Usuário'))
        self.role_label.config(text=self.form_data.get('cargo', 'Cargo não informado'))
        
        # Atualiza campos do formulário
        for field_name, widget in self.form_fields.items():
            if isinstance(widget, tk.StringVar):
                widget.set(self.form_data.get(field_name, ''))
            else:
                widget.delete(0, tk.END)
                widget.insert(0, self.form_data.get(field_name, ''))
    
    def _handle_edit(self):
        """Habilita edição"""
        self.is_editing = True
        self.edit_btn.pack_forget()
        self.cancel_btn.pack(side=tk.LEFT)
        self.save_btn.pack(side=tk.LEFT, padx=(16, 0))
        
        # Habilita campos
        for field_name, widget_info in self.form_widgets.items():
            widget = widget_info['widget']
            if isinstance(widget, tk.StringVar):
                # Para OptionMenu, precisa habilitar de outra forma
                pass
            else:
                widget.config(state="normal")
    
    def _handle_cancel(self):
        """Cancela edição"""
        self.is_editing = False
        self.errors = {}
        self.cancel_btn.pack_forget()
        self.save_btn.pack_forget()
        self.edit_btn.pack(side=tk.LEFT)
        
        # Restaura dados originais
        self._update_ui_with_data()
        
        # Desabilita campos e limpa erros
        for field_name, widget_info in self.form_widgets.items():
            widget = widget_info['widget']
            if isinstance(widget, tk.StringVar):
                pass
            else:
                widget.config(state="disabled")
            widget_info['error_label'].config(text="")
    
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
        ConfirmModal(
            self,
            is_open=True,
            title="Confirmar alterações",
            message="Tem certeza que deseja salvar as alterações do seu perfil?",
            on_confirm=self._perform_save,
            on_cancel=lambda: None
        )
    
    def _perform_save(self):
        """Executa salvamento"""
        self.is_loading = True
        self.save_btn.config(state="disabled", text="SALVANDO...")
        
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
            self.is_loading = False
            self.after(0, lambda: self.save_btn.config(state="normal", text="SALVAR ALTERAÇÕES"))

