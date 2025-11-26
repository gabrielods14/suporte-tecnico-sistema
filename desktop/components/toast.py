"""
Componente Toast para exibir mensagens de feedback
Baseado no Toast.jsx do projeto web
"""
import customtkinter as ctk
from typing import Literal


class Toast(ctk.CTkToplevel):
    """Toast para exibir mensagens de sucesso, erro, etc."""
    
    def __init__(self, parent, message: str, type: Literal['success', 'error', 'info', 'warning'] = 'error'):
        super().__init__(parent)
        
        self.message = message
        self.type = type
        
        # Configuração da janela
        self.overrideredirect(True)  # Remove bordas
        self.attributes('-topmost', True)
        
        # Cores baseadas no tipo
        colors = {
            'success': ('#28A745', '#D4EDDA'),
            'error': ('#DC3545', '#F8D7DA'),
            'info': ('#17A2B8', '#D1ECF1'),
            'warning': ('#FFC107', '#FFF3CD')
        }
        
        bg_color, text_bg = colors.get(type, colors['error'])
        
        # Frame principal
        self.frame = ctk.CTkFrame(
            self,
            fg_color=text_bg,
            corner_radius=8,
            border_width=2,
            border_color=bg_color
        )
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Conteúdo
        content_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Calcula largura necessária baseada no tamanho da mensagem
        # Estima aproximadamente 8-10 pixels por caractere
        # Para mensagens longas, permite quebra em múltiplas linhas
        estimated_chars = len(message)
        
        # Se a mensagem for curta, tenta manter em uma linha
        # Se for longa, permite quebra (max 550px de largura)
        if estimated_chars < 60:
            # Mensagem curta: tenta caber em uma linha
            estimated_width = max(400, estimated_chars * 9 + 120)
        else:
            # Mensagem longa: permite quebra em 2-3 linhas
            estimated_width = 550
        
        # Define largura inicial da janela
        self.geometry(f"{estimated_width}x100")
        self.update_idletasks()
        
        # Frame interno para mensagem e botão
        inner_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        inner_frame.pack(fill="x")
        
        # Mensagem com wraplength calculado para permitir quebra adequada
        # Se a mensagem for longa, permite quebrar em múltiplas linhas
        wrap_length = estimated_width - 140  # Largura menos padding, botão e margens
        
        self.message_label = ctk.CTkLabel(
            inner_frame,
            text=message,
            text_color=bg_color,
            font=ctk.CTkFont(size=14, weight="normal"),
            wraplength=wrap_length,
            anchor="w",
            justify="left"
        )
        self.message_label.pack(side="left", padx=(0, 15), fill="x", expand=True)
        
        # Botão fechar
        close_btn = ctk.CTkButton(
            inner_frame,
            text="×",
            width=30,
            height=30,
            fg_color="transparent",
            text_color=bg_color,
            hover_color=bg_color,
            font=ctk.CTkFont(size=20, weight="bold"),
            command=self.close_toast
        )
        close_btn.pack(side="right")
        
        # Atualiza para calcular tamanho real
        self.update_idletasks()
        
        # Recalcula largura baseada no conteúdo real
        # Garante largura mínima para mensagens curtas
        label_width = self.message_label.winfo_reqwidth()
        button_width = 50  # Botão + espaçamento
        padding = 100  # padding total (20*2 + 15*2 + 10*2 + margens)
        
        # Largura final: usa o maior entre o estimado e o necessário
        final_width = max(estimated_width, min(label_width + button_width + padding, 600))
        
        # Ajusta altura baseada no conteúdo (permitindo múltiplas linhas)
        final_height = max(80, self.message_label.winfo_reqheight() + 40)
        
        # Posiciona no canto superior direito
        x = parent.winfo_rootx() + parent.winfo_width() - final_width - 20
        y = parent.winfo_rooty() + 20
        self.geometry(f"{final_width}x{final_height}+{x}+{y}")
        
        # Auto-close após 4 segundos usando after (mais seguro que threading.Timer)
        self.after(4000, self.close_toast)
    
    def close_toast(self):
        """Fecha o toast"""
        try:
            # Verifica se o widget ainda existe antes de destruir
            if self.winfo_exists():
                self.destroy()
        except Exception:
            pass  # Ignora erros ao destruir


def show_toast(parent, message: str, type: Literal['success', 'error', 'info', 'warning'] = 'error'):
    """Função helper para mostrar um toast"""
    toast = Toast(parent, message, type)
    return toast
