# Sistema de Suporte Técnico com Inteligência Artificial

## Visão Geral
Este projeto tem como objetivo o desenvolvimento de um **sistema de suporte técnico de TI** auxiliado por **Inteligência Artificial**, capaz de realizar triagem de chamados, classificação de problemas e encaminhamento automático para equipe de suporte quando necessário.  

O sistema será composto por **três plataformas distintas** (Mobile, Desktop e Web), todas integradas a uma **API central**, formando um único ecossistema.

### 🚀 Status Atual do Projeto
- ✅ **Frontend Web (React)** - Implementado e funcional
- ✅ **Backend Flask** - Implementado e integrado com API externa
- ✅ **Sistema de Login** - Autenticação via API do Azure
- ✅ **Cadastro de Funcionários** - Formulário completo integrado
- ✅ **Design Responsivo** - Interface adaptável
- 🔄 **Mobile** - Em desenvolvimento
- 🔄 **Desktop** - Em desenvolvimento
- 🔄 **IA para Triagem** - Planejado para próximas versões

---

## Tecnologias Utilizadas

### ✅ Implementado
- **Frontend Web:** React 19.1.1, Vite, React Icons, CSS3
- **Backend Intermediário:** Flask, Flask-CORS, Flask-Bcrypt, Requests
- **API Externa:** Integração com Azure (C# .NET 8)
- **Infraestrutura:** GitHub, Git Flow, Azure Cloud

### 🔄 Planejado
- **Backend Principal:** C# (.NET 8), Entity Framework, SQL Server (Azure)
- **Mobile:** React Native
- **Desktop:** Python, Kivy
- **IA:** Integração com serviços de IA para triagem  

---

## 🚀 Execução Rápida

### Frontend (React)
```bash
cd web/my-project
npm install
npm run dev
# Acesse: http://localhost:5173
```

### Backend (Flask)
```bash
cd web/backend
python -m venv venv
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python app.py
# API disponível em: http://localhost:5000
```

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

## Contribuição

Confira o arquivo Contributing.md para entender como contribuir com o projeto.

Resumidamente:

Use branches de feature/fix/hotfix.

Faça commits descritivos seguindo boas práticas.

Sempre abra PRs para revisão antes do merge.

---

## Licença

Este projeto está licenciado sob a licença MIT – veja o arquivo [LICENSE]() para mais detalhes.