# HelpWave - Sistema de Suporte Técnico (Desktop)

Aplicação desktop desenvolvida em Python com Tkinter para gestão de chamados de suporte técnico. Interface moderna e intuitiva com integração à API centralizada.

## 🚀 Funcionalidades

- **Autenticação Segura**: Login com validação de credenciais via API
- **Dashboard Interativo**: Interface moderna com navegação lateral e cards de ação
- **Gestão de Chamados**: 
  - Criação de novos chamados
  - Visualização de chamados em andamento
  - Detalhes completos de chamados
  - Histórico de interações
- **Gestão de Usuários**: Cadastro de novos usuários (apenas para permissão TI)
- **Design Responsivo**: Interface adaptável com janela redimensionável
- **Integração com API**: Comunicação completa com a API centralizada

## 🛠️ Tecnologias

### Stack Principal
- **Python 3.8+**: Linguagem principal
- **Tkinter**: Framework GUI nativo do Python
- **Supabase Client**: Cliente para integração com Supabase (opcional)

### Dependências Principais
- `supabase`: Cliente Python para Supabase
- Bibliotecas padrão do Python (tkinter, json, etc.)

## 📦 Pré-requisitos

Antes de executar a aplicação, certifique-se de ter instalado:

- [Python 3.8 ou superior](https://www.python.org/downloads/)
- pip (gerenciador de pacotes Python)
- Conexão com a internet (para comunicação com a API)

## 🔧 Instalação

### Passo 1: Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd suporte-tecnico-sistema/desktop
```

### Passo 2: Criar Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
pip install supabase
```

Ou instale manualmente as dependências necessárias:

```bash
pip install supabase-py
```

## ⚙️ Configuração

### Configuração da API

1. Abra o arquivo `config.py`
2. Configure as variáveis de conexão:

```python
# URL da API centralizada
API_URL = "https://sua-api.com"

# Configurações do Supabase (se aplicável)
SUPABASE_URL = "https://seu-projeto.supabase.co"
SUPABASE_KEY = "sua-chave-api"
```

### Variáveis de Ambiente (Opcional)

Crie um arquivo `.env` na raiz do projeto desktop:

```env
API_URL=https://sua-api.com
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-api
```

## 🚀 Execução

### Executar a Aplicação

```bash
python main.py
```

A aplicação será iniciada com a tela de login.

### Estrutura de Execução

1. **Tela de Login**: Autenticação do usuário
2. **Dashboard Principal**: Após login bem-sucedido
   - Home: Cards de ação rápida
   - Novo Chamado: Formulário para criar chamados
   - Chamados em Andamento: Lista de chamados pendentes
   - Detalhes do Chamado: Visualização completa
   - Cadastrar Usuário: Apenas para permissão TI

## 📱 Navegação

### Menu Lateral
- **HOME**: Página inicial com cards de ação
- **NOVO CHAMADO**: Criar novo ticket de suporte
- **CHAMADOS EM ANDAMENTO**: Visualizar chamados pendentes
- **CADASTRAR USUÁRIO**: Apenas para usuários com permissão TI

### Funcionalidades por Permissão

#### Colaborador
- Criar chamados
- Visualizar próprios chamados
- Acompanhar status

#### Técnico (TI)
- Todas as funcionalidades de Colaborador
- Atender chamados
- Cadastrar novos usuários
- Visualizar todos os chamados

## 📂 Estrutura do Projeto

```
desktop/
├── main.py                 # Ponto de entrada da aplicação
├── config.py              # Configurações e variáveis de ambiente
├── supabase_service.py    # Serviço de integração com Supabase
├── login_page.py          # Tela de login
├── dashboard_base.py      # Dashboard principal com navegação
├── home_page.py           # Página inicial com cards
├── new_call_page.py       # Formulário de novo chamado
├── pending_calls_page.py  # Lista de chamados em andamento
├── call_details_page.py   # Detalhes de um chamado específico
├── create_user_page.py    # Cadastro de novos usuários
└── README.md              # Este arquivo
```

## 🎨 Design e Interface

### Paleta de Cores
- **Primária**: #8B0000 (Vermelho escuro)
- **Secundária**: #D3D3D3 (Cinza claro)
- **Fundo Escuro**: #1C1C1C
- **Hover**: #A52A2A

### Componentes
- **Janela Principal**: 1200x800px (redimensionável)
- **Header**: Barra superior com logo e informações do usuário
- **Sidebar**: Menu lateral com navegação
- **Content Area**: Área principal de conteúdo
- **Footer**: Rodapé com informações

## 🔐 Autenticação

A aplicação utiliza autenticação via API centralizada:

1. Usuário insere credenciais na tela de login
2. Credenciais são validadas na API
3. Token JWT é recebido e armazenado
4. Token é usado em requisições subsequentes

## 🧪 Testes

Para testar a aplicação:

1. Execute `python main.py`
2. Faça login com credenciais válidas
3. Navegue pelas diferentes páginas
4. Teste criação de chamados
5. Verifique permissões de usuário

## 🚨 Troubleshooting

### Problemas Comuns

1. **Erro de Conexão com API**
   - Verifique se a API está rodando
   - Confirme a URL em `config.py`
   - Verifique conexão com internet

2. **Erro ao Importar Módulos**
   - Certifique-se de que todas as dependências estão instaladas
   - Verifique se o ambiente virtual está ativado

3. **Janela não Abre**
   - Verifique se o Tkinter está instalado (geralmente vem com Python)
   - No Linux: `sudo apt-get install python3-tk`

4. **Erro de Autenticação**
   - Verifique credenciais
   - Confirme se a API está acessível
   - Verifique logs da API

## 📝 Desenvolvimento

### Adicionando Novas Funcionalidades

1. Crie um novo arquivo Python para a página
2. Herde de `tk.Frame`
3. Registre a página em `dashboard_base.py`
4. Adicione item no menu lateral

### Exemplo de Nova Página

```python
import tkinter as tk

class MinhaNovaPage(tk.Frame):
    def __init__(self, master_frame, user_info):
        super().__init__(master_frame, bg="#D3D3D3")
        self.pack(fill=tk.BOTH, expand=True)
        
        # Seu código aqui
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` na raiz do repositório para mais detalhes.

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Abra uma issue no repositório
- Entre em contato com a equipe de desenvolvimento
- Consulte a documentação da API centralizada

---

**HelpWave Desktop** - Simplificando o seu suporte técnico 🚀

