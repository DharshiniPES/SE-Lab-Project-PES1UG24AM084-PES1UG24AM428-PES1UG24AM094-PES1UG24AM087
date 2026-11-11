"""
Polishes and formats all Sprints, Components, Labels, Descriptions,
and Story Points in Abbey's live Atlassian Jira workspace (https://abbey6128.atlassian.net).
Project: DCLRG
"""

import urllib.request
import urllib.error
import base64
import json
import time

EMAIL = "abbey6128@gmail.com"
TOKEN = "ATATT3xFfGF0d2wjppzb9qzdE4lqbPJk_hj5Lqqi9Vn4xBJuADsz6zA1RxPOHV1lVu5Vj--3IMIQF4IvyKrRPRqonG4rfLpe8ebnEj67BZ36tR4u1wU0_7RNXm7S1sbSxrJIEYBZ31e__b9VYAawxNi4J0VvuIa2uIB8RWHo_8gcZJOEc3Y_wTw=D0180D06"
BASE_URL = "https://abbey6128.atlassian.net"
AUTH = "Basic " + base64.b64encode(f"{EMAIL}:{TOKEN}".encode()).decode()
DHARSHINI_ACCOUNT_ID = "712020:7079fec2-053a-47ac-a5d4-7d5f0cb2819c"

COMPONENTS = [
    {
        "name": "Catalog & Search Engine (Divyansh - PES1UG24AM094)",
        "description": "UC-01 & UC-02 Indexed search across titles, author, ISBN with query sanitization.",
        "project": "DCLRG"
    },
    {
        "name": "Authentication & QA (Dhareen G - PES1UG24AM084)",
        "description": "UC-05 Campus SSO auth, lockout middleware, title returns, and GitHub Actions CI/CD pipeline.",
        "project": "DCLRG"
    },
    {
        "name": "Database & Security (Dhruv Talavat - PES1UG24AM087)",
        "description": "UC-03 SQLite schemas, FIFO queue re-sequencing, 72h auto-expire cascade, rate limiter.",
        "project": "DCLRG"
    }
]

SPRINT_CONFIGS = [
    {
        "id": 3,
        "name": "Sprint 1: Core Search & Authentication Foundation",
        "state": "active",
        "startDate": "2026-10-19T09:00:00.000Z",
        "endDate": "2026-10-23T18:00:00.000Z",
        "goal": "Catalog search by title/author/ISBN, query sanitization, OpenID Connect SSO, database schema, responsive UI, baseline tests."
    },
    {
        "id": 4,
        "name": "Sprint 2: Hold Lifecycle & Administration",
        "state": "future",
        "startDate": "2026-10-26T09:00:00.000Z",
        "endDate": "2026-10-30T18:00:00.000Z",
        "goal": "Hold placement, cancellation, queue progression, librarian returns, hold demand report."
    },
    {
        "id": 37,
        "name": "Sprint 3: Spill-Overs, UC-04 Fine Settlement & Test Reporting",
        "state": "future",
        "startDate": "2026-11-02T09:00:00.000Z",
        "endDate": "2026-11-06T18:00:00.000Z",
        "goal": "UC-04 overdue fine calculation, Campus Wallet settlement, 72h auto-expire cascade, rate limiting, CI/CD pipeline, and all 4 test reports."
    }
]

