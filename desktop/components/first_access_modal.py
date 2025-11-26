"""
FirstAccessModal - Modal de primeiro acesso
Replica FirstAccessModal.jsx do web
"""
import tkinter as tk
from tkinter import ttk
from components.confirm_modal import ConfirmModal
from components.toast import show_toast
from api_client import UserService
import threading

class FirstAccessModal:
    """Modal de primeiro acesso para alteração de senha"""
    
    def __init__(self, parent, is_open, on_success):
        self.parent = parent
        self.is_open = is_open
        self.on_success = on_success
        self.modal = None
        self.confirm_modal = None
        self.is_loading = False
        self.errors = {}
        
        if is_open:
            self._create_modal()
    
    def _create_modal(self):
        """Cria o modal"""
        # Overlay
        self.overlay = tk.Frame(self.parent, bg="#000000")
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Modal
        self.modal = tk.Frame(self.overlay, bg="#FFFFFF", bd=2, relief=tk.SOLID)
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        self.modal.config(width=500, height=600)
        self.modal.pack_propagate(False)
        
        # Header
        header = tk.Frame(self.modal, bg="#A93226")
        header.pack(fill=tk.X, padx=0, pady=0)
        
        header_inner = tk.Frame(header, bg="#A93226")
        header_inner.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)
        
        icon_label = tk.Label(
            header_inner,
            text="🔒",
            font=("Inter", 48),
            bg="#A93226",
            fg="white"
        )
        icon_label.pack()
        
        title_label = tk.Label(
            header_inner,
            text="PRIMEIRO ACESSO",
            font=("Inter", 24, "bold"),
            bg="#A93226",
            fg="white"
        )
        title_label.pack(pady=(16, 8))
        
        subtitle_label = tk.Label(
            header_inner,
            text="Por favor, redefina sua senha para continuar",
            font=("Inter", 14),
            bg="#A93226",
            fg="white"
        )
        subtitle_label.pack()
        
        # Body
        body = tk.Frame(self.modal, bg="#FFFFFF")
        body.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)
        
        # Campos
        self.senha_atual_var = tk.StringVar()
        self.nova_senha_var = tk.StringVar()
        self.confirmar_senha_var = tk.StringVar()
        
        self.show_senha_atual = tk.BooleanVar(value=False)
        self.show_nova_senha = tk.BooleanVar(value=False)
        self.show_confirmar_senha = tk.BooleanVar(value=False)
        
        # Senha Atual
        senha_atual_frame = tk.Frame(body, bg="#FFFFFF")
        senha_atual_frame.pack(fill=tk.X, pady=(0, 16))
        
        senha_atual_label = tk.Label(
            senha_atual_frame,
            text="Senha Atual *",
            font=("Inter", 14, "bold"),
            bg="#FFFFFF",
            fg="#333333",
            anchor="w"
        )
        senha_atual_label.pack(fill=tk.X, pady=(0, 8))
        
        senha_atual_input_frame = tk.Frame(senha_atual_frame, bg="#FFFFFF")
        senha_atual_input_frame.pack(fill=tk.X)
        
        senha_atual_entry = tk.Entry(
            senha_atual_input_frame,
            textvariable=self.senha_atual_var,
            font=("Inter", 14),
            show="" if self.show_senha_atual.get() else "•",
            bg="#FFFFFF",
            fg="#333333",
            bd=2,
            relief=tk.SOLID,
            highlightthickness=0,
            highlightbackground="#E5E5E5",
            highlightcolor="#A93226"
        )
        senha_atual_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12)
        
        toggle_btn = tk.Button(
            senha_atual_input_frame,
            text="👁" if not self.show_senha_atual.get() else "🙈",
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#666666",
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self._toggle_password(senha_atual_entry, self.show_senha_atual)
        )
        toggle_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
        # Nova Senha
        nova_senha_frame = tk.Frame(body, bg="#FFFFFF")
        nova_senha_frame.pack(fill=tk.X, pady=(0, 16))
        
        nova_senha_label = tk.Label(
            nova_senha_frame,
            text="Nova Senha *",
            font=("Inter", 14, "bold"),
            bg="#FFFFFF",
            fg="#333333",
            anchor="w"
        )
        nova_senha_label.pack(fill=tk.X, pady=(0, 8))
        
        nova_senha_input_frame = tk.Frame(nova_senha_frame, bg="#FFFFFF")
        nova_senha_input_frame.pack(fill=tk.X)
        
        nova_senha_entry = tk.Entry(
            nova_senha_input_frame,
            textvariable=self.nova_senha_var,
            font=("Inter", 14),
            show="" if self.show_nova_senha.get() else "•",
            bg="#FFFFFF",
            fg="#333333",
            bd=2,
            relief=tk.SOLID,
            highlightthickness=0,
            highlightbackground="#E5E5E5",
            highlightcolor="#A93226"
        )
        nova_senha_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12)
        
        toggle_btn2 = tk.Button(
            nova_senha_input_frame,
            text="👁" if not self.show_nova_senha.get() else "🙈",
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#666666",
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self._toggle_password(nova_senha_entry, self.show_nova_senha)
        )
        toggle_btn2.pack(side=tk.RIGHT, padx=(8, 0))
        
        # Confirmar Senha
        confirmar_senha_frame = tk.Frame(body, bg="#FFFFFF")
        confirmar_senha_frame.pack(fill=tk.X, pady=(0, 24))
        
        confirmar_senha_label = tk.Label(
            confirmar_senha_frame,
            text="Confirmar Nova Senha *",
            font=("Inter", 14, "bold"),
            bg="#FFFFFF",
            fg="#333333",
            anchor="w"
        )
        confirmar_senha_label.pack(fill=tk.X, pady=(0, 8))
        
        confirmar_senha_input_frame = tk.Frame(confirmar_senha_frame, bg="#FFFFFF")
        confirmar_senha_input_frame.pack(fill=tk.X)
        
        confirmar_senha_entry = tk.Entry(
            confirmar_senha_input_frame,
            textvariable=self.confirmar_senha_var,
            font=("Inter", 14),
            show="" if self.show_confirmar_senha.get() else "•",
            bg="#FFFFFF",
            fg="#333333",
            bd=2,
            relief=tk.SOLID,
            highlightthickness=0,
            highlightbackground="#E5E5E5",
            highlightcolor="#A93226"
        )
        confirmar_senha_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12)
        
        toggle_btn3 = tk.Button(
            confirmar_senha_input_frame,
            text="👁" if not self.show_confirmar_senha.get() else "🙈",
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#666666",
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self._toggle_password(confirmar_senha_entry, self.show_confirmar_senha)
        )
        toggle_btn3.pack(side=tk.RIGHT, padx=(8, 0))
        
        # Botão
        submit_btn = tk.Button(
            body,
            text="Alterar Senha",
            font=("Inter", 16, "bold"),
            bg="#A93226",
            fg="white",
            activebackground="#8B0000",
            activeforeground="white",
            bd=0,
            relief=tk.FLAT,
            padx=24,
            pady=16,
            cursor="hand2",
            command=self._handle_submit
        )
        submit_btn.pack(fill=tk.X, pady=(0, 0))
    
    def _toggle_password(self, entry, var):
        """Alterna visibilidade da senha"""
        var.set(not var.get())
        entry.config(show="" if var.get() else "•")
    
    def _handle_submit(self):
        """Processa envio"""
        senha_atual = self.senha_atual_var.get()
        nova_senha = self.nova_senha_var.get()
        confirmar_senha = self.confirmar_senha_var.get()
        
        # Validação
        if not senha_atual or not nova_senha or not confirmar_senha:
            show_toast(self.parent, "Por favor, preencha todos os campos.", "error")
            return
        
        if nova_senha != confirmar_senha:
            show_toast(self.parent, "As senhas não conferem.", "error")
            return
        
        if len(nova_senha) < 6:
            show_toast(self.parent, "A senha deve ter pelo menos 6 caracteres.", "error")
            return
        
        # Abre modal de confirmação
        self.confirm_modal = ConfirmModal(
            self.overlay,
            title="CONFIRMAR ALTERAÇÃO DE SENHA",
            message="Tem certeza que é a senha escolhida? Você usará ela por agora.",
            on_confirm=self._perform_change_password,
            on_cancel=lambda: self.confirm_modal.close() if self.confirm_modal else None,
            confirm_text="Confirmar",
            cancel_text="Cancelar"
        )
    
    def _perform_change_password(self):
        """Executa alteração de senha"""
        if self.confirm_modal:
            self.confirm_modal.close()
        
        self.is_loading = True
        threading.Thread(target=self._do_change_password, daemon=True).start()
    
    def _do_change_password(self):
        """Faz alteração de senha"""
        try:
            senha_atual = self.senha_atual_var.get()
            nova_senha = self.nova_senha_var.get()
            
            UserService.alterar_senha(senha_atual, nova_senha)
            
            self.parent.after(0, lambda: show_toast(self.parent, "Senha alterada com sucesso!", "success"))
            self.parent.after(1500, lambda: self._handle_success())
        except Exception as e:
            self.parent.after(0, lambda: show_toast(self.parent, f"Erro ao alterar senha: {str(e)}", "error"))
        finally:
            self.parent.after(0, lambda: setattr(self, 'is_loading', False))
    
    def _handle_success(self):
        """Lida com sucesso"""
        self.close()
        if self.on_success:
            self.on_success()
    
    def close(self):
        """Fecha o modal"""
        if self.overlay:
            self.overlay.destroy()



