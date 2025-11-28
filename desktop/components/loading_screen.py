"""
LoadingScreen - Tela de carregamento
Replica LoadingScreen.jsx do web
"""
import tkinter as tk
from tkinter import ttk

class LoadingScreen(tk.Frame):
    """Tela de carregamento - estilo exato do web"""
    
    def __init__(self, parent, message="Aguarde..."):
        super().__init__(parent, bg="#FFFFFF")
        self.pack(fill=tk.BOTH, expand=True)
        
        # Container centralizado
        content = tk.Frame(self, bg="#FFFFFF")
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        # Spinner
        spinner_frame = tk.Frame(content, bg="#FFFFFF")
        spinner_frame.pack(pady=(0, 24))
        
        # Spinner animado (simulado com texto por enquanto)
        spinner_label = tk.Label(
            spinner_frame,
            text="⏳",
            font=("Inter", 48),
            bg="#FFFFFF",
            fg="#A93226"
        )
        spinner_label.pack()
        
        # Mensagem
        message_label = tk.Label(
            content,
            text=message,
            font=("Inter", 18),
            bg="#FFFFFF",
            fg="#333333"
        )
        message_label.pack()