# Mapping of ticket keys to their full metadata
TICKETS_METADATA = {
    # Sprint 1
    "DCLRG-9": {
        "owner": "Dhruv Talavat",
        "srn": "PES1UG24AM087",
        "role": "Database & Security Lead",
        "component": "Database & Security (Dhruv Talavat - PES1UG24AM087)",
        "labels": ["PES1UG24AM087", "Dhruv_Talavat", "Sprint_1", "Database", "SQLite"],
        "summary": "[Dhruv Talavat - PES1UG24AM087] LRG-101: Relational SQLite Schema & Initial Seed Data",
        "what": "Designed and deployed SQLite relational database schema with foreign key enforcement (PRAGMA foreign_keys = ON), unique constraints on titles/members, and seeded catalog entries for testing.",
        "ac": "Running schema initialization provisions titles, members, holds, fines, and audit_log tables with zero foreign-key errors.",
        "qa": "Verified in test_database.py and conftest.py fixtures.",
        "points": 5,
        "assign_to_dharshini": False
    },
    "DCLRG-10": {
        "owner": "Divyansh",
        "srn": "PES1UG24AM094",
        "role": "Backend & Catalog Lead",
        "component": "Catalog & Search Engine (Divyansh - PES1UG24AM094)",
        "labels": ["PES1UG24AM094", "Divyansh", "Sprint_1", "UC-01", "Search"],
        "summary": "[Divyansh - PES1UG24AM094] LRG-102: Catalog Search by Title, Author, ISBN (LRG-F-001)",
        "what": "Implemented high-speed indexed search across catalog titles supporting ISBN-10, ISBN-13, partial title, and author matching with sub-second response times.",
        "ac": "Sub-second response time for queries; normalized ISBN matches regardless of hyphens.",
        "qa": "Verified in TC-SRCH-01, TC-SRCH-02, TC-SRCH-07 in test_catalog_search.py.",
        "points": 5,
        "assign_to_dharshini": False
    },
    "DCLRG-11": {
        "owner": "Divyansh",
        "srn": "PES1UG24AM094",
        "role": "Backend & Catalog Lead",
        "component": "Catalog & Search Engine (Divyansh - PES1UG24AM094)",
        "labels": ["PES1UG24AM094", "Divyansh", "Sprint_1", "UC-01", "Security"],
        "summary": "[Divyansh - PES1UG24AM094] LRG-103: Search Input Validation & Sanitization (LRG-F-002)",
        "what": "Sanitized all user search inputs to neutralize SQL injection vectors and cross-site scripting (XSS) payloads using parameterized queries.",
        "ac": "SQL wildcards, HTML tags, and null bytes are escaped; empty queries prompt user without crashing.",
        "qa": "Verified in TC-SRCH-04 and TC-SEC-02 in test_security_audit.py.",
        "points": 3,
        "assign_to_dharshini": False
    },
    "DCLRG-12": {
        "owner": "Dhareen G",
        "srn": "PES1UG24AM084",
        "role": "QA Lead & Scrum Master",
        "component": "Authentication & QA (Dhareen G - PES1UG24AM084)",
        "labels": ["PES1UG24AM084", "Dhareen_G", "Sprint_1", "UC-05", "SSO_Auth"],
        "summary": "[Dhareen G - PES1UG24AM084] LRG-104: Campus SSO Authentication & Session Engine (LRG-F-010)",
        "what": "Implemented OpenID Connect SSO token verification, RBAC role assignment (student vs librarian), 30-min idle session timeout, and 5-attempt brute-force lockout for 15 minutes.",
        "ac": "Valid SSO token establishes session; 5 consecutive failed attempts lock account for 15 minutes.",
        "qa": "Verified in TC-AUTH-01, TC-AUTH-02, TC-AUTH-03 in test_auth.py.",
        "points": 5,
        "assign_to_dharshini": False
    },
    "DCLRG-13": {
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": "Fines & Payments (Dharshini V - PES1UG24AM428)",
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_1", "UI_UX", "WCAG"],
        "summary": "[Dharshini V - PES1UG24AM428] LRG-105: Responsive Catalog Search Web UI",
        "what": "Designed and implemented mobile-responsive web interface meeting WCAG 2.1 AA standards for catalog searching, pagination, and book detail cards.",
        "ac": "UI renders properly from 360px viewport width up; color contrast >= 4.5:1; fully keyboard navigable.",
        "qa": "Verified in TC-UX-01 in test_system_e2e.py.",
        "points": 3,
        "assign_to_dharshini": True
    },
    "DCLRG-14": {
        "owner": "Dhareen G",
        "srn": "PES1UG24AM084",
        "role": "QA Lead & Scrum Master",
        "component": "Authentication & QA (Dhareen G - PES1UG24AM084)",
        "labels": ["PES1UG24AM084", "Dhareen_G", "Sprint_1", "Testing", "Pytest"],
        "summary": "[Dhareen G - PES1UG24AM084] LRG-106: Baseline Unit Tests for Search & Authentication",
        "what": "Established hermetic automated pytest test suite for Sprint 1 deliverables with automated fixture isolation.",
        "ac": "All baseline unit tests pass without external network dependencies in under 2 seconds.",
        "qa": "Verified via pytest run producing 100% pass rate.",
        "points": 3,
        "assign_to_dharshini": False
    },

    # Sprint 2
    "DCLRG-15": {
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": "Fines & Payments (Dharshini V - PES1UG24AM428)",
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_2", "UC-03", "Holds"],
        "summary": "[Dharshini V - PES1UG24AM428] LRG-201: Place Hold on Checked-Out Book (LRG-F-020)",
        "what": "Implemented hold placement logic allowing authenticated students to place reservation holds on checked-out titles with automated FIFO queue position allocation.",
        "ac": "Hold request allocates next available sequential position in queue under ACID transactions.",
        "qa": "Verified in TC-HOLD-01 in test_reservation_manager.py.",
        "points": 5,
        "assign_to_dharshini": True
    },
    "DCLRG-16": {
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": "Fines & Payments (Dharshini V - PES1UG24AM428)",
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_2", "UC-03", "Validation"],
        "summary": "[Dharshini V - PES1UG24AM428] LRG-202: Prevent Duplicate & Available Holds (LRG-F-021)",
        "what": "Enforced business validation rules: reject hold attempts if book is currently Available, or if student already has an active hold.",
        "ac": "User receives clear explanatory error message; database state remains unchanged.",
        "qa": "Verified in TC-HOLD-02, TC-HOLD-03 in test_reservation_manager.py.",
        "points": 3,
        "assign_to_dharshini": True
    },
    "DCLRG-17": {
        "owner": "Divyansh",
        "srn": "PES1UG24AM094",
        "role": "Backend & Catalog Lead",
        "component": "Catalog & Search Engine (Divyansh - PES1UG24AM094)",
        "labels": ["PES1UG24AM094", "Divyansh", "Sprint_2", "UC-04", "Cancellation"],
        "summary": "[Divyansh - PES1UG24AM094] LRG-203: View & Cancel Active Holds (LRG-F-022)",
        "what": "Created student portal view of active holds with instant cancellation capability and ownership authorization check.",
        "ac": "Students can only cancel their own holds; unauthorized cancel attempts return 403 Forbidden.",
        "qa": "Verified in TC-HOLD-04 in test_reservation_manager.py.",
        "points": 3,
        "assign_to_dharshini": False
    },
    "DCLRG-18": {
        "owner": "Dhruv Talavat",
        "srn": "PES1UG24AM087",
        "role": "Database & Security Lead",
        "component": "Database & Security (Dhruv Talavat - PES1UG24AM087)",
        "labels": ["PES1UG24AM087", "Dhruv_Talavat", "Sprint_2", "UC-03", "FIFO_Queue"],
        "summary": "[Dhruv Talavat - PES1UG24AM087] LRG-204: Dynamic FIFO Queue Position Progression (LRG-F-023)",
        "what": "Automated queue re-sequencing upon cancellation or fulfillment so queue positions remain strictly gapless.",
        "ac": "Position 1 promoted to Ready; position 2 shifts to 1, position 3 shifts to 2.",
        "qa": "Verified in TC-HOLD-05 in test_reservation_manager.py.",
        "points": 5,
        "assign_to_dharshini": False
    },
    "DCLRG-19": {
        "owner": "Dhareen G",
        "srn": "PES1UG24AM084",
        "role": "QA Lead & Scrum Master",
        "component": "Authentication & QA (Dhareen G - PES1UG24AM084)",
        "labels": ["PES1UG24AM084", "Dhareen_G", "Sprint_2", "UC-06", "Admin_Return"],
        "summary": "[Dhareen G - PES1UG24AM084] LRG-205: Return Title & Hold Promotion to Ready (LRG-F-040)",
        "what": "Built librarian administration endpoint to mark returned books, check hold queues, and promote position-1 member to Ready with 72h window.",
        "ac": "Book marked Reserved for pickup; pickup window set to 72 hours; audit log records return.",
        "qa": "Verified in TC-ADM-01 in test_admin.py.",
        "points": 5,
        "assign_to_dharshini": False
    },
    "DCLRG-20": {
        "owner": "Divyansh",
        "srn": "PES1UG24AM094",
        "role": "Backend & Catalog Lead",
        "component": "Catalog & Search Engine (Divyansh - PES1UG24AM094)",
        "labels": ["PES1UG24AM094", "Divyansh", "Sprint_2", "UC-09", "Demand_Report"],
        "summary": "[Divyansh - PES1UG24AM094] LRG-206: Hold Demand Report for Librarian (LRG-F-041)",
        "what": "Generated aggregated report of high-demand titles ranked by queue length to inform procurement planning.",
        "ac": "Returns list of titles with >= 1 hold, sorted descending by active hold count.",
        "qa": "Verified in TC-ADM-02 in test_admin.py.",
        "points": 3,
        "assign_to_dharshini": False
    },

    # Sprint 3
    "DCLRG-8": {
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": "Fines & Payments (Dharshini V - PES1UG24AM428)",
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_3", "UC-04b", "Fine_Engine"],
        "summary": "[Dharshini V - PES1UG24AM428] LRG-301: UC-04 Overdue Fine Assessment & Balance Engine",
        "what": "Built late fee computation engine assessing daily overdue fees at $1/day from due date and managing itemized fine records per student in relational database.",
        "ac": "Calendar-day overdue fine computation; itemized fines per book; balance reflected immediately on portal.",
        "qa": "Verified in TC-FINE-01 in test_fine_manager.py.",
        "points": 5,
        "assign_to_dharshini": True
    },
    "DCLRG-21": {
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": "Fines & Payments (Dharshini V - PES1UG24AM428)",
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_3", "UC-04b", "Payment_Wallet"],
        "summary": "[Dharshini V - PES1UG24AM428] LRG-302: UC-04 Campus Wallet / UPI Settlement & Digital Receipt",
        "what": "Implemented payment settlement processing via simulated Campus Wallet and UPI gateway; issues cryptographically verifiable digital receipts with SHA-256 signatures.",
        "ac": "Fine marked PAID with transaction timestamp; balance resets to $0.00; receipt logged in audit table.",
        "qa": "Verified in TC-FINE-02 in test_fine_manager.py.",
        "points": 5,
        "assign_to_dharshini": True
    },
    "DCLRG-22": {
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": "Fines & Payments (Dharshini V - PES1UG24AM428)",
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_3", "UC-04b", "Hold_Restriction"],
        "summary": "[Dharshini V - PES1UG24AM428] LRG-303: UC-04 Hold Restriction when Unpaid Fines >= $20",
        "what": "Automated business rule blocking student members with unpaid fines >= $20 from placing new reservation holds until balance is cleared.",
        "ac": "Hold placement returns 403 Forbidden with prompt to clear dues; holds permitted immediately after payment.",
        "qa": "Verified in TC-FINE-03 in test_fine_manager.py.",
        "points": 3,
        "assign_to_dharshini": True
    },
    "DCLRG-23": {
        "owner": "Dhruv Talavat",
        "srn": "PES1UG24AM087",
        "role": "Database & Security Lead",
        "component": "Database & Security (Dhruv Talavat - PES1UG24AM087)",
        "labels": ["PES1UG24AM087", "Dhruv_Talavat", "Sprint_3", "UC-03", "72h_Auto_Expire"],
        "summary": "[Dhruv Talavat - PES1UG24AM087] LRG-304: 72-Hour Ready Hold Auto-Expiration & Cascade Promotion",
        "what": "Spill-Over 1: Built background worker that expires unclaimed Ready holds after 72 hours and cascades hold-ready status to the next member in queue.",
        "ac": "Expired hold marked Cancelled; position-2 member promoted to Ready; pickup window reset to 72 hours.",
        "qa": "Verified in TC-HOLD-06 in test_reservation_manager.py.",
        "points": 5,
        "assign_to_dharshini": False
    },
    "DCLRG-24": {
        "owner": "Divyansh",
        "srn": "PES1UG24AM094",
        "role": "Backend & Catalog Lead",
        "component": "Catalog & Search Engine (Divyansh - PES1UG24AM094)",
        "labels": ["PES1UG24AM094", "Divyansh", "Sprint_3", "UC-07", "Notification_Retry"],
        "summary": "[Divyansh - PES1UG24AM094] LRG-305: Notification Retry Engine & Failure Audit Logging",
        "what": "Spill-Over 2: Implemented exponential backoff retry queue (3 attempts) on SMTP dispatch failure with dead-letter logging.",
        "ac": "Transient failures retried automatically; permanent failures written to audit log with error details.",
        "qa": "Verified in TC-NOTF-03 in test_notification.py.",
        "points": 3,
        "assign_to_dharshini": False
    },
    "DCLRG-25": {
        "owner": "Dhruv Talavat",
        "srn": "PES1UG24AM087",
        "role": "Database & Security Lead",
        "component": "Database & Security (Dhruv Talavat - PES1UG24AM087)",
        "labels": ["PES1UG24AM087", "Dhruv_Talavat", "Sprint_3", "Security", "Rate_Limiting"],
        "summary": "[Dhruv Talavat - PES1UG24AM087] LRG-306: Sliding-Window Rate Limiter & Cookie Security (LRG-SR-007)",
        "what": "Spill-Over 3: In-memory sliding-window rate limiter (60 req/min/IP) and security cookie attributes (HttpOnly, SameSite=Strict).",
        "ac": "Exceeding 60 req/min returns HTTP 429 Too Many Requests with Retry-After header.",
        "qa": "Verified in TC-SEC-03, TC-SEC-07 in test_security_audit.py.",
        "points": 3,
        "assign_to_dharshini": False
    },
    "DCLRG-26": {
        "owner": "Dhareen G",
        "srn": "PES1UG24AM084",
        "role": "QA Lead & Scrum Master",
        "component": "Authentication & QA (Dhareen G - PES1UG24AM084)",
        "labels": ["PES1UG24AM084", "Dhareen_G", "Sprint_3", "CI_CD", "GitHub_Actions"],
        "summary": "[Dhareen G - PES1UG24AM084] LRG-307: Automated GitHub Actions CI/CD Pipeline (ci.yml)",
        "what": "Configured multi-stage GitHub Actions CI/CD workflow executing flake8 linting, hermetic pytest runs, and 70% coverage threshold gating.",
        "ac": "Workflow triggers on push and PR; fails build if coverage < 70% or any test fails.",
        "qa": "Verified via GitHub Actions workflow run logs.",
        "points": 3,
        "assign_to_dharshini": False
    },
    "DCLRG-27": {
        "owner": "Dhareen G & Dharshini V",
        "srn": "PES1UG24AM084 / PES1UG24AM428",
        "role": "QA Lead & Dev Lead",
        "component": "Fines & Payments (Dharshini V - PES1UG24AM428)",
        "labels": ["PES1UG24AM428", "PES1UG24AM084", "Sprint_3", "QA_Reports", "Coverage"],
        "summary": "[Dhareen G & Dharshini V] LRG-308: Execute Full Test Plan & Generate 4 Mandatory Test Reports",
        "what": "Executed full test plan across 117 automated tests and compiled all 4 formal reports: Unit Test, System Validation, Code Coverage (89%), and Branch Coverage (82.6%).",
        "ac": "Four comprehensive markdown reports authored, signed off, and uploaded to docs/ in project repository.",
        "qa": "Verified via docs/ reports and pytest-cov outputs.",
        "points": 5,
        "assign_to_dharshini": True
    }
}


