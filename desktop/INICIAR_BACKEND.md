# 🚀 Como Iniciar o Backend Flask

Para que a versão desktop funcione corretamente e acesse o mesmo banco de dados da versão web, você precisa iniciar o backend Flask.

## 📋 Passos para Iniciar o Backend

### 1. Abra um terminal/PowerShell

### 2. Navegue até a pasta do backend:

```powershell
cd web\backend
```

### 3. (Opcional) Ative o ambiente virtual se tiver um:

```powershell
.\venv\Scripts\activate
```

### 4. Instale as dependências (se ainda não instalou):

```powershell
pip install -r requirements.txt
```

### 5. Inicie o servidor Flask:

```powershell
python app.py
```

### 6. Você deve ver uma mensagem como:

```
Rotas registradas com sucesso!
Iniciando servidor Flask...
 * Running on http://127.0.0.1:5000
```

## ✅ Verificação

Após iniciar o servidor, você pode verificar se está rodando:

1. Abra outro terminal
2. Execute: `netstat -ano | findstr :5000`
3. Você deve ver uma linha com `TCP` e `:5000`

## ⚠️ Erro: "ModuleNotFoundError: No module named 'flask'"

Se você encontrar este erro ao tentar executar `python app.py`, significa que as dependências não estão instaladas. Execute:

```powershell
pip install -r requirements.txt
```

Aguarde a instalação terminar e então execute `python app.py` novamente.

## 🔄 Manter o Servidor Rodando

**IMPORTANTE:** Mantenha o terminal com o servidor Flask aberto enquanto usar a aplicação desktop. Se fechar o terminal, o servidor será encerrado e você verá o erro "Erro de conexão".

## 🎯 Resultado

Após iniciar o backend:
- ✅ A versão desktop poderá fazer login
- ✅ Verá os mesmos usuários da versão web
- ✅ Verá os mesmos chamados (abertos e concluídos)
- ✅ Tudo estará sincronizado com o mesmo banco de dados

