import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from supabase_service import supabase # Importa o cliente Supabase

class NewCallPage(tk.Frame):
    """
    Página de conteúdo para 'Novo Chamado'.
    Permite ao utilizador preencher os detalhes de um novo chamado.
    """
    def __init__(self, master_frame, user_login, dashboard_controller):
        super().__init__(master_frame, bg="#D3D3D3")
        self.pack(expand=True, fill=tk.BOTH, padx=50, pady=20)

        self.user_login = user_login
        self.dashboard_controller = dashboard_controller # Referência ao DashboardBase
        self.types_of_call = []

        self.primary_color = "#8B0000"
        self.background_light = "#D3D3D3"
        self.text_color_dark = "black"
        self.text_color_light = "white"
        self.entry_bg = "#FFFFFF"
        self.button_bg = "#8B0000"
        self.button_hover_color = "#A52A2A"

        # Container principal sem fundo branco
        main_container = tk.Frame(self, bg=self.background_light)
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Título da página integrado
        title_frame = tk.Frame(main_container, bg=self.background_light)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        tk.Label(title_frame, text="✎ NOVO CHAMADO", 
                font=("Inter", 16, "bold"), 
                fg=self.text_color_dark, 
                bg=self.background_light).pack(side=tk.LEFT)
        
        # Formulário integrado sem container branco
        self.new_call_form_frame = tk.Frame(main_container, bg=self.background_light)
        self.new_call_form_frame.pack(expand=True, fill=tk.BOTH)

        # --- Campo TIPO DE CHAMADO (Dropdown) ---
        type_frame = tk.Frame(self.new_call_form_frame, bg=self.background_light)
        type_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(type_frame, text="📂 TIPO DE CHAMADO *", font=("Inter", 11, "bold"), fg=self.text_color_dark, bg=self.background_light, anchor="w").pack(fill=tk.X, pady=(0, 8))
        self.type_call_var = tk.StringVar()
        self.type_call_combobox = ttk.Combobox(type_frame, textvariable=self.type_call_var, state="readonly", font=("Inter", 12))
        self.type_call_combobox.pack(fill=tk.X, ipady=8)
        self._load_call_types() # Carrega os tipos de chamado do Supabase

        # --- Campo TÍTULO DO CHAMADO ---
        title_frame = tk.Frame(self.new_call_form_frame, bg=self.background_light)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(title_frame, text="📝 TÍTULO DO CHAMADO", font=("Inter", 11, "bold"), fg=self.text_color_dark, bg=self.background_light, anchor="w").pack(fill=tk.X, pady=(0, 8))
        self.title_entry = tk.Entry(title_frame, font=("Inter", 12), bg=self.entry_bg, bd=1, relief=tk.SOLID, insertbackground="black")
        self.title_entry.pack(fill=tk.X, ipady=8)

        # --- Campo DESCRIÇÃO ---
        desc_frame = tk.Frame(self.new_call_form_frame, bg=self.background_light)
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        tk.Label(desc_frame, text="📄 DESCRIÇÃO", font=("Inter", 11, "bold"), fg=self.text_color_dark, bg=self.background_light, anchor="w").pack(fill=tk.X, pady=(0, 8))
        self.description_text = tk.Text(desc_frame, font=("Inter", 12), bg=self.entry_bg, bd=1, relief=tk.SOLID, height=8, insertbackground="black")
        self.description_text.pack(fill=tk.BOTH, expand=True)

        # --- Botão ENVIAR ---
        self.submit_button = tk.Button(self.new_call_form_frame, text="🚀 ENVIAR CHAMADO", 
                                      font=("Inter", 13, "bold"), fg=self.text_color_light, bg=self.button_bg, 
                                      activebackground=self.button_hover_color, activeforeground=self.text_color_light, 
                                      bd=0, relief=tk.FLAT, command=self._submit_call, cursor="hand2")
        self.submit_button.pack(pady=(20, 0), ipady=12, fill=tk.X)

        # Bind para a tecla Enter (submeter o chamado)
        self.bind('<Return>', lambda event=None: self._submit_call())

    def _load_call_types(self):
        """Carrega os tipos de chamado do Supabase para o combobox."""
        try:
            response = supabase.table("tipos_chamado").select("nome").execute()
            if response.data:
                self.types_of_call = [item['nome'] for item in response.data]
                self.type_call_combobox['values'] = self.types_of_call
                if self.types_of_call:
                    self.type_call_combobox.set(self.types_of_call[0]) # Seleciona o primeiro por padrão
            else:
                messagebox.showwarning("Erro de Tipos de Chamado", "Não foi possível carregar os tipos de chamado do Supabase.")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Ocorreu um erro ao carregar os tipos de chamado: {e}")

    def _submit_call(self):
        """Envia os dados do novo chamado para o banco de dados 'chamados' no Supabase."""
        selected_type = self.type_call_var.get()
        title = self.title_entry.get()
        description = self.description_text.get("1.0", tk.END).strip()

        if not selected_type or not title:
            messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha o 'Tipo de Chamado' e o 'Título do Chamado'.")
            return

        call_data = {
            "usuario_login": self.user_login,
            "tipo_chamado": selected_type,
            "titulo": title,
            "descricao": description if description else None,
            "STATUS": "Aberto" # AQUI: Adiciona o status 'Aberto' ao chamado
        }

        try:
            response = supabase.table("chamados").insert(call_data).execute()

            if response.data:
                messagebox.showinfo("Chamado Enviado", "Seu chamado foi registrado com sucesso!")
                self.dashboard_controller.show_page('Home') # Volta para a página Home após o envio
            else:
                error_message = response.error.get('message', 'Erro desconhecido ao registrar o chamado.') if response.error else 'Erro desconhecido.'
                messagebox.showerror("Erro ao Enviar Chamado", f"Falha ao registrar chamado: {error_message}")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Ocorreu um erro ao enviar o chamado: {e}")
