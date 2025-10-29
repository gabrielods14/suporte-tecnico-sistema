# HelpWave - Sistema de Suporte Técnico

Sistema completo de suporte técnico com interface moderna e integração backend/frontend.

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
- Node.js 18+ 
- Python 3.8+
- pip (gerenciador de pacotes Python)

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

1. **Frontend**: http://localhost:5173
2. **Backend**: http://localhost:5000

### Credenciais de Teste

```
Usuário: admin@helpwave.com
Senha: admin123
```

### Navegação

1. **Login**: Página de autenticação com validação
2. **Dashboard**: Cards de navegação para funcionalidades
3. **Cadastro**: Formulário para novos funcionários
4. **Tickets**: Criação e gestão de chamados

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
```

### Backend
```bash
cd web/backend
python -m pytest  # Executar testes (se implementados)
```

## 🚀 Deploy

### Frontend (Vercel/Netlify)
```bash
npm run build
# Deploy da pasta dist/
```

### Backend (Heroku/Railway)
```bash
# Configurar Procfile
# Deploy do código Python
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Email: suporte@helpwave.com
- Documentação: [docs.helpwave.com](https://docs.helpwave.com)

---

**HelpWave** - Simplificando o seu suporte técnico 🚀