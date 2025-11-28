"""Teste simples para verificar se HomePage funciona"""
import customtkinter as ctk
from home_page import HomePage

ctk.set_appearance_mode("light")

root = ctk.CTk()
root.title("Teste")
root.geometry("1400x900")

# Configura grid
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Dados de teste
user_info = {'nome': 'Gabriel', 'email': 'gabriel@teste.com', 'permissao': 1}

# Callbacks de teste
def on_logout():
    print("Logout!")

def on_navigate(page_id):
    print(f"Navegar para: {page_id}")

# Cria HomePage
print("Criando HomePage...")
home = HomePage(root, user_info, on_logout, on_navigate, 'home')
print("HomePage criado")
home.grid(row=0, column=0, sticky="nsew")
print("Grid configurado")

root.update_idletasks()
root.update()
print("Atualizado")

root.mainloop()





