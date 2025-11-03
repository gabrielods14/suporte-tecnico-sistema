import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta
from supabase_service import supabase # Importa o cliente Supabase

class PendingCallsPage(tk.Frame):
    """
    Página de conteúdo que exibe uma tabela com todos os chamados em andamento
    do usuário logado.
    """
    def __init__(self, master_frame, user_info, dashboard_controller):
        super().__init__(master_frame, bg="#D3D3D3")
        self.pack(expand=True, fill=tk.BOTH)

        self.user_info = user_info
        self.dashboard_controller = dashboard_controller
        self.primary_color = "#8B0000"
        self.background_light = "#D3D3D3"
        self.text_color_dark = "black"
        self.text_color_light = "white"
        self.button_hover_color = "#A52A2A"
        
        # Estilos antigos removidos - agora usando cards modernos
        
        # Container principal moderno
        main_container = tk.Frame(self, bg=self.background_light)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=20)
        
        # Header apenas com botão de atualizar (título removido para evitar duplicação)
        header_frame = tk.Frame(main_container, bg=self.background_light)
        header_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Botão de atualizar moderno
        refresh_btn = tk.Button(header_frame, text="🔄 Atualizar", 
                                font=("Inter", 11, "bold"),
                                fg=self.text_color_light,
                                bg=self.primary_color,
                                activebackground=self.button_hover_color,
                                activeforeground=self.text_color_light,
                                bd=0, relief=tk.FLAT,
                                command=self._load_pending_calls,
                                cursor="hand2")
        refresh_btn.pack(side=tk.RIGHT, ipady=8, ipadx=15)
        
        # Container para os cards com scroll
        self.cards_container = tk.Frame(main_container, bg=self.background_light)
        self.cards_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para scroll
        self.canvas = tk.Canvas(self.cards_container, bg=self.background_light, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.cards_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.background_light)
        
        # Configurar o canvas para ocupar toda a largura
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind para ajustar a largura do frame scrollável
        def configure_scroll_region(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            # Ajustar largura do frame scrollável para ocupar toda a largura do canvas
            canvas_width = self.canvas.winfo_width()
            if canvas_width > 1:
                self.canvas.itemconfig(self.canvas.find_all()[0], width=canvas_width)
        
        self.scrollable_frame.bind("<Configure>", configure_scroll_region)
        self.canvas.bind("<Configure>", configure_scroll_region)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self._load_pending_calls()

    def _get_priority_map(self):
        """Busca os tipos de chamado e prioridades do Supabase."""
        try:
            response = supabase.table("tipos_chamado").select("nome", "Prioridade").execute()
            priority_map = {item['nome']: item['Prioridade'] for item in response.data}
            return priority_map
        except Exception as e:
            messagebox.showerror("Erro de Prioridades", f"Não foi possível carregar as prioridades dos chamados: {e}")
            return {}

    def _create_call_card(self, call_data, priority, open_date_formatted, due_date_formatted):
        """Cria um card moderno para um chamado."""
        # Cores baseadas na prioridade
        if priority == 'Alta':
            card_bg = "#FFEBEE"  # Vermelho claro
            border_color = "#F44336"
            priority_icon = "🔴"
        elif priority == 'Média':
            card_bg = "#FFF3E0"  # Laranja claro
            border_color = "#FF9800"
            priority_icon = "🟠"
        else:
            card_bg = "#F8F9FA"  # Cinza claro
            border_color = "#9E9E9E"
            priority_icon = "⚪"
        
        # Frame do card
        card_frame = tk.Frame(self.scrollable_frame, bg=card_bg, relief="solid", bd=1)
        card_frame.pack(fill=tk.X, padx=2, pady=8)
        
        # Header do card
        header_frame = tk.Frame(card_frame, bg=card_bg)
        header_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        # ID e prioridade
        id_frame = tk.Frame(header_frame, bg=card_bg)
        id_frame.pack(side=tk.LEFT)
        
        tk.Label(id_frame, text=f"🔢 {call_data.get('id', 'N/A')[:8]}", 
                font=("Inter", 10, "bold"), fg="#666666", bg=card_bg).pack(anchor="w")
        tk.Label(id_frame, text=f"{priority_icon} {priority}", 
                font=("Inter", 9), fg=border_color, bg=card_bg).pack(anchor="w")
        
        # Status
        status_frame = tk.Frame(header_frame, bg=card_bg)
        status_frame.pack(side=tk.RIGHT)
        
        status = call_data.get('STATUS', 'Aberto')
        if status == "Aberto":
            status_text = "🔴 Aberto"
            status_color = "#F44336"
        elif status == "Concluído":
            status_text = "✅ Concluído"
            status_color = "#4CAF50"
        else:
            status_text = f"⚪ {status}"
            status_color = "#9E9E9E"
            
        tk.Label(status_frame, text=status_text, 
                font=("Inter", 10, "bold"), fg=status_color, bg=card_bg).pack(anchor="e")
        
        # Conteúdo do card
        content_frame = tk.Frame(card_frame, bg=card_bg)
        content_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Tipo e título
        tk.Label(content_frame, text=f"📂 {call_data.get('tipo_chamado', 'N/A')}", 
                font=("Inter", 11, "bold"), fg=self.text_color_dark, bg=card_bg).pack(anchor="w")
        tk.Label(content_frame, text=f"📝 {call_data.get('titulo', 'N/A')}", 
                font=("Inter", 12), fg=self.text_color_dark, bg=card_bg, wraplength=800, justify="left").pack(anchor="w", pady=(5, 0))
        
        # Footer com datas
        footer_frame = tk.Frame(card_frame, bg=card_bg)
        footer_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        tk.Label(footer_frame, text=f"📅 Aberto em: {open_date_formatted}", 
                font=("Inter", 9), fg="#666666", bg=card_bg).pack(side=tk.LEFT)
        tk.Label(footer_frame, text=f"⏰ Limite: {due_date_formatted}", 
                font=("Inter", 9), fg="#666666", bg=card_bg).pack(side=tk.RIGHT)
        
        # Bind para clique
        def on_card_click(event):
            self.dashboard_controller.show_page('Detalhes do Chamado', call_id=call_data.get('id'))
        
        for widget in [card_frame, header_frame, content_frame, footer_frame]:
            widget.bind("<Button-1>", on_card_click)
            for child in widget.winfo_children():
                child.bind("<Button-1>", on_card_click)
        
        return card_frame

    def _load_pending_calls(self):
        """
        Carrega os chamados em andamento do usuário a partir do Supabase e
        cria cards modernos, aplicando a lógica de hierarquia.
        """
        # Limpa os cards existentes
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        user_login = self.user_info.get('login')
        user_hierarchy = self.user_info.get('Hierarquia')

        if not user_login:
            messagebox.showwarning("Erro de Usuário", "Não foi possível identificar o usuário logado.")
            return

        priority_map = self._get_priority_map()
        if not priority_map:
            return

        try:
            # Lógica para filtrar por hierarquia
            if user_hierarchy and user_hierarchy.upper() == 'TI':
                # Usuário é do TI, mostrar todos os chamados em aberto
                response = supabase.table("chamados").select("*").or_("STATUS.eq.Aberto,STATUS.is.null").order("data_abertura", desc=True).execute()
            elif user_hierarchy and user_hierarchy.lower() == 'user':
                # Usuário comum, mostrar apenas seus próprios chamados
                response = supabase.table("chamados").select("*").eq("usuario_login", user_login).or_("STATUS.eq.Aberto,STATUS.is.null").order("data_abertura", desc=True).execute()
            else:
                # Caso a hierarquia não seja reconhecida, assume-se que é um usuário comum
                response = supabase.table("chamados").select("*").eq("usuario_login", user_login).or_("STATUS.eq.Aberto,STATUS.is.null").order("data_abertura", desc=True).execute()

            for call in response.data:
                call_type = call.get('tipo_chamado')
                open_date_str = call.get('data_abertura')
                
                if open_date_str:
                    open_date = datetime.fromisoformat(open_date_str).date()
                else:
                    open_date = datetime.now().date()

                priority = priority_map.get(call_type, 'Baixa')
                
                due_date = None
                if priority == 'Baixa':
                    due_date = open_date + timedelta(days=30)
                elif priority == 'Média':
                    due_date = open_date + timedelta(days=15)
                elif priority == 'Alta':
                    due_date = open_date + timedelta(days=5)

                open_date_formatted = open_date.strftime("%d/%m/%Y")
                due_date_formatted = due_date.strftime("%d/%m/%Y") if due_date else "N/A"
                
                # Cria o card do chamado
                self._create_call_card(call, priority, open_date_formatted, due_date_formatted)

        except Exception as e:
            messagebox.showerror("Erro de Carregamento", f"Ocorreu um erro ao carregar os chamados: {e}")

    def _on_card_click(self, call_id):
        """
        Lida com o clique em um card, abrindo a página de detalhes.
        """
        self.dashboard_controller.show_page('Detalhes do Chamado', call_id=call_id)