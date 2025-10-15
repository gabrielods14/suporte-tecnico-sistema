# Sistema de Suporte TÃ©cnico - Mobile

Este Ã© um aplicativo mÃ³vel React Native para que colaboradores possam visualizar e interagir com seus chamados de suporte de TI.

## Funcionalidades Principais

- **VisualizaÃ§Ã£o de chamados**: Lista todos os chamados (abertos e fechados)
- **Filtros inteligentes**: Sistema de abas para filtrar entre "Todos", "Abertos" e "Fechados"
- **Detalhes completos**: VisualizaÃ§Ã£o do histÃ³rico completo de cada chamado
- **Resposta condicional**: Possibilidade de responder apenas aos chamados abertos
- **Interface moderna**: Design limpo e intuitivo com paleta de cores profissional

## Tecnologias Utilizadas

- **React Native 0.72.6**
- **React Navigation 6** - Para navegaÃ§Ã£o entre telas
- **React 18.2.0**
- **JavaScript ES6+**

## Estrutura do Projeto

```
AppSuporte/
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ components/
â”‚   â”‚   â””â”€â”€ TicketListItem.js      # Componente para item da lista
â”‚   â”œâ”€â”€ navigation/
â”‚   â”‚   â””â”€â”€ AppNavigator.js        # ConfiguraÃ§Ã£o de navegaÃ§Ã£o
â”‚   â”œâ”€â”€ screens/
â”‚   â”‚   â”œâ”€â”€ HomeScreen.js          # Tela principal com filtros
â”‚   â”‚   â”œâ”€â”€ LoginScreen.js         # Tela de login
â”‚   â”‚   â””â”€â”€ TicketDetailScreen.js  # Detalhes do chamado
â”‚   â””â”€â”€ services/
â”‚       â””â”€â”€ api.js                 # ServiÃ§o de API (mock)
â”œâ”€â”€ App.js                         # Componente principal
â””â”€â”€ index.js                       # Ponto de entrada
```

## Telas e Funcionalidades

### ðŸ” Tela de Login (LoginScreen.js)
- Campos para e-mail e senha
- ValidaÃ§Ã£o de credenciais
- Design moderno com feedback visual

### ðŸ  Tela Principal (HomeScreen.js)
- Lista de todos os chamados do usuÃ¡rio
- **Sistema de filtros por abas**: Todos, Abertos, Fechados
- Contador de resultados
- Pull-to-refresh para atualizar dados
- **Sem botÃ£o de criaÃ§Ã£o** de novos chamados (conforme especificaÃ§Ã£o)

### ðŸ“‹ Componente TicketListItem.js
- Exibe tÃ­tulo, nÃºmero e status do chamado
- Badges coloridos para status e prioridade
- Data de criaÃ§Ã£o formatada
- Design responsivo e moderno

### ðŸ“ Tela de Detalhes (TicketDetailScreen.js)
- HistÃ³rico completo de mensagens
- **Resposta condicional**: Campo de texto e botÃ£o sÃ³ aparecem para chamados abertos
- Interface de chat com bolhas diferenciadas (usuÃ¡rio vs suporte)
- Contador de caracteres
- Aviso para chamados fechados

## Como Executar

### PrÃ©-requisitos
- Node.js >= 16
- React Native CLI
- Android Studio (para Android)
- Xcode (para iOS)

### InstalaÃ§Ã£o

1. **Instalar dependÃªncias:**
```bash
npm install
```

2. **Para Android:**
```bash
npm run android
```

3. **Para iOS:**
```bash
npm run ios
```

4. **Iniciar Metro bundler:**
```bash
npm start
```

## CaracterÃ­sticas TÃ©cnicas

### ðŸŽ¨ Design System
- **Paleta de cores**: Verde (#2E7D32) como cor principal
- **Tipografia**: Hierarquia clara com diferentes pesos
- **EspaÃ§amentos**: Sistema consistente de padding e margins
- **Sombras**: ElevaÃ§Ã£o sutil para profundidade visual

### ðŸ”„ Estado e NavegaÃ§Ã£o
- **Stack Navigator** para navegaÃ§Ã£o entre telas
- **Estado local** com useState e useEffect
- **API mock** para simulaÃ§Ã£o de dados
- **Refresh control** para atualizaÃ§Ã£o de dados

### ðŸ“± Responsividade
- **KeyboardAvoidingView** para telas com input
- **ScrollView** para conteÃºdo extenso
- **FlatList** otimizada para listas grandes
- **SafeAreaView** para diferentes tamanhos de tela

## Dados de Teste

O aplicativo inclui dados mock para demonstraÃ§Ã£o:
- 5 chamados de exemplo com diferentes status
- HistÃ³rico de mensagens completo
- Diferentes prioridades (Alta, MÃ©dia, Baixa)

## Login de Teste

Use qualquer e-mail e senha para testar o aplicativo.

## Funcionalidades Implementadas

âœ… **Sistema de login** com validaÃ§Ã£o  
âœ… **Lista de chamados** com filtros por status  
âœ… **Detalhes completos** com histÃ³rico de mensagens  
âœ… **Resposta condicional** apenas para chamados abertos  
âœ… **Interface moderna** com design profissional  
âœ… **NavegaÃ§Ã£o fluida** entre telas  
âœ… **Pull-to-refresh** para atualizaÃ§Ã£o  
âœ… **Feedback visual** para aÃ§Ãµes do usuÃ¡rio  

## PrÃ³ximos Passos

Para produÃ§Ã£o, considere:
- IntegraÃ§Ã£o com API real
- AutenticaÃ§Ã£o com tokens JWT
- NotificaÃ§Ãµes push
- Cache offline
- Testes automatizados

## LicenÃ§a

Este projeto Ã© privado e destinado ao uso interno da empresa.
