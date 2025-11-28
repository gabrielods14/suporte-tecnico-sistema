# HelpWave - Sistema de Suporte Técnico (Web)

Sistema web completo de suporte técnico com interface moderna e integração backend/frontend. Desenvolvido com React e Flask, oferecendo uma experiência de usuário intuitiva e responsiva.

## 🚀 Funcionalidades

- **Autenticação Segura**: Login com validação de credenciais
- **Dashboard Interativo**: Interface moderna com cards responsivos
- **Gestão de Usuários**: Cadastro e gerenciamento de funcionários
- **Sistema de Tickets**: Criação e acompanhamento de chamados
- **Design Responsivo**: Funciona perfeitamente em mobile, tablet e desktop
- **Heurísticas de UX**: Interface intuitiva seguindo princípios de usabilidade

## 🎨 Sistema de Design

### Paleta de Cores
- **Primária**: #A93226 (Vermelho HelpWave)
- **Secundária**: #2C3E50 (Azul Escuro)
- **Acento**: #F39C12 (Laranja)
- **Neutras**: Escala de cinzas do #FAFAFA ao #171717

### Tipografia
- **Fonte Principal**: Inter (Google Fonts)
- **Pesos**: 300, 400, 500, 600, 700
- **Hierarquia**: Títulos, subtítulos, corpo, legendas

### Componentes
- **Botões**: Gradientes com efeitos hover e estados
- **Cards**: Sombras suaves com animações
- **Formulários**: Validação em tempo real
- **Navegação**: Sidebar responsiva com indicadores visuais

## 🛠️ Tecnologias

### Frontend
- **React 19.1.1**: Framework principal
- **Vite**: Build tool e dev server
- **React Icons**: Ícones SVG
- **CSS Grid & Flexbox**: Layouts responsivos
- **CSS Custom Properties**: Sistema de design tokens

### Backend
- **Flask 3.0.0**: Framework web
- **Flask-CORS**: Cross-origin resource sharing
- **Flask-Bcrypt**: Hash de senhas
- **Requests**: Cliente HTTP para APIs externas

## 📦 Instalação

### Pré-requisitos

Antes de executar a aplicação, certifique-se de ter instalado:

