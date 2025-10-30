# 🚀 Servidores em Execução

## ✅ Status dos Serviços

### Backend Flask - ✅ RODANDO
- **URL:** http://localhost:5000
- **Status:** Servidor Flask ativo
- **Endpoints disponíveis:**
  - `POST /login` - Autenticação
  - `POST /register` - Cadastro de funcionários
  - `GET /chamados` - Listar chamados
  - `POST /chamados` - Criar chamado
  - `GET /chamados/<id>` - Detalhar chamado
  - `PUT /chamados/<id>` - Atualizar chamado
  - **`POST /api/gemini/sugerir-resposta`** - IA API (Gerar sugestão)

### Frontend React - ✅ RODANDO
- **URL:** http://localhost:5173
- **Status:** Servidor Vite ativo
- **Acesso:** Abra no navegador http://localhost:5173

---

## 🎯 Como Usar o Sistema

### 1. Acessar o Sistema

1. Abra seu navegador
2. Acesse: **http://localhost:5173**
3. Faça login com suas credenciais

### 2. Usar a Funcionalidade de IA

Para técnicos (permissão 2 ou 3):

1. Faça login no sistema
2. Navegue até **Chamados Pendentes**
3. Abra um chamado pendente
4. Na seção **"Registrar Solução"**, você verá o botão:
   - **🤖 Gerar Sugestão com IA**
5. Clique no botão e aguarde alguns segundos
6. A sugestão será gerada e exibida automaticamente
7. A sugestão será preenchida no campo de solução
8. Você pode editar a sugestão antes de concluir o chamado

---

## ⚙️ Configuração da IA API

**⚠️ IMPORTANTE:** Para usar a funcionalidade de IA, você precisa:

1. Criar arquivo `.env` em `web/backend/`
2. Adicionar sua chave do Gemini:

```env
GEMINI_API_KEY=sua_chave_api_aqui
```

**Como obter a chave:**
- Acesse: https://makersuite.google.com/app/apikey
- Crie uma chave de API do Google Gemini
- Cole a chave no arquivo `.env`

3. Reinicie o servidor Flask (se necessário)

---

## 📋 Resumo dos Serviços

| Serviço | URL | Status | Descrição |
|---------|-----|--------|-----------|
| **Backend** | http://localhost:5000 | ✅ Rodando | API Flask com endpoints |
| **Frontend** | http://localhost:5173 | ✅ Rodando | Interface React |
| **IA API** | `/api/gemini/sugerir-resposta` | ⚠️ Precisa chave | Geração de sugestões |

---

## 🛠️ Comandos Úteis

### Parar os servidores:
- **Backend:** Pressione `Ctrl+C` no terminal do Flask
- **Frontend:** Pressione `Ctrl+C` no terminal do Vite

### Reiniciar os servidores:

**Backend:**
```powershell
cd web\backend
.\venv\Scripts\python.exe app.py
```

**Frontend:**
```powershell
cd web\my-project
npm run dev
```

---

## ✅ Tudo Pronto!

O sistema está **100% funcional** e pronto para uso:

- ✅ Backend rodando
- ✅ Frontend rodando
- ✅ Integração IA configurada
- ✅ Botão de sugestão IA implementado
- ⚠️ Apenas falta configurar a chave da API para usar a IA

**Acesse agora:** http://localhost:5173

