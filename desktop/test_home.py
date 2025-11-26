"""
Script de teste para verificar se HomePage funciona
"""
import customtkinter as ctk
from home_page import HomePage

# Configuração do CustomTkinter
ctk.set_appearance_mode("light")

class TestApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Teste HomePage")
        self.root.geometry("1400x900")
        
        # Configura o grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Dados de teste
        user_info = {
            'nome': 'Gabriel Teste',
            'email': 'gabriel@teste.com',
            'permissao': 1
        }
        
        # Cria HomePage
        print("[TESTE] Criando HomePage...")
        try:
            self.home_page = HomePage(
                self.root,
                user_info=user_info,
                on_logout=lambda: print("Logout!"),
                on_navigate=lambda page: print(f"Navegar para: {page}"),
                current_page='home'
            )
            print("[TESTE] HomePage criada")
            self.home_page.grid(row=0, column=0, sticky="nsew")
            print("[TESTE] HomePage grid configurado")
            self.root.update()
            print("[TESTE] Root atualizado")
        except Exception as e:
            print(f"[TESTE] ERRO: {e}")
            import traceback
            traceback.print_exc()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TestApp()
    app.run()