- [Node.js 18+](https://nodejs.org/)
- [Python 3.8+](https://www.python.org/downloads/)
- pip (gerenciador de pacotes Python)
- Conexão com a internet (para comunicação com a API)

### Frontend (React)

```bash
# Navegar para o diretório do frontend
cd web/my-project

# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm run dev
```

### Backend (Flask)

```bash
# Navegar para o diretório do backend
cd web/backend

# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python app.py
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Backend
SECRET_KEY=sua-chave-secreta-aqui
JWT_SECRET_KEY=sua-jwt-secreta-aqui
API_URL_BASE=https://sua-api-externa.com

# Frontend (opcional)
VITE_API_URL=http://localhost:5000
```

### Configuração da API Externa

O sistema está configurado para integrar com uma API externa. Para configurar:

1. Edite o arquivo `web/backend/config.py`
2. Atualize a variável `API_URL_BASE`
3. Configure os endpoints necessários

## 🚀 Uso

### Acesso ao Sistema

Após iniciar os servidores:

1. **Frontend**: http://localhost:5173
2. **Backend**: http://localhost:5000

### Navegação

1. **Login**: Página de autenticação com validação de credenciais
2. **Dashboard**: Cards de navegação para funcionalidades principais
3. **Meus Chamados**: Visualização e gestão dos próprios chamados
4. **Novo Chamado**: Formulário para criação de novos tickets
5. **Chamados Pendentes**: Lista de chamados aguardando atendimento (técnicos)
6. **Detalhes do Chamado**: Visualização completa com histórico

### Funcionalidades por Permissão

#### Colaborador
- Criar chamados
- Visualizar próprios chamados
- Acompanhar status e histórico

#### Técnico
- Todas as funcionalidades de Colaborador
- Atender chamados pendentes
- Propor soluções
- Visualizar todos os chamados

#### Administrador
- Todas as funcionalidades anteriores
- Gerenciar usuários
- Acessar relatórios e estatísticas

## 📱 Responsividade

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1023px
- **Desktop**: 1024px+
- **Large Desktop**: 1400px+

### Adaptações
- **Mobile**: Layout em coluna única, sidebar oculta
- **Tablet**: Layout híbrido com sidebar reduzida
- **Desktop**: Layout completo com sidebar fixa

## 🎯 Heurísticas de UX Implementadas

### 1. Visibilidade do Status
- Indicadores de carregamento
- Mensagens de feedback
- Estados visuais dos formulários

### 2. Controle e Liberdade
- Botões de navegação
- Possibilidade de cancelar ações
- Histórico de navegação

### 3. Consistência e Padrões
- Paleta de cores unificada
- Componentes reutilizáveis
- Padrões de interação consistentes

### 4. Prevenção de Erros
- Validação em tempo real
- Confirmações para ações críticas
- Placeholders informativos

### 5. Reconhecimento vs. Recordação
- Ícones intuitivos
- Labels descritivos
- Navegação clara

### 6. Flexibilidade e Eficiência
- Atalhos de teclado
- Campos de busca
- Ações rápidas

### 7. Design Estético e Minimalista
- Interface limpa
- Hierarquia visual clara
- Foco no conteúdo essencial

## 🔍 Estrutura do Projeto

```
web/
├── backend/                 # API Flask
│   ├── app.py              # Aplicação principal
│   ├── config.py           # Configurações
│   ├── pages/              # Rotas da API
│   └── requirements.txt    # Dependências Python
├── my-project/             # Frontend React
│   ├── src/
│   │   ├── components/     # Componentes reutilizáveis
│   │   ├── hooks/          # Hooks personalizados
│   │   ├── pages/          # Páginas da aplicação
│   │   ├── styles/         # Arquivos CSS
│   │   ├── utils/          # Utilitários
│   │   └── App.jsx         # Componente principal
│   ├── package.json        # Dependências Node.js
│   └── vite.config.js      # Configuração Vite
└── README.md               # Este arquivo
```

## 🧪 Testes

### Frontend

```bash
cd web/my-project
npm run lint    # Verificar código
npm run build   # Build de produção
npm run preview # Preview do build de produção
```

### Backend

```bash
cd web/backend
python -m pytest  # Executar testes (se implementados)
python test_final.py  # Testes específicos da aplicação
```

## 🚨 Troubleshooting

### Problemas Comuns

1. **Erro de Conexão com API**
   - Verifique se a API centralizada está rodando
   - Confirme a URL em `web/backend/config.py`
   - Verifique conexão com internet

2. **Erro ao Instalar Dependências**
   - Limpe o cache: `npm cache clean --force`
   - Reinstale: `rm -rf node_modules && npm install`

3. **Erro no Backend Flask**
   - Verifique se o ambiente virtual está ativado
   - Confirme se todas as dependências estão instaladas
   - Verifique logs de erro no terminal

4. **Porta já em uso**
   - Frontend: Altere a porta no `vite.config.js`
   - Backend: Altere a porta no `app.py`

## 🚀 Deploy

### Frontend (Vercel/Netlify)

```bash
cd web/my-project
npm run build
# Deploy da pasta dist/
```

### Backend (Heroku/Railway)

```bash
cd web/backend
# Configurar Procfile
# Deploy do código Python
# Configurar variáveis de ambiente
```

### Variáveis de Ambiente para Deploy

Configure as seguintes variáveis no ambiente de produção:

```env
SECRET_KEY=sua-chave-secreta-producao
JWT_SECRET_KEY=sua-jwt-secreta-producao
API_URL_BASE=https://sua-api-producao.com
FLASK_ENV=production
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 📝 Desenvolvimento

### Adicionando Novas Funcionalidades

1. Crie componentes em `web/my-project/src/components/`
2. Adicione páginas em `web/my-project/src/pages/`
3. Configure rotas conforme necessário
4. Adicione estilos em `web/my-project/src/styles/`

### Estrutura de Componentes

- **Components**: Componentes reutilizáveis (Header, Footer, etc.)
- **Pages**: Páginas principais da aplicação
- **Hooks**: Hooks personalizados para lógica reutilizável
- **Utils**: Funções utilitárias e helpers
- **Styles**: Arquivos CSS por componente/página

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Abra uma issue no repositório
- Entre em contato com a equipe de desenvolvimento
- Consulte a documentação da API centralizada

---

**HelpWave Web** - Simplificando o seu suporte técnico 🚀