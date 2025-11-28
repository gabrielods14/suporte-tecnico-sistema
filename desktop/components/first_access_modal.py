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
        # Obtém a janela principal (toplevel)
        self.toplevel = self.parent.winfo_toplevel()
        
        # Garante que a janela principal está atualizada
        self.toplevel.update_idletasks()
        
        # Obtém posição e tamanho da janela principal
        x = self.toplevel.winfo_x()
        y = self.toplevel.winfo_y()
        width = self.toplevel.winfo_width()
        height = self.toplevel.winfo_height()
        
        # === OVERLAY COM TRANSPARÊNCIA ===
        # Usa Toplevel mas posiciona para não cobrir a barra de título
        # Calcula a altura real da barra de título
        self.toplevel.update_idletasks()
        root_y = self.toplevel.winfo_rooty()
        frame_y = self.toplevel.winfo_y()
        title_bar_height = root_y - frame_y if root_y > frame_y else 30
        
        self.overlay_window = tk.Toplevel(self.toplevel)
        self.overlay_window.overrideredirect(True)
        self.overlay_window.transient(self.toplevel)
        
        # Calcula posição e tamanho do overlay (abaixo da barra de título)
        # Usa a área do cliente da janela (sem a barra de título)
        overlay_x = x
        overlay_y = y + title_bar_height
        overlay_width = width
        overlay_height = height - title_bar_height
        
        self.overlay_window.geometry(f"{overlay_width}x{overlay_height}+{overlay_x}+{overlay_y}")
        self.overlay_window.configure(bg="black")
        
        # Frame overlay
        self.overlay = tk.Frame(self.overlay_window, bg="black", highlightthickness=0)
        self.overlay.pack(fill=tk.BOTH, expand=True)
        self.overlay.bind("<Button-1>", lambda e: None)  # Não fecha ao clicar no overlay
        
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
        
        # Garante que o modal seja totalmente opaco
        try:
            self.modal_window.attributes('-alpha', 1.0)
        except:
            pass
        
        # Tamanho do modal
        modal_width = 500
        modal_height = 650
        
        # Centraliza o modal na janela principal (não na tela)
        # Aguarda a janela principal estar atualizada
        self.toplevel.update_idletasks()
        
        # Obtém posição e tamanho da janela principal
        main_x = self.toplevel.winfo_x()
        main_y = self.toplevel.winfo_y()
        main_width = self.toplevel.winfo_width()
        main_height = self.toplevel.winfo_height()
        
        # Calcula posição central na janela principal
        modal_x = main_x + (main_width - modal_width) // 2
        modal_y = main_y + (main_height - modal_height) // 2
        
        self.modal_window.geometry(f"{modal_width}x{modal_height}+{modal_x}+{modal_y}")
        self.modal_window.configure(bg="#FFFFFF")
        
        # Frame interno do modal
        self.modal = tk.Frame(self.modal_window, bg="#FFFFFF", bd=2, relief=tk.SOLID)
        self.modal.pack(fill=tk.BOTH, expand=True)
        
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
        senha_atual_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=14)
        
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
        nova_senha_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=14)
        
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
        confirmar_senha_frame.pack(fill=tk.X, pady=(0, 16))
        
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
        confirmar_senha_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=14)
        
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
        
        # Botão - usando Label estilizado para controle total da altura
        def on_btn_click(event):
            self._handle_submit()
        
        def on_btn_enter(event):
            submit_btn_label.config(bg="#8B0000")
        
        def on_btn_leave(event):
            submit_btn_label.config(bg="#A93226")
        
        submit_btn_label = tk.Label(
            body,
            text="Alterar Senha",
            font=("Inter", 16, "bold"),
            bg="#A93226",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            bd=0,
            height=3,  # Altura em linhas de texto (aproximadamente 50-60px)
            anchor="center"
        )
        submit_btn_label.pack(fill=tk.X, pady=(16, 0))
        submit_btn_label.bind("<Button-1>", on_btn_click)
        submit_btn_label.bind("<Enter>", on_btn_enter)
        submit_btn_label.bind("<Leave>", on_btn_leave)
        
        # Garante que o modal seja exibido e fique acima do overlay
        self.modal_window.update_idletasks()
        self.modal_window.deiconify()
        self.modal_window.lift()
        self.modal_window.focus_force()
        self.modal_window.update()
        
        # Aplica grab_set APÓS o modal estar completamente renderizado
        try:
            self.modal_window.grab_set()
        except:
            pass
        
        # Função para reposicionar o modal quando a janela for redimensionada
        def reposition_modal(event=None):
            try:
                if hasattr(self, 'toplevel') and self.toplevel.winfo_exists():
                    self.toplevel.update_idletasks()
                    main_x = self.toplevel.winfo_x()
                    main_y = self.toplevel.winfo_y()
                    main_width = self.toplevel.winfo_width()
                    main_height = self.toplevel.winfo_height()
                    
                    # Calcula altura da barra de título dinamicamente
                    root_y = self.toplevel.winfo_rooty()
                    frame_y = self.toplevel.winfo_y()
                    title_bar_height = root_y - frame_y if root_y > frame_y else 30
                    
                    # Reposiciona overlay (abaixo da barra de título)
                    if hasattr(self, 'overlay_window') and self.overlay_window.winfo_exists():
                        overlay_x = main_x
                        overlay_y = main_y + title_bar_height
                        overlay_width = main_width
                        overlay_height = main_height - title_bar_height
                        self.overlay_window.geometry(f"{overlay_width}x{overlay_height}+{overlay_x}+{overlay_y}")
                    
                    # Reposiciona modal
                    if hasattr(self, 'modal_window') and self.modal_window.winfo_exists():
                        modal_x = main_x + (main_width - modal_width) // 2
                        modal_y = main_y + (main_height - modal_height) // 2
                        self.modal_window.geometry(f"{modal_width}x{modal_height}+{modal_x}+{modal_y}")
            except:
                pass
        
        # Bind eventos de redimensionamento
        try:
            self.toplevel.bind('<Configure>', reposition_modal)
        except:
            pass
    
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
        target_window = self.modal_window if hasattr(self, 'modal_window') else self.parent
        if not senha_atual or not nova_senha or not confirmar_senha:
            show_toast(target_window, "Por favor, preencha todos os campos.", "error")
            return
        
        if nova_senha != confirmar_senha:
            show_toast(target_window, "As senhas não conferem.", "error")
            return
        
        if len(nova_senha) < 6:
            show_toast(target_window, "A senha deve ter pelo menos 6 caracteres.", "error")
            return
        
        # Abre modal de confirmação
        self.confirm_modal = ConfirmModal(
            self.modal_window if hasattr(self, 'modal_window') else self.toplevel,
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
            if hasattr(self, 'modal_window') and self.modal_window:
                self.modal_window.after(0, lambda: show_toast(self.modal_window, f"Erro ao alterar senha: {str(e)}", "error"))
            else:
                self.parent.after(0, lambda: show_toast(self.parent, f"Erro ao alterar senha: {str(e)}", "error"))
        finally:
            if hasattr(self, 'modal_window') and self.modal_window:
                self.modal_window.after(0, lambda: setattr(self, 'is_loading', False))
            else:
                self.parent.after(0, lambda: setattr(self, 'is_loading', False))
    
    def _handle_success(self):
        """Lida com sucesso"""
        self.close()
        if self.on_success:
            self.on_success()
    
    def close(self):
        """Fecha o modal"""
        if hasattr(self, 'modal_window') and self.modal_window:
            try:
                self.modal_window.destroy()
            except:
                pass
        if hasattr(self, 'overlay_window') and self.overlay_window:
            try:
                self.overlay_window.destroy()
            except:
                pass






