import tkinter as tk
from tkinter import messagebox
from supabase import create_client

from config import SUPABASE_URL, SUPABASE_KEY

# Inicializa o cliente Supabase aqui para que seja acessível a todas as classes
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    messagebox.showerror("Erro de Conexão Supabase", f"Não foi possível conectar ao Supabase: {e}")
    exit()

class LoginApp:
    def __init__(self, master, app_controller):
        self.master = master
        self.app_controller = app_controller  # Referência ao controlador para mudar de tela
        self.frame = tk.Frame(master, bg="#1C1C1C")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Configurações de cores da interface
        self.primary_color = "#8B0000"
        self.background_dark = "#1C1C1C"
        self.text_color_light = "white"
        self.entry_bg = "#D3D3D3"
        self.button_hover_color = "#A52A2A"

        # Frame da seção vermelha (esquerda)
        self.red_section = tk.Frame(self.frame, bg=self.primary_color, width=400)
        self.red_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        self.red_section.pack_propagate(False)

        # Frame da seção preta (direita) com o formulário de login
        self.login_section = tk.Frame(self.frame, bg=self.background_dark)
        self.login_section.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Centraliza o formulário de login
        self.login_form_frame = tk.Frame(self.login_section, bg=self.background_dark)
        self.login_form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Componentes do formulário
        self.login_label = tk.Label(self.login_form_frame, text="LOGIN", font=("Inter", 16, "bold"), fg=self.text_color_light, bg=self.background_dark)
        self.login_label.grid(row=0, column=0, columnspan=2, pady=20)

        self.username_label = tk.Label(self.login_form_frame, text="UTILIZADOR", font=("Inter", 10), fg=self.text_color_light, bg=self.background_dark)
        self.username_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.username_entry = tk.Entry(self.login_form_frame, width=30, font=("Inter", 12), bg=self.entry_bg, bd=0, relief=tk.FLAT)
        self.username_entry.grid(row=2, column=0, columnspan=2, pady=(0, 10), ipady=5)

        self.password_label = tk.Label(self.login_form_frame, text="SENHA", font=("Inter", 10), fg=self.text_color_light, bg=self.background_dark)
        self.password_label.grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        self.password_entry = tk.Entry(self.login_form_frame, width=30, show="*", font=("Inter", 12), bg=self.entry_bg, bd=0, relief=tk.FLAT)
        self.password_entry.grid(row=4, column=0, columnspan=2, pady=(0, 10), ipady=5)

        self.remember_var = tk.BooleanVar()
        self.remember_checkbox = tk.Checkbutton(self.login_form_frame, text="Lembrar", variable=self.remember_var, fg=self.text_color_light, bg=self.background_dark, selectcolor=self.background_dark, activebackground=self.background_dark, activeforeground=self.text_color_light, font=("Inter", 9))
        self.remember_checkbox.grid(row=5, column=0, sticky=tk.W, pady=(0, 10))

        self.forgot_password_button = tk.Button(self.login_form_frame, text="Esqueci a senha", fg=self.primary_color, bg=self.background_dark, bd=0, relief=tk.FLAT, font=("Inter", 9, "underline"), cursor="hand2", command=self._forgot_password_placeholder)
        self.forgot_password_button.grid(row=5, column=1, sticky=tk.E, pady=(0, 10))

        self.login_button = tk.Button(self.login_form_frame, text="ENTRAR", font=("Inter", 12, "bold"), fg=self.text_color_light, bg=self.primary_color, activebackground=self.button_hover_color, activeforeground=self.text_color_light, width=20, height=1, bd=0, relief=tk.FLAT, command=self._login)
        self.login_button.grid(row=6, column=0, columnspan=2, pady=20, ipady=5)

        self.master.bind('<Return>', lambda event=None: self._login())
        
    def _login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos de login.")
            return

        try:
            response = supabase.table("usuarios").select("*").eq("login", username).eq("senha", password).execute()

            user_data = response.data
            if user_data:
                messagebox.showinfo("Login Sucesso", "Login realizado com sucesso!")
                self.app_controller.show_page("homepage", user_data[0]) # Chama o controlador para mudar para a página inicial
            else:
                messagebox.showerror("Erro de Login", "Utilizador ou senha inválidos.")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Ocorreu um erro ao tentar fazer login: {e}")

    def _forgot_password_placeholder(self):
        messagebox.showinfo("Esqueci a Senha", "Funcionalidade 'Esqueci a senha' ainda não implementada.")