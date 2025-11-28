# HelpWave - Sistema de Suporte Técnico (Mobile)

Aplicativo mobile desenvolvido em React Native para gestão de chamados de suporte técnico. Interface nativa para Android e iOS com integração completa à API centralizada.

## 🚀 Funcionalidades

- **Autenticação Segura**: Login com validação de credenciais via API
- **Dashboard Interativo**: Interface moderna com cards de navegação
- **Gestão de Chamados**:
  - Criação de novos chamados
  - Visualização de chamados em andamento
  - Visualização de chamados concluídos
  - Detalhes completos de tickets
  - Histórico de interações
- **Integração com IA**: Configuração e uso de Gemini Pro para sugestões
- **Navegação Intuitiva**: Stack navigation com React Navigation
- **Design Responsivo**: Interface adaptável para diferentes tamanhos de tela
- **Configurações**: Ajustes de aplicativo e gerenciamento de cache

## 🛠️ Tecnologias

### Stack Principal
- **React Native 0.82.0**: Framework para desenvolvimento mobile
- **React 19.1.1**: Biblioteca JavaScript
- **TypeScript**: Tipagem estática (opcional)

### Bibliotecas Principais
- **@react-navigation/native**: Navegação entre telas
- **@react-navigation/stack**: Stack navigator
- **react-native-vector-icons**: Ícones vetoriais
- **react-native-gesture-handler**: Gestos nativos
- **react-native-safe-area-context**: Áreas seguras
- **react-native-screens**: Otimização de telas

### DevDependencies
- **ESLint**: Linter para qualidade de código
- **Jest**: Framework de testes
- **TypeScript**: Tipagem estática
- **Prettier**: Formatação de código

## 📦 Pré-requisitos

Antes de executar a aplicação, certifique-se de ter instalado:

