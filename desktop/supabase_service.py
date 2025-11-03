# supabase_service.py
from supabase import create_client, Client
from tkinter import messagebox
import config

# Inicializa o cliente Supabase
def create_supabase_client() -> Client:
    """
    Cria e retorna uma instância do cliente Supabase.
    Exibe uma mensagem de erro e sai do aplicativo se a conexão falhar.
    """
    try:
        supabase_client: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        return supabase_client
    except Exception as e:
        messagebox.showerror("Erro de Conexão Supabase", f"Não foi possível conectar ao Supabase: {e}\nPor favor, verifique sua chave de API e sua conexão com a internet.")
        exit() # Sai da aplicação em caso de erro de conexão

supabase = create_supabase_client()