def jira_req(path, data=None, method="GET"):
    url = f"{BASE_URL}{path}"
    headers = {
        "Authorization": AUTH,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Antigravity-Jira-Live/2.0"
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            c = r.read().decode("utf-8")
            return r.status, json.loads(c) if c else {}
    except urllib.error.HTTPError as e:
        c = e.read().decode("utf-8")
        try:
            return e.code, json.loads(c)
        except Exception:
            return e.code, {"error": c}


def main():
    print("=" * 70)
    print("UPDATING ABBEY'S LIVE ATLASSIAN JIRA WORKSPACE")
    print(f"Site: {BASE_URL} | Project: DCLRG")
    print("=" * 70)

    # 1. Create remaining components
    print("\n[1/3] Ensuring Components exist...")
    for comp in COMPONENTS:
        st, res = jira_req("/rest/api/3/component", data=comp, method="POST")
        if st in (200, 201):
            print(f"  + Created Component: {comp['name']}")
        else:
            print(f"  Component exists/skipped: {comp['name']}")

    # 2. Update Sprints metadata
    print("\n[2/3] Updating Sprint names, dates, and goals...")
    for sc in SPRINT_CONFIGS:
        sid = sc["id"]
        st, res = jira_req(f"/rest/agile/1.0/sprint/{sid}", data=sc, method="PUT")
        if st in (200, 201):
            print(f"  + Updated Sprint {sid}: {sc['name']} ({sc['startDate'][:10]} to {sc['endDate'][:10]})")
        else:
            print(f"  Sprint {sid} update response ({st}): {res}")

    # 3. Update each ticket
    print("\n[3/3] Updating Ticket Summaries, Owners, Components, Labels, and DoD...")
    updated_count = 0

    for key, meta in TICKETS_METADATA.items():
        doc_desc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "Assigned Team Member: ", "marks": [{"type": "strong"}]},
                        {"type": "text", "text": f"{meta['owner']} ("},
                        {"type": "text", "text": meta['srn'], "marks": [{"type": "code"}]},
                        {"type": "text", "text": f") - {meta['role']}"}
                    ]
                },
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "Story Points: ", "marks": [{"type": "strong"}]},
                        {"type": "text", "text": f"{meta['points']} (Fibonacci scale)"}
                    ]
                },
                {
                    "type": "heading",
                    "attrs": {"level": 3},
                    "content": [{"type": "text", "text": "What Was Done (Implementation Details)"}]
                },
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": meta['what']}]
                },
                {
                    "type": "heading",
                    "attrs": {"level": 3},
                    "content": [{"type": "text", "text": "Acceptance Criteria"}]
                },
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": meta['ac']}]
                },
                {
                    "type": "heading",
                    "attrs": {"level": 3},
                    "content": [{"type": "text", "text": "Quality Assurance & Verification"}]
                },
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": meta['qa']}]
                }
            ]
        }

        fields_update = {
            "summary": meta["summary"],
            "description": doc_desc,
            "labels": meta["labels"],
            "components": [{"name": meta["component"]}],
            "customfield_10016": meta["points"]
        }

        if meta["assign_to_dharshini"]:
            fields_update["assignee"] = {"accountId": DHARSHINI_ACCOUNT_ID}

        st, res = jira_req(f"/rest/api/3/issue/{key}", data={"fields": fields_update}, method="PUT")
        if st in (200, 204):
            updated_count += 1
            print(f"  + [{key}] Updated: {meta['summary'][:60]}")
        else:
            print(f"  - [{key}] Update failed (HTTP {st}): {res}")
        time.sleep(0.2)

    print("\n" + "=" * 70)
    print(f"SUCCESS: Updated {updated_count} issues with full team details & components!")
    print(f"Open your live Scrum Board: {BASE_URL}/jira/software/projects/DCLRG/boards/2")
    print(f"Open your live Backlog:     {BASE_URL}/jira/software/projects/DCLRG/boards/2/backlog")
    print("=" * 70)


if __name__ == "__main__":
    main()
