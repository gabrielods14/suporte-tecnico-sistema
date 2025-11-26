# 🔍 POR QUE NÃO VEJO OS USUÁRIOS? - Guia de Troubleshooting

Se você não está vendo os usuários na página de relatório, siga este guia passo a passo.

---

## ✅ Passo 1: Verifique se a API está Respondendo

Execute no terminal:

```bash
# Teste conexão com a API
$token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZW1haWwiOiJhZG1pbjJAaGVscHdhdmUuY29tIiwicm9sZSI6IkFkbWluaXN0cmFkb3IiLCJleHAiOjE3NjM4NzIyMTAsImlzcyI6Imh0dHBzOi8vYXBpLXN1cG9ydGUtZ3J1cG8tYmhnaGd1YTVoYmQ0ZTVoay5icmF6aWxzb3V0aC0wMS5henVyZXdlYnNpdGVzLm5ldCIsImF1ZCI6Imh0dHBzOi8vYXBpLXN1cG9ydGUtZ3J1cG8tYmhnaGd1YTVoYmQ0ZTVoay5icmF6aWxzb3V0aC0wMS5henVyZXdlYnNpdGVzLm5ldCJ9.YgNgT7Fz0_OSUGdULhWZrAjpnp5csUfFFxuknQAZog4'

Invoke-WebRequest -Uri 'http://localhost:5000/api/Usuarios' `
  -Headers @{'Authorization'="Bearer $token"} `
  -UseBasicParsing | Select-Object -ExpandProperty Content
```

### ✅ Resposta Esperada:
```json
{
  "porPermissao": {
    "admin": 2,
    "colaborador": 2,
    "suporte": 2
  },
  "total": 6,
  "usuarios": [
    { "id": 1, "nome": "...", "email": "...", "cargo": "..." },
    ...
  ]
}
```

### ❌ Se receber erro:
- Erro 404: Backend não está rodando → `dotnet run` na pasta api/ApiParaBD
- Erro 401: Token inválido → Use um token válido ou faça login novamente
- Erro de conexão: Porta 5000 não está acessível

---

## ✅ Passo 2: Execute o Script de Debug

```bash
cd web/my-project
node debug-users.js
```

Isso vai:
- Testar conexão com API
- Mostrar todos os 6 usuários em tabela
- Validar estrutura dos dados

### ✅ Saída Esperada:
```
🔍 HelpWave Users Report - Data Loading Debug
📋 Found: usuarios array with 6 items
📑 Users List:
┌─────────────────────────────────────────────────────────────┐
│  ID  │        NOME        │         E-MAIL         │ CARGO  │
├─────────────────────────────────────────────────────────────┤
│ 1    │ Administrador Sist │ admin@helpwave.com     │ Gestor  │
│ 2    │ Técnico Padrão     │ tecnico@helpwave.com   │ Suporte │
│ 3    │ Administrador Sist │ admin2@helpwave.com    │ Gestor  │
│ 4    │ Julio Dantas Moura │ julio.dantas1@helpwave │ Técnico │
│ 5    │ Thiago Roberto Alv │ thiago.roberto1@helpwa │ Almoxar │
│ 6    │ João Gabriel Goula │ gabriel.goulart1@helpw │ Contador│
└─────────────────────────────────────────────────────────────┘
✅ Data loading test completed successfully!
```

---

## ✅ Passo 3: Verifique as Permissões

Abra o navegador em `http://localhost:5173` e faça login.

Depois, abra DevTools (F12) e execute no Console:

```javascript
// Verificar qual usuário está logado
console.log('Usuário logado:', userInfo);
console.log('Permissão:', userInfo.permissao);
console.log('É Admin?', userInfo.permissao === 3);
console.log('É Técnico?', userInfo.permissao === 2);
```

### ✅ Esperado para Ver Usuários:
```javascript
{
  id: 3,
  nome: "Administrador Sistema",
  email: "admin2@helpwave.com",
  permissao: 3,  // ← DEVE SER 2 ou 3!
  cargo: "Gestor de TI"
}
```

### ❌ Se a permissão for 1:
- Você é um Colaborador
- Colaboradores NÃO têm acesso à página de usuários
- Use um login com email: `admin@helpwave.com` ou `tecnico@helpwave.com`

---

## ✅ Passo 4: Verifique se a Página está Carregando

1. Faça login como Admin
2. Procure no sidebar (menu lateral esquerdo) por **"RELATÓRIOS"** ou **"RELATÓRIO DE USUÁRIOS"**
3. Clique nele

### ✅ O que você deve ver:
- Título: "RELATÓRIO DE USUÁRIOS"
- Caixa de busca com ícone de lupa
- Tabela com colunas: ID | NOME | E-MAIL | CARGO
- 6 linhas de usuários

