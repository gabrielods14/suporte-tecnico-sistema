# Instruções para Testar a IA API

## Status dos Testes Realizados

✅ **Código verificado e corrigido:**
- Dependências adicionadas ao `requirements.txt`
- Tratamento de erros melhorado
- Validação de entrada implementada
- Frontend integrado com botão de sugestão IA
- Endpoint configurado corretamente no `app.py`

✅ **Testes parciais realizados:**
- Servidor Flask iniciou corretamente
- Validação de endpoint funcionando (teste sem descrição retornou 400)
- Estrutura do código verificada

## Como Testar Manualmente

### Passo 1: Ativar o ambiente virtual

```powershell
cd web\backend
.\venv\Scripts\Activate.ps1
```

### Passo 2: Verificar se a chave da API está configurada

Certifique-se de que o arquivo `.env` existe em `web/backend/` com:

```env
GEMINI_API_KEY=sua_chave_aqui
```

### Passo 3: Iniciar o servidor Flask

```powershell
python app.py
```

Você deve ver:
```
[INFO] Caminho raiz adicionado ao sys.path: C:\Dev\suporte-tecnico-sistema
Rotas registradas com sucesso!
Iniciando servidor Flask...
 * Running on http://127.0.0.1:5000
```

### Passo 4: Testar o endpoint (em outro terminal)

**Teste 1: Validação (sem descrição)**
```powershell
cd web\backend
.\venv\Scripts\python.exe test_gemini_api.py
```

**Ou teste manualmente com curl:**
```powershell
curl -X POST http://localhost:5000/api/gemini/sugerir-resposta -H "Content-Type: application/json" -d "{\"titulo\":\"Teste\"}"
```
Esperado: Status 400 com erro "Descrição do chamado é obrigatória"

**Teste 2: Geração de sugestão completa**
```powershell
curl -X POST http://localhost:5000/api/gemini/sugerir-resposta -H "Content-Type: application/json" -d "{\"titulo\":\"Problema com impressora\",\"descricao\":\"A impressora não está imprimindo documentos.\"}"
```
Esperado: Status 200 com JSON contendo "sugestao"

### Passo 5: Testar no Frontend

1. Inicie o frontend React:
```powershell
cd web\my-project
npm run dev
```

2. Acesse: http://localhost:5173

3. Faça login como técnico (permissão 2 ou 3)

4. Abra um chamado pendente

5. Na seção "Registrar Solução", clique no botão "🤖 Gerar Sugestão com IA"

6. Aguarde a sugestão ser gerada e exibida

7. A sugestão será preenchida automaticamente no campo de solução

## Resultados Esperados

✅ **Se tudo estiver OK:**
- Botão "Gerar Sugestão com IA" aparece para técnicos
- Ao clicar, aparece loading e depois a sugestão
- Sugestão é preenchida automaticamente no campo
- É possível editar a sugestão antes de concluir

❌ **Possíveis problemas:**

1. **Erro: "GEMINI_API_KEY não configurada"**
   - Solução: Configure a variável no arquivo `.env`

2. **Erro: "Erro ao gerar sugestão"**
   - Solução: Verifique se a chave da API é válida
   - Verifique conexão com internet

3. **Servidor não inicia**
   - Solução: Verifique se a porta 5000 está livre
   - Verifique se todas as dependências estão instaladas

## Endpoints Disponíveis

- **POST /api/gemini/sugerir-resposta**
  - Body: `{"titulo": "string", "descricao": "string"}`
  - Resposta (200): `{"sugestao": "string"}`
  - Erro (400): `{"erro": "string"}`

## Arquivos Importantes

- `web/backend/app.py` - Servidor Flask (já configurado)
- `web/IAAPI/GeminiController.py` - Controller da IA
- `web/IAAPI/gemini_service.py` - Serviço do Gemini
- `web/my-project/src/pages/TicketDetailPage.jsx` - Frontend com botão IA
- `web/my-project/src/utils/api.js` - Função `aiService.gerarSugestao()`

