# Continuous Integration & Continuous Deployment (CI/CD) Workflow Documentation

This document provides complete architectural, operational, and verification details for the **Continuous Integration and Continuous Deployment (CI/CD)** pipeline implemented for the **Digital Campus Library Reservation Gateway (DCLRG)** mini-project, in accordance with course evaluation criteria (**Department of Computer Science and Engineering, PES University**).

---

## 1. CI/CD Architecture Overview

The DCLRG pipeline is orchestrated using **GitHub Actions** and modern open-source DevOps tooling. It enforces automated quality gates from code push to containerized production deployment.

```
+---------------------------------------------------------------------------------------------------------------------+
|                                          DCLRG MULTI-STAGE CI/CD WORKFLOW                                           |
+---------------------------------------------------------------------------------------------------------------------+
|                                                                                                                     |
|  [ Git Push / PR ]                                                                                                  |
|          |                                                                                                          |
|          v                                                                                                          |
|  +-----------------------------------+                                                                              |
|  | STAGE 1: Code Quality & Security  |  --> Python 3.11 Bytecode Pre-compilation (`py_compile`)                    |
|  |           (DevSecOps)             |  --> Flake8 PEP 8 Code Style Audit (`flake8 src tests`)                     |
|  +-----------------------------------+  --> Bandit Security AST Static Analysis (`bandit -r src -s B101`)           |
|          |                                                                                                          |
|          v (Pass Gate)                                                                                              |
|  +-----------------------------------+                                                                              |
|  | STAGE 2: Hermetic Automated Tests |  --> Pytest Runner: 118 Unit, Integration, Security & E2E Tests              |
|  |         & Coverage Gating         |  --> Pytest-Cov: Statement (94.0%) & Branch (82.6%) Coverage                 |
|  +-----------------------------------+  --> Automated Threshold: Fail Build if Coverage < 70%                       |
|          |                              --> Artifact Archive: `docs/coverage_html` & `docs/coverage.xml`            |
|          v (Pass Gate)                                                                                              |
|  +-----------------------------------+                                                                              |
|  | STAGE 3: Build & Open-Source      |  --> Multi-Stage Production `Dockerfile` Build (Python 3.11-slim)            |
|  |         Containerization          |  --> Non-Root Least-Privilege Execution (`appuser:1000`)                     |
|  +-----------------------------------+  --> Container Spin-up & Smoke Test in GitHub Runner                         |
|          |                              --> REST API Healthcheck Probe (`curl -f http://localhost:5000/health`)     |
|          v (Pass Gate - main branch)                                                                                |
|  +-----------------------------------+                                                                              |
|  | STAGE 4: Continuous Deployment    |  --> Production Release Bundle (`dclrg-production-release-v1.0.0.tar.gz`)    |
|  |           (CD Staging)            |  --> PaaS Manifest Verification (`Procfile`, `docker-compose.yml`)           |
|  +-----------------------------------+  --> Ready for 1-Click Deployment (Render, Railway, Docker Engine)           |
|                                                                                                                     |
+---------------------------------------------------------------------------------------------------------------------+
```

---

## 2. Open-Source Tooling & Platform Matrix

In compliance with the project guidelines, all stages rely strictly on industry-standard open-source tools:

| Pipeline Domain | Open-Source Tool / Platform | Configuration File | Purpose & Verification Scope |
| :--- | :--- | :--- | :--- |
| **Workflow Automation** | **GitHub Actions** | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) | Orchestrates automated build, test, and deployment jobs across virtualized runners. |
| **Code Style & Linting** | **Flake8** (v7.5.0) | [`.flake8`](../.flake8) | Enforces PEP 8 compliance, clean imports, and structural readability. |
| **Security Scanning (SAST)** | **Bandit** (v1.9.4) | CLI flag `-s B101` | Analyzes Python Abstract Syntax Trees (AST) for common security vulnerabilities (OWASP Top 10). |
| **Automated Testing** | **Pytest** (v9.1.1) | [`pytest.ini`](../pytest.ini) | Executes 118 hermetic unit, integration, admin, loan, and security test cases. |
| **Coverage Analysis** | **Pytest-Cov / Coverage.py** | `requirements.txt` | Measures statement and branch decision coverage; gates build on 70% threshold. |
| **Containerization** | **Docker Engine & Buildx** | [`Dockerfile`](../Dockerfile) | Creates reproducible, lightweight container image based on `python:3.11-slim`. |
| **Container Orchestration**| **Docker Compose** | [`docker-compose.yml`](../docker-compose.yml) | Multi-container local/cloud orchestration with integrated health checks. |
| **Production WSGI Server** | **Gunicorn** (v21.2.0) | [`Procfile`](../Procfile) | Pre-fork worker process model for high-throughput production serving. |

---

## 3. Pipeline Stages & Automated Quality Gates

### Stage 1: Code Quality, Bytecode & DevSecOps Static Analysis
1. **Bytecode Verification**: Pre-compiles all Python source files via `python -m py_compile` to catch syntax or indentation regressions before running tests.
2. **Flake8 Style Audit**: Ensures all files in `src/` and `tests/` adhere to PEP 8 standards with zero critical linting failures.
3. **Bandit Security AST Scanner**: Scans the codebase for security flaws:
   - Verifies zero hardcoded secret tokens.
   - Verifies parameterized SQL queries preventing SQL injection (`B608`).
   - Verifies debug flags are disabled in production runtime (`B201`).
   - Verifies host binding security (`B104`).

### Stage 2: Hermetic Automated Testing & Coverage Enforcement
1. **Hermetic Test Execution**: Runs 118 automated tests hermetically in under 3.5 seconds using isolated in-memory and tempfile SQLite fixtures without external network dependencies.
2. **Strict Coverage Threshold Gating**:
   - Minimum Required: **70%**.
   - Achieved Statement Coverage: **94.0%** (855 of 910 lines).
   - Achieved Branch Coverage: **82.6%** (176 of 213 decision branches).
   - The workflow executes `--cov-fail-under=70`. If any branch or line drops overall coverage below 70%, the build fails immediately and blocks branch merge.
3. **Artifact Publishing**: The job archives both HTML (`docs/coverage_html/`) and XML (`docs/coverage.xml`) reports as downloadable GitHub build artifacts.

### Stage 3: Build & Docker Containerization Smoke Test
1. **Container Image Build**: Docker Buildx builds `dclrg-gateway:latest` using a multi-stage Dockerfile:
   - Base image: `python:3.11-slim`.
   - Security hardening: Executes under an unprivileged user (`appuser:1000`).
   - Integrated healthcheck: Probes `http://localhost:5000/health`.
