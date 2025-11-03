# main.py
import tkinter as tk
from login_page import LoginApp
from dashboard_base import DashboardBase

class AppManager:
    """
    Gerencia o fluxo principal do aplicativo, alternando entre a tela de login
    e o dashboard principal.
    """
    def __init__(self, master):
        self.master = master
        self.master.geometry("1200x800") # Tamanho inicial da janela
        self.master.resizable(True, True) # Permite redimensionar

        self.current_view = None # Para manter referência à tela atual (LoginApp ou DashboardBase)
        self.user_data = None # Para armazenar os dados do usuário logado

        self.show_login_page()

    def show_login_page(self):
        """Exibe a tela de login."""
        if self.current_view:
            self.current_view.destroy()
        self.current_view = LoginApp(self.master, self.on_login_success)

    def on_login_success(self, user_info):
        """Callback chamada quando o login é bem-sucedido."""
        self.user_data = user_info
        self.show_dashboard()

    def show_dashboard(self):
        """Exibe o dashboard principal após o login."""
        if self.current_view:
            self.current_view.destroy()
        self.current_view = DashboardBase(self.master, self.user_data, self) # Passa 'self' como app_manager_callback

if __name__ == "__main__":
    root = tk.Tk()
    app_manager = AppManager(root)
    root.mainloop()

