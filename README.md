# 🚀 DevOps Learning API

Uma aplicação FastAPI simples criada para **aprender DevOps do básico ao avançado**, com foco em CI/CD, Docker, GitHub Actions e segurança.

## 📋 O que você vai aprender

Este projeto é um **plano de estudo prático estruturado em 5 etapas**, cada uma adicionando complexidade:

| Etapa | Foco | Duração |
|-------|------|---------|
| **1** | Fundamentos: Lint, Testes, CI | Semana 1 |
| **2** | Docker: Build, Push, Registry | Semana 2 |
| **3** | Deploy: Staging, Production | Semana 3 |
| **4** | Segurança: Scanning, Secrets | Semana 4 |
| **5** | Observabilidade: Métricas, SLO | Semana 5+ |

## 🏗️ Arquitetura

```
┌─────────────┐
│   GitHub    │  Push Code / Create PR
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│   GitHub Actions CI/CD Pipelines    │
├─────────────────────────────────────┤
│ Stage 1: Lint & Test                │
│ Stage 2: Build Docker Image         │
│ Stage 3: Deploy (Staging/Prod)      │
│ Stage 4: Security Scanning          │
│ Stage 5: Observability & Metrics    │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│   Container Registry (GHCR)         │
│   ghcr.io/username/repo:tag         │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│   Deployment Environments           │
├─────────────────────────────────────┤
│ ✓ Staging (auto-deploy on main)     │
│ ✓ Production (deploy on tag)        │
└─────────────────────────────────────┘
```

## 🎯 Aplicação

A API tem endpoints simples para gerenciar itens (to-do list):

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/health` | Health check |
| `GET` | `/api/items` | Listar itens |
| `POST` | `/api/items` | Criar item |
| `GET` | `/api/items/{id}` | Obter item |
| `PUT` | `/api/items/{id}` | Atualizar item |
| `DELETE` | `/api/items/{id}` | Deletar item |

## 🚀 Quick Start

### 1️⃣ Localmente

```bash
# Clonar repo
git clone <seu-repo>
cd devops-learning-api

# Setup Python
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Rodar testes
pytest --cov=app

# Rodar aplicação
uvicorn app.main:app --reload

# Acessar: http://localhost:8000/docs
```

### 2️⃣ Com Docker

```bash
# Build
docker build -t devops-learning-api .

# Run
docker run -p 8000:8000 devops-learning-api

# Test
curl http://localhost:8000/health
```

### 3️⃣ Com GitHub Actions (Automático!)

Basta fazer `push` para `main` ou criar um `PR`:
- ✅ Testes rodam
- ✅ Imagem Docker é built
- ✅ Segurança é scaneada
- ✅ Deploy automático (staging)

## 📚 Documentação Detalhada

- [🎓 DevOps Guide](docs/DEVOPS_GUIDE.md) - Conceitos e explicações de cada etapa
- [🛠️ Setup Instructions](docs/SETUP_INSTRUCTIONS.md) - Passo a passo detalhado
- [🔄 Workflows](docs/WORKFLOWS.md) - Explicação de cada GitHub Action

## 🗂️ Estrutura do Projeto

```
devops-learning-api/
├── .github/workflows/          # GitHub Actions (5 etapas)
│   ├── stage-1-lint-test.yml
│   ├── stage-2-build-docker.yml
│   ├── stage-3-deploy.yml
│   ├── stage-4-security.yml
│   └── stage-5-observability.yml
├── app/                        # Aplicação
│   ├── __init__.py
│   └── main.py                 # FastAPI app
├── tests/                      # Testes
│   └── test_main.py
├── docs/                       # Documentação
│   ├── DEVOPS_GUIDE.md
│   ├── SETUP_INSTRUCTIONS.md
│   └── WORKFLOWS.md
├── Dockerfile                  # Multi-stage build
├── requirements.txt            # Dependências Python
├── pyproject.toml             # Configuração do projeto
├── pytest.ini                 # Configuração de testes
├── .flake8                    # Configuração de linting
├── .dockerignore              # Arquivos ignorados no Docker
├── .gitignore                 # Arquivos ignorados no Git
├── .env.example               # Variáveis de ambiente
└── README.md                  # Este arquivo
```

## ✅ Checklist de Estudo

### Semana 1 - Fundamentos

- [ ] Entender conceitos: CI/CD, Pipeline, Build, Deploy
- [ ] Ler [Stage 1 Explanation](docs/DEVOPS_GUIDE.md#stage-1)
- [ ] Rodar testes localmente
- [ ] Ver logs do workflow Stage 1 no GitHub
- [ ] Modificar código e ver pipeline rodar

### Semana 2 - Docker

- [ ] Aprender Docker basics
- [ ] Ler [Stage 2 Explanation](docs/DEVOPS_GUIDE.md#stage-2)
- [ ] Fazer build local da imagem
- [ ] Testar imagem rodando
- [ ] Ver imagem sendo pushed no workflow

### Semana 3 - Deploy

- [ ] Entender ambientes (dev/staging/prod)
- [ ] Ler [Stage 3 Explanation](docs/DEVOPS_GUIDE.md#stage-3)
- [ ] Criar um servidor de teste (VPS/EC2/Digital Ocean)
- [ ] Implementar deploy real
- [ ] Testar deployment

### Semana 4 - Segurança

- [ ] Aprender sobre segurança em pipelines
- [ ] Ler [Stage 4 Explanation](docs/DEVOPS_GUIDE.md#stage-4)
- [ ] Revisar secrets no GitHub
- [ ] Executar scans de segurança localmente
- [ ] Configurar branch protection rules

### Semana 5+ - Observabilidade

- [ ] Aprender métricas e SLOs
- [ ] Ler [Stage 5 Explanation](docs/DEVOPS_GUIDE.md#stage-5)
- [ ] Configurar logging
- [ ] Integrar com ferramenta de monitoramento
- [ ] Criar dashboards

## 🛠️ Ferramentas Utilizadas

- **FastAPI** - Web framework moderno
- **Pytest** - Framework de testes
- **Docker** - Containerização
- **GitHub Actions** - CI/CD
- **Python 3.11** - Linguagem

## 🔐 Segurança

- Usuário non-root no Docker
- Secrets gerenciados pelo GitHub
- Scanning de vulnerabilidades automático
- Code scanning com CodeQL
- Linting e formatting obrigatório

## 📊 Métricas e Monitoring

O projeto inclui:
- ✅ Code coverage tracking
- ✅ Performance testing
- ✅ SLO definitions
- ✅ Dependency monitoring
- ✅ Security audit logs

## 🤝 Próximos Passos

Após completar o plano:

1. **Deploy Real**
   - Criar VPS ou usar cloud provider
   - Implementar deploy automático completo
   - Configurar SSL/TLS

2. **Monitoramento Avançado**
   - Integrar Prometheus + Grafana
   - Setup ELK Stack (logs)
   - Jaeger (distributed tracing)

3. **Escalabilidade**
   - Kubernetes
   - Multi-container orchestration
   - Load balancing

4. **Projeto Real**
   - Aplicar este conhecimento em um projeto real
   - Experiência em produção

## 📝 Licença

MIT

## 💬 Dúvidas?

Veja o arquivo [docs/DEVOPS_GUIDE.md](docs/DEVOPS_GUIDE.md) para explicações detalhadas de cada conceito!

---

**Happy learning! 🚀**
