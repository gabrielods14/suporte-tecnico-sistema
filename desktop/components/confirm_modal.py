"""
ConfirmModal - Modal de confirmação genérico
Replica ConfirmModal.jsx do web
"""
import tkinter as tk
from tkinter import ttk

class ConfirmModal:
    """Modal de confirmação genérico"""
    
    def __init__(self, parent, title, message, on_confirm, on_cancel, 
                 confirm_text="Confirmar", cancel_text="Cancelar", 
                 is_dangerous=False, is_loading=False):
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.is_loading = is_loading
        
        # Overlay - tkinter não suporta alpha diretamente, usa cor cinza escura para simular transparência
        self.overlay = tk.Frame(parent, bg="#404040")  # Cor cinza escura que simula overlay semi-transparente
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self.overlay.lift()  # Garante que fique acima de outros elementos
        self.overlay.bind("<Button-1>", lambda e: self._handle_cancel())
        
        # Modal
        self.modal = tk.Frame(self.overlay, bg="#FFFFFF", bd=2, relief=tk.SOLID)
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        self.modal.bind("<Button-1>", lambda e: self._stop_propagation(e))
        
        # Header
        header = tk.Frame(self.modal, bg="#FFFFFF")
        header.pack(fill=tk.X, padx=24, pady=(24, 16))
        
        title_label = tk.Label(
            header,
            text=title,
            font=("Inter", 20, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        title_label.pack()
        
        # Body
        body = tk.Frame(self.modal, bg="#FFFFFF")
        body.pack(fill=tk.X, padx=24, pady=(0, 24))
        
        message_label = tk.Label(
            body,
            text=message,
            font=("Inter", 14),
            bg="#FFFFFF",
            fg="#666666",
            wraplength=400,
            justify=tk.LEFT
        )
        message_label.pack()
        
        # Footer
        footer = tk.Frame(self.modal, bg="#FFFFFF")
        footer.pack(fill=tk.X, padx=24, pady=(0, 24))
        
        # Botões
        buttons_frame = tk.Frame(footer, bg="#FFFFFF")
        buttons_frame.pack(side=tk.RIGHT, pady=(0, 0))
        
        cancel_btn = tk.Button(
            buttons_frame,
            text=cancel_text,
            font=("Inter", 14),
            bg="#E5E5E5",
            fg="#333333",
            activebackground="#D5D5D5",
            activeforeground="#333333",
            bd=0,
            relief=tk.FLAT,
            padx=24,
            pady=12,
            cursor="hand2",
            command=self._handle_cancel,
            state=tk.NORMAL if not is_loading else tk.DISABLED
        )
        cancel_btn.pack(side=tk.LEFT, padx=(0, 12))
        
        confirm_color = "#DC3545" if is_dangerous else "#A93226"
        confirm_btn = tk.Button(
            buttons_frame,
            text="Processando..." if is_loading else confirm_text,
            font=("Inter", 14, "bold"),
            bg=confirm_color,
            fg="white",
            activebackground="#8B0000" if not is_dangerous else "#C82333",
            activeforeground="white",
            bd=0,
            relief=tk.FLAT,
            padx=24,
            pady=12,
            cursor="hand2" if not is_loading else "wait",
            command=self._handle_confirm,
            state=tk.NORMAL if not is_loading else tk.DISABLED
        )
        confirm_btn.pack(side=tk.LEFT)
    
    def _stop_propagation(self, event):
        """Impede que o clique no modal feche o overlay"""
        event.widget = self.modal
    
    def _handle_confirm(self):
        """Lida com confirmação"""
        if not self.is_loading and self.on_confirm:
            self.on_confirm()
    
    def _handle_cancel(self):
        """Lida com cancelamento"""
        if not self.is_loading and self.on_cancel:
            self.on_cancel()
        self.close()
    
    def close(self):
        """Fecha o modal"""
        if self.overlay:
            self.overlay.destroy()


