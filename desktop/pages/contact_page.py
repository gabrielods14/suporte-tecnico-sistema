"""
ContactPage - Replica ContactPage.jsx do web
"""
import tkinter as tk
import customtkinter as ctk
import webbrowser
from pages.base_page import BasePage
from config import COLORS

class ContactPage(BasePage):
    """Página de contato - replica ContactPage.jsx"""
    
    def __init__(self, parent, on_logout, on_navigate_to_home, on_navigate_to_page,
                 current_page, user_info, on_navigate_to_profile):
        super().__init__(parent, on_logout, on_navigate_to_page, current_page, user_info, page_title="CONTATO", create_header_sidebar=False)
        
        self.on_navigate_to_home = on_navigate_to_home
        
        # Informações de contato do administrador
        self.admin_contact = {
            'email': 'admin2@helpwave.com',
            'phone': '(12) 99999-8888'
        }
        
        self._create_ui()
    
    def _create_ui(self):
        """Cria interface igual à versão web"""
        container = tk.Frame(self.main_content, bg="#F8F9FA")
        container.pack(fill=tk.BOTH, expand=True, padx=48, pady=48)
        
        # Botão voltar
        back_frame = tk.Frame(container, bg="#F8F9FA")
        back_frame.pack(fill="x", anchor="w", pady=(0, 20))
        
        back_btn = ctk.CTkButton(
            back_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color=COLORS['primary'],
            hover_color=COLORS['neutral_100'],
            anchor="w",
            command=self.on_navigate_to_home
        )
        back_btn.pack(side="left")
        
        # Header da página
        header_frame = tk.Frame(container, bg="#F8F9FA")
        header_frame.pack(fill=tk.X, pady=(0, 32))
        
        title_frame = tk.Frame(header_frame, bg="#F8F9FA")
        title_frame.pack()
        
        title_icon = tk.Label(title_frame, text="🎧", font=("Inter", 24), bg="#F8F9FA", fg="#A93226")
        title_icon.pack(side=tk.LEFT, padx=(0, 12))
        
        title_label = tk.Label(
            title_frame,
            text="Entre em Contato",
            font=("Inter", 32, "bold"),
            bg="#F8F9FA",
            fg="#262626"
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle = tk.Label(
            header_frame,
            text="Entre em contato com o administrador do sistema",
            font=("Inter", 16),
            bg="#F8F9FA",
            fg="#737373"
        )
        subtitle.pack(pady=(12, 0))
        
        # Conteúdo
        content_frame = tk.Frame(container, bg="#F8F9FA")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Introdução
        intro_frame = tk.Frame(content_frame, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        intro_frame.pack(fill=tk.X, pady=(0, 32))
        
        intro_inner = tk.Frame(intro_frame, bg="#FFFFFF")
        intro_inner.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)
        
        intro_text = tk.Label(
            intro_inner,
            text="Precisa entrar em contato com o administrador do sistema? Utilize os canais abaixo para suporte, dúvidas ou solicitações.",
            font=("Inter", 14),
            bg="#FFFFFF",
            fg="#262626",
            wraplength=800,
            justify="left"
        )
        intro_text.pack(anchor="w")
        
        # Cards de contato
        cards_frame = tk.Frame(content_frame, bg="#F8F9FA")
        cards_frame.pack(fill=tk.X, pady=(0, 32))
        cards_frame.grid_columnconfigure(0, weight=1, minsize=400)
        cards_frame.grid_columnconfigure(1, weight=1, minsize=400)
        
        # Card Email
        email_card = tk.Frame(cards_frame, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        email_card.grid(row=0, column=0, padx=12, pady=0, sticky="nsew")
        
        email_inner = tk.Frame(email_card, bg="#FFFFFF")
        email_inner.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)
        
        email_icon_frame = tk.Frame(email_inner, bg="#FFFFFF", width=60, height=60)
        email_icon_frame.pack()
        email_icon_frame.pack_propagate(False)
        
        email_icon = tk.Label(email_icon_frame, text="✉️", font=("Inter", 32), bg="#FFFFFF", fg="#A93226")
        email_icon.place(relx=0.5, rely=0.5, anchor="center")
        
        email_title = tk.Label(email_inner, text="E-mail", font=("Inter", 20, "bold"), bg="#FFFFFF", fg="#262626")
        email_title.pack(pady=(16, 8))
        
        email_desc = tk.Label(
            email_inner,
            text="Envie um e-mail para o administrador",
            font=("Inter", 14),
            bg="#FFFFFF",
            fg="#737373"
        )
        email_desc.pack(pady=(0, 16))
        
        email_link = tk.Label(
            email_inner,
            text=self.admin_contact['email'],
            font=("Inter", 14, "underline"),
            bg="#FFFFFF",
            fg="#A93226",
            cursor="hand2"
        )
        email_link.pack(pady=(0, 16))
        email_link.bind("<Button-1>", lambda e: self._handle_email_click())
        
        email_btn = tk.Button(
            email_inner,
            text="Enviar E-mail",
            font=("Inter", 14, "bold"),
            bg="#A93226",
            fg="white",
            activebackground="#8B0000",
            activeforeground="white",
            bd=0,
            relief=tk.FLAT,
            padx=24,
            pady=12,
            cursor="hand2",
            command=self._handle_email_click
        )
        email_btn.pack()
        
        # Card Telefone
        phone_card = tk.Frame(cards_frame, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        phone_card.grid(row=0, column=1, padx=12, pady=0, sticky="nsew")
        
        phone_inner = tk.Frame(phone_card, bg="#FFFFFF")
        phone_inner.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)
        
        phone_icon_frame = tk.Frame(phone_inner, bg="#FFFFFF", width=60, height=60)
        phone_icon_frame.pack()
        phone_icon_frame.pack_propagate(False)
        
        phone_icon = tk.Label(phone_icon_frame, text="📞", font=("Inter", 32), bg="#FFFFFF", fg="#A93226")
        phone_icon.place(relx=0.5, rely=0.5, anchor="center")
        
        phone_title = tk.Label(phone_inner, text="Telefone", font=("Inter", 20, "bold"), bg="#FFFFFF", fg="#262626")
        phone_title.pack(pady=(16, 8))
        
        phone_desc = tk.Label(
            phone_inner,
            text="Entre em contato por telefone",
            font=("Inter", 14),
            bg="#FFFFFF",
            fg="#737373"
        )
        phone_desc.pack(pady=(0, 16))
        
        phone_link = tk.Label(
            phone_inner,
            text=self.admin_contact['phone'],
            font=("Inter", 14, "underline"),
            bg="#FFFFFF",
            fg="#A93226",
            cursor="hand2"
        )
        phone_link.pack(pady=(0, 16))
        phone_link.bind("<Button-1>", lambda e: self._handle_phone_click())
        
        phone_btn = tk.Button(
            phone_inner,
            text="Ligar Agora",
            font=("Inter", 14, "bold"),
            bg="#A93226",
            fg="white",
            activebackground="#8B0000",
            activeforeground="white",
            bd=0,
            relief=tk.FLAT,
            padx=24,
            pady=12,
            cursor="hand2",
            command=self._handle_phone_click
        )
        phone_btn.pack()
        
        # Informação adicional
        info_box = tk.Frame(content_frame, bg="#FFF3CD", bd=1, relief=tk.SOLID)
        info_box.pack(fill=tk.X)
        
        info_inner = tk.Frame(info_box, bg="#FFF3CD")
        info_inner.pack(fill=tk.BOTH, expand=True, padx=24, pady=16)
        
        info_text = tk.Label(
            info_inner,
            text="Observação: Para questões relacionadas a chamados técnicos, utilize a funcionalidade de criar novo chamado no sistema.",
            font=("Inter", 14),
            bg="#FFF3CD",
            fg="#856404",
            wraplength=800,
            justify="left"
        )
        info_text.pack(anchor="w")
    
    def _handle_email_click(self):
        """Abre cliente de email"""
        email = self.admin_contact['email']
        subject = "Contato HelpWave"
        mailto_link = f"mailto:{email}?subject={subject}"
        webbrowser.open(mailto_link)
    
    def _handle_phone_click(self):
        """Abre dialer de telefone"""
        phone = self.admin_contact['phone'].replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
        tel_link = f"tel:{phone}"
        webbrowser.open(tel_link)


