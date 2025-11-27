# Guia de Contribuição

Obrigado por querer contribuir com este projeto!
Siga estas orientações para mantermos o repositório organizado e colaborativo.

---

## 📂 Estrutura do Repositório
O projeto está dividido em múltiplas pastas:
- `api/` → Código da API (backend + IA + banco de dados).  
- `web/` → Aplicação web.  
- `mobile/` → Aplicativo mobile.  
- `desktop/` → Aplicativo desktop.  
- `docs/` → Documentação, backlog e diagramas.  

---

## 🔄 Fluxo de Trabalho com Git

---

### 1. Clonar o repositório
```bash

git clone https://github.com/gabrielods14/suporte-tecnico-sistema.git

cd suporte-tecnico-sistema
```

---

### 2. Criar branch a partir de develop
```bash
git checkout develop
git pull origin develop
git checkout -b feature/nome-da-feature
```

---

### 3. Fazer commits descritivos

Use mensagens claras e no imperativo (ex: Adiciona login na API, Corrige bug na tela de cadastro).
Evite commits genéricos como "update", "fix" ou "teste".

---

### 4. Enviar para o repositório remoto
```bash
git add .
git commit -m "Mensagem descritiva"
git push origin feature/nome-da-feature
```

---

### 5. Abrir Pull Request (PR)

No GitHub, abra um PR da sua branch para develop.
Aguarde revisão de pelo menos um colega antes do merge.