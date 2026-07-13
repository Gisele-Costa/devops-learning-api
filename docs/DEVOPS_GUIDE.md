# 📚 DevOps Guide - Complete Learning Path

Este guia explica **cada conceito DevOps** que você vai aprender neste projeto, stage por stage.

## 📖 Índice

1. [Fundamentos](#fundamentos)
2. [Stage 1: CI - Lint & Test](#stage-1-ci---lint--test)
3. [Stage 2: Build](#stage-2-build)
4. [Stage 3: CD - Deploy](#stage-3-cd---deploy)
5. [Stage 4: Segurança](#stage-4-segurança)
6. [Stage 5: Observabilidade](#stage-5-observabilidade)
7. [Glossário](#glossário)

---

## 📖 Fundamentos

### O que é DevOps?

DevOps é a **integração entre Desenvolvimento e Operações**. Significa automatizar:
- ✅ Build (compilação/empacotamento)
- ✅ Test (testes automatizados)
- ✅ Deploy (colocar em produção)
- ✅ Monitor (acompanhar saúde da aplicação)

**Objetivo**: Entrega rápida e confiável de software.

### CI/CD - O coração do DevOps

```
CI (Continuous Integration)
    └─ Integração contínua de código
    └─ Build automático
    └─ Testes automatizados
    └─ Qualidade verificada
            │
            ▼
CD (Continuous Delivery/Deployment)
    └─ Deploy automatizado
    └─ Sem intervenção manual
    └─ Seguro e previsível
```

**Diferença:**
- **CI/CD**: Automação + Deploy automático
- **CD de Delivery**: Código pronto pra produção (manual final)
- **CD de Deployment**: Automático até a produção

### Pipeline

Um **pipeline é uma sequência de etapas automatizadas**:

```
Code Push
    │
    ▼
┌─ Lint (verificar código)
│
├─ Testes (validar comportamento)
│
├─ Build (gerar artefato)
│
├─ Security Scan (verificar vulnerabilidades)
│
├─ Deploy (colocar online)
│
└─ Monitor (acompanhar)
```

---

## Stage 1: CI - Lint & Test

### 🎯 Objetivo
Garantir que **todo código que entra no repositório é de qualidade**.

### 📚 Conceitos

#### 1️⃣ Lint (Linting)

**O que é?** Ferramenta que verifica se o código segue padrões de formatação e qualidade.

**Por quê?**
- ✅ Código consistente entre desenvolvedores
- ✅ Previne erros comuns
- ✅ Melhora legibilidade

**Ferramentas:**
- `flake8` - Linter Python (verifica estilo)
- `pylint` - Verificação mais profunda
- `black` - Formatador automático
- `isort` - Organiza imports

**Exemplo:**
```python
# ❌ Ruim (violação flake8)
x=1  # Espaços em volta do = importantes
import os, sys  # Imports em uma linha
def foo( ):pass  # Espaços desnecessários

# ✅ Bom (passa em linters)
x = 1  # Espaçamento correto
import os
import sys  # Imports separados
def foo():
    pass  # Indentação correta
```

#### 2️⃣ Testes Automatizados (Testing)

**O que é?** Código que valida se o código principal funciona corretamente.

**Por quê?**
- ✅ Previne regressões (bugs que voltam)
- ✅ Documenta comportamento esperado
- ✅ Confiança pra refatorar

**Tipos:**
- **Unit Tests**: Testam função isolada
- **Integration Tests**: Testam múltiplos componentes
- **E2E Tests**: Testam fluxo completo

**Exemplo:**
```python
# Teste simples
def test_create_item():
    response = client.post("/api/items", json={"title": "Test"})
    assert response.status_code == 201  # Esperado: sucesso
    assert response.json()["title"] == "Test"
```

#### 3️⃣ Code Coverage

**O que é?** Percentual do código que é testado.

**Exemplo:**
- Se você tem 100 linhas e 80 linhas têm testes: **80% coverage**
- Meta: > 80% (varia por projeto)

**Usando Pytest:**
```bash
pytest --cov=app --cov-report=html
# Gera relatório HTML com coverage
```

### ✅ No nosso projeto (Stage 1)

O workflow `.github/workflows/stage-1-lint-test.yml` faz:

1. **Lint**
   - Flake8 verifica formatação
   - Black verifica formatting
   - isort verifica organização de imports

2. **Tests**
   - Pytest roda todos os testes
   - Gera coverage report
   - Falha se coverage < objetivo

3. **Status Check**
   - PR não pode ser merged se falhar

### 🚀 Como funciona no GitHub

```
Você faz: git push
    │
    ▼
GitHub Actions dispara Stage 1
    │
    ├─ Instala dependências
    │
    ├─ Roda flake8
    │
    ├─ Roda pytest
    │
    ├─ Calcula coverage
    │
    └─ ✅ ou ❌ Status
```

---

## Stage 2: Build

### 🎯 Objetivo
Empacotar a aplicação em um **container Docker** pronto para produção.

### 📚 Conceitos

#### 1️⃣ Containerização

**O que é?** Empacotar aplicação + dependências em uma unidade isolada.

**Por quê?**
- ✅ "Funciona no meu PC" não é mais desculpa
- ✅ Consistência entre ambientes
- ✅ Fácil escalabilidade

**Comparação:**

```
Virtual Machine (VM)
└─ 100GB disco
└─ 4GB RAM
└─ Full OS separado
└─ Lento, pesado

Docker Container
└─ 500MB disco (aprox)
└─ Compartilha kernel do SO
└─ Rápido, leve
```

#### 2️⃣ Docker & Dockerfile

**Docker**: Plataforma de containerização.

**Dockerfile**: Receita pra buildar um container.

**Exemplo:**
```dockerfile
FROM python:3.11-slim      # Imagem base
WORKDIR /app              # Diretório de trabalho
COPY requirements.txt .   # Copiar deps
RUN pip install -r requirements.txt  # Instalar
COPY app/ .              # Copiar código
CMD ["uvicorn", "app.main:app"]  # Comando padrão
```

**Conceitos:**
- `FROM`: Imagem base (Python já instalado)
- `WORKDIR`: Pasta dentro do container
- `COPY`: Copia arquivo do host pra container
- `RUN`: Executa comando (durante build)
- `CMD`: Comando padrão (quando inicia container)

#### 3️⃣ Multi-stage Build

**Problema**: Dockerfile grande = container grande

**Solução**: Separar build e runtime

```dockerfile
# Stage 1: Build
FROM python:3.11 as builder
RUN pip install -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
COPY --from=builder /dependencies .
COPY app/ .
CMD [...]
```

**Benefício:** Imagem final menor (sem compiladores, etc)

#### 4️⃣ Container Registry

**O que é?** Armazém de imagens Docker (tipo GitHub para containers).

**Exemplos:**
- Docker Hub (docker.io)
- GitHub Container Registry (ghcr.io) ← Usado aqui
- AWS ECR
- Google Container Registry

**Flow:**
```
Build local
    │
    ▼
Tag imagem com registry
    example: ghcr.io/user/app:v1.0
    │
    ▼
Push pro registry
    docker push ghcr.io/user/app:v1.0
    │
    ▼
Pull em qualquer lugar
    docker pull ghcr.io/user/app:v1.0
```

### ✅ No nosso projeto (Stage 2)

O workflow `.github/workflows/stage-2-build-docker.yml` faz:

1. **Build da imagem**
   - Multi-stage Dockerfile
   - Otimizado pra produção
   - Usuário non-root (segurança)

2. **Push pro registry**
   - GitHub Container Registry (GHCR)
   - Tag automática (branch, version)

3. **Teste da imagem**
   - Inicia container
   - Testa health check
   - Valida que funciona

### 🚀 Como funciona

```
Stage 1 passa ✅
    │
    ▼
Stage 2 dispara
    │
    ├─ docker build .
    ├─ Tag imagem
    ├─ docker push
    │
    └─ ✅ Imagem pronta em ghcr.io
```

---

## Stage 3: CD - Deploy

### 🎯 Objetivo
Colocar a aplicação **rodando em produção** automaticamente.

### 📚 Conceitos

#### 1️⃣ Ambientes

**Diferentes estágios de uma app:**

```
Development (DEV)
├─ Seu PC local
├─ Mudanças frequentes
├─ Sem restrição
└─ Pode quebrar

Staging (STG/QA)
├─ Cópia de Produção
├─ Testa antes de ir pra prod
├─ Auto-deploy (qualquer branch)
└─ Seguro pra errar

Production (PROD)
├─ Servidor real
├─ Usuários reais
├─ Deploy cuidadoso (apenas releases)
└─ Zero-downtime required
```

#### 2️⃣ Estratégias de Deploy

**Blue-Green:**
```
Versão Azul (ATUAL)
    ↓ (recebe tráfico)
Versão Verde (NOVA)
    │
    └─ Testes passam?
       ├─ SIM: Muda tráfico pra Verde
       └─ NÃO: Volta pra Azul
```

**Canary:**
```
Versão Nova
    │
    ├─ 10% tráfico → teste
    ├─ 50% tráfico → mais teste
    └─ 100% tráfico → deploy completo
```

**Rolling:**
```
Versão V1: [V1, V1, V1, V1] ← 4 instances
    ↓ Substitui 1 por vez
Versão V2: [V2, V1, V1, V1]
    ↓
Versão V2: [V2, V2, V1, V1]
    ↓
Versão V2: [V2, V2, V2, V2]
```

#### 3️⃣ Deployment Automation

**O que é?** Máquina dispara deploy sem interferência humana.

**Trigger:**
- **Automático**: Merge pra main = deploy staging
- **Semi-automático**: Tag Git = deploy prod (com aprovação)
- **Manual**: Botão no GitHub (workflow_dispatch)

#### 4️⃣ Health Check & Monitoring

**Problema:** Deploy falhou, como saber?

**Solução:** Health check
```bash
GET /health
└─ {"status": "healthy", "timestamp": ...}
```

**Deployment verifica:**
- Container startou?
- Porta aberta?
- Health check responde OK?

### ✅ No nosso projeto (Stage 3)

O workflow `.github/workflows/stage-3-deploy.yml` faz:

1. **Deploy pra Staging**
   - Automático todo merge em main
   - Testa aplicação

2. **Deploy pra Production**
   - Quando cria TAG (v1.0, v2.0)
   - Com aprovação manual
   - Zero-downtime

3. **Rollback**
   - Se falhar, volta pra versão anterior

### 🚀 Como funciona

```
Merge em main
    │
    ▼
Stage 3 dispara
    │
    ├─ Deploy pra Staging
    ├─ Health checks passam?
    │
    └─ Se tudo OK, pronto pra Production

Criar TAG v1.0.0
    │
    ▼
Stage 3 dispara (Production job)
    │
    ├─ Requer aprovação
    ├─ Deploy pra Production
    ├─ Monitora
    │
    └─ ✅ Em produção!
```

---

## Stage 4: Segurança

### 🎯 Objetivo
Garantir que **nada malicioso ou vulnerável** chega a produção.

### 📚 Conceitos

#### 1️⃣ Dependency Scanning

**Problema:** Você usa biblioteca X, X tem vulnerability.

**Solução:** Scan automático de dependências

**Ferramentas:**
- `safety` - Verifica conhecido vulnerabilities
- `pip-audit` - Auditoria de pacotes
- GitHub Dependabot - Automático

**Exemplo:**
```bash
$ safety check
# Output:
# - Django 3.0 has SQL injection vulnerability
# - Flask 1.0 deprecated
```

#### 2️⃣ SAST (Static Application Security Testing)

**O que é?** Analisa código **sem executar**.

**Detecta:**
- SQL injection
- XSS vulnerabilities
- Insecure cryptography
- Hard-coded credentials

**Ferramentas:**
- CodeQL (GitHub)
- SonarQube
- Bandit (Python)

#### 3️⃣ Container Scanning

**Problema:** Imagem Docker tem vulnerabilidades.

**Solução:** Scan de imagem

**Ferramentas:**
- Trivy
- Grype
- Anchore

**Exemplo:**
```bash
trivy image ghcr.io/user/app:latest
# Output:
# - glibc 2.31 has CVE-2021-3...
# - Python 3.8 deprecated
```

#### 4️⃣ Secret Management

**Problema:** Credentials hard-coded no código

**Solução:** GitHub Secrets

**Boas práticas:**
```bash
# ❌ NUNCA faça
DATABASE_PASSWORD = "senha123"  # No código!

# ✅ SEMPRE faça
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
# E no GitHub: Settings → Secrets
```

**GitHub Secrets:**
```yaml
# No workflow
- name: Deploy
  env:
    DB_PASS: ${{ secrets.DATABASE_PASSWORD }}
  run: ...
```

#### 5️⃣ Secret Scanning Automático

**GitHub Secret Scanning** detecta automaticamente:
- AWS keys
- GitHub tokens
- API keys
- Certificados

Se achar, avisa pra revogar!

### ✅ No nosso projeto (Stage 4)

O workflow `.github/workflows/stage-4-security.yml` faz:

1. **Dependency Scanning**
   - Safety check
   - Vulnerabilities report

2. **SAST**
   - CodeQL analysis
   - Vulnerabilities detected

3. **Container Scanning**
   - Trivy scan
   - Reports uploaded

4. **Secret Scanning**
   - TruffleHog
   - Detecta secrets vazados

### 🚀 Como funciona

```
Você faz: git push
    │
    ▼
Stage 1: Lint & Test ✅
    │
    ▼
Stage 2: Build ✅
    │
    ▼
Stage 4: Security Scan
    │
    ├─ Dependency check
    ├─ Code analysis (SAST)
    ├─ Container scan
    ├─ Secret scan
    │
    └─ ✅ Seguro!
```

---

## Stage 5: Observabilidade

### 🎯 Objetivo
**Entender o que está acontecendo** com sua aplicação em produção.

### 📚 Conceitos

#### 1️⃣ Observabilidade vs Monitoramento

**Monitoramento:**
```
Faz: GET /api/items
└─ Resposta: 200 OK
└─ Tempo: 50ms
```

**Observabilidade:**
```
GET /api/items
├─ API recebeu
│  ├─ Validou parâmetros
│  ├─ Consultou banco
│  │   └─ Query demorou 40ms
│  ├─ Processou dados
│  └─ Retornou
│
└─ Resposta: 200 OK em 50ms (visibilidade TOTAL)
```

**3 pilares:**
- **Logs**: O que aconteceu?
- **Metrics**: Números (CPU, memória, requisições)
- **Traces**: Caminho da requisição pelo sistema

#### 2️⃣ SLO (Service Level Objective)

**O que é?** Meta de confiabilidade/performance.

**Exemplos:**
```
Availability: 99.9%
├─ Aplicação offline < 45 minutos/mês

Response Time: < 200ms (P95)
├─ 95% das requisições respondem em < 200ms

Error Rate: < 0.1%
├─ Menos de 1 em 1000 requisições falham
```

#### 3️⃣ Métricas Importantes

**Quatro Golden Signals:**
1. **Latência** - Quanto tempo leva?
2. **Tráfico** - Quantas requisições?
3. **Errors** - Quantas falharam?
4. **Saturation** - CPU/memória quase full?

**Exemplo:**
```
GET /api/items
├─ Latência: 50ms ✅
├─ Tráfico: 1000 req/s ✅
├─ Errors: 0 ✅
└─ CPU: 45% ✅ (não saturado)
```

#### 4️⃣ Logging

**Estruturado vs Unstructured:**

```yaml
# ❌ Unstructured
"2024-01-13 10:30:45 User created"

# ✅ Structured (JSON)
{
  "timestamp": "2024-01-13T10:30:45Z",
  "level": "INFO",
  "event": "user_created",
  "user_id": 123,
  "email": "user@example.com",
  "duration_ms": 45
}
```

**Benefício:** Fácil buscar, filtrar, agregar.

#### 5️⃣ Code Metrics

**O que medir:**
- **Lines of Code (LOC)** - Tamanho do projeto
- **Cyclomatic Complexity** - Quanto complexo?
- **Coverage** - % de código testado
- **Technical Debt** - Quanto "refactor" precisa?

**Exemplo:**
```
app/main.py
├─ 250 LOC
├─ 5 functions
├─ 3 classes
├─ 85% coverage ✅
└─ Low complexity ✅
```

### ✅ No nosso projeto (Stage 5)

O workflow `.github/workflows/stage-5-observability.yml` faz:

1. **Métricas**
   - Linhas de código
   - Functions/Classes count
   - Coverage

2. **Performance**
   - Load test
   - Response time baseline

3. **Dependency Updates**
   - Verifica packages outdated
   - Sugere atualizações

4. **SLO Check**
   - Define SLOs
   - Verifica compliance

### 🚀 Como funciona

```
Aplicação rodando
    │
    ▼
Logger coleta eventos
    │
    ├─ Metrics exporter
    ├─ Logs coletados
    └─ Traces recorded
    │
    ▼
Backend (Prometheus, ELK, etc)
    │
    ▼
Dashboard (Grafana)
    │
    ▼
Alertas se SLO violado
```

---

## 📊 Overview Completo

```
┌─────────────────────────────────────────────────────┐
│ Você escreve código                                  │
└──────────────┬──────────────────────────────────────┘
               │
    ┌──────────▼──────────┐
    │ git push / PR       │
    └──────────┬──────────┘
               │
    ┌──────────▼──────────────────────────┐
    │ Stage 1: Lint & Test                │
    │ ✓ Qualidade                         │
    │ ✓ Testes                            │
    └──────────┬──────────────────────────┘
               │
    ┌──────────▼──────────────────────────┐
    │ Stage 2: Build Docker               │
    │ ✓ Imagem criada                     │
    │ ✓ Push registry                     │
    └──────────┬──────────────────────────┘
               │
    ┌──────────▼──────────────────────────┐
    │ Stage 3: Deploy                     │
    │ ✓ Staging (automático)              │
    │ ✓ Production (com tag)              │
    └──────────┬──────────────────────────┘
               │
    ┌──────────▼──────────────────────────┐
    │ Stage 4: Security                   │
    │ ✓ Dependency check                  │
    │ ✓ Code scanning                     │
    │ ✓ Secret scanning                   │
    └──────────┬──────────────────────────┘
               │
    ┌──────────▼──────────────────────────┐
    │ Stage 5: Observabilidade            │
    │ ✓ Métricas                          │
    │ ✓ SLO check                         │
    │ ✓ Performance                       │
    └──────────┬──────────────────────────┘
               │
    ┌──────────▼──────────────────────────┐
    │ ✅ Aplicação em Produção!           │
    └─────────────────────────────────────┘
```

---

## 🔤 Glossário

| Termo | Significa | Exemplo |
|-------|-----------|---------|
| **CI/CD** | Continuous Integration/Deployment | GitHub Actions |
| **Pipeline** | Sequência automatizada | Lint → Test → Build → Deploy |
| **Artifact** | Saída do build | JAR, Docker image |
| **Registry** | Repositório de imagens | Docker Hub, GHCR |
| **Health Check** | Verificação de saúde | GET /health → 200 |
| **SLO** | Service Level Objective | 99.9% uptime |
| **SAST** | Static code analysis | CodeQL |
| **Lint** | Verificação de estilo | flake8 |
| **Coverage** | % código testado | 85% |
| **Deployment** | Colocar em produção | docker run |
| **Rollback** | Voltar versão anterior | Revert deploy |
| **Observability** | Visibilidade do sistema | Logs + Metrics + Traces |

---

## 📚 Recursos Adicionais

### Documentação Oficial
- [GitHub Actions](https://docs.github.com/en/actions)
- [Docker](https://docs.docker.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pytest](https://docs.pytest.org/)

### Blogs/Articles
- [CI/CD Explained](https://www.redhat.com/en/topics/devops/what-is-ci-cd)
- [DevOps for Beginners](https://www.atlassian.com/devops)

### Próximo Passo
Após dominar os 5 stages, veja [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) para implementar em um projeto real!

---

**Keep learning! 🚀**