2. **Container Smoke Test**:
   - The container is spun up inside the GitHub Actions runner.
   - An automated curl routine polls `http://localhost:5000/health` until HTTP 200 is confirmed.
   - The root `/` endpoint is fetched to verify catalog template rendering.
   - The container is safely terminated and pruned.

### Stage 4: Continuous Deployment & Release Packaging
1. **Trigger Condition**: Automatically triggers on pushes to the `main` branch once all upstream stages pass.
2. **Manifest Verification**: Verifies presence and syntax of `Dockerfile`, `docker-compose.yml`, `Procfile`, and `requirements.txt`.
3. **Release Bundle Generation**: Archives a deployable production release tarball (`dclrg-production-release-v1.0.0.tar.gz`) containing all application code, static templates, database seeds, and deployment descriptors.
4. **Cloud / PaaS Readiness**:
   - Ready for 1-click deployment on **Render**, **Railway**, or **Heroku** via `Procfile`.
   - Ready for container platforms (AWS ECS, Google Cloud Run, Azure Container Instances) via `Dockerfile`.

---

## 4. Local Execution & Verification

To verify the entire CI/CD pipeline locally before pushing commits:

```bash
# Run the local verification runner
python scripts/verify_cicd_locally.py
```

### Verification Script Output:
```text
======================================================================
LOCAL CI/CD PIPELINE VERIFICATION SUITE
Project: Digital Campus Library Reservation Gateway (DCLRG)
======================================================================
STAGE: 1. Python Syntax & Bytecode Pre-compilation
[PASSED] Bytecode Compilation Check

STAGE: 2. Flake8 Code Style & PEP 8 Standards Audit
[PASSED] Flake8 Quality Gate

STAGE: 3. Bandit DevSecOps Security AST (SAST) Scanner
[PASSED] Bandit Security Scan (0 Vulnerabilities)

STAGE: 4. Automated Hermetic Test Suite & 70% Coverage Gating
[PASSED] Pytest 118 Tests & Coverage Enforcement (91.17% total coverage)

STAGE: 5. Application Factory & REST API Healthcheck Probe
[PASSED] Healthcheck endpoint returned HTTP 200 with status=UP and db=CONNECTED

STAGE: 6. Production Deployment Manifests Check
[PASSED] All production deployment manifests verified

======================================================================
ALL CI/CD STAGES PASSED SUCCESSFULLY!
Your repository is 100% ready for GitHub Actions CI/CD and final submission evaluation.
======================================================================
```

---

## 5. Running the Application via Docker

### 1. Build and Run with Docker Compose
```bash
docker-compose up --build -d
```
Access the application at `http://localhost:5000`.

### 2. Check Container Health Status
```bash
docker ps --filter "name=dclrg_gateway_service"
```
The status column will display `(healthy)` following the initial 5-second startup grace period.

### 3. Stop Container
```bash
docker-compose down
```
