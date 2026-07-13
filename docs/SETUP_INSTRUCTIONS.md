# 🛠️ Setup Instructions - Passo a Passo

Este guia te leva do zero até ter o projeto rodando e deployado!

## 📋 Tabela de Conteúdo

1. [Pré-requisitos](#pré-requisitos)
2. [Setup Local](#setup-local)
3. [GitHub Setup](#github-setup)
4. [Rodar Localmente](#rodar-localmente)
5. [Rodar com Docker](#rodar-com-docker)
6. [Ver Workflows](#ver-workflows)
7. [Próximos Passos](#próximos-passos)

---

## 🔧 Pré-requisitos

Você precisa ter instalado:

- **Git** - Controle de versão
  ```bash
  git --version  # Verifica se tem
  ```

- **Python 3.11+** - Linguagem
  ```bash
  python --version  # ou python3 --version
  ```

- **Docker** (opcional, mas recomendado)
  ```bash
  docker --version
  ```

- **Conta GitHub** - Para clonar e pushear

### ✅ Verificar Instalação

```bash
# Windows/Mac/Linux
python --version
pip --version
git --version

# Se tem Docker
docker --version
docker run hello-world
```

---

## 📥 Setup Local

### 1️⃣ Clonar o Repositório

```bash
# HTTPS (mais fácil)
git clone https://github.com/SEU_USUARIO/devops-learning-api.git

# SSH (se tiver chave SSH)
git clone git@github.com:SEU_USUARIO/devops-learning-api.git

# Entrar na pasta
cd devops-learning-api
```

### 2️⃣ Criar Virtual Environment

**Por quê?** Cada projeto Python tem suas próprias dependências, sem conflitar com outras.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

**Como saber se ativou?** Deve aparecer `(venv)` no início da linha no terminal.

```
# Antes
C:\Users\seu_user\Estudos DevOps\Revisão DevOps\devops-learning-api>

# Depois
(venv) C:\Users\seu_user\Estudos DevOps\Revisão DevOps\devops-learning-api>
```

### 3️⃣ Instalar Dependências

```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt

# Verifica instalação
pip list
```

### 4️⃣ Criar .env (Variáveis de Ambiente)

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

**Editar o `.env`** com suas variáveis (deixa como está pra começar).

---

## 🌐 GitHub Setup

### 1️⃣ Fork ou Clone pra você

Você tem 2 opções:

**Opção A: Fork (recomendado pra aprender)**
- Vai em https://github.com/SEU_USUARIO/devops-learning-api
- Clica em "Fork" (canto superior direito)
- GitHub cria uma cópia sua

**Opção B: Clone direto**
- `git clone ...` e começa a usar

### 2️⃣ Configurar Seu Repositório

```bash
# Configurar nome e email (importante!)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Verificar
git config --list
```

### 3️⃣ Entender Branches

```bash
# Ver branch atual
git branch

# Main branch é a principal
# Develop branch é pra testes

# Criar nova branch pra trabalhar
git checkout -b minha-feature
# Agora você está em "minha-feature"

# Voltar pra main
git checkout main
```

### 4️⃣ Configurar Secrets (para Workflows)

Alguns workflows precisam de credenciais (Docker registry, deploy, etc).

**No GitHub:**
1. Vai em: Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Adiciona cada secret:

**Secrets necessários:**
```
# Se quiser usar Docker Hub
DOCKER_USERNAME = seu_usuario
DOCKER_PASSWORD = seu_token_personal_access

# Se quiser usar GitHub Container Registry
# Já usa GITHUB_TOKEN (automático)

# Deploy (quando implementar)
# DEPLOY_HOST = seu_servidor_ip
# DEPLOY_KEY = sua_chave_ssh
```

**Como gerar Docker Token:**
1. Docker Hub → Account → Security
2. New Access Token
3. Copiar token
4. Adicionar no GitHub Secrets

---

## 🚀 Rodar Localmente

### 1️⃣ Verificar Estrutura

```bash
# Listar arquivos
ls -la

# Deve ter:
# ✓ app/
# ✓ tests/
# ✓ requirements.txt
# ✓ Dockerfile
# ✓ .github/workflows/
```

### 2️⃣ Rodar Testes

```bash
# Ativar venv (se não tiver ativado)
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Rodar todos os testes
pytest

# Ver resultados detalhados
pytest -v

# Ver coverage
pytest --cov=app --cov-report=html
# Abre: htmlcov/index.html no navegador
```

### 3️⃣ Rodar Lint

```bash
# Flake8
flake8 app/ tests/

# Black (check)
black --check app/ tests/

# Black (auto-fix)
black app/ tests/

# isort
isort app/ tests/
```

### 4️⃣ Rodar Aplicação

```bash
# Opção 1: Direto com Uvicorn
uvicorn app.main:app --reload

# Opção 2: Executar main.py
python app/main.py

# Acessa no navegador: http://localhost:8000
# Documentação interativa: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

**O que significa `--reload`?** Reinicia servidor quando você modifica código (útil pra desenvolvimento).

### 5️⃣ Testar Endpoints

Abra http://localhost:8000/docs (Swagger UI)

Ou use `curl`:

```bash
# Health check
curl http://localhost:8000/health

# Listar items
curl http://localhost:8000/api/items

# Criar item
curl -X POST http://localhost:8000/api/items \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender DevOps", "description": "CI/CD com GitHub Actions"}'

# Obter item (substituir ID)
curl http://localhost:8000/api/items/1
```

---

## 🐳 Rodar com Docker

### 1️⃣ Build da Imagem

```bash
# Build
docker build -t devops-learning-api:latest .

# Verificar imagem criada
docker images | grep devops-learning-api
```

### 2️⃣ Rodar Container

```bash
# Rodar
docker run -p 8000:8000 devops-learning-api:latest

# No outro terminal, testar:
curl http://localhost:8000/health

# Ver containers rodando
docker ps
```

### 3️⃣ Docker Compose (opcional)

Criar `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
    volumes:
      - .:/app
```

Rodar:
```bash
docker-compose up
docker-compose down
```

### 4️⃣ Debug no Docker

```bash
# Ver logs
docker logs CONTAINER_ID

# Entrar no container
docker exec -it CONTAINER_ID /bin/bash

# Parar container
docker stop CONTAINER_ID

# Remover container
docker rm CONTAINER_ID
```

---

## 👀 Ver Workflows

### 1️⃣ Fazer Alteração e Push

```bash
# Criar/modificar um arquivo
echo "# Teste" >> README.md

# Add ao git
git add .

# Commit
git commit -m "Teste de workflow"

# Push
git push origin main  # ou sua branch
```

### 2️⃣ Ver Workflow Rodando

**No GitHub:**
1. Vai no seu repositório
2. Clica em "Actions"
3. Vê o workflow rodando
4. Clica para ver detalhes

**Fases:**
1. Stage 1 (Lint & Test) - 2-3 minutos
2. Stage 2 (Build Docker) - 3-5 minutos (se main)
3. Stage 3 (Deploy) - 1 minuto (se main)
4. Stage 4 (Security) - 5-10 minutos (automático)
5. Stage 5 (Observability) - 2-3 minutos

### 3️⃣ Entender Logs

Clica na etapa que quer ver:

```
✅ Lint with Flake8
  └─ $ flake8 app/ tests/ --count ...
    └─ (output aqui)

✅ Run tests with pytest
  └─ $ pytest --verbose
    └─ test_health_check_returns_ok PASSED
    └─ test_create_item PASSED
    └─ ... (todos os testes)

✅ Build and push Docker image
  └─ Pushed image: ghcr.io/user/repo:main
```

### 4️⃣ Solucionar Problemas

**Se workflow falhar:**

1. Clica em "Actions"
2. Vê qual stage falhou
3. Expande o job com erro
4. Lê a mensagem de erro
5. Corrige localmente
6. Push novamente

**Erros comuns:**

| Erro | Causa | Solução |
|------|-------|--------|
| `FAILED - test_create_item` | Teste falhou | Rodar `pytest` local e debugar |
| `E501 line too long` | Linha > 100 caracteres | Quebrar linha ou rodar `black` |
| `ModuleNotFoundError` | Dependência faltando | `pip install -r requirements.txt` |
| `Connection refused` | Porta 8000 ocupada | `lsof -i :8000` (Mac/Linux) ou end task (Windows) |

---

## 📊 Próximos Passos

### Semana 1: Dominando Stage 1

- [ ] Rodar testes localmente
- [ ] Modificar um teste e ver falhar
- [ ] Fazer um commit e ver workflow rodar
- [ ] Conseguir 100% coverage
- [ ] Entender cada ferramenta (flake8, black, pytest)

```bash
# Exercício
# 1. Abra tests/test_main.py
# 2. Mude um assert pra falso
# 3. git push
# 4. Veja workflow falhar
# 5. Conserte de volta
# 6. Push novamente
```

### Semana 2: Docker & Build

- [ ] Build imagem Docker
- [ ] Testar container local
- [ ] Entender Dockerfile
- [ ] Ver imagem sendo pushed (GitHub Actions)
- [ ] Pull imagem do registry e rodar

```bash
# Exercício
# 1. docker build -t devops-api:v1 .
# 2. docker run -p 8000:8000 devops-api:v1
# 3. curl http://localhost:8000/health
# 4. Ver imagem em GitHub Container Registry
```

### Semana 3: Deploy

- [ ] Criar um servidor (VPS, EC2, etc)
- [ ] Configurar Deploy SSH
- [ ] Implementar Stage 3 real
- [ ] Deployar aplicação
- [ ] Testar em produção

### Semana 4: Segurança

- [ ] Revisar security scan results
- [ ] Corrigir vulnerabilidades encontradas
- [ ] Configurar secrets corretamente
- [ ] Aprender sobre OWASP top 10

### Semana 5+: Observabilidade

- [ ] Configurar logging
- [ ] Integrar Prometheus
- [ ] Criar dashboard Grafana
- [ ] Setup alertas

---

## 📞 Precisa de Ajuda?

### Comandos Úteis

```bash
# Ver histórico de commits
git log --oneline

# Ver diferenças
git diff

# Ver status
git status

# Desfazer último commit (local)
git reset --soft HEAD~1

# Ver branch remoto
git remote -v

# Atualizar local com remoto
git pull origin main
```

### Debugging

```bash
# Python REPL
python
>>> from app.main import app
>>> app
<FastAPI app>

# Pytest verbose
pytest -vv

# Docker bash
docker run -it python:3.11 /bin/bash

# Ver portas ocupadas
# Windows: netstat -ano | findstr :8000
# Mac/Linux: lsof -i :8000
```

---

## ✅ Checklist Final

- [ ] Python 3.11+ instalado
- [ ] Git configurado
- [ ] Repositório clonado
- [ ] Virtual environment criado
- [ ] Dependências instaladas
- [ ] Testes passando localmente
- [ ] Aplicação rodando em http://localhost:8000
- [ ] Docker instalado e testado
- [ ] Imagem Docker buildada e rodada
- [ ] GitHub secrets configurados
- [ ] Primeiro workflow rodou
- [ ] Entendi o que cada stage faz

---

## 🚀 Você está pronto!

Parabéns! Agora você tem:
- ✅ Projeto local configurado
- ✅ Testes rodando
- ✅ Docker funcionando
- ✅ CI/CD pipeline ativo
- ✅ Segurança checando
- ✅ Métricas coletando

**Próximo passo:** Fazer mudanças, ver pipeline funcionar, aprender na prática!

Bora começar? 🚀

```bash
# Seu primeiro push
git checkout -b minha-primeira-feature
# ... (faz uma mudança)
git add .
git commit -m "Primeira mudança"
git push origin minha-primeira-feature

# Vai em GitHub, cria PR, vê workflow rodar!
```

**Happy DevOps Learning! 🎉**
