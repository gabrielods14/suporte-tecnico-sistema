# 🔑 Como Configurar a Chave da API do Gemini

## Problema Identificado e Corrigido ✅

O código estava usando um nome de variável incorreto. **Já corrigi isso!**

Agora você só precisa adicionar sua chave de API.

---

## 📝 Passo a Passo

### 1. Criar/Editar o arquivo `.env`

Abra ou crie o arquivo: `web/backend/.env`

### 2. Adicionar sua chave de API

Adicione esta linha no arquivo `.env`:

```env
GEMINI_API_KEY=sua_chave_api_aqui
```

**Substitua `sua_chave_api_aqui` pela sua chave real do Gemini**

### 3. Como Obter a Chave de API

1. Acesse: **https://makersuite.google.com/app/apikey**
2. Faça login com sua conta Google
3. Clique em "Create API Key" (Criar Chave de API)
4. Copie a chave gerada
5. Cole no arquivo `.env`

### 4. Exemplo do arquivo `.env`

```env
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 5. Reiniciar o Servidor Flask

**⚠️ IMPORTANTE:** Após adicionar a chave, **reinicie o servidor Flask**:

1. Pressione `Ctrl+C` no terminal do Flask para parar
2. Execute novamente:
   ```powershell
   cd web\backend
   .\venv\Scripts\python.exe app.py
   ```

---

## ✅ Verificar se Funcionou

Após reiniciar o servidor:

1. Abra o frontend: http://localhost:5173
2. Faça login como técnico
3. Abra um chamado pendente
4. Clique em **"🤖 Gerar Sugestão com IA"**
5. Agora deve funcionar! ✨

---

## 🔍 Problema Resolvido

✅ Código corrigido (`gemini_service.py`)
✅ Arquivo `.env` pode ser criado
✅ Variável de ambiente configurada corretamente

**Apenas falta:** Adicionar sua chave de API no arquivo `.env`

