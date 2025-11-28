# 📚 Documentação do Sistema - HelpWave

Esta pasta contém toda a documentação técnica do sistema de suporte técnico, incluindo diagramas de banco de dados, arquitetura UML e modelos conceituais.

## 📋 Conteúdo

Esta pasta armazena os arquivos de modelagem e documentação técnica do projeto:

- **Diagramas de Entidade-Relacionamento (ER)**: Modelos conceituais e lógicos do banco de dados
- **Diagramas UML**: Representação da arquitetura e estrutura do sistema
- **Documentação de Arquitetura**: Especificações técnicas e decisões de design

## 📊 Arquivos de Diagramas

### Diagramas de Banco de Dados

#### 1. **Conceitual_DiagramaER_sistema-suporte.brM3**
- **Tipo**: Diagrama ER Conceitual
- **Formato**: BrModelo (.brM3)
- **Descrição**: Modelo conceitual do banco de dados, representando as entidades principais e seus relacionamentos em alto nível, sem detalhes de implementação.
- **Entidades Principais**:
  - **Usuario**: Representa usuários do sistema (Colaboradores, Técnicos, Administradores)
  - **Chamado**: Representa tickets de suporte técnico
  - **HistoricoChamado**: Representa o histórico de interações e mensagens

#### 2. **Lógico_DiagramaER_sistema-suporte.brM3**
- **Tipo**: Diagrama ER Lógico
- **Formato**: BrModelo (.brM3)
- **Descrição**: Modelo lógico do banco de dados, detalhando atributos, tipos de dados, chaves primárias e estrangeiras, e relacionamentos com cardinalidades específicas.
- **Detalhes**:
  - Especificação completa de atributos
  - Tipos de dados e restrições
  - Chaves primárias e estrangeiras
  - Cardinalidades dos relacionamentos

### Diagramas de Arquitetura

#### 3. **Diagrama UML Sistema.asta**
- **Tipo**: Diagrama UML
- **Formato**: Astah (.asta)
- **Descrição**: Diagrama de arquitetura do sistema, representando a estrutura de classes, componentes, casos de uso ou sequência do sistema.
- **Conteúdo**:
  - Estrutura de classes e interfaces
  - Relacionamentos entre componentes
  - Fluxos de processo
  - Arquitetura de camadas

## 🗄️ Estrutura do Banco de Dados

### Modelo de Dados

O sistema utiliza três entidades principais:

#### **Usuario**
Gerencia todos os usuários do sistema com três níveis de permissão:
- **Colaborador (1)**: Usuário comum que pode criar e acompanhar seus próprios chamados
- **SuporteTecnico (2)**: Técnico que pode atender chamados e propor soluções
- **Administrador (3)**: Acesso total ao sistema, incluindo gestão de usuários

**Atributos**:
- `Id` (int, PK)
- `Nome` (string, required)
- `Email` (string, required, unique)
- `SenhaHash` (string, required) - Hash BCrypt
- `Telefone` (string, nullable)
- `Cargo` (string, required)
- `Permissao` (enum: 1=Colaborador, 2=SuporteTecnico, 3=Administrador)
- `PrimeiroAcesso` (bool) - Flag para primeiro acesso

#### **Chamado**
Representa tickets de suporte técnico:

**Atributos**:
- `Id` (int, PK)
- `Titulo` (string, required)
- `Descricao` (string, required)
- `DataAbertura` (datetime)
- `DataFechamento` (datetime, nullable)
- `Solucao` (string, nullable) - Solução proposta pelo técnico
- `SolicitanteId` (int, FK → Usuario)
- `TecnicoResponsavelId` (int, FK → Usuario, nullable)
- `Prioridade` (enum: 1=Baixa, 2=Media, 3=Alta)
- `Status` (enum: 1=Aberto, 2=EmAtendimento, 3=AguardandoUsuario, 4=Resolvido, 5=Fechado)
- `Tipo` (string, required)

#### **HistoricoChamado**
Registra todas as interações e mensagens relacionadas a um chamado:

**Atributos**:
- `Id` (int, PK)
- `Mensagem` (string, required)
- `DataOcorrencia` (datetime)
- `EhMensagemDeIA` (bool, default: false)
- `ChamadoId` (int, FK → Chamado)
- `UsuarioId` (int, FK → Usuario, nullable)

### Relacionamentos

```
Usuario 1:N Chamado (como Solicitante)
Usuario 1:N Chamado (como TecnicoResponsavel)
Usuario 1:N HistoricoChamado
Chamado 1:N HistoricoChamado
```

## 🛠️ Ferramentas para Visualização

