# 🚨 SOLUÇÃO RÁPIDA - Configurar Chave de API

## ❌ Problema Atual
O arquivo `.env` existe mas está **VAZIO**. Por isso a IA não está funcionando.

## ✅ SOLUÇÃO EM 3 PASSOS

### OPÇÃO 1: Usar o Script Automático (MAIS FÁCIL)

1. **Execute o script:**
   ```powershell
   cd web\backend
   .\venv\Scripts\python.exe configurar_chave_api.py
   ```

2. **Cole sua chave de API quando solicitado**

3. **Reinicie o servidor Flask** (Ctrl+C e depois `python app.py`)

---

### OPÇÃO 2: Configuração Manual

1. **Abra o arquivo** `web/backend/.env` no seu editor

2. **Adicione esta linha:**
   ```env
   GEMINI_API_KEY=COLE_SUA_CHAVE_AQUI
   ```

3. **Salve o arquivo**

4. **Reinicie o servidor Flask**

---

## 🔑 Como Obter a Chave de API

1. Acesse: **https://makersuite.google.com/app/apikey**
2. Faça login com sua conta Google
3. Clique em **"Create API Key"** (Criar Chave de API)
4. Copie a chave gerada (começa com `AIzaSy...`)
5. Cole no arquivo `.env`

---

## 📝 Exemplo do Arquivo .env

```env
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**⚠️ NÃO USE ASPAS!** Apenas: `GEMINI_API_KEY=sua_chave_aqui`

---

## ✅ Verificar se Funcionou

Após configurar e reiniciar o servidor:

1. Abra o frontend: http://localhost:5173
2. Faça login como técnico
3. Abra um chamado pendente
4. Clique em **"🤖 Gerar Sugestão com IA"**
5. Se funcionar, você verá a sugestão sendo gerada! ✨

---

## 🔍 Localização do Arquivo

```
C:\Dev\suporte-tecnico-sistema\web\backend\.env
```

---

**Dúvidas?** Execute o script `configurar_chave_api.py` para ajuda automática!