### Geral
- [Node.js 20+](https://nodejs.org/)
- [npm](https://www.npmjs.com/) ou [Yarn](https://yarnpkg.com/)
- [Git](https://git-scm.com/)

### Para Android
- [Android Studio](https://developer.android.com/studio)
- Android SDK (API 21+)
- Emulador Android ou dispositivo físico com USB debugging habilitado
- Variáveis de ambiente configuradas:
  - `ANDROID_HOME`
  - `JAVA_HOME`

### Para iOS (apenas macOS)
- [Xcode](https://developer.apple.com/xcode/)
- [CocoaPods](https://cocoapods.org/)
- Simulador iOS ou dispositivo físico

## 🔧 Instalação

### Passo 1: Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd suporte-tecnico-sistema/mobile/SuporteTecnico
```

### Passo 2: Instalar Dependências

```bash
# Usando npm
npm install

# OU usando Yarn
yarn install
```

### Passo 3: Instalar Dependências Nativas (iOS)

```bash
# Instalar CocoaPods (primeira vez)
bundle install

# Instalar dependências nativas
cd ios
bundle exec pod install
cd ..
```

## ⚙️ Configuração

### Configuração da API

1. Configure a URL da API no arquivo de configuração
2. Ajuste as credenciais de autenticação conforme necessário

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (se aplicável):

```env
API_URL=https://sua-api.com
GEMINI_API_KEY=sua-chave-gemini
```

### Configuração do Gemini (Opcional)

A aplicação suporta integração com Gemini Pro para sugestões de solução:
- Acesse Configurações no app
- Configure sua chave de API do Gemini
- Ative/desative conforme necessário

## 🚀 Execução

### Iniciar Metro Bundler

```bash
# Usando npm
npm start

# OU usando Yarn
yarn start
```

### Executar no Android

```bash
# Usando npm
npm run android

# OU usando Yarn
yarn android
```

### Executar no iOS

```bash
# Usando npm
npm run ios

# OU usando Yarn
yarn ios
```

## 📱 Estrutura de Telas

### Telas Principais

1. **LoginScreen**: Autenticação do usuário
2. **HomeScreen**: Dashboard com cards de ação
3. **CreateTicketScreen**: Formulário para criar novos chamados
4. **PendingTicketsScreen**: Lista de chamados em andamento
5. **CompletedTicketsScreen**: Lista de chamados finalizados
6. **TicketDetailScreen**: Detalhes completos de um chamado
7. **SettingsScreen**: Configurações do aplicativo

### Navegação

A aplicação utiliza React Navigation com Stack Navigator:
- Navegação entre telas com animações nativas
- Header customizado com cores do tema
- Botões de voltar automáticos

## 📂 Estrutura do Projeto

```
SuporteTecnico/
├── src/
│   ├── screens/           # Telas da aplicação
│   │   ├── LoginScreen.js
│   │   ├── HomeScreen.js
│   │   ├── CreateTicketScreen.js
│   │   ├── PendingTicketsScreen.js
│   │   ├── CompletedTicketsScreen.js
│   │   ├── TicketDetailScreen.js
│   │   └── SettingsScreen.js
│   ├── components/       # Componentes reutilizáveis
│   │   ├── ConfirmationModal.js
│   │   └── GeminiConfigModal.js
│   ├── context/          # Context API
│   │   └── TicketContext.js
│   ├── navigation/      # Configuração de navegação
│   │   └── AppNavigator.js
│   └── utils/           # Utilitários
├── android/             # Código nativo Android
├── ios/                 # Código nativo iOS
├── App.tsx              # Componente raiz
├── package.json         # Dependências
└── README.md            # Este arquivo
```

## 🎨 Design e Interface

### Paleta de Cores
- **Primária**: #dc3545 (Vermelho HelpWave)
- **Secundária**: #ffffff (Branco)
- **Fundo**: #f5f5f5 (Cinza claro)
- **Texto**: #333333 (Cinza escuro)

### Componentes
- **Cards**: Cards de ação com ícones e cores temáticas
- **Botões**: Botões com feedback visual
- **Modais**: Modais de confirmação e configuração
- **Listas**: Listas otimizadas com FlatList

## 🔐 Autenticação

A aplicação utiliza autenticação via API centralizada:

1. Usuário insere credenciais na tela de login
2. Credenciais são validadas na API
3. Token JWT é recebido e armazenado
4. Token é usado em requisições subsequentes
5. Logout limpa dados de autenticação

## 🧪 Testes

### Executar Testes

```bash
# Usando npm
npm test

# OU usando Yarn
yarn test
```

### Linter

```bash
# Verificar código
npm run lint

# OU
yarn lint
```

## 🚨 Troubleshooting

### Problemas Comuns

1. **Metro Bundler não inicia**
   - Limpe o cache: `npm start -- --reset-cache`
   - Reinstale dependências: `rm -rf node_modules && npm install`

2. **Erro no Android**
   - Verifique se o Android SDK está configurado
   - Execute: `cd android && ./gradlew clean`
   - Verifique se o emulador está rodando

3. **Erro no iOS**
   - Execute: `cd ios && pod install`
   - Limpe o build: `cd ios && xcodebuild clean`
   - Verifique se o CocoaPods está atualizado

4. **Erro de dependências nativas**
   - Reinstale pods: `cd ios && pod deintegrate && pod install`
   - Limpe node_modules e reinstale

5. **Erro de conexão com API**
   - Verifique se a API está rodando
   - Confirme a URL da API
   - Verifique permissões de rede no dispositivo

## 📝 Desenvolvimento

### Adicionando Novas Telas

1. Crie o arquivo da tela em `src/screens/`
2. Registre a tela em `src/navigation/AppNavigator.js`
3. Adicione navegação conforme necessário

### Exemplo de Nova Tela

```javascript
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const MinhaNovaTela = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text>Minha Nova Tela</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default MinhaNovaTela;
```

### Build de Produção

#### Android
```bash
cd android
./gradlew assembleRelease
```

#### iOS
```bash
cd ios
xcodebuild -workspace SuporteTecnico.xcworkspace -scheme SuporteTecnico -configuration Release
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` na raiz do repositório para mais detalhes.

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Abra uma issue no repositório
- Entre em contato com a equipe de desenvolvimento
- Consulte a documentação da API centralizada

---

**HelpWave Mobile** - Simplificando o seu suporte técnico 📱🚀
