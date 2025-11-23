# 🚀 Como Acessar a Página de Relatório de Usuários

## Pré-requisitos

1. **API Backend rodando** na porta 5000
   ```bash
   # Terminal 1: Inicie a API .NET
   cd api/ApiParaBD
   dotnet run
   ```

2. **Frontend rodando** na porta 5173 (ou configure em vite.config.js)
   ```bash
   # Terminal 2: Inicie o frontend
   cd web/my-project
   npm run dev
   ```

## Passo 1: Faça Login como Administrador

1. Abra o navegador: `http://localhost:5173`
2. Use as credenciais de admin:
   - **Email**: `admin@helpwave.com` ou `admin2@helpwave.com`
   - **Senha**: Aquela que você configurou no banco de dados
   
   ⚠️ **Importante**: Apenas Admin e Suporte Técnico podem acessar a página de usuários!

## Passo 2: Navegue até Relatório de Usuários

Após fazer login, você está na página HOME. Agora:

### Opção 1: Via Sidebar (Menu Lateral)
1. Procure no menu lateral à esquerda
2. Clique em **"RELATÓRIOS"** ou **"RELATÓRIO DE USUÁRIOS"**
   - Apenas admins veem esta opção
   - Técnicos podem ver se tiverem permissão

### Opção 2: Via URL Direta
1. Digite na barra de endereços: `http://localhost:5173` (seu app já estará lá)
2. A rota será ativada automaticamente

## Passo 3: Veja a Tabela de Usuários

Você deverá ver uma tabela com:

| Coluna | Conteúdo |
|--------|----------|
| **ID** | ID único do usuário |
| **NOME** | Nome completo |
| **E-MAIL** | E-mail cadastrado |
| **CARGO** | Cargo/Posição (ex: Gestor de TI) |

### Dados Esperados (6 usuários):
```
1 | Administrador Sistema | admin@helpwave.com | Gestor de TI
2 | Técnico Padrão | tecnico@helpwave.com | Suporte N1
3 | Administrador Sistema | admin2@helpwave.com | Gestor de TI
4 | Julio Dantas Moura | julio.dantas1@helpwave.com | Técnico TI
5 | Thiago Roberto Alves | thiago.roberto1@helpwave.com | Almoxarife
6 | João Gabriel Goulart | gabriel.goulart1@helpwave.com | Contador
```

## Passo 4: Use a Busca e Filtro

Na caixa de busca, você pode:
- 🔍 Buscar por **ID**: Digite `1`, `2`, `3`, etc.
- 🔍 Buscar por **Nome**: Digite `Administrador`, `Técnico`, `Julio`, etc.
- 🔍 Buscar por **E-mail**: Digite `admin@helpwave.com`, `julio...`, etc.

A tabela se atualiza em tempo real conforme você digita.

## Passo 5: Clique em um Usuário para Ver Detalhes

1. Clique em qualquer linha da tabela
2. Você será levado para a página **"ATIVIDADE DO USUÁRIO"**
3. Você verá:
   - Resumo do usuário (ID, Email, Cargo, Permissão, Logins)
   - Lista de chamados abertos por este usuário
   - Lista de chamados resolvidos por este usuário
   - Tempo aberto para cada chamado

## Solução de Problemas

### ❌ Problema: "Nenhum usuário encontrado"
- **Causa**: API não retornando dados ou formato incorreto
- **Solução**: 
  1. Verifique se API está rodando: `http://localhost:5000/api/Usuarios`
  2. Abra o console do navegador (F12) e procure por erros
  3. Execute: `node debug-users.js` para testar API

### ❌ Problema: "Carregando usuários..." (fica preso)
- **Causa**: Erro de conexão ou token inválido
- **Solução**:
  1. Verifique se backend está rodando
  2. Faça logout e login novamente
  3. Verifique localStorage: abra DevTools > Application > localStorage

### ❌ Problema: Página está em branco
- **Causa**: Sem permissão de acesso
- **Solução**:
  1. Verifique se está logado como Admin ou Técnico
  2. User role deve ser 2 (Técnico) ou 3 (Admin)
  3. No console, verifique: `console.log(userInfo)` para ver permissão

### ❌ Problema: Token expirado (Erro 401)
- **Causa**: Token JWT expirado
- **Solução**:
  1. Faça logout (clique em seu nome no header)
  2. Faça login novamente
  3. Token será renovado

## Testando via Console do Navegador

Abra DevTools (F12) e execute no Console:

```javascript
// Ver dados do usuário logado
console.log(userInfo);

// Ver token JWT
console.log(localStorage.getItem('authToken'));

// Fazer requisição manual para API
fetch('http://localhost:5000/api/Usuarios', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
  }
})
.then(r => r.json())
.then(d => console.log(d))
.catch(e => console.error(e));
```

## Testando via Script Node

```bash
cd web/my-project
node debug-users.js
```

Este script:
- ✅ Testa conexão com API
- ✅ Valida o JWT token
- ✅ Mostra todos os usuários em formato tabela
- ✅ Mostra detalhes do primeiro usuário

## Fluxo Completo de Funcionalidades

```
┌─────────────────────────────────┐
│   PÁGINA HOME (após login)      │
│  - Usuário admin logado         │
│  - Sidebar visível              │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  CLIQUE EM "RELATÓRIOS"         │
│  (opcão no sidebar)             │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  USERS REPORT PAGE              │
│  - Tabela com 6 usuários        │
│  - Search/Filter funcionando    │
│  - Pode clicar em linhas        │
└────────────┬────────────────────┘
             │
             ▼
        CLIQUE EM USUÁRIO
             │
             ▼
┌─────────────────────────────────┐
│  USER ACTIVITY PAGE             │
│  - Perfil do usuário            │
│  - Tickets abertos              │
│  - Tickets resolvidos           │
│  - Botão "Voltar" para reports  │
└─────────────────────────────────┘
```

## Permissões por Tipo de Usuário

| User Type | Acesso | O Que Vê |
|-----------|--------|---------|
| **Colaborador** (1) | ❌ Não | Apenas seus próprios chamados ("Meus Chamados") |
| **Técnico** (2) | ✅ Sim | Tabela de usuários + atividade (com restrições) |
| **Admin** (3) | ✅ Sim | Tudo - Relatórios completos + Dashboard |

## Verificando Permissões em Tempo Real

1. Abra DevTools (F12)
2. Vá para aba **Console**
3. Execute:
```javascript
// Mostra permissão do usuário logado
console.log('Permissão:', localStorage.getItem('userPermissao'));

// Decodifica token para ver role
const token = localStorage.getItem('authToken');
const payload = JSON.parse(atob(token.split('.')[1]));
console.log('Role do token:', payload.role);
```

## Próximas Funcionalidades Planejadas

- [ ] Exportar usuários para CSV
- [ ] Filtros avançados (data, permissão, cargo)
- [ ] Paginação para 1000+ usuários
- [ ] Editar usuário diretamente da tabela
- [ ] Gráficos e analytics por usuário

---

**Última atualização**: Novembro 2025
**Status**: ✅ Funcionando
**Testado com**: 6 usuários no banco de dados
