🚀 Documentação do Backend (Flask / Python)
Este README.md lista os comandos exatos que foram executados para instalar e rodar o servidor Flask, que atua como um intermediário seguro para a API de Dados do Azure.

🛠️ Guia de Instalação Rápida
Para rodar o backend, você deve ter o Python e o pip instalados.

1. Preparar e Ativar o Ambiente Virtual (venv)
Execute os comandos a partir da pasta backend:

Bash

# 1. Cria o ambiente
python -m venv venv
Em seguida, ative o ambiente (essencial para isolar as bibliotecas):

Bash

# Se estiver no Windows:
.\venv\Scripts\activate

# Se estiver no macOS ou Linux:
source venv/bin/activate
Resultado: O (venv) deve aparecer no início do seu terminal.

2. Instalar Pacotes e Bibliotecas Essenciais
Instale todos os pacotes que foram adicionados para o projeto. Eles garantem a comunicação e a segurança do servidor:

Bash

(venv) pip install flask flask-cors flask-bcrypt requests
flask: É o framework principal para construir a API.

flask-cors: Permite a comunicação com o Frontend (React).

flask-bcrypt: É o módulo de criptografia (instalado para segurança, mas o hash está desativado nas rotas de repasse).

requests: Faz a comunicação com a API de Dados do Azure.

3. Rodar o Servidor
Com o (venv) ativo, inicie o servidor Flask:

Bash

(venv) python app.py
Pronto! O servidor estará rodando em http://127.0.0.1:5000.

🌐 Endpoints da API
Lembre-se de usar o Postman ou Insomnia para enviar requisições POST para estes endereços, pois o navegador não funcionará:

Login: Endereço /login

Cadastro: Endereço /register
