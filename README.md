# Digital Campus Library Reservation Gateway (LRG)
## Software Engineering Mini-Project - Consolidated Team Repository

[![CI Quality Gate](https://github.com/DharshiniPES/SE-Lab-Project-PES1UG24AM084-PES1UG24AM428-PES1UG24AM094-PES1UG24AM087/actions/workflows/ci.yml/badge.svg)](https://github.com/DharshiniPES/SE-Lab-Project-PES1UG24AM084-PES1UG24AM428-PES1UG24AM094-PES1UG24AM087/actions)
![Tests](https://img.shields.io/badge/tests-88%2F88%20passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-89%25-brightgreen)
![Branch Coverage](https://img.shields.io/badge/branch%20coverage-83%25-brightgreen)
![WCAG](https://img.shields.io/badge/accessibility-WCAG%202.1%20AA-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)

Consolidated collaborative repository for the **Software Engineering Mini-Project**, Department of Computer Science and Engineering, **PES University**.

---

## 1. Project Team Members and Use Case Allocation

| Student Name | SRN | Role | Assigned Use Case / System Domain |
| :--- | :--- | :--- | :--- |
| **Dharshini V** | **PES1UG24AM428** | Dev Lead and Full-Stack Architect | **UC-04b: Pay Overdue Fine & Settle Dues**, UC-03 Hold Gatekeeper, Full-Stack Architecture |
| **Dhareen G** | **PES1UG24AM084** | QA Lead and Scrum Master | **UC-01: Search ISBN Catalog**, **UC-06: Return Title & Availability**, **UC-07: Notifications** |
| **Divyansh** | **PES1UG24AM094** | Backend and Analytics Lead | **UC-01: Search ISBN Catalog**, **UC-08: Manage Catalog Entries**, **UC-09: Hold Demand Report** |
| **Dhruv Talavat** | **PES1UG24AM087** | Database and Security Lead | **UC-02: View Book Details**, **UC-03: Place Hold Request**, **UC-04: View & Cancel Holds** |

---

## 2. Project Deliverables Summary

All three course deliverables are maintained in this single repository:

### Deliverable 1: System Specifications and Architecture (`Lab-04-SRS-SAD-STP/`)
Foundational software engineering documentation for the Digital Campus Library Reservation Gateway:
- **Software Requirements Specification (SRS)**: [`Lab-04-SRS-SAD-STP/SRS_Library_Reservation_Gateway (1).pdf`](Lab-04-SRS-SAD-STP/SRS_Library_Reservation_Gateway%20(1).pdf)
  - Complete functional requirements (`LRG-F-001` to `LRG-F-052`), non-functional requirements (`LRG-NF-001` to `LRG-NF-007`), security specifications (`LRG-SR-001` to `LRG-SR-007`), UML use-case models, and Requirements Traceability Matrix (RTM).
- **Software Architecture and Design (SAD)**: [`Lab-04-SRS-SAD-STP/SAD_Library_Reservation_Gateway (1).pdf`](Lab-04-SRS-SAD-STP/SAD_Library_Reservation_Gateway%20(1).pdf)
  - Layered modular architecture, provided and required component interfaces, sequence diagrams, REST API schemas, and STRIDE threat modeling.
- **Software Test Plan (STP v2.0 - Post-Sprint Updated)**: [`Lab-04-SRS-SAD-STP/Test_Plan_Library_Reservation_Gateway.docx`](Lab-04-SRS-SAD-STP/Test_Plan_Library_Reservation_Gateway.docx)
  - Post-sprint updated test strategy, entry and exit criteria, updated test catalogue for all 10 use cases, and 100% accepted RTM.

### Deliverable 2: Software Implementation (`src/`)
Production-grade modular web application built with **Python 3.11 / Flask** and **SQLite** (foreign keys enforced with ACID transactions):
- **`src/catalog_search.py`**: Search across 100,000 titles by ISBN, title, or author; pagination (10/page); book detail view; hyphen-flexible ISBN normalization (`TC-SRCH-07`).
- **`src/auth.py`**: Campus OpenID Connect SSO authentication; 30-minute idle session timeout; 5-attempt brute-force lockout for 15 minutes (`LRG-SR-005`).
- **`src/reservation_manager.py`**: FIFO hold queue placement; 5-hold limit; Available title rejection; 72-hour auto-expiration worker with cascade queue promotion (`TC-HOLD-06`).
- **`src/fine_manager.py`**: **UC-04b: Pay Overdue Fine & Settle Dues**; daily overdue balance calculation ($1/day); payment processing via Campus Wallet and UPI; digital receipt issuance; automated hold restrictions.
- **`src/notification.py`**: Hold-ready notices (72h pickup window); 24h expiration reminders; 3-attempt exponential backoff retry on SMTP downtime.
- **`src/admin.py`**: Librarian administration center; title return processing; hold demand rankings; book addition and editing; strict RBAC.
- **`src/security.py`**: Sliding-window rate limiter (60 req/min); SQL injection and XSS sanitization; password non-storage enforcement.
- **`src/database.py`**: Relational schema, SQLite transactional connection manager, and catalog seed data.
- **`src/templates/` and `src/static/`**: High-contrast, mobile-responsive web UI meeting **WCAG 2.1 AA** standards from 360px viewport width up.

### Deliverable 3: Quality Assurance, Verification and Sprint Tracking (`docs/`)
All four formal test reports executed during the testing window (**2nd Nov to 6th Nov 2026**):

| Deliverable Item | Document Reference | Scope and Results |
| :--- | :--- | :--- |
| **Updated Test Cases** | [`docs/Updated_Test_Case_Document.md`](docs/Updated_Test_Case_Document.md) | Granular post-sprint changes for all 10 use cases, baseline comparisons, and updated test cases. |
| **Unit Test Report** | [`docs/Unit_Test_Report.md`](docs/Unit_Test_Report.md) | 88 automated unit and integration tests itemized by use case; **100% pass rate**; 0 open defects. |
| **System Validation Report** | [`docs/System_Validation_Report.md`](docs/System_Validation_Report.md) | Multi-tier E2E validation for all 10 use cases, NFR latency benchmarks (0.0051s), WCAG compliance, STRIDE matrix. |
| **Code Coverage Report** | [`docs/Code_Coverage_Report.md`](docs/Code_Coverage_Report.md) | **89% overall statement coverage**; **93.8% business-layer coverage** (surpassing 70% requirement). |
| **Branch Coverage Report** | [`docs/Branch_Coverage_Report.md`](docs/Branch_Coverage_Report.md) | **82.6% branch coverage** across 270 decision points; verifies all boundary conditions and error branches. |
| **Executive Test Summary** | [`docs/Test_Summary_Report.md`](docs/Test_Summary_Report.md) | Executive summary and formal sign-offs across all 4 team members. |
| **Sprint-3 and Jira Report** | [`docs/Sprint_3_Report_and_Jira_Tracking.md`](docs/Sprint_3_Report_and_Jira_Tracking.md) | Agile tracking, user stories, Fibonacci story points (85 pts total), 100% completed burndown chart. |
| **Interactive Jira Dashboard** | [`docs/jira_dashboard.html`](docs/jira_dashboard.html) | Interactive Atlassian Jira Software board (Kanban columns, Backlog, Burndown chart, SRS Traceability). Also served at `/jira`. |
| **Test Plan Word Document** | [`docs/Test_Plan_Library_Reservation_Gateway_v2.0.docx`](docs/Test_Plan_Library_Reservation_Gateway_v2.0.docx) | Official formatted Microsoft Word STP v2.0 document. |

---

## 3. Git Architecture and Branching Model

This repository is organized strictly for the consolidated project:

```
+-----------------------------------------------------------------------------------------+
|                                    GIT BRANCHING MODEL                                  |
|                                                                                         |
|   [feature/sprint branches]  --->  [PES1UG24AM428]  --->  [PR / CI Gate]  --->  [main]  |
|                                                                                         |
|   - main: Stable production release branch containing verified deliverables             |
|   - PES1UG24AM428: Active developer tracking branch for Dharshini V (Dev Lead)          |
|   - CI/CD Actions: Triggers on PR and push to validate all 88 tests and coverage >= 70% |
+-----------------------------------------------------------------------------------------+
```

### Git Directory Structure

```text
SE-Lab-Project/
|-- .github/
|   `-- workflows/
|       `-- ci.yml                               # Automated GitHub Actions CI/CD pipeline
|-- Lab-04-SRS-SAD-STP/                          # Deliverable 1: Core Project Specifications
|   |-- SRS_Library_Reservation_Gateway (1).pdf  # Software Requirements Specification
|   |-- SAD_Library_Reservation_Gateway (1).pdf  # Software Architecture & Design Document
|   |-- Test_Plan_Library_Reservation_Gateway.docx # Software Test Plan v2.0
|   `-- readme.md
|-- docs/                                        # Deliverable 3: Test Reports & Quality Assurance
|   |-- Unit_Test_Report.md                      # 88 Unit tests itemized by use case
|   |-- System_Validation_Report.md              # E2E validation traces across all 10 use cases
|   |-- Code_Coverage_Report.md                  # 89% statement coverage analysis
|   |-- Branch_Coverage_Report.md                # 82.6% branch coverage across 270 branches
|   |-- Test_Summary_Report.md                   # Executive testing summary & team approvals
|   |-- Updated_Test_Case_Document.md            # Post-sprint test case catalogue
|   |-- Test_Plan_Library_Reservation_Gateway_v2.0.docx # Formatted Word STP v2.0
|   |-- Sprint_3_Report_and_Jira_Tracking.md     # Sprints 1-3 Jira tracking & burndown chart
|   |-- coverage.xml                             # Machine-readable Cobertura XML report
|   `-- coverage_html/                           # Interactive HTML code coverage site
|-- src/                                         # Deliverable 2: Software Implementation
|   |-- __init__.py
|   |-- app.py                                   # Flask REST API and UI router
|   |-- admin.py                                 # Head Librarian administration & RBAC
|   |-- audit.py                                 # Immutable audit logging (1-year retention)
|   |-- auth.py                                  # Campus SSO, idle expiry & lockout
|   |-- catalog_search.py                        # ISBN search, pagination & normalization
|   |-- database.py                              # SQLite relational schema & seeds
|   |-- fine_manager.py                          # UC-04b: Overdue fine calculation & payment
|   |-- notification.py                          # Hold-ready email & exponential retry queue
|   |-- reservation_manager.py                   # FIFO hold queue & 72h auto-expire cascade
|   |-- security.py                              # Sliding-window rate limiter & sanitization
|   |-- templates/                               # WCAG 2.1 AA accessible HTML templates
|   `-- static/                                  # Responsive stylesheets and client scripts
|-- tests/                                       # Automated Test Suites (88 Tests Passing)
|   |-- conftest.py                              # Pytest fixtures & isolated in-memory DB
|   |-- test_all_use_cases.py                    # 27 dedicated tests directly validating UC-01 to UC-09
|   |-- test_admin.py                            # TC-ADM tests
|   |-- test_app_routes.py                       # HTTP routes & web view integration tests
|   |-- test_auth.py                             # TC-AUTH tests
|   |-- test_catalog_search.py                   # TC-SRCH tests
|   |-- test_fine_manager.py                     # TC-FINE tests (UC-04b)
|   |-- test_notification.py                     # TC-NOTF tests
|   |-- test_reservation_manager.py              # TC-HOLD tests
|   |-- test_security_audit.py                   # TC-SEC and TC-AUD tests
|   |-- test_system_e2e.py                       # Multi-stage end-to-end system flows
|   `-- test_coverage_boost.py                   # Edge-case decision branch tests
|-- scripts/
|   |-- run_all_tests.py                         # Automated test execution script
|   |-- seed_data.py                             # Relational database seeding script
|   `-- generate_docx_test_plan.py               # Word document generation script
|-- .gitignore
|-- pytest.ini
|-- requirements.txt
`-- README.md
```

---

## 4. Local Quick Start Instructions

### 1. Clone the Repository and Install Dependencies
```bash
git clone https://github.com/DharshiniPES/SE-Lab-Project-PES1UG24AM084-PES1UG24AM428-PES1UG24AM094-PES1UG24AM087.git
cd SE-Lab-Project-PES1UG24AM084-PES1UG24AM428-PES1UG24AM094-PES1UG24AM087
pip install -r requirements.txt
```

### 2. Run the Automated Test Suite and Check Coverage
```bash
# Execute all 88 tests with statement and branch coverage
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html:docs/coverage_html --cov-report=xml:docs/coverage.xml

# Alternatively, run via the automated script
python scripts/run_all_tests.py
```

### 3. Launch the Web Application
```bash
python -m src.app
```
Open a browser and navigate to `http://localhost:5000`:
- **Catalog Search**: `/`
- **Book Details and Hold Placement**: `/book/<isbn>`
- **My Active Holds**: `/my-holds`
- **Overdue Fines and Payment Desk (UC-04b)**: `/fines`
- **Head Librarian Administration**: `/admin`
- **Campus SSO Login**: `/login`
- **Interactive Jira Agile Dashboard**: `/jira`
- **System Health Endpoint**: `/health`

---

## 5. Continuous Integration (CI/CD) Pipeline

Configured at [`.github/workflows/ci.yml`](.github/workflows/ci.yml):
- **Triggers**: On every `push` and `pull_request` to `main` and teammate branches.
- **Pipeline Stages**:
  1. Environment Provisioning & Dependency Caching
  2. Code Linting & Syntax Verification
  3. Hermetic Unit Test Execution
  4. End-to-End System Validation
  5. Code Coverage Threshold Gating ($\ge 70\%$)
  6. Artifact Archiving (HTML and XML coverage reports)

---

2026 PES University - Software Engineering Mini-Project Team Collaboration
