"""Teste direto do fluxo de login"""
import customtkinter as ctk
from login_page import LoginPage
from home_page import HomePage

ctk.set_appearance_mode("light")

root = ctk.CTk()
root.title("Teste Login Flow")
root.geometry("1400x900")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

main_frame = None

def on_login_success(user_data):
    global main_frame
    print(f"CALLBACK CHAMADO! user_data: {user_data}")
    
    # Remove login
    if main_frame:
        print("Destruindo login...")
        main_frame.destroy()
        main_frame = None
    
    # Cria home
    print("Criando HomePage...")
    main_frame = HomePage(
        root,
        user_info=user_data,
        on_logout=lambda: print("Logout"),
        on_navigate=lambda page: print(f"Navigate: {page}"),
        current_page='home'
    )
    print("HomePage criado")
    main_frame.grid(row=0, column=0, sticky="nsew")
    print("HomePage grid configurado")
    root.update()
    print("Root atualizado")
    print(f"HomePage visível: {main_frame.winfo_viewable()}")
    print(f"HomePage size: {main_frame.winfo_width()}x{main_frame.winfo_height()}")

# Cria login
print("Criando LoginPage...")
main_frame = LoginPage(root, on_login_success)
main_frame.grid(row=0, column=0, sticky="nsew")
print("LoginPage criado e configurado")

root.mainloop()





