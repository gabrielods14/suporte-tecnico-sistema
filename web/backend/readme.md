# Backend - Sistema de Suporte Técnico HelpWave

Este é o backend do sistema HelpWave, desenvolvido em Flask, que atua como intermediário seguro para a API de Dados do Azure.

## 🛠️ Instalação Rápida

### Pré-requisitos
- Python 3.7+
- pip

### Passos de Instalação

1. **Criar ambiente virtual:**
```bash
python -m venv venv
```

2. **Ativar ambiente virtual:**
```bash
# Windows:
.\venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

3. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

4. **Executar servidor:**
```bash
python app.py
```

O servidor estará disponível em `http://localhost:5000`

## 🌐 Endpoints da API

- `POST /login` - Autenticação de usuário
- `POST /register` - Cadastro de funcionário

## 🔧 Configuração

O backend está configurado para se conectar com a API externa do Azure:
- **URL Base:** `https://api-suporte-grupoads-e4hmccf7gaczdbht.brazilsouth-01.azurewebsites.net`
- **Endpoint de Login:** `/api/Autenticacao`
- **Endpoint de Cadastro:** `/api/Usuarios`

## 📦 Dependências

- **Flask:** Framework principal para construir a API
- **Flask-CORS:** Permite comunicação com o Frontend (React)
- **Flask-Bcrypt:** Módulo de criptografia para segurança
- **Requests:** Comunicação com a API de Dados do Azure
