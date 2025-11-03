# Guia para Conectar com o GitHub

## Passo 1: Configurar o Git (se ainda não configurou)

Configure seu nome e email do Git:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"
```

**Exemplo:**
```bash
git config --global user.name "Gabriel Silva"
git config --global user.email "gabriel@example.com"
```

## Passo 2: Criar um Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique no botão **"+"** no canto superior direito
3. Selecione **"New repository"**
4. Escolha um nome para o repositório (ex: `PIM`)
5. Selecione se será público ou privado
6. **NÃO marque** "Initialize this repository with a README" (já temos arquivos)
7. Clique em **"Create repository"**

## Passo 3: Conectar o Repositório Local com o GitHub

Após criar o repositório no GitHub, você verá uma página com instruções. Execute os seguintes comandos no terminal:

### Se você ainda não fez o commit inicial:

```bash
# Fazer o commit inicial (se ainda não fez)
git commit -m "Initial commit"

# Adicionar o repositório remoto do GitHub
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git

# Renomear a branch principal para main (se necessário)
git branch -M main

# Enviar os arquivos para o GitHub
git push -u origin main
```

### Se você já fez o commit:

```bash
# Adicionar o repositório remoto do GitHub
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git

# Renomear a branch principal para main (se necessário)
git branch -M main

# Enviar os arquivos para o GitHub
git push -u origin main
```

**Substitua:**
- `SEU_USUARIO` pelo seu nome de usuário do GitHub
- `SEU_REPOSITORIO` pelo nome do repositório que você criou

## Passo 4: Autenticação no GitHub

Se você usar HTTPS, o GitHub pode pedir autenticação. Você tem duas opções:

### Opção A: Token de Acesso Pessoal (Recomendado)

1. No GitHub, vá em **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Clique em **"Generate new token (classic)"**
3. Dê um nome ao token e selecione as permissões necessárias (pelo menos `repo`)
4. Copie o token gerado
5. Quando o Git pedir senha, use o token em vez da senha

### Opção B: GitHub CLI (gh)

Instale o GitHub CLI e faça login:

```bash
# Instalar GitHub CLI (se ainda não tiver)
# Windows: via winget ou baixar de https://cli.github.com

# Fazer login
gh auth login
```

## Comandos Úteis para o Futuro

```bash
# Ver o status dos arquivos
git status

# Adicionar arquivos modificados
git add .

# Fazer commit
git commit -m "Descrição das mudanças"

# Enviar para o GitHub
git push

# Baixar atualizações do GitHub
git pull

# Ver o repositório remoto configurado
git remote -v
```

## Troubleshooting

### Se der erro de autenticação:
- Verifique se você está usando o token correto
- Considere usar SSH em vez de HTTPS (mais seguro)

### Se quiser usar SSH:
1. Gere uma chave SSH: `ssh-keygen -t ed25519 -C "seu.email@example.com"`
2. Adicione a chave pública no GitHub: Settings → SSH and GPG keys
3. Use a URL SSH ao adicionar o remote: `git@github.com:SEU_USUARIO/SEU_REPOSITORIO.git`

