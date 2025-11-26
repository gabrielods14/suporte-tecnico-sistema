"""
Configurações do Backend HelpWave
"""
import os
from datetime import timedelta

class Config:
    """Configuração base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'helpwave-secret-key-2025'
    
    # Configurações do CORS
    # Em desenvolvimento, permitir todas as origens para facilitar testes com mobile
    # Em produção, especificar apenas as origens permitidas
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        # Adicionar IPs do mobile (desenvolvimento)
        "http://192.168.15.118:8081",  # Metro Bundler React Native
        "http://192.168.15.118:*",     # Qualquer porta do mobile
        "*"  # Em desenvolvimento, permitir todas as origens (remover em produção)
    ]
    
    # Configurações da API externa
    API_URL_BASE = 'https://api-suporte-grupoads-e4hmccf7gaczdbht.brazilsouth-01.azurewebsites.net'
    API_TIMEOUT = 30
    
    # Configurações de autenticação
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-helpwave'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Configurações de logging
    LOG_LEVEL = 'INFO'
    
    # Configurações de cache
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300

class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False
    TESTING = False
    
    # Configurações de segurança para produção
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    WTF_CSRF_ENABLED = False

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

