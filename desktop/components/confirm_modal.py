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
        
        # Obtém a janela principal (toplevel)
        self.toplevel = parent.winfo_toplevel()
        
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
        self.overlay.bind("<Button-1>", lambda e: self._handle_cancel())
        
        # Configura transparência de 30% (alpha = 0.3) ANTES de exibir
        # Isso permite ver 70% do conteúdo de fundo através do overlay
        try:
            self.overlay_window.attributes('-alpha', 0.3)
        except tk.TclError:
            # Fallback: cor que escurece o fundo visivelmente
            # Usa cinza médio que escurece mas ainda permite ver conteúdo
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
        
        # Tamanho inicial do modal (será ajustado)
        modal_width = 500
        modal_height = 200
        center_x = x + (width - modal_width) // 2
        center_y = y + (height - modal_height) // 2
        self.modal_window.geometry(f"{modal_width}x{modal_height}+{center_x}+{center_y}")
        
        # Frame do modal
        self.modal = tk.Frame(self.modal_window, bg="#FFFFFF", bd=2, relief=tk.SOLID)
        self.modal.pack(fill=tk.BOTH, expand=True)
        self.modal.grid_columnconfigure(0, weight=1)
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
        
        # Footer com botões centralizados (igual ao web)
        footer = tk.Frame(self.modal, bg="#FFFFFF")
        footer.pack(fill=tk.X, padx=24, pady=(0, 24))
        
        # Container centralizado para os botões - usa expand para centralizar
        buttons_container = tk.Frame(footer, bg="#FFFFFF")
        buttons_container.pack(expand=True)  # Centraliza horizontalmente
        
        cancel_btn = tk.Button(
            buttons_container,
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
            buttons_container,
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
        
        # Atualiza tamanho do modal após criar conteúdo
        self.modal_window.update_idletasks()
        self.modal.update_idletasks()
        
        # Recalcula tamanho do modal
        modal_width = max(450, self.modal.winfo_reqwidth() + 20)
        modal_height = max(200, self.modal.winfo_reqheight() + 20)
        
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
    
    def _handle_confirm(self):
        """Lida com confirmação"""
        if not self.is_loading and self.on_confirm:
            self.on_confirm()
            self.close()  # Fecha o modal após confirmação
    
    def _handle_cancel(self):
        """Lida com cancelamento"""
        if not self.is_loading and self.on_cancel:
            self.on_cancel()
        self.close()
    
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
            if self.toplevel.winfo_exists():
                self.toplevel.unbind("<Configure>")
        except:
            pass