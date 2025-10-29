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
        app.add_url_rule('/login', view_func=login_user, methods=['POST'])
        
        from pages.cadastro_de_funcionario import register_user
        app.add_url_rule('/register', view_func=register_user, methods=['POST'])
        
        from pages.chamados_criar import criar_chamado
        app.add_url_rule('/chamados', view_func=criar_chamado, methods=['POST'])
        
        from pages.chamados_listar import listar_chamados, listar_chamados_em_andamento
        app.add_url_rule('/chamados', view_func=listar_chamados, methods=['GET'])
        app.add_url_rule('/chamados/andamento', view_func=listar_chamados_em_andamento, methods=['GET'])

        # Garante o registro das rotas de detalhar e atualizar
        import pages.chamados_detalhar_atualizar  # noqa: F401
        
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