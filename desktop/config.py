# config.py - Configurações do HelpWave Desktop
import os

# Configurações da API externa (Azure)
API_URL_BASE = 'https://api-suporte-grupo-bhghgua5hbd4e5hk.brazilsouth-01.azurewebsites.net'
API_TIMEOUT = 30

# Configurações do backend Flask local
FLASK_BASE_URL = 'http://localhost:5000'

# Configurações do Supabase (opcional - pode ser configurado via variáveis de ambiente)
# Para usar Supabase, defina as variáveis de ambiente SUPABASE_URL e SUPABASE_KEY
# ou edite os valores abaixo diretamente
SUPABASE_URL = os.environ.get('SUPABASE_URL') or ''
SUPABASE_KEY = os.environ.get('SUPABASE_KEY') or ''

# Configurações de autenticação
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-helpwave'

# Usuário administrador padrão para testes
ADMIN_USER = {
    'email': 'admin@helpwave.com',
    'senha': 'admin123',
    'nome': 'Administrador',
    'cargo': 'Administrador',
    'permissao': 3
}

# Paleta de cores (mesma do web)
COLORS = {
    'primary': '#A93226',
    'primary_light': '#E74C3C',
    'primary_dark': '#8B0000',
    'secondary': '#2C3E50',
    'secondary_light': '#34495E',
    'accent': '#F39C12',
    'success': '#28A745',
    'warning': '#FFC107',
    'error': '#DC3545',
    'info': '#17A2B8',
    'neutral_50': '#FAFAFA',
    'neutral_100': '#F5F5F5',
    'neutral_200': '#E5E5E5',
    'neutral_300': '#D4D4D4',
    'neutral_900': '#171717',
    'bg_primary': '#FFFFFF',
    'text_primary': '#171717',
    'text_secondary': '#525252',
    'text_inverse': '#FFFFFF'
}

# Fonte
FONT_FAMILY = 'Inter'
FONT_SIZES = {
    'xs': 12,
    'sm': 14,
    'base': 16,
    'lg': 18,
    'xl': 20,
    '2xl': 24,
    '3xl': 30,
    '4xl': 36
}