### ❌ Se não aparecer:
- A opção "RELATÓRIOS" não está no menu?
  - Você não é Admin (permissão deve ser 3)
  - Faça logout e login com admin@helpwave.com

---

## ✅ Passo 5: Verifique o Console do Navegador

Abra DevTools (F12) e vá para a aba **Console**.

Você deve ver mensagens como:
```
UsersReportPage - Resposta da API: Object {porPermissao: {...}, total: 6, usuarios: Array(6)}
UsersReportPage - Lista extraída: Array(6)
UsersReportPage - Dados mapeados: Array(6)
```

### ❌ Se ver erros:
- Copie a mensagem de erro
- Procure por padrões conhecidos:
  - **"Cannot read property 'usuarios'"** → API retornou formato diferente
  - **"401 Unauthorized"** → Token expirado, faça login novamente
  - **"Failed to fetch"** → Backend não está rodando

---

## ✅ Passo 6: Teste de Forma Manual no Browser Console

Cole no console do DevTools (F12):

```javascript
// Teste 1: Token válido?
const token = localStorage.getItem('authToken');
console.log('Token existe?', !!token);
if (token) {
  const payload = JSON.parse(atob(token.split('.')[1]));
  console.log('Token decodificado:', payload);
}

// Teste 2: Chamar API manualmente
fetch('http://localhost:5000/api/Usuarios', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
    'Content-Type': 'application/json'
  }
})
.then(r => {
  console.log('Status:', r.status);
  return r.json();
})
.then(d => {
  console.log('Resposta:', d);
  if (d.usuarios) {
    console.table(d.usuarios);
  }
})
.catch(e => console.error('Erro:', e));
```

### ✅ Esperado:
```
Status: 200
Resposta: Object {porPermissao: {...}, total: 6, usuarios: Array(6)}
(Tabela com 6 usuários aparecerá abaixo)
```

---

## 🎯 Checklist de Diagnóstico

Marque cada item conforme conseguir:

- [ ] **API respondendo**: `node debug-users.js` mostra 6 usuários
- [ ] **Token válido**: `console.log(localStorage.getItem('authToken'))` retorna algo
- [ ] **Permissão correta**: `console.log(userInfo.permissao)` é 2 ou 3
- [ ] **Build atualizado**: Rodou `npm run build`? (ou `npm run dev` está rodando?)
- [ ] **Frontend conecta**: DevTools mostra chamadas para `/api/Usuarios`
- [ ] **Dados chegam**: DevTools mostra resposta com array de usuários

---

## 📋 Matriz de Troubleshooting

| Sintoma | Causa Provável | Solução |
|---------|---|---|
| Página branca | Componente não renderiza | F5 para recarregar / npm run dev |
| "Carregando..." preso | API não responde | Verificar dotnet run |
| Tabela vazia | Dados não mapeados | Ver debug-users.js output |
| "Sem permissão" | Não é Admin | Logout e use admin@... |
| 401 Unauthorized | Token expirado | Logout e login novamente |
| Erro no console | API retorna formato inesperado | Ver formato esperado no INTEGRATION_STATUS.md |

---

## 🚨 Se TUDO Falhar

1. Verifique se ambos estão rodando:
   ```bash
   # Terminal 1: Backend
   cd api/ApiParaBD && dotnet run
   
   # Terminal 2: Frontend  
   cd web/my-project && npm run dev
   ```

2. Limpe tudo e comece novamente:
   ```bash
   # Frontend
   cd web/my-project
   rm -r node_modules package-lock.json dist
   npm install
   npm run dev
   
   # Backend
   cd api/ApiParaBD
   dotnet clean
   dotnet build
   dotnet run
   ```

3. Teste via script:
   ```bash
   node validate-integration.js
   ```

4. Se ainda não funcionar:
   - Verifique banco de dados: há usuários cadastrados?
   - Verifique JWT_SECRET no backend
   - Verifique API_URL no frontend
   - Procure por CORS errors no console

---

## ✅ Confirmação de Sucesso

Quando tudo estiver funcionando, você verá:

```
✅ npm run dev rodando sem erros
✅ Backend respondendo em http://localhost:5000
✅ Login funciona com admin@helpwave.com
✅ Sidebar mostra opção "RELATÓRIOS"
✅ Clique em RELATÓRIOS carrega tabela
✅ Tabela mostra 6 usuários
✅ Pode buscar por ID/nome/email
✅ Clique em usuário mostra atividade
```

Se tudo isso estiver acontecendo → **SUCESSO! 🎉**

---

**Última atualização**: Novembro 2025
**Contato**: Verifique documentação no repo
