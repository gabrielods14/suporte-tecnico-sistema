"""
Página de Cadastro de Funcionário
Baseada no RegisterEmployeePage.jsx do projeto web
"""
import customtkinter as ctk
from api_client import UserService
from components.toast import show_toast
from config import COLORS
import threading
import re


class RegisterEmployeePage(ctk.CTkScrollableFrame):
    """Página para cadastrar novo funcionário"""
    
    def __init__(self, parent, user_info, on_navigate_home):
        super().__init__(parent)
        
        self.user_info = user_info
        self.on_navigate_home = on_navigate_home
        self.is_loading = False
        self.users = []
        self.loading_users = False
        self.search_term = ""
        self.editing_user = None
        self.delete_confirm_user = None
        self.is_loading_edit = False
        self.is_loading_delete = False
        self.edit_modal = None
        self.confirm_edit_modal = None
        self.confirm_delete_modal = None
        self.change_password = False
        self.edit_password = ""
        self.edit_confirm_password = ""
        self.show_edit_password = False
        
        # Configuração
        self.configure(fg_color=COLORS['neutral_50'])
        
        # Container principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Botão voltar
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color=COLORS['primary'],
            hover_color=COLORS['neutral_100'],
            anchor="w",
            command=on_navigate_home
        )
        back_btn.pack(anchor="w", pady=(0, 20))
        
        # Formulário
        form_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=16)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        form_inner = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_inner.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Permissão
        permissao_label = ctk.CTkLabel(
            form_inner,
            text="PERMISSÃO",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        permissao_label.pack(fill="x", pady=(0, 10))
        
        self.permissao_var = ctk.StringVar(value="1")
        permissao_combo = ctk.CTkComboBox(
            form_inner,
            values=["1 - Colaborador", "2 - Suporte Técnico", "3 - Administrador"],
            variable=self.permissao_var,
            font=ctk.CTkFont(size=14),
            height=45,
            dropdown_font=ctk.CTkFont(size=14),
            command=self._on_permissao_change
        )
        permissao_combo.pack(fill="x", pady=(0, 20))
        
        # Nome
        nome_label = ctk.CTkLabel(
            form_inner,
            text="NOME COMPLETO *",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        nome_label.pack(fill="x", pady=(0, 10))
        
        self.nome_entry = ctk.CTkEntry(
            form_inner,
            placeholder_text="Digite o nome completo",
            font=ctk.CTkFont(size=14),
            height=45
        )
        # Acessibilidade: aria-label (via tooltip se disponível)
        try:
            self.nome_entry.configure(tooltip="Campo obrigatório: Nome completo do funcionário")
        except:
            pass
        self.nome_entry.pack(fill="x", pady=(0, 5))
        
        self.nome_error = ctk.CTkLabel(
            form_inner,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['error'],
            anchor="w"
        )
        self.nome_error.pack(fill="x", pady=(0, 20))
        
        # Email
        email_label = ctk.CTkLabel(
            form_inner,
            text="E-MAIL *",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        email_label.pack(fill="x", pady=(0, 10))
        
        self.email_entry = ctk.CTkEntry(
            form_inner,
            placeholder_text="exemplo@helpwave.com",
            font=ctk.CTkFont(size=14),
            height=45
        )
        # Acessibilidade: aria-label
        try:
            self.email_entry.configure(tooltip="Campo obrigatório: Email do funcionário")
        except:
            pass
        self.email_entry.pack(fill="x", pady=(0, 5))
        
        self.email_error = ctk.CTkLabel(
            form_inner,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['error'],
            anchor="w"
        )
        self.email_error.pack(fill="x", pady=(0, 20))
        
        # Cargo
        cargo_label = ctk.CTkLabel(
            form_inner,
            text="CARGO *",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        cargo_label.pack(fill="x", pady=(0, 10))
        
        self.cargo_entry = ctk.CTkEntry(
            form_inner,
            placeholder_text="Ex: Administrador, Gestor, Técnico",
            font=ctk.CTkFont(size=14),
            height=45
        )
        self.cargo_entry.pack(fill="x", pady=(0, 5))
        
        self.cargo_error = ctk.CTkLabel(
            form_inner,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['error'],
            anchor="w"
        )
        self.cargo_error.pack(fill="x", pady=(0, 20))
        
        # Telefone
        telefone_label = ctk.CTkLabel(
            form_inner,
            text="TELEFONE",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        telefone_label.pack(fill="x", pady=(0, 10))
        
        self.telefone_entry = ctk.CTkEntry(
            form_inner,
            placeholder_text="(11) 99999-9999",
            font=ctk.CTkFont(size=14),
            height=45
        )
        self.telefone_entry.pack(fill="x", pady=(0, 5))
        
        self.telefone_error = ctk.CTkLabel(
            form_inner,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['error'],
            anchor="w"
        )
        self.telefone_error.pack(fill="x", pady=(0, 20))
        
        # Senha
        senha_label = ctk.CTkLabel(
            form_inner,
            text="SENHA *",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        senha_label.pack(fill="x", pady=(0, 10))
        
        self.senha_entry = ctk.CTkEntry(
            form_inner,
            placeholder_text="Mínimo 6 caracteres",
            font=ctk.CTkFont(size=14),
            height=45,
            show="*"
        )
        self.senha_entry.pack(fill="x", pady=(0, 5))
        
        self.senha_error = ctk.CTkLabel(
            form_inner,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['error'],
            anchor="w"
        )
        self.senha_error.pack(fill="x", pady=(0, 20))
        
        # Botão cadastrar
        self.submit_btn = ctk.CTkButton(
            form_inner,
            text="CADASTRAR",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_dark'],
            height=50,
            command=self.handle_submit
        )
        self.submit_btn.pack(fill="x", pady=(10, 10))
        
        # Ajuda
        help_label = ctk.CTkLabel(
            form_inner,
            text="* Campos obrigatórios",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_secondary']
        )
        help_label.pack()
        
        # Tabela de usuários abaixo do formulário
        self._create_users_table(main_frame)
        
        # Carrega usuários ao inicializar
        self._load_users()
    
    def _on_permissao_change(self, value):
        """Atualiza permissão quando muda"""
        pass
    
    def validate_form(self):
        """Valida o formulário"""
        errors = {}
        
        nome = self.nome_entry.get().strip()
        if not nome:
            errors['nome'] = "Nome é obrigatório"
        elif len(nome) < 2:
            errors['nome'] = "Nome deve ter pelo menos 2 caracteres"
        
        email = self.email_entry.get().strip()
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not email:
            errors['email'] = "E-mail é obrigatório"
        elif not re.match(email_regex, email):
            errors['email'] = "E-mail inválido"
        
        cargo = self.cargo_entry.get().strip()
        if not cargo:
            errors['cargo'] = "Cargo é obrigatório"
        
        telefone = self.telefone_entry.get().strip()
        if telefone and not re.match(r'^[\d\s\-\(\)\+]+$', telefone):
            errors['telefone'] = "Telefone deve conter apenas números e símbolos válidos"
        
        senha = self.senha_entry.get()
        if not senha:
            errors['senha'] = "Senha é obrigatória"
        elif len(senha) < 6:
            errors['senha'] = "Senha deve ter pelo menos 6 caracteres"
        
        # Atualiza mensagens de erro
        self.nome_error.configure(text=errors.get('nome', ''))
        self.email_error.configure(text=errors.get('email', ''))
        self.cargo_error.configure(text=errors.get('cargo', ''))
        self.telefone_error.configure(text=errors.get('telefone', ''))
        self.senha_error.configure(text=errors.get('senha', ''))
        
        return len(errors) == 0
    
    def handle_submit(self):
        """Processa o envio do formulário"""
        if self.is_loading:
            return
        
        if not self.validate_form():
            show_toast(self, "Por favor, corrija os erros antes de continuar", "error")
            return
        
        self.is_loading = True
        self.submit_btn.configure(text="CADASTRANDO...", state="disabled")
        
        # Coleta dados
        permissao_str = self.permissao_var.get()
        permissao = int(permissao_str.split(' - ')[0])
        
        user_data = {
            'nome': self.nome_entry.get().strip(),
            'email': self.email_entry.get().strip(),
            'cargo': self.cargo_entry.get().strip(),
            'senha': self.senha_entry.get(),
            'telefone': self.telefone_entry.get().strip(),
            'permissao': permissao
        }
        
        # Envia em thread separada
        threading.Thread(target=self._submit_user, args=(user_data,), daemon=True).start()
    
    def _submit_user(self, user_data):
        """Envia o usuário"""
        try:
            response = UserService.register(user_data)
            self.after(0, self._submit_success)
        except Exception as e:
            error_msg = str(e)
            self.after(0, self._submit_error, error_msg)
    
    def _submit_success(self):
        """Callback de sucesso"""
        self.is_loading = False
        self.submit_btn.configure(text="CADASTRAR", state="normal")
        
        # Limpa formulário
        self.nome_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.cargo_entry.delete(0, "end")
        self.telefone_entry.delete(0, "end")
        self.senha_entry.delete(0, "end")
        self.permissao_var.set("1")
        
        self.nome_error.configure(text="")
        self.email_error.configure(text="")
        self.cargo_error.configure(text="")
        self.telefone_error.configure(text="")
        self.senha_error.configure(text="")
        
        show_toast(self, "Funcionário cadastrado com sucesso!", "success")
        
        # Recarrega lista de usuários
        self._load_users()
    
    def _submit_error(self, error_msg):
        """Callback de erro"""
        self.is_loading = False
        self.submit_btn.configure(text="CADASTRAR", state="normal")
        show_toast(self, f"Erro ao cadastrar: {error_msg}", "error")
    
    def _create_users_table(self, parent):
        """Cria a tabela de usuários"""
        # Seção de lista de usuários
        users_section = ctk.CTkFrame(parent, fg_color="white", corner_radius=16)
        users_section.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header da seção
        users_header = ctk.CTkFrame(users_section, fg_color="transparent")
        users_header.pack(fill="x", padx=30, pady=(30, 20))
        
        title_label = ctk.CTkLabel(
            users_header,
            text="LISTA DE USUÁRIOS",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS['text_primary']
        )
        title_label.pack(side="left")
        
        # Campo de busca
        self.search_entry = ctk.CTkEntry(
            users_header,
            placeholder_text="Buscar usuário...",
            font=ctk.CTkFont(size=14),
            height=35,
            width=300
        )
        self.search_entry.pack(side="right")
        self.search_entry.bind("<KeyRelease>", self._on_search_change)
        
        # Frame interno para controlar larguras consistentes
        table_inner = ctk.CTkFrame(users_section, fg_color="transparent")
        table_inner.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Cabeçalho fixo da tabela (fora do scroll)
        self.table_header_frame = ctk.CTkFrame(table_inner, fg_color=COLORS['neutral_100'], corner_radius=8)
        self.table_header_frame.pack(fill="x", pady=(0, 0))
        
        # Define larguras fixas para garantir alinhamento perfeito
        # Usa um frame interno no cabeçalho com larguras fixas
        header_inner = ctk.CTkFrame(self.table_header_frame, fg_color="transparent")
        header_inner.pack(fill="x", padx=0, pady=0)
        
        # Larguras fixas para cada coluna (em pixels)
        col_widths = [250, 300, 200, 150, 120]  # Nome, Email, Cargo, Permissão, Ações
        
        headers = ["Nome", "Email", "Cargo", "Permissão", "Ações"]
        for i, (header, width) in enumerate(zip(headers, col_widths)):
            label = ctk.CTkLabel(
                header_inner,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=COLORS['text_primary'],
                width=width,
                anchor="w" if i < 3 else "center"
            )
            label.grid(row=0, column=i, padx=15, pady=12, sticky="w" if i < 3 else "ew")
        
        # Guarda as larguras para usar nas linhas
        self.column_widths = col_widths
        
        # Container scrollável para o corpo da tabela (sem cabeçalho)
        # Altura mínima para mostrar pelo menos 6 linhas
        # Cada linha tem aproximadamente 60px de altura (com padding e pady=5)
        # 6 linhas = 6 * 60px = 360px, arredondando para 400px
        self.table_container = ctk.CTkScrollableFrame(table_inner, fg_color="transparent")
        self.table_container.pack(fill="both", expand=True, pady=(0, 0))
        
        # Define altura mínima através do configure após criação
        # Altura mínima: 6 linhas * ~60px = 360px, usando 400px para garantir
        def configure_height():
            try:
                # Acessa o canvas interno do CTkScrollableFrame
                canvas = None
                for child in self.table_container.winfo_children():
                    if hasattr(child, 'winfo_class') and 'Canvas' in child.winfo_class():
                        canvas = child
                        break
                
                if canvas:
                    canvas.configure(height=400)
            except Exception as e:
                print(f"Erro ao configurar altura: {e}")
        
        self.after(300, configure_height)
        
        # Label de loading/empty
        self.users_status_label = ctk.CTkLabel(
            self.table_container,
            text="Carregando usuários...",
            font=ctk.CTkFont(size=14),
            text_color=COLORS['text_secondary']
        )
        self.users_status_label.pack(pady=20)
    
    def _on_search_change(self, event=None):
        """Atualiza busca"""
        self.search_term = self.search_entry.get().lower()
        self._update_users_display()
    
    def _load_users(self):
        """Carrega lista de usuários"""
        if self.loading_users:
            return
        
        self.loading_users = True
        
        # Verifica se o label existe antes de configurá-lo
        try:
            if hasattr(self, 'users_status_label') and self.users_status_label.winfo_exists():
                self.users_status_label.configure(text="Carregando usuários...")
            else:
                # Cria o label se não existir
                self.users_status_label = ctk.CTkLabel(
                    self.table_container,
                    text="Carregando usuários...",
                    font=ctk.CTkFont(size=14),
                    text_color=COLORS['text_secondary']
                )
                self.users_status_label.pack(pady=20)
        except:
            # Se houver erro, cria o label
            try:
                self.users_status_label = ctk.CTkLabel(
                    self.table_container,
                    text="Carregando usuários...",
                    font=ctk.CTkFont(size=14),
                    text_color=COLORS['text_secondary']
                )
                self.users_status_label.pack(pady=20)
            except:
                pass
        
        threading.Thread(target=self._do_load_users, daemon=True).start()
    
    def _do_load_users(self):
        """Faz carregamento dos usuários"""
        try:
            response = UserService.get_users()
            
            # Normaliza resposta (pode ser array ou objeto com usuarios/items/users)
            if isinstance(response, list):
                self.users = response
            elif isinstance(response, dict):
                self.users = (
                    response.get('usuarios') or 
                    response.get('items') or 
                    response.get('users') or 
                    []
                )
            else:
                self.users = []
            
            self.after(0, self._update_users_display)
        except Exception as e:
            print(f"Erro ao carregar usuários: {e}")
            self.users = []
            def show_error():
                try:
                    if hasattr(self, 'users_status_label') and self.users_status_label.winfo_exists():
                        self.users_status_label.configure(
                            text="Erro ao carregar usuários.",
                            text_color=COLORS['error']
                        )
                except:
                    pass
            
            self.after(0, show_error)
        finally:
            self.loading_users = False
    
    def _update_users_display(self):
        """Atualiza exibição da tabela"""
        # Limpa tabela anterior (incluindo spacer se existir)
        # Mas preserva o label de status se existir
        status_widget = None
        if hasattr(self, 'users_status_label'):
            try:
                if self.users_status_label.winfo_exists():
                    status_widget = self.users_status_label
            except:
                pass
        
        for widget in self.table_container.winfo_children():
            if widget != status_widget:
                try:
                    widget.destroy()
                except:
                    pass
        
        # Filtra usuários
        filtered = self._filter_users()
        
        if not filtered:
            # Remove label de status se existir
            if status_widget:
                try:
                    status_widget.destroy()
                except:
                    pass
            
            empty_label = ctk.CTkLabel(
                self.table_container,
                text="Nenhum usuário encontrado",
                font=ctk.CTkFont(size=14),
                text_color=COLORS['text_secondary']
            )
            empty_label.pack(pady=20)
            return
        
        # Remove label de status se existir (já que vamos mostrar a tabela)
        if status_widget:
            try:
                status_widget.destroy()
            except:
                pass
        
        # Linhas da tabela
        for user in filtered:
            self._create_user_row(user)
        
        # Remove qualquer spacer anterior (não queremos espaço extra)
        if hasattr(self, 'table_spacer'):
            try:
                self.table_spacer.destroy()
                delattr(self, 'table_spacer')
            except:
                pass
    
    def _filter_users(self):
        """Filtra usuários por termo de busca"""
        if not self.search_term:
            return self.users
        
        search = self.search_term.lower()
        filtered = []
        for user in self.users:
            nome = (user.get('nome') or user.get('Nome') or '').lower()
            email = (user.get('email') or user.get('Email') or '').lower()
            cargo = (user.get('cargo') or user.get('Cargo') or '').lower()
            
            if search in nome or search in email or search in cargo:
                filtered.append(user)
        
        return filtered
    
    def _get_permission_label(self, permissao):
        """Retorna label da permissão"""
        permissao = int(permissao) if permissao else 1
        labels = {1: 'Colaborador', 2: 'Suporte Técnico', 3: 'Administrador'}
        return labels.get(permissao, 'Desconhecido')
    
    def _get_permission_color(self, permissao):
        """Retorna cor da permissão"""
        permissao = int(permissao) if permissao else 1
        colors = {1: '#4299e1', 2: '#f6ad55', 3: '#48bb78'}
        return colors.get(permissao, '#6c757d')
    
    def _create_user_row(self, user):
        """Cria uma linha da tabela para um usuário"""
        row_frame = ctk.CTkFrame(self.table_container, fg_color="white", corner_radius=8)
        row_frame.pack(fill="x", pady=5)
        
        # Frame interno com larguras fixas (mesmas do cabeçalho)
        row_inner = ctk.CTkFrame(row_frame, fg_color="transparent")
        row_inner.pack(fill="x", padx=0, pady=0)
        
        # Usa as mesmas larguras do cabeçalho
        col_widths = getattr(self, 'column_widths', [250, 300, 200, 150, 120])
        
        # Nome
        nome = user.get('nome') or user.get('Nome') or 'N/A'
        nome_label = ctk.CTkLabel(
            row_inner,
            text=nome,
            font=ctk.CTkFont(size=13),
            text_color=COLORS['text_primary'],
            anchor="w",
            width=col_widths[0]
        )
        nome_label.grid(row=0, column=0, padx=15, pady=12, sticky="w")
        
        # Email
        email = user.get('email') or user.get('Email') or 'N/A'
        email_label = ctk.CTkLabel(
            row_inner,
            text=email,
            font=ctk.CTkFont(size=13),
            text_color=COLORS['text_primary'],
            anchor="w",
            width=col_widths[1]
        )
        email_label.grid(row=0, column=1, padx=15, pady=12, sticky="w")
        
        # Cargo
        cargo = user.get('cargo') or user.get('Cargo') or 'N/A'
        cargo_label = ctk.CTkLabel(
            row_inner,
            text=cargo,
            font=ctk.CTkFont(size=13),
            text_color=COLORS['text_primary'],
            anchor="w",
            width=col_widths[2]
        )
        cargo_label.grid(row=0, column=2, padx=15, pady=12, sticky="w")
        
        # Permissão
        permissao = user.get('permissao') or user.get('Permissao') or 1
        permissao_label = ctk.CTkLabel(
            row_inner,
            text=self._get_permission_label(permissao),
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="white",
            fg_color=self._get_permission_color(permissao),
            corner_radius=12,
            height=24,
            padx=12,
            width=col_widths[3]
        )
        permissao_label.grid(row=0, column=3, padx=15, pady=12, sticky="ew")
        
        # Ações
        actions_frame = ctk.CTkFrame(row_inner, fg_color="transparent", width=col_widths[4])
        actions_frame.grid(row=0, column=4, padx=15, pady=12, sticky="ew")
        actions_frame.grid_propagate(False)
        
        # Botão editar (por enquanto apenas placeholder)
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="👁️",
            font=ctk.CTkFont(size=14),
            width=35,
            height=30,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_dark'],
            command=lambda u=user: self._handle_edit_user(u)
        )
        edit_btn.pack(side="left", padx=3)
        
        # Botão excluir
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            font=ctk.CTkFont(size=14),
            width=35,
            height=30,
            fg_color="#DC3545",
            hover_color="#C82333",
            command=lambda u=user: self._handle_delete_user(u)
        )
        delete_btn.pack(side="left", padx=3)
    
    def _handle_edit_user(self, user):
        """Lida com edição de usuário - igual ao web"""
        self.editing_user = {
            'id': user.get('id') or user.get('Id'),
            'nome': user.get('nome') or user.get('Nome') or '',
            'email': user.get('email') or user.get('Email') or '',
            'cargo': user.get('cargo') or user.get('Cargo') or '',
            'telefone': user.get('telefone') or user.get('Telefone') or '',
            'permissao': user.get('permissao') or user.get('Permissao') or 1
        }
        self.change_password = False
        self.edit_password = ''
        self.edit_confirm_password = ''
        self.show_edit_password = False
        self._show_edit_modal()
    
    def _handle_delete_user(self, user):
        """Lida com exclusão de usuário - igual ao web"""
        self.delete_confirm_user = user
        self._show_delete_confirm_modal()
    
    def _show_edit_modal(self):
        """Mostra modal de edição de usuário"""
        from components.edit_user_modal import EditUserModal
        
        if self.edit_modal:
            try:
                self.edit_modal.close()
            except:
                pass
        
        # Cria função wrapper para atualizar dados quando modal fechar
        def on_save_wrapper():
            # Os dados já foram atualizados no modal
            self._handle_save_edit()
        
        self.edit_modal = EditUserModal(
            self,
            user=self.editing_user,
            on_save=on_save_wrapper,
            on_cancel=self._handle_close_edit_modal,
            on_change_password_toggle=self._on_change_password_toggle,
            change_password=self.change_password,
            edit_password=self.edit_password,
            edit_confirm_password=self.edit_confirm_password,
            show_password=self.show_edit_password,
            on_password_change=self._on_edit_password_change,
            on_confirm_password_change=self._on_edit_confirm_password_change,
            on_toggle_show_password=self._on_toggle_show_edit_password
        )
    
    def _handle_close_edit_modal(self):
        """Fecha modal de edição"""
        if self.edit_modal:
            try:
                self.edit_modal.close()
            except:
                pass
            self.edit_modal = None
        self.editing_user = None
        self.change_password = False
        self.edit_password = ''
        self.edit_confirm_password = ''
        self.show_edit_password = False
    
    def _on_change_password_toggle(self, value):
        """Callback quando checkbox de alterar senha muda"""
        self.change_password = value
        if not value:
            self.edit_password = ''
            self.edit_confirm_password = ''
    
    def _on_edit_password_change(self, value):
        """Callback quando senha de edição muda"""
        self.edit_password = value
    
    def _on_edit_confirm_password_change(self, value):
        """Callback quando confirmação de senha muda"""
        self.edit_confirm_password = value
    
    def _on_toggle_show_edit_password(self):
        """Alterna mostrar/ocultar senha"""
        self.show_edit_password = not self.show_edit_password
    
    def _handle_save_edit(self):
        """Valida e salva edição - igual ao web"""
        if not self.editing_user:
            return
        
        # Validação básica
        if not self.editing_user.get('nome', '').strip() or \
           not self.editing_user.get('email', '').strip() or \
           not self.editing_user.get('cargo', '').strip():
            show_toast(self, 'Por favor, preencha todos os campos obrigatórios.', 'error')
            return
        
        # Validação de email
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, self.editing_user.get('email', '')):
            show_toast(self, 'E-mail inválido.', 'error')
            return
        
        # Validação de senha se a opção de alterar senha estiver marcada
        if self.change_password:
            if not self.edit_password.strip():
                show_toast(self, 'Por favor, preencha a nova senha.', 'error')
                return
            if len(self.edit_password) < 6:
                show_toast(self, 'A senha deve ter pelo menos 6 caracteres.', 'error')
                return
            if self.edit_password != self.edit_confirm_password:
                show_toast(self, 'As senhas não conferem.', 'error')
                return
        
        # Abre modal de confirmação
        self._show_confirm_edit_modal()
    
    def _show_confirm_edit_modal(self):
        """Mostra modal de confirmação de edição"""
        from components.confirm_modal import ConfirmModal
        
        if self.confirm_edit_modal:
            try:
                self.confirm_edit_modal.close()
            except:
                pass
        
        self.confirm_edit_modal = ConfirmModal(
            self,
            title="CONFIRMAR EDIÇÃO",
            message=f"Tem certeza que deseja salvar as alterações no usuário {self.editing_user.get('nome', '')}?",
            confirm_text="Salvar",
            cancel_text="Cancelar",
            on_confirm=self._handle_confirm_save_edit,
            on_cancel=lambda: self._close_confirm_edit_modal(),
            is_dangerous=False,
            is_loading=self.is_loading_edit
        )
    
    def _close_confirm_edit_modal(self):
        """Fecha modal de confirmação de edição"""
        if self.confirm_edit_modal:
            try:
                self.confirm_edit_modal.close()
            except:
                pass
            self.confirm_edit_modal = None
    
    def _handle_confirm_save_edit(self):
        """Confirma e salva edição - igual ao web"""
        if not self.editing_user:
            return
        
        self._close_confirm_edit_modal()
        # Não fecha o modal de edição aqui, apenas quando salvar com sucesso
        self.is_loading_edit = True
        
        threading.Thread(target=self._do_save_edit, daemon=True).start()
    
    def _do_save_edit(self):
        """Executa salvamento da edição"""
        try:
            user_id = self.editing_user.get('id')
            update_data = {
                'Nome': self.editing_user.get('nome', '').strip(),
                'Email': self.editing_user.get('email', '').strip(),
                'Cargo': self.editing_user.get('cargo', '').strip(),
                'Telefone': self.editing_user.get('telefone', '').strip() or None,
                'Permissao': self.editing_user.get('permissao', 1)
            }
            
            # Adiciona NovaSenha apenas se a opção de alterar senha estiver marcada
            if self.change_password and self.edit_password.strip():
                update_data['NovaSenha'] = self.edit_password.strip()
            
            UserService.update_user(user_id, update_data)
            
            self.after(0, lambda: show_toast(self, 'Usuário atualizado com sucesso!', 'success'))
            self.after(0, self._load_users)
            self.after(0, self._handle_close_edit_modal)
            self.after(0, self._reset_edit_state)
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'data') and e.data:
                error_msg = e.data.get('message', error_msg)
            self.after(0, lambda msg=error_msg: show_toast(self, f'Erro ao atualizar usuário: {msg}', 'error'))
            # Reabre o modal em caso de erro
            self.after(0, self._show_edit_modal)
        finally:
            self.after(0, lambda: setattr(self, 'is_loading_edit', False))
    
    def _reset_edit_state(self):
        """Reseta estado de edição"""
        self.editing_user = None
        self.change_password = False
        self.edit_password = ''
        self.edit_confirm_password = ''
        self.show_edit_password = False
    
    def _show_delete_confirm_modal(self):
        """Mostra modal de confirmação de exclusão"""
        from components.confirm_modal import ConfirmModal
        
        if self.confirm_delete_modal:
            try:
                self.confirm_delete_modal.close()
            except:
                pass
        
        user_name = self.delete_confirm_user.get('nome') or self.delete_confirm_user.get('Nome') or ''
        self.confirm_delete_modal = ConfirmModal(
            self,
            title="CONFIRMAR EXCLUSÃO",
            message=f"Tem certeza que deseja excluir o usuário {user_name}? Esta ação não pode ser desfeita.",
            confirm_text="Excluir",
            cancel_text="Cancelar",
            on_confirm=self._handle_confirm_delete,
            on_cancel=lambda: self._close_delete_confirm_modal(),
            is_dangerous=True,
            is_loading=self.is_loading_delete
        )
    
    def _close_delete_confirm_modal(self):
        """Fecha modal de confirmação de exclusão"""
        if self.confirm_delete_modal:
            try:
                self.confirm_delete_modal.close()
            except:
                pass
            self.confirm_delete_modal = None
        self.delete_confirm_user = None
    
    def _handle_confirm_delete(self):
        """Confirma e executa exclusão - igual ao web"""
        if not self.delete_confirm_user:
            return
        
        self._close_delete_confirm_modal()
        self.is_loading_delete = True
        
        threading.Thread(target=self._do_delete_user, daemon=True).start()
    
    def _do_delete_user(self):
        """Executa exclusão do usuário"""
        try:
            user_id = self.delete_confirm_user.get('id') or self.delete_confirm_user.get('Id')
            UserService.delete_user(user_id)
            
            self.after(0, lambda: show_toast(self, 'Usuário excluído com sucesso!', 'success'))
            self.after(0, self._load_users)
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'data') and e.data:
                error_msg = e.data.get('message', error_msg)
            self.after(0, lambda msg=error_msg: show_toast(self, f'Erro ao excluir usuário: {msg}', 'error'))
        finally:
            self.after(0, lambda: setattr(self, 'is_loading_delete', False))
            self.after(0, lambda: setattr(self, 'delete_confirm_user', None))




