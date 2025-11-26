"""
RegisterEmployeePage - Replica EXATAMENTE RegisterEmployeePage.jsx do web
"""
import tkinter as tk
from pages.base_page import BasePage
from api_client import UserService
from components.toast import show_toast
import re
import threading

class RegisterEmployeePage(BasePage):
    """Página de cadastro de funcionário - layout IDÊNTICO ao web"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, user_info):
        def dummy_navigate(page_id):
            pass
        super().__init__(parent, on_logout, dummy_navigate, 'register', user_info, page_title="CADASTRO DE FUNCIONÁRIO", create_header_sidebar=False)
        
        self.on_navigate_to_home = on_navigate_to_home
        self.is_loading = False
        self.errors = {}
        self.form_data = {
            'nome': '',
            'email': '',
            'cargo': '',
            'senha': '',
            'telefone': '',
            'permissao': 1
        }
        
        self._create_ui()
    
    def _create_ui(self):
        """Cria interface IDÊNTICA ao web"""
        # Container principal com padding de 48px (var(--space-2xl))
        container = tk.Frame(self.main_content, bg="#F8F9FA")
        container.pack(fill=tk.BOTH, expand=True, padx=48, pady=48)
        
        
        # Header do formulário - centralizado, max-width 600px
        header_frame = tk.Frame(container, bg="#F8F9FA")
        header_frame.pack(fill=tk.X, pady=(0, 48))
        
        # Formulário - fundo branco, borda, sombra, padding 48px, max-width 700px, centralizado
        # border: 2px solid #F5F5F5, border-radius: var(--radius-2xl) = 16px
        # box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1)
        form_frame = tk.Frame(container, bg="#FFFFFF", bd=2, relief=tk.SOLID, highlightbackground="#F5F5F5")
        form_frame.pack(fill=tk.X, pady=(0, 24))
        form_frame.config(width=700)
        form_frame.pack_propagate(False)
        
        # Padding interno do formulário (var(--space-2xl) = 48px)
        form_inner = tk.Frame(form_frame, bg="#FFFFFF")
        form_inner.pack(fill=tk.BOTH, expand=True, padx=48, pady=48)
        
        # Campo Permissão (fora do form no web, mas dentro aqui para manter estrutura)
        self._create_select_field(form_inner, "Permissão", "permissao", 
                                  [("1", "Colaborador"), ("2", "Suporte Técnico"), ("3", "Administrador")],
                                  self.form_data['permissao'])
        
        # Campos do formulário - grid de 2 colunas no desktop
        fields_frame = tk.Frame(form_inner, bg="#FFFFFF")
        fields_frame.pack(fill=tk.BOTH, expand=True)
        
        # Grid de 2 colunas
        fields_frame.grid_columnconfigure(0, weight=1, pad=12)
        fields_frame.grid_columnconfigure(1, weight=1, pad=12)
        
        # Nome (coluna 1)
        self._create_text_field(fields_frame, "Nome Completo *", "nome", row=0, col=0, required=True)
        
        # Email (coluna 2)
        self._create_text_field(fields_frame, "E-mail *", "email", row=0, col=1, required=True)
        
        # Cargo (coluna 1)
        self._create_text_field(fields_frame, "Cargo *", "cargo", row=1, col=0, required=True)
        
        # Telefone (coluna 2)
        self._create_text_field(fields_frame, "Telefone", "telefone", row=1, col=1, required=False)
        
        # Senha (ocupa 2 colunas)
        self._create_password_field(fields_frame, "Senha *", "senha", row=2, col=0, colspan=2, required=True)
        
        # Botão submit - largura total, gradiente vermelho
        # width: 100%, padding: var(--space-md) var(--space-lg) = 16px 24px
        # border-radius: var(--radius-lg) = 8px, font-size: var(--font-size-lg) = 18px
        # box-shadow: var(--shadow-md), text-transform: uppercase, letter-spacing: 0.5px
        submit_btn = tk.Button(
            form_inner,
            text="CADASTRAR",
            font=("Inter", 18, "bold"),  # var(--font-size-lg), semibold
            bg="#A93226",
            fg="white",
            activebackground="#8B0000",
            activeforeground="white",
            bd=0,
            relief=tk.FLAT,
            padx=24,  # var(--space-lg)
            pady=16,  # var(--space-md)
            cursor="hand2",
            command=self._handle_submit
        )
        submit_btn.pack(fill=tk.X, pady=(24, 16))  # margin-top: var(--space-lg) = 24px
        
        # Ajuda
        help_label = tk.Label(
            form_inner,
            text="* Campos obrigatórios",
            font=("Inter", 12),
            fg="#666666",
            bg="#FFFFFF"
        )
        help_label.pack()
    
    def _create_text_field(self, parent, label_text, field_name, row, col, required=False, colspan=1):
        """Cria campo de texto com estilo do web"""
        frame = tk.Frame(parent, bg="#FFFFFF")
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=12, pady=(0, 24))
        
        label = tk.Label(
            frame,
            text=label_text,
            font=("Inter", 12, "bold"),
            fg="#333333",
            bg="#FFFFFF",
            anchor="w"
        )
        label.pack(fill=tk.X, pady=(0, 8))
        
        entry = tk.Entry(
            frame,
            font=("Inter", 16),
            bg="#FFFFFF",
            fg="#1A1A1A",
            bd=2,
            relief=tk.SOLID,
            highlightthickness=0,
            insertbackground="#000000"
        )
        entry.pack(fill=tk.X, ipady=16)
        entry.config(highlightbackground="#E5E5E5", highlightcolor="#E5E5E5")
        entry.bind("<KeyRelease>", lambda e: self._validate_field(field_name, entry.get()))
        entry.bind("<FocusIn>", lambda e: entry.config(highlightbackground="#A93226", highlightcolor="#A93226"))
        entry.bind("<FocusOut>", lambda e: entry.config(highlightbackground="#E5E5E5", highlightcolor="#E5E5E5") if field_name not in self.errors else None)
        
        setattr(self, f"{field_name}_entry", entry)
        
        error_label = tk.Label(
            frame,
            text="",
            font=("Inter", 10),
            fg="#DC3545",
            bg="#FFFFFF",
            anchor="w"
        )
        error_label.pack(fill=tk.X, pady=(4, 0))
        setattr(self, f"{field_name}_error", error_label)
    
    def _create_password_field(self, parent, label_text, field_name, row, col, colspan=1, required=False):
        """Cria campo de senha"""
        self._create_text_field(parent, label_text, field_name, row, col, required, colspan)
        entry = getattr(self, f"{field_name}_entry")
        entry.config(show="*")
    
    def _create_select_field(self, parent, label_text, field_name, options, default_value):
        """Cria campo de seleção com estilo do web"""
        frame = tk.Frame(parent, bg="#FFFFFF")
        frame.pack(fill=tk.X, pady=(0, 24))
        
        label = tk.Label(
            frame,
            text=label_text,
            font=("Inter", 12, "bold"),
            fg="#333333",
            bg="#FFFFFF",
            anchor="w"
        )
        label.pack(fill=tk.X, pady=(0, 8))
        
        # Container do select com seta customizada
        select_container = tk.Frame(frame, bg="#FFFFFF")
        select_container.pack(fill=tk.X)
        
        var = tk.StringVar(value=str(default_value))
        var.trace('w', lambda *args: self._update_form_data(field_name, int(var.get())))
        
        option_menu = tk.OptionMenu(select_container, var, *[opt[0] for opt in options],
                                   command=lambda v: self._update_form_data(field_name, int(v)))
        option_menu.config(
            font=("Inter", 16),
            bg="#FFFFFF",
            fg="#1A1A1A",
            activebackground="#F0F0F0",
            activeforeground="#1A1A1A",
            bd=2,
            relief=tk.SOLID,
            highlightthickness=0,
            highlightbackground="#E5E5E5",
            highlightcolor="#E5E5E5",
            padx=16,
            pady=16,
            anchor="w",
            direction="below"
        )
        option_menu.pack(fill=tk.X)
        
        setattr(self, f"{field_name}_var", var)
    
    def _update_form_data(self, field_name, value):
        """Atualiza form_data"""
        self.form_data[field_name] = value
    
    def _validate_field(self, name, value):
        """Valida campo em tempo real"""
        error_msg = ""
        
        if name == 'nome':
            if not value.strip():
                error_msg = 'Nome é obrigatório'
            elif len(value.strip()) < 2:
                error_msg = 'Nome deve ter pelo menos 2 caracteres'
        elif name == 'email':
            email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not value.strip():
                error_msg = 'E-mail é obrigatório'
            elif not re.match(email_regex, value):
                error_msg = 'E-mail inválido'
        elif name == 'senha':
            if not value:
                error_msg = 'Senha é obrigatória'
            elif len(value) < 6:
                error_msg = 'Senha deve ter pelo menos 6 caracteres'
        elif name == 'cargo':
            if not value.strip():
                error_msg = 'Cargo é obrigatório'
        elif name == 'telefone':
            if value and not re.match(r'^[\d\s\-\(\)\+]+$', value):
                error_msg = 'Telefone deve conter apenas números e símbolos válidos'
        
        if name in self.errors:
            if not error_msg:
                del self.errors[name]
        else:
            if error_msg:
                self.errors[name] = error_msg
        
        error_label = getattr(self, f"{name}_error", None)
        if error_label:
            error_label.config(text=error_msg)
        
        entry = getattr(self, f"{name}_entry", None)
        if entry:
            if error_msg:
                entry.config(highlightbackground="#DC3545", highlightcolor="#DC3545")
            else:
                entry.config(highlightbackground="#28A745", highlightcolor="#28A745")
    
    def _handle_submit(self):
        """Processa envio"""
        self.form_data['nome'] = self.nome_entry.get()
        self.form_data['email'] = self.email_entry.get()
        self.form_data['cargo'] = self.cargo_entry.get()
        self.form_data['senha'] = self.senha_entry.get()
        self.form_data['telefone'] = self.telefone_entry.get()
        self.form_data['permissao'] = int(self.permissao_var.get())
        
        for field in ['nome', 'email', 'cargo', 'senha']:
            self._validate_field(field, self.form_data[field])
        
        if self.errors or not all([self.form_data['nome'], self.form_data['email'], 
                                   self.form_data['cargo'], self.form_data['senha']]):
            show_toast(self, 'Por favor, corrija os erros antes de continuar.', 'error')
            return
        
        if self.is_loading:
            return
        
        self.is_loading = True
        threading.Thread(target=self._do_submit, daemon=True).start()
    
    def _do_submit(self):
        """Faz envio"""
        try:
            response = UserService.register(self.form_data)
            if response:
                self.after(0, lambda: show_toast(self, 'Funcionário cadastrado com sucesso!', 'success'))
                self.after(0, self._clear_form)
            else:
                self.after(0, lambda: show_toast(self, 'Erro ao cadastrar funcionário.', 'error'))
        except Exception as e:
            self.after(0, lambda: show_toast(self, f'Erro de conexão: {str(e)}', 'error'))
        finally:
            self.after(0, lambda: setattr(self, 'is_loading', False))
    
    def _clear_form(self):
        """Limpa formulário"""
        self.nome_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.cargo_entry.delete(0, tk.END)
        self.senha_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.permissao_var.set("1")
        self.errors = {}
        for field in ['nome', 'email', 'cargo', 'senha', 'telefone']:
            error_label = getattr(self, f"{field}_error", None)
            if error_label:
                error_label.config(text="")