### BrModelo
Para visualizar e editar os diagramas ER (.brM3):
- **Download**: [BrModelo - Download Oficial](http://www.sis4.com/brModelo/download.html)
- **Plataforma**: Windows, Linux, macOS
- **Uso**: Abra o arquivo .brM3 diretamente no BrModelo

### Astah
Para visualizar e editar o diagrama UML (.asta):
- **Download**: [Astah Community Edition](https://astah.net/downloads/)
- **Plataforma**: Windows, Linux, macOS
- **Uso**: Abra o arquivo .asta diretamente no Astah

### Alternativas

Se não tiver acesso às ferramentas originais, você pode:
- Exportar os diagramas para formatos universais (PNG, PDF, SVG) usando as ferramentas originais
- Usar ferramentas alternativas que suportem importação:
  - **MySQL Workbench**: Para diagramas ER
  - **Draw.io / diagrams.net**: Para diagramas gerais
  - **Lucidchart**: Para diagramas online

## 📐 Arquitetura do Sistema

### Visão Geral

O sistema segue uma arquitetura centralizada com três camadas principais:

```
┌─────────────────────────────────────────┐
│         Camada de Apresentação          │
│  ┌────────┐  ┌────────┐  ┌────────┐    │
│  │  Web   │  │ Mobile │  │ Desktop│    │
│  │ (React)│  │(RNative)│ │(Tkinter)│   │
│  └────────┘  └────────┘  └────────┘    │
└─────────────────────────────────────────┘
              │         │         │
              └─────────┴─────────┘
                      │
┌─────────────────────────────────────────┐
│      Camada de Aplicação (API)          │
│  ┌──────────────────────────────────┐   │
│  │   API REST (.NET 8.0)           │   │
│  │   - Controllers                  │   │
│  │   - DTOs                         │   │
│  │   - JWT Authentication           │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
                      │
┌─────────────────────────────────────────┐
│      Camada de Dados                    │
│  ┌──────────────────────────────────┐   │
│  │   Entity Framework Core          │   │
│  │   SQL Server (Azure)            │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Fluxo de Dados

1. **Cliente** (Web/Mobile/Desktop) faz requisição
2. **API Centralizada** valida autenticação JWT
3. **Entity Framework** processa consulta
4. **SQL Server** retorna dados
5. **API** formata resposta
6. **Cliente** recebe e exibe dados

## 🔄 Fluxo de Estados do Chamado

```
[Aberto] 
   ↓
[Em Atendimento] ← Técnico assume
   ↓
[Aguardando Usuário] ← Solução proposta
   ↓
[Resolvido] ← Usuário confirma
   ↓
[Fechado] ← Finalização
```

## 📝 Convenções de Modelagem

### Diagramas ER
- **Entidades**: Representadas por retângulos
- **Atributos**: Representados por elipses ou listas
- **Relacionamentos**: Representados por losangos
- **Cardinalidades**: 1:1, 1:N, N:M

### Diagramas UML
- **Classes**: Representam entidades do sistema
- **Associações**: Representam relacionamentos
- **Herança**: Representa especialização
- **Agregação/Composição**: Representa relacionamentos parte-todo

## 🔍 Como Usar Esta Documentação

### Para Desenvolvedores
1. Consulte os diagramas ER para entender a estrutura do banco de dados
2. Use o diagrama UML para compreender a arquitetura do sistema
3. Referencie esta documentação ao implementar novas funcionalidades

### Para Analistas
1. Use os diagramas conceituais para entender o domínio do problema
2. Consulte os diagramas lógicos para especificações técnicas
3. Atualize os diagramas conforme o sistema evolui

### Para Gestores
1. Use os diagramas para visualizar a arquitetura do sistema
2. Consulte para planejamento de recursos e infraestrutura
3. Use como referência para documentação de processos

## 🔄 Manutenção da Documentação

### Quando Atualizar
- Adição de novas entidades ao banco de dados
- Mudanças na estrutura de relacionamentos
- Alterações significativas na arquitetura
- Implementação de novos módulos ou funcionalidades

### Processo de Atualização
1. Atualize o diagrama conceitual primeiro (visão de alto nível)
2. Atualize o diagrama lógico com detalhes técnicos
3. Atualize o diagrama UML se houver mudanças arquiteturais
4. Documente as mudanças neste README
5. Commit as alterações com mensagem descritiva

## 📚 Referências

- [Documentação do BrModelo](http://www.sis4.com/brModelo/)
- [Documentação do Astah](https://astah.net/support/)
- [Entity Framework Core](https://docs.microsoft.com/en-us/ef/core/)
- [UML Notation Guide](https://www.uml-diagrams.org/)

## 🤝 Contribuição

Ao adicionar ou modificar diagramas:

1. Mantenha a consistência com os diagramas existentes
2. Use as convenções estabelecidas
3. Documente mudanças significativas
4. Exporte versões em formatos universais (PNG/PDF) quando possível
5. Atualize este README se necessário

## 📞 Suporte

Para dúvidas sobre a documentação:
- Consulte os READMEs específicos de cada módulo (api, web, mobile, desktop)
- Abra uma issue no repositório
- Entre em contato com a equipe de desenvolvimento

---

**Documentação HelpWave** - Mantendo a arquitetura documentada e atualizada 📐📚

