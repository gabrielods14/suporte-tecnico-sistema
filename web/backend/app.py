import sys
import os

# Adiciona o diretório raiz do projeto (duas pastas acima) ao sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

print("[INFO] Caminho raiz adicionado ao sys.path:", root_path)

# Import absoluto a partir do diretório raiz do projeto
# O pacote IAAPI está dentro da pasta `web/IAAPI`, portanto importamos via `web.IAAPI`.
from web.IAAPI.GeminiController import gemini_bp
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from config import config
from dotenv import load_dotenv




load_dotenv()

# ----------------------------------------------------
# 1. Configuração e Inicialização do Aplicativo Flask
# ----------------------------------------------------
def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Carrega as configurações
    app.config.from_object(config[config_name])
    
    # Inicializa as extensões
    # CORS: Em desenvolvimento, permitir todas as origens para facilitar testes com mobile
    # Em produção, remover o '*' e especificar apenas as origens permitidas
    cors_origins = app.config.get('CORS_ORIGINS', [])
    
    # Se contém "*", permitir todas as origens (apenas em desenvolvimento)
    if '*' in cors_origins:
        CORS(app, 
             origins='*',  # Permite todas as origens
             supports_credentials=False,  # Não funciona com origins='*'
             allow_headers=['Content-Type', 'Authorization'],
             methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    else:
        CORS(app, 
             origins=cors_origins,
             supports_credentials=True,
             allow_headers=['Content-Type', 'Authorization'],
             methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    bcrypt = Bcrypt(app)
    
    return app

app = create_app()


# ----------------------------------------------------
# 2. Agregação e Mapeamento de Rotas
# ----------------------------------------------------

# Importa e registra as rotas dos módulos internos
def register_routes():
    try:
        from pages.Login import login_user
        app.add_url_rule('/login', view_func=login_user, methods=['POST'])
        
        from pages.cadastro_de_funcionario import register_user
        app.add_url_rule('/register', view_func=register_user, methods=['POST'])
        
        from pages.chamados_criar import criar_chamado
        app.add_url_rule('/chamados', view_func=criar_chamado, methods=['POST'])
        
        from pages.chamados_listar import listar_chamados, listar_chamados_em_andamento
        app.add_url_rule('/chamados', view_func=listar_chamados, methods=['GET'])
        app.add_url_rule('/chamados/andamento', view_func=listar_chamados_em_andamento, methods=['GET'])

        # Importa e registra rotas de detalhar e atualizar usando uma rota unificada
        from pages.chamados_detalhar_atualizar import detalhar_chamado
        app.add_url_rule('/chamados/<int:chamado_id>', view_func=detalhar_chamado, methods=['GET', 'PUT', 'OPTIONS'])
        
        # Importa funções de usuários
        from pages.atualizar_usuario import gerenciar_usuario
        from pages.meu_perfil import gerenciar_meu_perfil
        from pages.listar_usuarios_relatorios import listar_usuarios
        
        # IMPORTANTE: Rotas mais específicas devem vir ANTES das rotas com parâmetros
        # Rota para listar usuários (sem parâmetros)
        app.add_url_rule('/api/Usuarios', view_func=listar_usuarios, methods=['GET', 'OPTIONS'])
        
        # Rota para gerenciar meu próprio perfil (específica, deve vir antes da rota com parâmetro)
        app.add_url_rule('/api/Usuarios/meu-perfil', view_func=gerenciar_meu_perfil, methods=['GET', 'PUT', 'OPTIONS'])
        
        # Rota para gerenciar usuário por ID (deve vir DEPOIS das rotas específicas)
        app.add_url_rule('/api/Usuarios/<int:usuario_id>', view_func=gerenciar_usuario, methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
        
        # Rota alternativa para /usuarios/<id> (mantida para compatibilidade)
        app.add_url_rule('/usuarios/<int:usuario_id>', view_func=gerenciar_usuario, methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
        
        print("Rotas registradas com sucesso!")
        print("Rotas de Usuários:")
        print("  - GET, PUT, DELETE /api/Usuarios/<id>")
        print("  - GET, PUT /api/Usuarios/meu-perfil")
        print("  - GET /api/Usuarios")
    except Exception as e:
        print(f"Erro ao registrar rotas: {e}")

# Registra as rotas após criar o app
register_routes()

# Registra as rotas da IA Gemini
app.register_blueprint(gemini_bp, url_prefix='/api/gemini')

# Handler para métodos não permitidos (405)
@app.errorhandler(405)
def method_not_allowed(e):
    print(f'[ERROR 405] Método não permitido: {request.method} em {request.url}')
    print(f'[ERROR 405] Rotas disponíveis: {[str(rule) for rule in app.url_map.iter_rules()]}')
    return jsonify({"message": f"Método {request.method} não permitido para esta rota"}), 405

# ----------------------------------------------------
# 3. Execução do Servidor
# ----------------------------------------------------
if __name__ == "__main__":
    print("Iniciando servidor Flask...")
    app.run(debug=True, port=5000)