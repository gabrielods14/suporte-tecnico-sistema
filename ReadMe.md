<div align="center">
  <img src="web/my-project/public/logo.png" alt="HelpWave Logo" width="250"/>
  
  # HelpWave
  
  ### Sistema de Suporte Técnico com Inteligência Artificial
  
  Sistema completo de suporte técnico auxiliado por IA para geração de sugestões aos técnicos
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</div>

---

## Visão Geral
Este projeto tem como objetivo o desenvolvimento de um **sistema de suporte técnico de TI** auxiliado por **Inteligência Artificial** para geração de sugestões de solução aos técnicos de suporte. A IA analisa o contexto do chamado e fornece recomendações que auxiliam o técnico na resolução de problemas, agilizando o atendimento e melhorando a qualidade das soluções propostas.

O sistema é composto por **três plataformas distintas** (Mobile, Desktop e Web), todas integradas a uma **API central**, formando um único ecossistema unificado.


### 🚀 Status Atual do Projeto
- ✅ **API Centralizada (.NET 8)** - Implementada e funcional
- ✅ **Frontend Web (React)** - Implementado e funcional
- ✅ **Backend Flask** - Implementado e integrado com API centralizada
- ✅ **Sistema de Login** - Autenticação JWT via API centralizada
- ✅ **Gestão de Usuários** - Cadastro e gerenciamento completo
- ✅ **Sistema de Chamados** - Criação, acompanhamento e resolução
- ✅ **Integração com IA (Gemini)** - Geração de sugestões para técnicos
- ✅ **Aplicativo Mobile (React Native)** - Implementado e funcional
- ✅ **Aplicativo Desktop (Python/Tkinter)** - Implementado e funcional
- ✅ **Design Responsivo** - Interface adaptável em todas as plataformas
- ✅ **Documentação** - READMEs padronizados e diagramas técnicos

---

## Tecnologias Utilizadas

### ✅ Implementado
- **API Centralizada:** C# .NET 8.0, Entity Framework Core, SQL Server (Azure)
- **Frontend Web:** React 19.1.1, Vite, React Icons, CSS3
- **Backend Intermediário:** Flask, Flask-CORS, Flask-Bcrypt, Requests
- **Mobile:** React Native 0.82.0, React Navigation, Vector Icons
- **Desktop:** Python 3.8+, Tkinter, Supabase Client
- **IA:** Integração com Gemini Pro para sugestões de solução
- **Autenticação:** JWT Bearer, BCrypt para hash de senhas
- **Infraestrutura:** GitHub, Git Flow, Azure Cloud, Swagger/OpenAPI  

---

## 🚀 Execução Rápida

### API Centralizada (.NET 8)
```bash
cd api/ApiParaBD
dotnet restore
dotnet run
# API disponível em: https://localhost:7000
# Swagger: https://localhost:7000/swagger
```

### Frontend Web (React)
```bash
cd web/my-project
npm install
npm run dev
# Acesse: http://localhost:5173
```

### Backend Intermediário (Flask)
```bash
cd web/backend
python -m venv venv
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python app.py
# API disponível em: http://localhost:5000
```

### Mobile (React Native)
```bash
cd mobile/SuporteTecnico
npm install
npm start
# Android: npm run android
# iOS: npm run ios
```

### Desktop (Python/Tkinter)
```bash
cd desktop
python -m venv venv
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install supabase
python main.py
```

> 📖 **Nota**: Cada módulo possui um README.md específico com instruções detalhadas de instalação e configuração.

---

## 🎯 Funcionalidades Principais

### Sistema de Usuários
- Gerenciamento de colaboradores, técnicos e administradores
- Sistema de permissões hierárquico (3 níveis)
- Autenticação JWT segura
- Controle de primeiro acesso

### Sistema de Chamados
- Criação de tickets de suporte
- Acompanhamento de status em tempo real
- Atribuição de técnicos responsáveis
- Histórico completo de interações
- Priorização (Baixa, Média, Alta)
- Estados: Aberto → Em Atendimento → Aguardando Usuário → Resolvido → Fechado

### Inteligência Artificial
- **Geração de Sugestões**: A IA analisa o contexto do chamado e gera sugestões de solução para auxiliar o técnico de suporte
- **Integração Gemini Pro**: Utiliza Google Gemini Pro para análise contextual
- **Assistência Inteligente**: Fornece recomendações baseadas na descrição do problema

### Plataformas
- **Web**: Interface moderna e responsiva para acesso via navegador
- **Mobile**: Aplicativo nativo para Android e iOS
- **Desktop**: Aplicação desktop multiplataforma  


---

## 📂 Estrutura do Repositório

```bash

📂 suporte-tecnico-sistema
│── 📂 api # Código da API (backend + IA + banco de dados)
│── 📂 mobile # Código do aplicativo mobile
│── 📂 desktop # Código do sistema desktop
│── 📂 web # Código da aplicação web
│── 📂 docs # Documentação, diagramas UML, backlog e sprints
│
│── ReadMe.md # Documentação principal do repositório
│── Contributing.md # Guia de contribuição para colaboradores
│── LICENSE # Licença do projeto
│── .gitignore

```


Cada subpasta contém um `README.md` próprio, descrevendo como instalar e rodar o projeto específico.

---

## Fluxo de Trabalho (Git Flow Simplificado)

- **main** → versão estável (pronta para apresentação).  
- **develop** → versão em desenvolvimento (features consolidadas).  
- **feature/** → novas funcionalidades (ex: `feature/web-login`).  
- **fix/** → correções de bugs.  
- **hotfix/** → correções urgentes diretamente em `main`.  

---

### 📝 Exemplo de fluxo
1. Criar branch a partir de `develop`:  
```bash
git checkout develop
git pull origin develop
git checkout -b feature/web-dashboard
```

2. Implementar a funcionalidade e fazer commits.

3. Abrir Pull Request (PR) para develop.

4. Revisão de código por colegas do time.

5. Merge após aprovação.

6. Versões estáveis de develop são integradas em main.

---

## Organização do Time

O projeto segue princípios do Scrum, com sprints curtas para entrega de incrementos funcionais.

Backlog: gerenciado em docs/backlog.md e no GitHub Projects.

Sprints: organizadas em docs/sprints/.

Tarefas: abertas como issues no GitHub, vinculadas a PRs.

---

## 🤝 Contribuição

Confira o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para entender como contribuir com o projeto.

Resumidamente:
- Use branches de feature/fix/hotfix
- Faça commits descritivos seguindo boas práticas
- Sempre abra PRs para revisão antes do merge
- Siga os padrões de código estabelecidos
- Documente mudanças significativas

## 📚 Documentação

Cada módulo possui documentação específica:
- **API**: `api/ApiParaBD/README.md`
- **Web**: `web/README.md`
- **Mobile**: `mobile/SuporteTecnico/README.md`
- **Desktop**: `desktop/README.md`
- **Documentação Técnica**: `docs/README.md`

---

## Licença

Este projeto está licenciado sob a licença MIT – veja o arquivo [LICENSE]() para mais detalhes.