from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from config import config

# ----------------------------------------------------
# 1. Configuração e Inicialização do Aplicativo Flask
# ----------------------------------------------------
def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Carrega as configurações
    app.config.from_object(config[config_name])
    
    # Inicializa as extensões
    CORS(app, origins=app.config['CORS_ORIGINS'])
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
        app.add_url_rule('/login', 'login_user', login_user, methods=['POST'])
        
        from pages.cadastro_de_funcionario import register_user
        app.add_url_rule('/register', 'register_user', register_user, methods=['POST'])
        
        from pages.chamados_criar import criar_chamado
        app.add_url_rule('/chamados', 'criar_chamado', criar_chamado, methods=['POST'], endpoint='create_ticket')
        
        from pages.chamados_listar import listar_chamados, listar_chamados_em_andamento
        app.add_url_rule('/chamados', 'listar_chamados', listar_chamados, methods=['GET'], endpoint='list_tickets')
        app.add_url_rule('/chamados/andamento', 'listar_chamados_em_andamento', listar_chamados_em_andamento, methods=['GET'])
        
        print("Rotas registradas com sucesso!")
    except Exception as e:
        print(f"Erro ao registrar rotas: {e}")

# Registra as rotas após criar o app
register_routes()


# ----------------------------------------------------
# 3. Execução do Servidor
# ----------------------------------------------------
if __name__ == "__main__":
    print("Iniciando servidor Flask...")
    app.run(debug=True, port=5000)