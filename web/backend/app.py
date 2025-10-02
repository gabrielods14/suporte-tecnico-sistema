from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt

# ----------------------------------------------------
# 1. Configuração e Inicialização do Aplicativo Flask
# ----------------------------------------------------
app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)


# ----------------------------------------------------
# 2. Agregação e Mapeamento de Rotas
# ----------------------------------------------------

# Importa as rotas dos módulos internos (pages é o pacote)
# Usamos 'import *' para garantir que as rotas sejam carregadas.
try:
    from pages.Login import *
    from pages.cadastro_de_funcionario import *
except ImportError as e:
    print(f"Erro ao importar módulos de rotas: {e}")
    print("Verifique a sintaxe de importação ou se 'app.py' está no mesmo nível de 'pages'.")


# ----------------------------------------------------
# 3. Execução do Servidor
# ----------------------------------------------------
if __name__ == "__main__":
    print("Iniciando servidor Flask...")
    app.run(debug=True, port=5000)