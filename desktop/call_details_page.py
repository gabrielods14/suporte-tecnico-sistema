import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from supabase_service import supabase # Importa o cliente Supabase

class CallDetailsPage(tk.Frame):
    """
    Página de conteúdo para exibir os detalhes de um chamado específico,
    com um layout corrigido e responsivo.
    """
    def __init__(self, master_frame, call_id, dashboard_controller, user_info):
        super().__init__(master_frame, bg="#D3D3D3")
        self.pack(expand=True, fill=tk.BOTH, padx=10, pady=20)

        self.call_id = call_id
        self.dashboard_controller = dashboard_controller
        self.user_info = user_info
        self.primary_color = "#8B0000"
        self.background_light = "#D3D3D3"
        self.text_color_dark = "black"
        self.text_color_light = "white"
        self.button_hover_color = "#A52A2A"
        
        # Cria um Canvas para a barra de rolagem
        self.canvas = tk.Canvas(self, bg=self.background_light, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.details_frame = tk.Frame(self.canvas, bg=self.background_light, padx=40, pady=30, bd=0, highlightthickness=0)
        self.canvas.create_window((0, 0), window=self.details_frame, anchor="nw")

        self.details_frame.bind("<Configure>", lambda event, canvas=self.canvas: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.resolution_text_widget = None
        self.resolution_status_var = tk.StringVar()
        self._load_call_details()

    def _load_call_details(self):
        """Busca os detalhes do chamado e do usuário no Supabase."""
        try:
            response_call = supabase.table("chamados").select("*").eq("id", self.call_id).execute()
            call_data = response_call.data[0] if response_call.data else None

            if not call_data:
                messagebox.showerror("Chamado Não Encontrado", "O chamado selecionado não pôde ser encontrado.")
                self.dashboard_controller.show_page('Chamados em Andamento')
                return

            user_login = call_data.get('usuario_login')
            response_user = supabase.table("usuarios").select("*").eq("login", user_login).execute()
            user_data = response_user.data[0] if response_user.data else {}

            self._display_details(call_data, user_data)

        except Exception as e:
            messagebox.showerror("Erro de Carregamento", f"Ocorreu um erro ao carregar os detalhes do chamado: {e}")
            self.dashboard_controller.show_page('Chamados em Andamento')

    def _create_modern_info_item(self, parent, icon, title, content, column, colspan=1):
        """Cria um item de informação moderno com ícone."""
        item_frame = tk.Frame(parent, bg="white")
        item_frame.grid(row=0, column=column, sticky="ew", padx=10, pady=5)
        
        # Ícone e título
        header_frame = tk.Frame(item_frame, bg="white")
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(header_frame, text=icon, font=("Inter", 12), fg=self.primary_color, bg="white").pack(side=tk.LEFT)
        tk.Label(header_frame, text=title, font=("Inter", 10, "bold"), fg="#666666", bg="white").pack(side=tk.LEFT, padx=(5, 0))
        
        # Conteúdo
        content_label = tk.Label(item_frame, text=content, font=("Inter", 12), fg=self.text_color_dark, bg="white", anchor="w", wraplength=200)
        content_label.pack(fill=tk.X)
        
        # Configurar peso da coluna
        parent.grid_columnconfigure(column, weight=1)
        
        return item_frame

    def _get_ai_suggestion(self, call_type):
        """Gera uma sugestão de resolução com base no tipo de chamado, agora mais detalhada."""
        suggestions = {
            'Problema de Hardware': "Comece com uma verificação visual do equipamento. Em seguida, verifique todas as conexões de cabos (energia, dados) para garantir que estão firmes. Se o problema persistir, reinicie o sistema e tente executar um diagnóstico de hardware. Se houver componentes removíveis, como memória ou disco, verifique a posição deles. Finalmente, se nada funcionar, considere a necessidade de substituir o hardware ou encaminhar para um reparo especializado.",
            'Problema de Software': "Inicie a análise buscando por atualizações pendentes do software ou do sistema operacional, pois muitos problemas são corrigidos assim. Caso o software não inicie, tente executar uma reparação ou reinstalação. Verifique se há conflitos com outros programas ou se o software tem permissão para rodar. Uma limpeza de cache e arquivos temporários também pode ser útil para resolver falhas e comportamentos inesperados do aplicativo. Se a falha for crítica, pode ser necessário restaurar o sistema para um ponto anterior ou em último caso formatar e reinstalar o SO.",
            'Solicitação de Serviço': "Para este tipo de chamado, a primeira etapa é entender a viabilidade e as restrições da solicitação. Identifique todos os recursos, licenças e permissões necessárias. Comunique o prazo de atendimento ao usuário e verifique a disponibilidade de equipe para executar a tarefa. Se o serviço for complexo, divida-o em etapas menores e forneça feedback ao usuário sobre o progresso. Ao concluir, peça a confirmação da solução e feche o chamado, documentando o processo.",
            'Outros': "Dado que o problema não se encaixa nas categorias padrão, é crucial uma análise detalhada da descrição. Utilize palavras-chave da descrição para realizar uma pesquisa em bases de conhecimento internas ou na web. Se a informação fornecida pelo usuário for insuficiente, entre em contato para solicitar mais detalhes, como mensagens de erro, capturas de tela ou o momento em que o problema começou. Documente todas as etapas de diagnóstico para futuras consultas e, ao encontrar a solução, descreva-a de forma clara para o usuário."
        }
        return suggestions.get(call_type, suggestions['Outros'])[:500]

    def _submit_resolution(self):
        """Envia a resolução do chamado para o Supabase e atualiza o status."""
        resolution = self.resolution_text_widget.get("1.0", tk.END).strip()
        resolution_status = self.resolution_status_var.get()
        
        if not resolution or not resolution_status:
            messagebox.showwarning("Campos Vazios", "A resolução e o status do chamado não podem estar vazios.")
            return

        final_status = "Concluído" if resolution_status == "Sim" else "Aberto"
        
        try:
            response = supabase.table("chamados").update({
                "STATUS": final_status,
                "resolucao": resolution
            }).eq("id", self.call_id).execute()

            if response.data:
                messagebox.showinfo("Sucesso", "O chamado foi atualizado com sucesso!")
                self.dashboard_controller.show_page('Chamados em Andamento')
            else:
                error_message = response.error.get('message', 'Erro desconhecido.') if response.error else 'Erro desconhecido.'
                messagebox.showerror("Erro", f"Não foi possível atualizar o chamado: {error_message}")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Ocorreu um erro ao enviar a resolução: {e}")

    def _display_details(self, call_data, user_data):
        """Cria e exibe os widgets com os detalhes do chamado e do usuário, com base na hierarquia."""
        
        # --- Frame principal moderno ---
        main_content_frame = tk.Frame(self.details_frame, bg=self.background_light)
        main_content_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=20)

        user_hierarchy = self.user_info.get('Hierarquia', '').upper()
        
        # --- Card de Informações Principais ---
        info_card = tk.Frame(main_content_frame, bg="white", relief="solid", bd=1)
        info_card.pack(fill=tk.X, pady=(0, 0))
        
        # Header do card
        card_header = tk.Frame(info_card, bg=self.primary_color, height=50)
        card_header.pack(fill=tk.X)
        card_header.pack_propagate(False)
        
        tk.Label(card_header, text="📋 INFORMAÇÕES DO CHAMADO", 
                font=("Inter", 14, "bold"), fg=self.text_color_light, bg=self.primary_color).pack(pady=15)
        
        # Conteúdo do card em grid moderno
        content_frame = tk.Frame(info_card, bg="white")
        content_frame.pack(fill=tk.X, padx=15, pady=20)
        
        # Linha 1: Tipo, Status, Código
        row1_frame = tk.Frame(content_frame, bg="white")
        row1_frame.pack(fill=tk.X, pady=(0, 15))
        
        self._create_modern_info_item(row1_frame, "📂", "TIPO DO CHAMADO", call_data.get('tipo_chamado', 'N/A'), 0)
        self._create_modern_info_item(row1_frame, "⚡", "STATUS", call_data.get('STATUS', 'N/A'), 1)
        self._create_modern_info_item(row1_frame, "🔢", "CÓDIGO", call_data.get('id', 'N/A')[:8], 2)
        
        # Linha 2: Título
        row2_frame = tk.Frame(content_frame, bg="white")
        row2_frame.pack(fill=tk.X, pady=(0, 15))
        
        self._create_modern_info_item(row2_frame, "📝", "TÍTULO", call_data.get('titulo', 'N/A'), 0, colspan=3)
        
        # Linha 3: Usuário, Email, Telefone
        row3_frame = tk.Frame(content_frame, bg="white")
        row3_frame.pack(fill=tk.X, pady=(0, 15))
        
        self._create_modern_info_item(row3_frame, "👤", "ABERTO POR", user_data.get('login', 'N/A'), 0)
        self._create_modern_info_item(row3_frame, "📧", "E-MAIL", user_data.get('email', 'N/A'), 1)
        self._create_modern_info_item(row3_frame, "📞", "TELEFONE", user_data.get('telefone', 'N/A'), 2)
        
        # Linha 4: Datas
        row4_frame = tk.Frame(content_frame, bg="white")
        row4_frame.pack(fill=tk.X)
        
        open_date = call_data.get('data_abertura', 'N/A').split('T')[0] if call_data.get('data_abertura') else 'N/A'
        self._create_modern_info_item(row4_frame, "📅", "ABERTO EM", open_date, 0)
        self._create_modern_info_item(row4_frame, "⏰", "DATA LIMITE", "N/A", 1)
        self._create_modern_info_item(row4_frame, "🕒", "PRIORIDADE", "Alta", 2)

        # --- Card de Descrição ---
        desc_card = tk.Frame(main_content_frame, bg="white", relief="solid", bd=1)
        desc_card.pack(fill=tk.X, pady=(0, 0))
        
        # Header da descrição
        desc_header = tk.Frame(desc_card, bg="#F5F5F5", height=40)
        desc_header.pack(fill=tk.X)
        desc_header.pack_propagate(False)
        
        tk.Label(desc_header, text="📄 DESCRIÇÃO", 
                font=("Inter", 12, "bold"), fg=self.text_color_dark, bg="#F5F5F5").pack(pady=10)
        
        # Conteúdo da descrição
        desc_content = tk.Frame(desc_card, bg="white")
        desc_content.pack(fill=tk.X, padx=15, pady=20)
        
        desc_text = call_data.get('descricao', 'N/A')
        if desc_text == 'N/A' or not desc_text:
            desc_text = "Nenhuma descrição fornecida."
            
        tk.Label(desc_content, text=desc_text, font=("Inter", 12), fg=self.text_color_dark, bg="white", 
                wraplength=800, justify=tk.LEFT, anchor="w").pack(fill=tk.X)


        # --- Lógica de Hierarquia para a exibição de campos extras ---
        if user_hierarchy == 'TI' and call_data.get('STATUS') != 'Concluído':
            # --- Card de Sugestão da IA ---
            ai_card = tk.Frame(main_content_frame, bg="white", relief="solid", bd=1)
            ai_card.pack(fill=tk.X, pady=(0, 0))
            
            # Header da IA
            ai_header = tk.Frame(ai_card, bg="#E3F2FD", height=40)
            ai_header.pack(fill=tk.X)
            ai_header.pack_propagate(False)
            
            tk.Label(ai_header, text="🤖 SUGESTÃO DA IA", 
                    font=("Inter", 12, "bold"), fg="#1976D2", bg="#E3F2FD").pack(pady=10)
            
            # Conteúdo da IA
            ai_content = tk.Frame(ai_card, bg="white")
            ai_content.pack(fill=tk.X, padx=15, pady=20)
            
            ai_suggestion = self._get_ai_suggestion(call_data.get('tipo_chamado'))
            tk.Label(ai_content, text=ai_suggestion, font=("Inter", 11), fg="#666666", bg="white", 
                    wraplength=800, justify=tk.LEFT, anchor="w").pack(fill=tk.X)

            # --- Card de Resolução do TI ---
            resolution_card = tk.Frame(main_content_frame, bg="white", relief="solid", bd=1)
            resolution_card.pack(fill=tk.X, pady=(0, 0))
            
            # Header da resolução
            resolution_header = tk.Frame(resolution_card, bg="#FFF3E0", height=40)
            resolution_header.pack(fill=tk.X)
            resolution_header.pack_propagate(False)
            
            tk.Label(resolution_header, text="✍️ RESOLUÇÃO DO TI", 
                    font=("Inter", 12, "bold"), fg="#F57C00", bg="#FFF3E0").pack(pady=10)
            
            # Conteúdo da resolução
            resolution_content = tk.Frame(resolution_card, bg="white")
            resolution_content.pack(fill=tk.X, padx=15, pady=20)
            
            # Campo de texto para resolução
            self.resolution_text_widget = tk.Text(resolution_content, font=("Inter", 12), bd=1, relief=tk.SOLID, 
                                                height=6, bg="white", wrap=tk.WORD)
            self.resolution_text_widget.pack(fill=tk.X, pady=(0, 15))

            # Status de resolução
            status_frame = tk.Frame(resolution_content, bg="white")
            status_frame.pack(fill=tk.X, pady=(0, 15))
            
            tk.Label(status_frame, text="O chamado foi resolvido?", font=("Inter", 11, "bold"), 
                    fg=self.text_color_dark, bg="white").pack(side=tk.LEFT)
            
            self.resolution_status_var.set("Não")
            resolution_options = ["Sim", "Não"]
            status_combobox = ttk.Combobox(status_frame, textvariable=self.resolution_status_var, 
                                         values=resolution_options, state="readonly", font=("Inter", 11))
            status_combobox.pack(side=tk.RIGHT, padx=(10, 0))
            
            # Botão de envio moderno
            tk.Button(resolution_content, text="🚀 ENVIAR RESOLUÇÃO", 
                     font=("Inter", 12, "bold"), fg=self.text_color_light, bg=self.primary_color, 
                     activebackground=self.button_hover_color, activeforeground=self.text_color_light,
                     bd=0, relief=tk.FLAT, command=self._submit_resolution, cursor="hand2").pack(fill=tk.X, ipady=10)
        
        elif call_data.get('resolucao'):
            # --- Card de Resolução (para chamados concluídos) ---
            resolution_display_card = tk.Frame(main_content_frame, bg="white", relief="solid", bd=1)
            resolution_display_card.pack(fill=tk.X, pady=(0, 0))
            
            # Header da resolução
            resolution_header = tk.Frame(resolution_display_card, bg="#E8F5E8", height=40)
            resolution_header.pack(fill=tk.X)
            resolution_header.pack_propagate(False)
            
            tk.Label(resolution_header, text="✅ RESOLUÇÃO", 
                    font=("Inter", 12, "bold"), fg="#2E7D32", bg="#E8F5E8").pack(pady=10)
            
            # Conteúdo da resolução
            resolution_content = tk.Frame(resolution_display_card, bg="white")
            resolution_content.pack(fill=tk.X, padx=15, pady=20)
            
            tk.Label(resolution_content, text=call_data.get('resolucao'), font=("Inter", 12), 
                    fg=self.text_color_dark, bg="white", wraplength=800, justify=tk.LEFT, anchor="w").pack(fill=tk.X)

        # Botão de voltar moderno
        tk.Button(main_content_frame, text="⬅️ VOLTAR", 
                 font=("Inter", 12, "bold"), fg=self.text_color_light, bg=self.primary_color, 
                 activebackground=self.button_hover_color, activeforeground=self.text_color_light,
                 bd=0, relief=tk.FLAT, command=lambda: self.dashboard_controller.show_page('Chamados em Andamento'),
                 cursor="hand2").pack(pady=20, ipady=10, fill=tk.X)