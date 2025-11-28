"""
EditUserModal - Modal de edição de usuário
Replica o modal de edição do RegisterEmployeePage.jsx do web
"""
import tkinter as tk
import customtkinter as ctk
from config import COLORS
import re

class EditUserModal:
    """Modal de edição de usuário"""
    
    def __init__(self, parent, user, on_save, on_cancel, on_change_password_toggle,
                 change_password=False, edit_password="", edit_confirm_password="",
                 show_password=False, on_password_change=None, on_confirm_password_change=None,
                 on_toggle_show_password=None):
        self.parent = parent
        self.user = user.copy() if user else {}
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.on_change_password_toggle = on_change_password_toggle
        self.change_password = change_password
        self.edit_password = edit_password
        self.edit_confirm_password = edit_confirm_password
        self.show_password = show_password
        self.on_password_change = on_password_change
        self.on_confirm_password_change = on_confirm_password_change
        self.on_toggle_show_password = on_toggle_show_password
        
        self.modal = None
        self.overlay = None
        
        # Lista de cargos corporativos (igual ao web)
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
        
        self._create_modal()
    
    def _create_modal(self):
        """Cria o modal - igual ao ConfirmModal"""
        # Obtém a janela principal (toplevel)
        self.toplevel = self.parent.winfo_toplevel()
        
        # Garante que a janela principal está atualizada
        self.toplevel.update_idletasks()
        x = self.toplevel.winfo_x()
        y = self.toplevel.winfo_y()
        width = self.toplevel.winfo_width()
        height = self.toplevel.winfo_height()
        
        # === OVERLAY COM TRANSPARÊNCIA ===
        self.overlay_window = tk.Toplevel(self.toplevel)
        self.overlay_window.overrideredirect(True)
        self.overlay_window.transient(self.toplevel)
        self.overlay_window.geometry(f"{width}x{height}+{x}+{y}")
        self.overlay_window.configure(bg="black")
        
        # Frame overlay
        self.overlay = tk.Frame(self.overlay_window, bg="black", highlightthickness=0)
        self.overlay.pack(fill=tk.BOTH, expand=True)
        self.overlay.bind("<Button-1>", lambda e: self.close())
        
        # Configura transparência de 30% (alpha = 0.3) ANTES de exibir
        try:
            self.overlay_window.attributes('-alpha', 0.3)
        except tk.TclError:
            # Fallback: cor que escurece o fundo visivelmente
            self.overlay.configure(bg="#808080")
        
        # Garante que a janela seja exibida e fique visível
        self.overlay_window.update_idletasks()
        self.overlay_window.deiconify()
        self.overlay_window.lift()
        self.overlay_window.update()
        
        # === MODAL OPAQUE ===
        self.modal_window = tk.Toplevel(self.toplevel)
        self.modal_window.overrideredirect(True)
        self.modal_window.transient(self.toplevel)
        self.modal_window.grab_set()
        
        # Garante que o modal seja totalmente opaco
        try:
            self.modal_window.attributes('-alpha', 1.0)
        except:
            pass
        
        # Tamanho do modal
        modal_width = 600
        modal_height = 700
        center_x = x + (width - modal_width) // 2
        center_y = y + (height - modal_height) // 2
        self.modal_window.geometry(f"{modal_width}x{modal_height}+{center_x}+{center_y}")
        
        # Frame do modal
        self.modal = tk.Frame(self.modal_window, bg="#FFFFFF", bd=0, relief=tk.FLAT)
        self.modal.pack(fill=tk.BOTH, expand=True)
        self.modal.grid_columnconfigure(0, weight=1)
        self.modal.bind("<Button-1>", lambda e: self._stop_propagation(e))
        
        # Header vermelho
        header = tk.Frame(self.modal, bg="#8B0000", height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title_label = tk.Label(
            header,
            text="EDITAR USUÁRIO",
            font=("Inter", 18, "bold"),
            bg="#8B0000",
            fg="#FFFFFF"
        )
        title_label.pack(expand=True)
        
        # Body scrollável
        body_container = tk.Frame(self.modal, bg="#FFFFFF")
        body_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        body_canvas = tk.Canvas(body_container, bg="#FFFFFF", highlightthickness=0)
        body_scrollbar = tk.Scrollbar(body_container, orient="vertical", command=body_canvas.yview)
        body_frame = tk.Frame(body_canvas, bg="#FFFFFF")
        
        body_frame.bind(
            "<Configure>",
            lambda e: body_canvas.configure(scrollregion=body_canvas.bbox("all"))
        )
        
        body_canvas.create_window((0, 0), window=body_frame, anchor="nw")
        body_canvas.configure(yscrollcommand=body_scrollbar.set)
        
        def on_canvas_configure(event):
            canvas_width = event.width
            body_canvas.itemconfig(body_canvas.find_all()[0], width=canvas_width)
        
        body_canvas.bind("<Configure>", on_canvas_configure)
        
        body_canvas.pack(side="left", fill="both", expand=True)
        body_scrollbar.pack(side="right", fill="y")
        
        # Habilita scroll do mouse
        def on_mousewheel(event):
            if event.num == 4 or event.delta > 0:
                body_canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                body_canvas.yview_scroll(1, "units")
        
        def bind_mousewheel(event):
            body_canvas.bind_all("<MouseWheel>", on_mousewheel)
            body_canvas.bind_all("<Button-4>", on_mousewheel)
            body_canvas.bind_all("<Button-5>", on_mousewheel)
        
        def unbind_mousewheel(event):
            body_canvas.unbind_all("<MouseWheel>")
            body_canvas.unbind_all("<Button-4>")
            body_canvas.unbind_all("<Button-5>")
        
        body_canvas.bind("<Enter>", bind_mousewheel)
        body_canvas.bind("<Leave>", unbind_mousewheel)
        
        # Container do formulário
        form_container = tk.Frame(body_frame, bg="#FFFFFF")
        form_container.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Nome
        nome_label = tk.Label(
            form_container,
            text="Nome Completo *",
            font=("Inter", 14, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        nome_label.pack(fill="x", pady=(0, 10))
        
        self.nome_entry = ctk.CTkEntry(
            form_container,
            placeholder_text="Digite o nome completo",
            font=ctk.CTkFont(size=14),
            height=45
        )
        self.nome_entry.pack(fill="x", pady=(0, 20))
        self.nome_entry.insert(0, self.user.get('nome', ''))
        self.nome_entry.bind("<KeyRelease>", lambda e: self._update_user_field('nome', self.nome_entry.get()))
        
        # Email
        email_label = tk.Label(
            form_container,
            text="E-mail *",
            font=("Inter", 14, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        email_label.pack(fill="x", pady=(0, 10))
        
        self.email_entry = ctk.CTkEntry(
            form_container,
            placeholder_text="exemplo@helpwave.com",
            font=ctk.CTkFont(size=14),
            height=45
        )
        self.email_entry.pack(fill="x", pady=(0, 20))
        self.email_entry.insert(0, self.user.get('email', ''))
        self.email_entry.bind("<KeyRelease>", lambda e: self._update_user_field('email', self.email_entry.get()))
        
        # Cargo
        cargo_label = tk.Label(
            form_container,
            text="Cargo *",
            font=("Inter", 14, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        cargo_label.pack(fill="x", pady=(0, 10))
        
        cargo_value = self.user.get('cargo', '')
        # Se o cargo não estiver na lista, adiciona como primeira opção
        cargo_values = self.cargos_corporativos.copy()
        if cargo_value and cargo_value not in cargo_values:
            cargo_values.insert(0, cargo_value)
        
        self.cargo_var = ctk.StringVar(value=cargo_value)
        self.cargo_combo = ctk.CTkComboBox(
            form_container,
            values=cargo_values,
            variable=self.cargo_var,
            font=ctk.CTkFont(size=14),
            height=45,
            dropdown_font=ctk.CTkFont(size=14),
            command=lambda v: self._update_user_field('cargo', v)
        )
        self.cargo_combo.pack(fill="x", pady=(0, 20))
        
        # Telefone
        telefone_label = tk.Label(
            form_container,
            text="Telefone",
            font=("Inter", 14, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        telefone_label.pack(fill="x", pady=(0, 10))
        
        self.telefone_entry = ctk.CTkEntry(
            form_container,
            placeholder_text="(11) 99999-9999",
            font=ctk.CTkFont(size=14),
            height=45
        )
        self.telefone_entry.pack(fill="x", pady=(0, 20))
        self.telefone_entry.insert(0, self.user.get('telefone', ''))
        self.telefone_entry.bind("<KeyRelease>", lambda e: self._update_user_field('telefone', self.telefone_entry.get()))
        
        # Permissão
        permissao_label = tk.Label(
            form_container,
            text="Permissão *",
            font=("Inter", 14, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        permissao_label.pack(fill="x", pady=(0, 10))
        
        permissao_value = self.user.get('permissao', 1)
        permissao_str = f"{permissao_value} - {['Colaborador', 'Suporte Técnico', 'Administrador'][permissao_value - 1] if permissao_value in [1, 2, 3] else 'Desconhecido'}"
        
        self.permissao_var = ctk.StringVar(value=permissao_str)
        
        def on_permissao_change(value):
            permissao_num = int(value.split(' - ')[0])
            self._update_user_field('permissao', permissao_num)
        
        permissao_combo = ctk.CTkComboBox(
            form_container,
            values=["1 - Colaborador", "2 - Suporte Técnico", "3 - Administrador"],
            variable=self.permissao_var,
            font=ctk.CTkFont(size=14),
            height=45,
            dropdown_font=ctk.CTkFont(size=14),
            command=on_permissao_change
        )
        permissao_combo.pack(fill="x", pady=(0, 20))
        
        # Checkbox alterar senha
        self.change_password_var = tk.BooleanVar(value=self.change_password)
        change_password_check = ctk.CTkCheckBox(
            form_container,
            text="Alterar senha",
            font=ctk.CTkFont(size=14),
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_dark'],
            variable=self.change_password_var,
            command=lambda: self._on_change_password_check()
        )
        change_password_check.pack(fill="x", pady=(0, 20))
        
        # Campos de senha (inicialmente ocultos)
        self.password_frame = tk.Frame(form_container, bg="#FFFFFF")
        
        # Nova Senha
        senha_label = tk.Label(
            self.password_frame,
            text="Nova Senha *",
            font=("Inter", 14, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        senha_label.pack(fill="x", pady=(0, 10))
        
        senha_container = tk.Frame(self.password_frame, bg="#FFFFFF")
        senha_container.pack(fill="x", pady=(0, 20))
        
        self.senha_entry = ctk.CTkEntry(
            senha_container,
            placeholder_text="Mínimo 6 caracteres",
            font=ctk.CTkFont(size=14),
            height=45,
            show="*" if not self.show_password else ""
        )
        self.senha_entry.pack(side="left", fill="x", expand=True)
        self.senha_entry.insert(0, self.edit_password)
        self.senha_entry.bind("<KeyRelease>", lambda e: self._on_password_entry_change())
        
        show_password_btn = ctk.CTkButton(
            senha_container,
            text="👁️",
            font=ctk.CTkFont(size=14),
            width=50,
            height=45,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_dark'],
            command=self._toggle_show_password
        )
        show_password_btn.pack(side="right", padx=(10, 0))
        
        # Confirmar Senha
        confirm_senha_label = tk.Label(
            self.password_frame,
            text="Confirmar Nova Senha *",
            font=("Inter", 14, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            anchor="w"
        )
        confirm_senha_label.pack(fill="x", pady=(0, 10))
        
        confirm_senha_container = tk.Frame(self.password_frame, bg="#FFFFFF")
        confirm_senha_container.pack(fill="x", pady=(0, 20))
        
        self.confirm_senha_entry = ctk.CTkEntry(
            confirm_senha_container,
            placeholder_text="Repita a senha",
            font=ctk.CTkFont(size=14),
            height=45,
            show="*" if not self.show_password else ""
        )
        self.confirm_senha_entry.pack(side="left", fill="x", expand=True)
        self.confirm_senha_entry.insert(0, self.edit_confirm_password)
        self.confirm_senha_entry.bind("<KeyRelease>", lambda e: self._on_confirm_password_entry_change())
        
        show_confirm_password_btn = ctk.CTkButton(
            confirm_senha_container,
            text="👁️",
            font=ctk.CTkFont(size=14),
            width=50,
            height=45,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_dark'],
            command=self._toggle_show_password
        )
        show_confirm_password_btn.pack(side="right", padx=(10, 0))
        
        # Mostra/esconde campos de senha baseado no checkbox
        if self.change_password:
            self.password_frame.pack(fill="x", pady=(0, 20))
        else:
            self.password_frame.pack_forget()
        
        # Footer
        footer = tk.Frame(self.modal, bg="#FFFFFF")
        footer.pack(fill="x", padx=40, pady=(0, 30))
        
        buttons_frame = tk.Frame(footer, bg="#FFFFFF")
        buttons_frame.pack(expand=True)
        
        cancel_btn = tk.Button(
            buttons_frame,
            text="Cancelar",
            font=("Inter", 14),
            bg="#E5E5E5",
            fg="#333333",
            activebackground="#D5D5D5",
            activeforeground="#333333",
            bd=0,
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.close
        )
        cancel_btn.pack(side="left", padx=(0, 12))
        
        save_btn = tk.Button(
            buttons_frame,
            text="Salvar",
            font=("Inter", 14, "bold"),
            bg="#8B0000",
            fg="#FFFFFF",
            activebackground="#6B0000",
            activeforeground="#FFFFFF",
            bd=0,
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self._handle_save
        )
        save_btn.pack(side="left")
        
        # Atualiza tamanho do modal após criar conteúdo
        self.modal_window.update_idletasks()
        self.modal.update_idletasks()
        
        # Recalcula tamanho do modal
        modal_width = max(600, self.modal.winfo_reqwidth() + 20)
        modal_height = max(700, min(800, self.modal.winfo_reqheight() + 20))
        
        # Recalcula posição
        self.toplevel.update_idletasks()
        x = self.toplevel.winfo_x()
        y = self.toplevel.winfo_y()
        width = self.toplevel.winfo_width()
        height = self.toplevel.winfo_height()
        
        # Atualiza overlay
        if self.overlay_window.winfo_exists():
            self.overlay_window.geometry(f"{width}x{height}+{x}+{y}")
            self.overlay_window.lift()
        
        # Centraliza modal
        center_x = x + (width - modal_width) // 2
        center_y = y + (height - modal_height) // 2
        self.modal_window.geometry(f"{modal_width}x{modal_height}+{center_x}+{center_y}")
        self.modal_window.lift()
        self.modal_window.focus_set()
        
        # Configura atualizações de posição
        self._setup_position_updates()
    
    def _setup_position_updates(self):
        """Configura atualizações de posição"""
        def update_position(event=None):
            try:
                if not self.toplevel.winfo_exists():
                    return
                    
                self.toplevel.update_idletasks()
                x = self.toplevel.winfo_x()
                y = self.toplevel.winfo_y()
                width = self.toplevel.winfo_width()
                height = self.toplevel.winfo_height()
                
                if hasattr(self, 'overlay_window') and self.overlay_window.winfo_exists():
                    self.overlay_window.geometry(f"{width}x{height}+{x}+{y}")
                    self.overlay_window.lift()
                
                if hasattr(self, 'modal_window') and self.modal_window.winfo_exists():
                    modal_width = self.modal_window.winfo_width()
                    modal_height = self.modal_window.winfo_height()
                    center_x = x + (width - modal_width) // 2
                    center_y = y + (height - modal_height) // 2
                    self.modal_window.geometry(f"{modal_width}x{modal_height}+{center_x}+{center_y}")
                    self.modal_window.lift()
            except:
                pass
        
        # Bind para atualizar quando a janela principal mover
        try:
            self.toplevel.bind("<Configure>", update_position)
        except:
            pass
    
    def _stop_propagation(self, event):
        """Impede que o clique no modal feche o overlay"""
        event.widget = self.modal
    
    def _update_user_field(self, field, value):
        """Atualiza campo do usuário"""
        self.user[field] = value
        # Atualiza também no parent se existir
        if hasattr(self.parent, 'editing_user') and self.parent.editing_user:
            self.parent.editing_user[field] = value
    
    def _on_change_password_check(self):
        """Callback quando checkbox de alterar senha muda"""
        checked = self.change_password_var.get()
        self.change_password = checked
        if self.on_change_password_toggle:
            self.on_change_password_toggle(checked)
        
        if checked:
            self.password_frame.pack(fill="x", pady=(0, 20))
        else:
            self.password_frame.pack_forget()
            self.senha_entry.delete(0, "end")
            self.confirm_senha_entry.delete(0, "end")
    
    def _on_password_entry_change(self):
        """Callback quando senha muda"""
        self.edit_password = self.senha_entry.get()
        if self.on_password_change:
            self.on_password_change(self.edit_password)
    
    def _on_confirm_password_entry_change(self):
        """Callback quando confirmação de senha muda"""
        self.edit_confirm_password = self.confirm_senha_entry.get()
        if self.on_confirm_password_change:
            self.on_confirm_password_change(self.edit_confirm_password)
    
    def _toggle_show_password(self):
        """Alterna mostrar/ocultar senha"""
        self.show_password = not self.show_password
        show_char = "" if self.show_password else "*"
        self.senha_entry.configure(show=show_char)
        self.confirm_senha_entry.configure(show=show_char)
        if self.on_toggle_show_password:
            self.on_toggle_show_password()
    
    def _handle_save(self):
        """Lida com salvamento"""
        # Atualiza campos do usuário
        self.user['nome'] = self.nome_entry.get().strip()
        self.user['email'] = self.email_entry.get().strip()
        cargo_value = self.cargo_var.get()
        if cargo_value:
            self.user['cargo'] = cargo_value
        self.user['telefone'] = self.telefone_entry.get().strip()
        permissao_str = self.permissao_var.get()
        self.user['permissao'] = int(permissao_str.split(' - ')[0])
        
        # Atualiza senhas se necessário
        if self.change_password:
            self.edit_password = self.senha_entry.get()
            self.edit_confirm_password = self.confirm_senha_entry.get()
        
        # Atualiza referência no parent
        if hasattr(self.parent, 'editing_user'):
            self.parent.editing_user = self.user.copy()
        if hasattr(self.parent, 'edit_password'):
            self.parent.edit_password = self.edit_password
        if hasattr(self.parent, 'edit_confirm_password'):
            self.parent.edit_confirm_password = self.edit_confirm_password
        if hasattr(self.parent, 'change_password'):
            self.parent.change_password = self.change_password
        
        if self.on_save:
            self.on_save()
    
    def close(self):
        """Fecha o modal"""
        try:
            if hasattr(self, 'overlay_window') and self.overlay_window.winfo_exists():
                self.overlay_window.destroy()
        except:
            pass
        try:
            if hasattr(self, 'modal_window') and self.modal_window.winfo_exists():
                self.modal_window.destroy()
        except:
            pass
        # Remove bind
        try:
            if hasattr(self, 'toplevel') and self.toplevel.winfo_exists():
                self.toplevel.unbind("<Configure>")
        except:
            pass
        if self.on_cancel:
            self.on_cancel()

