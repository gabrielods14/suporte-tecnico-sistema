# 🔑 Como Obter a Chave de API do Gemini

## ⚠️ Problema Identificado

A chave fornecida (`gen-lang-client-0816271080`) **não é uma chave de API válida** do Gemini.

O erro retornado foi:
```
API key not valid. Please pass a valid API key.
```

Isso indica que o valor fornecido não é uma chave de API real do Google Gemini.

---

## ✅ Como Obter uma Chave de API Válida

### Passo a Passo:

1. **Acesse o site do Google AI Studio:**
   - URL: **https://aistudio.google.com/apikey**
   - Ou: **https://makersuite.google.com/app/apikey**

2. **Faça login com sua conta Google**

3. **Clique em "Create API Key" ou "Criar Chave de API"**

4. **Selecione ou crie um projeto Google Cloud**
   - Você pode criar um novo projeto se não tiver

5. **Copie a chave gerada**
   - A chave começa com `AIzaSy...` (não com `gen-lang-client-`)
   - Exemplo: `AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

6. **Configure a chave no arquivo `.env`:**
   - Abra: `web/backend/.env`
   - Substitua a linha por:
     ```env
     GEMINI_API_KEY=AIzaSySuaChaveAqui
     ```

7. **Reinicie o servidor Flask**

---

## 📝 Formato Correto de uma Chave de API

Uma chave de API válida do Gemini:
- ✅ Começa com `AIzaSy...`
- ✅ Tem aproximadamente 39 caracteres
- ✅ Exemplo: `AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

Uma chave **NÃO válida**:
- ❌ `gen-lang-client-0816271080` (isso é um ID de cliente)
- ❌ Qualquer string que não comece com `AIzaSy`

---

## 🔄 Depois de Obter a Chave Correta

1. **Edite o arquivo `.env`:**
   ```env
   GEMINI_API_KEY=AIzaSySuaChaveRealAqui
   ```

2. **Salve o arquivo**

3. **Reinicie o servidor Flask:**
   - Pressione `Ctrl+C` no terminal do Flask
   - Execute: `python app.py`

4. **Teste novamente** o botão de IA no frontend

---

## 💡 Dica

Se você já tem uma chave de API do Gemini em outro projeto, você pode reutilizá-la. Apenas certifique-se de que seja uma chave válida que comece com `AIzaSy...`.

---

## ❓ Ainda com Problemas?

Se você obteve uma chave que começa com `AIzaSy` mas ainda dá erro, verifique:

1. ✅ A chave foi copiada completamente (sem espaços)
2. ✅ O arquivo `.env` está em `web/backend/.env`
3. ✅ O servidor Flask foi reiniciado após adicionar a chave
4. ✅ Você tem acesso à API do Gemini habilitado no Google Cloud

