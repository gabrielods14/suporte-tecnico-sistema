import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from supabase_service import supabase # Importa o cliente Supabase

class CreateUserPage(tk.Frame):
    """
    Página para cadastrar um novo usuário.
    Apenas acessível a usuários com hierarquia 'TI'.
    """
    def __init__(self, master_frame, dashboard_controller):
        super().__init__(master_frame, bg="#D3D3D3")
        self.pack(expand=True, fill=tk.BOTH, padx=50, pady=20)
        
        self.dashboard_controller = dashboard_controller
        self.background_light = "#D3D3D3"
        self.text_color_dark = "black"
        self.entry_bg = "#FFFFFF"

        # Frame central que centralizará o formulário
        self.form_container = tk.Frame(self, bg=self.background_light, padx=40, pady=30)
        self.form_container.pack(fill=tk.BOTH, expand=True)

        # Título removido para evitar duplicação (já existe na barra vermelha)

        # Campos do formulário em duas colunas usando grid
        self._create_form_field(self.form_container, "NOME COMPLETO", "nome_completo_entry", row=0, col=0)
        self._create_form_field(self.form_container, "LOGIN", "login_entry", row=0, col=1)
        self._create_form_field(self.form_container, "SENHA", "senha_entry", row=2, col=0, show="*")
        self._create_form_field(self.form_container, "DEPARTAMENTO", "departamento_entry", row=2, col=1)
        self._create_form_field(self.form_container, "E-MAIL", "email_entry", row=4, col=0)
        self._create_form_field(self.form_container, "TELEFONE", "telefone_entry", row=4, col=1)
        
        # O campo de Hierarquia foi removido

        # Botão de Envio
        tk.Button(self.form_container, text="CADASTRAR", font=("Inter", 12, "bold"), fg="white", bg="#8B0000", activebackground="#A52A2A", activeforeground="white", bd=0, relief=tk.FLAT, command=self._submit_user).grid(row=6, column=0, columnspan=2, pady=20, ipady=8, sticky="ew", padx=5)
        
        # Configuração para que as colunas se expandam
        self.form_container.grid_columnconfigure(0, weight=1)
        self.form_container.grid_columnconfigure(1, weight=1)

    def _create_form_field(self, parent, label_text, entry_name, row, col, show=None):
        """Cria um par de rótulos e entrada para o formulário usando grid."""
        tk.Label(parent, text=label_text, font=("Inter", 10, "bold"), fg=self.text_color_dark, bg=self.background_light, anchor="w").grid(row=row, column=col, sticky="ew", padx=5, pady=(10, 0))
        entry = tk.Entry(parent, font=("Inter", 12), bg=self.entry_bg, bd=1, relief=tk.SOLID, show=show, width=30)
        entry.grid(row=row+1, column=col, sticky="ew", padx=5, pady=(0, 15))
        setattr(self, entry_name, entry)

    def _submit_user(self):
        """Coleta os dados do formulário e envia para o Supabase."""
        user_data = {
            "nome_completo": self.nome_completo_entry.get(),
            "login": self.login_entry.get(),
            "senha": self.senha_entry.get(),
            "departamento": self.departamento_entry.get(),
            "email": self.email_entry.get(),
            "telefone": self.telefone_entry.get(),
            "Hierarquia": "user" # Valor fixo para usuários de nível "user"
        }

        # Validação simples
        if not all(user_data.values()):
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos obrigatórios.")
            return

        try:
            # Insere os dados no Supabase
            response = supabase.table("usuarios").insert(user_data).execute()

            if response.data:
                messagebox.showinfo("Sucesso", f"O usuário '{user_data['login']}' foi cadastrado com sucesso!")
                self._clear_form()
            else:
                messagebox.showerror("Erro de Cadastro", "Não foi possível cadastrar o usuário. Tente novamente.")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Ocorreu um erro ao cadastrar o usuário: {e}")

    def _clear_form(self):
        """Limpa todos os campos do formulário."""
        self.nome_completo_entry.delete(0, tk.END)
        self.login_entry.delete(0, tk.END)
        self.senha_entry.delete(0, tk.END)
        self.departamento_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)