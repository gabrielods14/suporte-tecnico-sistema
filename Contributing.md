# Guia de Contribuição

Obrigado por querer contribuir com este projeto!
Siga estas orientações para mantermos o repositório organizado e colaborativo.

---

## 📂 Estrutura do Repositório

O projeto está dividido em múltiplas pastas:
- `api/` → API centralizada (.NET 8) com banco de dados e integração com IA
- `web/` → Aplicação web (React + Flask)
- `mobile/` → Aplicativo mobile (React Native)
- `desktop/` → Aplicativo desktop (Python/Tkinter)
- `docs/` → Documentação técnica, diagramas UML e ER

---

## 🔄 Fluxo de Trabalho com Git

### 1. Clonar o repositório

```bash
git clone https://github.com/gabrielods14/suporte-tecnico-sistema.git
cd suporte-tecnico-sistema
```

### 2. Criar branch a partir de develop

```bash
git checkout develop
git pull origin develop
git checkout -b feature/nome-da-feature
```

### 3. Fazer commits descritivos

Use mensagens claras e no imperativo (ex: Adiciona login na API, Corrige bug na tela de cadastro).
Evite commits genéricos como "update", "fix" ou "teste".

### 4. Enviar para o repositório remoto

```bash
git add .
git commit -m "Mensagem descritiva"
git push origin feature/nome-da-feature
```

### 5. Abrir Pull Request (PR)

No GitHub, abra um PR da sua branch para develop.
Aguarde revisão de pelo menos um colega antes do merge.

---

## 📝 Convenções

### Nomenclatura de Branches
- `feature/descricao-feature` - Para novas funcionalidades
- `fix/descricao-bug` - Para correções de bugs
- `hotfix/descricao-urgente` - Para correções urgentes
- `docs/descricao-docs` - Para atualizações de documentação

### Mensagens de Commit

✅ **Bom:**
- "Adiciona autenticação JWT na API"
- "Corrige validação de email no formulário"
- "Implementa página de detalhes do chamado"

❌ **Evite:**
- "update"
- "fix"
- "teste"
- "mudanças"

---

## ✅ Checklist antes de enviar PR

- [ ] Código compila/executa sem erros
- [ ] Funcionalidade foi testada
- [ ] Commits são descritivos
- [ ] Documentação atualizada (se necessário)

---

## 📞 Dúvidas?

Se tiver dúvidas sobre como contribuir:
- Abra uma issue no repositório
- Consulte os READMEs específicos de cada módulo

---

**Obrigado por contribuir!** 🚀
