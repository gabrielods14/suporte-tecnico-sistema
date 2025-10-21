# Frontend - Sistema de Suporte Técnico HelpWave

Este é o frontend do sistema HelpWave, desenvolvido em React com Vite, que fornece uma interface moderna e responsiva para o sistema de suporte técnico.

## 🛠️ Instalação Rápida

### Pré-requisitos
- Node.js 18.0+
- npm ou yarn

### Passos de Instalação

1. **Navegar para a pasta do projeto:**
```bash
cd web/my-project
```

2. **Instalar dependências:**
```bash
npm install
```

3. **Executar servidor de desenvolvimento:**
```bash
npm run dev
```

O aplicativo estará disponível em `http://localhost:5173`

## 🚀 Scripts Disponíveis

- `npm run dev` - Inicia o servidor de desenvolvimento
- `npm run build` - Cria build de produção
- `npm run lint` - Executa o linter ESLint
- `npm run preview` - Visualiza o build de produção

## 🎨 Funcionalidades

### Páginas Disponíveis
- **Login** - Autenticação de usuários
- **Home** - Dashboard principal do sistema
- **Cadastro de Funcionário** - Interface para registro de novos funcionários

### Componentes
- **Header** - Cabeçalho com navegação e informações do usuário
- **Sidebar** - Menu lateral de navegação
- **Toast** - Notificações de feedback para o usuário
- **Modal** - Componentes modais para funcionalidades específicas

## 🔧 Configuração

O frontend está configurado para se comunicar com o backend:
- **URL Base:** `http://localhost:5000`
- **Endpoint de Login:** `/login`
- **Endpoint de Cadastro:** `/register`

## 📦 Dependências Principais

### Dependências de Produção
- **React 19.1.1** - Biblioteca principal para interface de usuário
- **React DOM 19.1.1** - Renderização do React no DOM
- **React Icons 5.5.0** - Biblioteca de ícones para React

### Dependências de Desenvolvimento
- **Vite 7.1.2** - Build tool e servidor de desenvolvimento
- **ESLint 9.33.0** - Linter para qualidade de código
- **@vitejs/plugin-react 5.0.0** - Plugin do Vite para React

## 🎯 Tecnologias Utilizadas

- **React** - Framework principal
- **Vite** - Build tool e bundler
- **CSS3** - Estilização com variáveis CSS e Flexbox/Grid
- **ESLint** - Linting e qualidade de código
- **React Icons** - Biblioteca de ícones

## 📱 Design Responsivo

O sistema foi desenvolvido com abordagem mobile-first, garantindo:
- Compatibilidade com dispositivos móveis
- Interface adaptável para tablets e desktops
- Acessibilidade seguindo padrões WCAG
- Performance otimizada

## 🔄 Integração com Backend

O frontend se comunica com o backend Flask através de:
- Requisições HTTP para autenticação
- Formulários com validação em tempo real
- Gerenciamento de estado local
- Feedback visual para o usuário
