# supabase_service.py
from supabase import create_client, Client
from tkinter import messagebox
import config

# Variável global para armazenar o cliente Supabase (inicialização lazy)
_supabase_client = None

# Inicializa o cliente Supabase
def create_supabase_client() -> Client:
    """
    Cria e retorna uma instância do cliente Supabase.
    Retorna None se as credenciais não estiverem configuradas.
    """
    global _supabase_client
    
    # Verifica se já foi criado
    if _supabase_client is not None:
        return _supabase_client
    
    # Verifica se as credenciais estão configuradas
    if not config.SUPABASE_URL or not config.SUPABASE_KEY:
        print("[AVISO] Supabase não configurado. Configure SUPABASE_URL e SUPABASE_KEY no config.py ou variáveis de ambiente.")
        return None
    
    try:
        _supabase_client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        return _supabase_client
    except Exception as e:
        print(f"[ERRO] Não foi possível conectar ao Supabase: {e}")
        return None

# Função para obter o cliente Supabase (lazy initialization)
def get_supabase_client() -> Client:
    """
    Retorna o cliente Supabase, criando-o se necessário.
    Retorna None se não estiver configurado.
    """
    return create_supabase_client()

# Mantém compatibilidade com código que importa 'supabase' diretamente
# Mas agora usa inicialização lazy para não quebrar na importação
def _get_supabase():
    """Wrapper para manter compatibilidade com import direto"""
    client = get_supabase_client()
    if client is None:
        raise RuntimeError("Supabase não está configurado. Configure SUPABASE_URL e SUPABASE_KEY no config.py")
    return client

# Cria uma propriedade que inicializa apenas quando acessada
class SupabaseProxy:
    """Proxy para inicialização lazy do Supabase"""
    def __getattr__(self, name):
        client = get_supabase_client()
        if client is None:
            raise RuntimeError("Supabase não está configurado. Configure SUPABASE_URL e SUPABASE_KEY no config.py")
        return getattr(client, name)

supabase = SupabaseProxy()