"""
ForgotPasswordModal - Modal de recuperação de senha
Replica ForgotPasswordModal.jsx do web
"""
import tkinter as tk
from tkinter import ttk

class ForgotPasswordModal:
    """Modal de recuperação de senha"""
    
    def __init__(self, parent, is_open, on_close):
        self.parent = parent
        self.is_open = is_open
        self.on_close = on_close
        self.modal = None
        self.overlay = None
        
        if is_open:
            self._create_modal()
    
    def _create_modal(self):
        """Cria o modal"""
        # Obtém a janela raiz para garantir que o overlay cubra tudo
        root = self.parent.winfo_toplevel()
        
        # Overlay com fundo escuro (semi-transparente visualmente)
        self.overlay = tk.Frame(root, bg="#000000")
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self.overlay.lift()  # Garante que o overlay fique acima de tudo
        self.overlay.bind("<Button-1>", lambda e: self.close())
        
        # Modal centralizado
        self.modal = tk.Frame(self.overlay, bg="#FFFFFF", bd=0, relief=tk.FLAT)
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        self.modal.config(width=450, height=280)
        self.modal.pack_propagate(False)
        self.modal.lift()  # Garante que o modal fique acima do overlay
        
        # Impede que cliques no modal fechem o overlay
        def stop_propagation(event):
            return "break"
        
        self.modal.bind("<Button-1>", stop_propagation)
        
        # Header vermelho
        header = tk.Frame(self.modal, bg="#8B0000", height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title_label = tk.Label(
            header,
            text="RECUPERAR SENHA",
            font=("Inter", 18, "bold"),
            bg="#8B0000",
            fg="#FFFFFF"
        )
        title_label.pack(expand=True)
        
        # Body branco
        body = tk.Frame(self.modal, bg="#FFFFFF")
        body.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)
        
        message_label = tk.Label(
            body,
            text="Para recuperar a sua senha envie mensagem para o seu gestor.",
            font=("Inter", 14),
            bg="#FFFFFF",
            fg="#262626",
            wraplength=350,
            justify=tk.LEFT,
            anchor="w"
        )
        message_label.pack(fill=tk.X, pady=(0, 20))
        
        # Linha tracejada vermelha (separador visual)
        separator = tk.Frame(body, bg="#8B0000", height=1)
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # Footer com botão
        footer = tk.Frame(self.modal, bg="#FFFFFF")
        footer.pack(fill=tk.X, padx=32, pady=(0, 24))
        
        # Função para fechar o modal (garante que funcione)
        def close_modal():
            try:
                if self.overlay:
                    self.overlay.destroy()
                if self.modal:
                    self.modal.destroy()
                if self.on_close:
                    self.on_close()
            except Exception as e:
                print(f"Erro ao fechar modal: {e}")
        
        ok_button = tk.Button(
            footer,
            text="OK",
            font=("Inter", 14, "bold"),
            bg="#8B0000",
            fg="#FFFFFF",
            activebackground="#6B0000",
            activeforeground="#FFFFFF",
            bd=0,
            relief=tk.FLAT,
            padx=50,
            pady=12,
            cursor="hand2",
            command=close_modal
        )
        ok_button.pack()
        
        # Impede propagação apenas em frames e labels (não em botões)
        def bind_children(widget):
            for child in widget.winfo_children():
                # Aplica stop_propagation apenas em Frames e Labels, não em Buttons
                widget_type = child.winfo_class()
                if widget_type in ['Frame', 'Label']:
                    child.bind("<Button-1>", stop_propagation)
                # Continua recursivamente para filhos
                bind_children(child)
        
        # Aguarda um pouco para garantir que os widgets filhos sejam criados
        self.modal.after(10, lambda: bind_children(self.modal))
    
    def close(self):
        """Fecha o modal"""
        try:
            # Destrói o modal primeiro (que está dentro do overlay)
            if self.modal:
                try:
                    self.modal.destroy()
                except:
                    pass
            # Depois destrói o overlay
            if self.overlay:
                try:
                    self.overlay.destroy()
                except:
                    pass
            # Chama callback se existir
            if self.on_close:
                try:
                    self.on_close()
                except:
                    pass
            # Limpa referências
            self.modal = None
            self.overlay = None
        except Exception as e:
            print(f"Erro ao fechar modal: {e}")
            # Tenta destruir de qualquer forma
            try:
                if self.overlay:
                    self.overlay.destroy()
            except:
                pass




