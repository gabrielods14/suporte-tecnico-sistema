# 🤖 Integração com API de IA - Sistema Mobile

Este documento descreve como o sistema mobile integra com a API de IA do backend Flask, utilizando o mesmo endpoint do sistema web.

## 📋 Visão Geral

O sistema mobile utiliza o mesmo endpoint de IA do backend Flask (`/api/gemini/sugerir-resposta`) que é usado pelo sistema web, garantindo consistência e centralização da lógica de IA.

## 🔗 Endpoint Utilizado

**Backend Flask:**
- **URL:** `http://localhost:5000/api/gemini/sugerir-resposta` (desenvolvimento)
- **Método:** `POST`
- **Content-Type:** `application/json`

**Request Body:**
```json
{
  "titulo": "Tipo de problema - Descrição resumida...",
  "descricao": "Descrição completa do problema"
}
```

**Response:**
```json
{
  "sugestao": "Texto da sugestão gerada pelo Gemini AI"
}
```

## ⚙️ Configuração

### 1. URL do Backend Flask

A URL do backend Flask é configurada no arquivo `src/services/AIService.js`:

```javascript
const getFlaskApiUrl = () => {
  // Em desenvolvimento
  if (__DEV__) {
    return 'http://localhost:5000'; // Para iOS
    // OU use o IP da sua máquina para Android:
    // return 'http://192.168.1.100:5000';
  }
  
  // Em produção
  return 'https://seu-backend-flask.herokuapp.com';
};
```

### 2. Configuração para Android

**IMPORTANTE:** No Android, `localhost` não funciona. Você precisa usar o IP da sua máquina.

**Como encontrar seu IP:**
- **Windows:** Execute `ipconfig` e procure por "IPv4 Address"
- **macOS/Linux:** Execute `ifconfig | grep "inet "` ou `hostname -I`

**Exemplo de configuração:**
```javascript
return 'http://192.168.1.100:5000'; // Substitua pelo seu IP
```

### 3. Configuração via Variável de Ambiente

Você também pode configurar a URL via variável de ambiente:

```javascript
// No código, será lido automaticamente se disponível
process.env.FLASK_API_URL
```

## 📝 Fluxo de Funcionamento

1. **Usuário seleciona um chamado** na tela de chamados pendentes
2. **Sistema chama `AIService.getSuggestion()`** com tipo e descrição do problema
3. **AIService faz requisição POST** para `/api/gemini/sugerir-resposta`
4. **Backend Flask processa** usando o serviço Gemini (mesmo do sistema web)
5. **Resposta é convertida** para formato estruturado esperado pelo mobile
6. **Sugestão é exibida** na interface do usuário

## 🔄 Conversão de Resposta

O serviço converte a resposta de texto do Flask para o formato estruturado esperado pelo mobile:

```javascript
{
  analysis: "Análise técnica do problema",
  steps: ["Passo 1", "Passo 2", "Passo 3"],
  stepByStepSolution: ["Passo 1", "Passo 2", "Passo 3"],
  specificCommands: [],
  rootCause: "",
  symptoms: [],
  additional: "Informações adicionais",
  confidence: "75%",
  estimatedTime: "20-30 minutos",
  priority: "Média",
  sentiment: "Neutro"
}
```

## 🛡️ Tratamento de Erros

O sistema possui fallback automático em caso de erro:

1. **Erro de conexão:** Sistema usa sugestões de fallback baseadas no tipo de problema
2. **Erro de parsing:** Sistema extrai informações básicas do texto retornado
3. **Serviço indisponível:** Sistema usa sugestões pré-definidas por tipo de problema

## 📦 Arquivos Relacionados

- **`src/services/AIService.js`** - Serviço principal de IA
- **`src/screens/PendingTicketsScreen.js`** - Tela que utiliza o serviço de IA
- **`src/components/ConfirmationModal.js`** - Modal de confirmação (usado na finalização)

## 🚀 Como Testar

### 1. Iniciar o Backend Flask

```bash
cd suporte-tecnico-sistema/web/backend
python app.py
```

O servidor Flask estará disponível em `http://localhost:5000`

### 2. Configurar URL no Mobile

Edite `src/services/AIService.js` e ajuste a URL conforme necessário:

```javascript
// Para Android (use o IP da sua máquina)
return 'http://192.168.1.100:5000';

// Para iOS (pode usar localhost)
return 'http://localhost:5000';
```

### 3. Testar no Aplicativo

1. Abra o aplicativo mobile
2. Navegue até "Chamados em Andamento"
3. Toque em um chamado
4. A sugestão de IA deve aparecer automaticamente

## 🔍 Debug

Para verificar se a integração está funcionando, verifique os logs no console:

```javascript
console.log('=== AIService: Iniciando busca de sugestão via Flask API ===');
console.log('Status da resposta Flask:', response.status);
console.log('Resposta do Flask:', data);
```

## 📚 Referências

- **Backend Flask:** `web/backend/app.py`
- **Endpoint IA:** `web/IAAPI/GeminiController.py`
- **Serviço Gemini:** `web/IAAPI/gemini_service.py`

## ⚠️ Notas Importantes

1. **CORS:** O backend Flask deve ter CORS configurado para permitir requisições do mobile
2. **Rede:** Certifique-se de que o dispositivo mobile está na mesma rede do servidor Flask (em desenvolvimento)
3. **Produção:** Em produção, configure a URL do servidor Flask hospedado
4. **Chave de API:** A chave do Gemini deve estar configurada no backend Flask (arquivo `.env`)

## 🎯 Próximos Passos

1. Configurar variáveis de ambiente para diferentes ambientes (dev, staging, prod)
2. Implementar cache de sugestões para melhorar performance
3. Adicionar retry automático em caso de falha temporária
4. Implementar métricas de uso da IA


