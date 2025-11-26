# HelpWave Desktop - Versão Desktop

Versão desktop do sistema HelpWave baseada no projeto web, desenvolvida em Python com CustomTkinter.

## 🚀 Funcionalidades

- **Autenticação Segura**: Login com validação de credenciais
- **Dashboard Interativo**: Interface moderna com cards responsivos
- **Gestão de Usuários**: Cadastro e gerenciamento de funcionários
- **Sistema de Tickets**: Criação e acompanhamento de chamados
- **Integração com IA**: Sugestões de resposta usando Gemini AI
- **Design Moderno**: Interface bonita e intuitiva usando CustomTkinter

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Backend Flask rodando em `http://localhost:5000` (do projeto web)

## 🔧 Instalação

### Passo 1: Instalar dependências do desktop

```bash
cd desktop
pip install -r requirements.txt
```

### Passo 2: Iniciar o Backend Flask (OBRIGATÓRIO)

⚠️ **IMPORTANTE:** O aplicativo desktop precisa do backend Flask rodando para funcionar!

Abra um terminal e execute:

```bash
cd ../web/backend
python app.py
```

Você deve ver a mensagem:
```
Iniciando servidor Flask...
 * Running on http://127.0.0.1:5000
```

**Deixe este terminal aberto** enquanto usar o aplicativo desktop.

### Passo 3: Executar a aplicação desktop

Abra **outro terminal** e execute:

```bash
cd desktop
python main.py
```

A janela do aplicativo desktop será aberta.

## 🎨 Características

- **Mesma paleta de cores** do projeto web
- **Mesmas APIs** e endpoints
- **Mesmas funcionalidades** da versão web
- **Interface desktop moderna** com CustomTkinter
- **Integração com Gemini AI** para sugestões de resposta

## 📁 Estrutura do Projeto

```
desktop/
├── main.py                    # Ponto de entrada da aplicação
├── config.py                  # Configurações (API, cores, etc)
├── api_client.py              # Cliente HTTP para comunicação com API
├── login_page.py              # Página de login
├── home_page.py               # Página principal/dashboard
├── components/                # Componentes reutilizáveis
│   ├── sidebar.py
│   ├── header.py
│   ├── dropdown_menu.py
│   └── toast.py
└── pages/                     # Páginas da aplicação
    ├── new_ticket_page.py
    ├── pending_tickets_page.py
    ├── completed_tickets_page.py
    ├── ticket_detail_page.py
    ├── register_employee_page.py
    └── reports_page.py
```

## 🔐 Credenciais de Teste

```
Email: admin@helpwave.com
Senha: admin123
```

## 📝 Notas

- Esta versão desktop usa as mesmas APIs e backend do projeto web
- Certifique-se de que o backend Flask está rodando antes de iniciar a aplicação desktop
- A aplicação salva o token de autenticação em `~/.helpwave_token`

## 🐛 Solução de Problemas

### Erro: "Não foi possível conectar ao servidor"

**Solução:** O backend Flask não está rodando. 

1. Abra um terminal
2. Navegue até `web/backend`
3. Execute `python app.py`
4. Aguarde a mensagem "Running on http://127.0.0.1:5000"
5. Tente novamente no aplicativo desktop

### Erro: "ModuleNotFoundError: No module named 'customtkinter'"

**Solução:** Instale as dependências:

```bash
pip install -r requirements.txt
```

### Erro: "Erro ao registrar rotas" no backend

**Solução:** Verifique se você está no diretório correto e se todas as dependências do backend estão instaladas:

```bash
cd web/backend
pip install -r requirements.txt
python app.py
```

### A aplicação não conecta mesmo com o backend rodando

1. Verifique se o backend está realmente rodando acessando `http://localhost:5000` no navegador
2. Verifique se não há firewall bloqueando a porta 5000
3. Verifique se há outro processo usando a porta 5000

