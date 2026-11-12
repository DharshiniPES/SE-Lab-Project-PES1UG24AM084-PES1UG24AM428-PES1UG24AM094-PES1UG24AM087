"""
format_all_jira_stories.py
Formats all 26 Agile User Stories and 5 Epics in live Atlassian Jira (https://abbey6128.atlassian.net)
Project: DCLRG (Digital Campus Library Reservation Gateway)

Ensures every Story displays:
1. Standard User Story Narrative (As a... I want to... So that...) in a highlighted blue Info Panel.
2. Given / When / Then Acceptance Criteria in formatted bullet lists.
3. Definition of Done (DoD) & Automated Test Case ID verification in a green Success Panel.
4. Team Member Attribution (Name, SRN, Subsystem Component, Role) in a purple Note Panel.
5. Fibonacci Story Points (in both customfield_10037 and customfield_10016).
6. Official Parent Epic linkage (DCLRG-1, DCLRG-28, DCLRG-29, DCLRG-30, DCLRG-31).
7. Correct Sprint placement across Sprint 1 (id 3), Sprint 2 (id 4), and Sprint 3 (id 37).
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

EPIC_FINE = "DCLRG-1"      # Overdue Fine Payment & Settlement
EPIC_CATALOG = "DCLRG-28"  # Core Catalog Search & Discovery Engine
EPIC_AUTH = "DCLRG-29"     # Campus SSO Authentication & Security Shield
EPIC_HOLD = "DCLRG-30"     # Hold Reservation & Queue Progression Engine
EPIC_QA = "DCLRG-31"       # Automated Testing, CI/CD & Quality Assurance

COMP_FINE = "Fines & Payments (Dharshini V - PES1UG24AM428)"
COMP_CATALOG = "Catalog & Search Engine (Divyansh - PES1UG24AM094)"
COMP_AUTH = "Authentication & QA (Dhareen G - PES1UG24AM084)"
COMP_DB = "Database & Security (Dhruv Talavat - PES1UG24AM087)"

STORIES = {
    # -------------------------------------------------------------------------
    # SPRINT 1 (ID: 3) STORIES
    # -------------------------------------------------------------------------
    "DCLRG-9": {
        "sprint_id": 3,
        "sprint_name": "Sprint 1",
        "epic": EPIC_QA,
        "points": 5,
        "summary": "[Dhruv Talavat - PES1UG24AM087] LRG-101: Relational SQLite Schema & Initial Seed Data",
        "owner": "Dhruv Talavat",
        "srn": "PES1UG24AM087",
        "role": "Database & Security Lead",
        "component": COMP_DB,
        "labels": ["PES1UG24AM087", "Dhruv_Talavat", "Sprint_1", "Database", "SQLite", "Schema"],
        "assign_to_dharshini": False,
        "as_a": "Database Administrator and Backend Developer",
        "i_want": "a normalized SQLite relational database schema with strict foreign key constraints (PRAGMA foreign_keys = ON), unique indexing, and automated catalog seed fixtures",
        "so_that": "all library transaction data remains ACID-compliant, referentially intact, and reproducible across hermetic testing environments.",
        "scenarios": [
            ("Schema Provisioning", "Given the database initialization script runs on an empty database, When table DDL is executed, Then members, titles, holds, fines, and audit_log tables are created with appropriate indexes and primary keys."),
            ("Foreign Key Enforcement", "Given PRAGMA foreign_keys is enabled, When a hold or fine is inserted referencing a non-existent member_id or title_id, Then SQLite raises a foreign key integrity violation and aborts the insert."),
            ("Reproducible Catalog Seeding", "Given conftest fixtures execute, When sample academic titles are populated, Then ISBNs, authors, and initial shelf copy quantities match the standardized test catalog.")
        ],
        "qa_test": "TC-DB-01 to TC-DB-05 in tests/test_database.py",
        "coverage": "100% schema integrity and fixture isolation",
        "quality_gate": "Zero SQLite lock contention, sub-millisecond in-memory setup."
    },

    "DCLRG-10": {
        "sprint_id": 3,
        "sprint_name": "Sprint 1",
        "epic": EPIC_CATALOG,
        "points": 5,
        "summary": "[Divyansh - PES1UG24AM094] LRG-102: Catalog Search by Title, Author, ISBN (LRG-F-001)",
        "owner": "Divyansh",
        "srn": "PES1UG24AM094",
        "role": "Backend & Catalog Lead",
        "component": COMP_CATALOG,
        "labels": ["PES1UG24AM094", "Divyansh", "Sprint_1", "UC-01", "Search", "Catalog"],
        "assign_to_dharshini": False,
        "as_a": "Student Member or Faculty Researcher",
        "i_want": "to search the library catalog by Title, Author, or ISBN-10/ISBN-13 with sub-second response times",
        "so_that": "I can instantly discover whether required reference books are in the collection and inspect their live borrowing availability.",
        "scenarios": [
            ("Multi-field Partial Match", "Given a search query with partial text 'Software Engineering', When executed, Then all catalog titles containing that substring in title or author are returned sorted by relevance."),
            ("ISBN Normalization", "Given an ISBN query entered with hyphens (e.g., '978-0134685991') or bare digits ('9780134685991'), When searched, Then the system normalizes the string and returns the exact matching book record."),
            ("Zero Results Handling", "Given a search query matching no items in the database, When submitted, Then the API returns an empty list with HTTP 200 and a helpful message rather than an error.")
        ],
        "qa_test": "TC-SRCH-01, TC-SRCH-02, TC-SRCH-07 in tests/test_catalog_search.py",
        "coverage": "96% statement coverage in search_service.py",
        "quality_gate": "Indexed query execution under 250ms for 10,000 catalog entries."
    },

    "DCLRG-11": {
        "sprint_id": 3,
        "sprint_name": "Sprint 1",
        "epic": EPIC_CATALOG,
        "points": 3,
        "summary": "[Divyansh - PES1UG24AM094] LRG-103: Search Input Validation & Sanitization (LRG-F-002)",
        "owner": "Divyansh",
        "srn": "PES1UG24AM094",
        "role": "Backend & Catalog Lead",
        "component": COMP_CATALOG,
        "labels": ["PES1UG24AM094", "Divyansh", "Sprint_1", "UC-01", "Security", "Sanitization"],
        "assign_to_dharshini": False,
        "as_a": "System Security Officer",
        "i_want": "all catalog search input parameters to be strictly sanitized, stripped of control characters, and bound via parameterized SQL queries",
        "so_that": "SQL injection attacks, Cross-Site Scripting (XSS), and database enumeration exploits are rendered completely harmless.",
        "scenarios": [
            ("SQL Injection Neutralization", "Given a search query containing SQL injection payloads such as '' OR '1'='1' --', When submitted, Then parameterized binding treats the input as a literal string without executing SQL commands."),
            ("XSS HTML Escaping", "Given an input containing script tags '<script>alert(1)</script>', When reflected back in search responses, Then characters are escaped to prevent browser script execution."),
            ("Whitespace & Length Truncation", "Given an oversized search string exceeding 128 characters or containing trailing whitespace, When validated, Then the input is trimmed and bounded to valid lengths.")
        ],
        "qa_test": "TC-SRCH-04, TC-SEC-02 in tests/test_security_audit.py",
        "coverage": "100% parameter validation coverage",
        "quality_gate": "Zero injection vulnerabilities on OWASP Top 10 A03 audit."
    },

    "DCLRG-12": {
        "sprint_id": 3,
        "sprint_name": "Sprint 1",
        "epic": EPIC_AUTH,
        "points": 5,
        "summary": "[Dhareen G - PES1UG24AM084] LRG-104: Campus SSO Authentication & Session Engine (LRG-F-010)",
        "owner": "Dhareen G",
        "srn": "PES1UG24AM084",
        "role": "QA Lead & Scrum Master",
        "component": COMP_AUTH,
        "labels": ["PES1UG24AM084", "Dhareen_G", "Sprint_1", "UC-05", "SSO", "Auth", "RBAC"],
        "assign_to_dharshini": False,
        "as_a": "Campus User (Student or Librarian)",
        "i_want": "to authenticate securely using Campus OpenID Connect SSO with role-based session tokens and automated brute-force account lockout",
        "so_that": "my student profile is verified safely and privileged library administration endpoints are strictly protected from unauthorized access.",
        "scenarios": [
            ("Valid SSO Authentication", "Given valid campus SSO credentials, When submitted to /api/auth/login, Then the server issues a cryptographically signed session token with assigned RBAC roles (Student / Librarian)."),
            ("Brute-force Account Lockout", "Given 5 consecutive failed login attempts within a 10-minute window, When the 5th attempt fails, Then the account is locked for 15 minutes and security alerts are emitted."),
            ("Session Expiration & Logout", "Given an authenticated session idle for 30 minutes, When a subsequent request is received, Then the session is invalidated requiring re-authentication.")
        ],
        "qa_test": "TC-AUTH-01, TC-AUTH-02, TC-AUTH-03 in tests/test_auth.py",
        "coverage": "94% statement coverage in auth_service.py",
        "quality_gate": "Argon2/PBKDF2 password hashing with secure cookie flags."
    },

    "DCLRG-13": {
        "sprint_id": 3,
        "sprint_name": "Sprint 1",
        "epic": EPIC_CATALOG,
        "points": 3,
        "summary": "[Dharshini V - PES1UG24AM428] LRG-105: Responsive Catalog Search Web UI",
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": COMP_FINE,
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_1", "UI_UX", "Responsive", "WCAG"],
        "assign_to_dharshini": True,
        "as_a": "Student Member using mobile smartphones, tablets, or desktop laptops",
        "i_want": "a clean, mobile-responsive web user interface meeting WCAG 2.1 AA accessibility guidelines for searching titles and viewing availability",
        "so_that": "I can effortlessly look up and place holds on library books from any device or screen size without usability hurdles.",
        "scenarios": [
            ("Mobile Viewport Adaptation", "Given viewport widths ranging from 360px up to 1920px, When the catalog page renders, Then cards, search bars, and filter toggles adapt fluidly without horizontal scrollbars."),
            ("WCAG 2.1 AA Contrast & Focus", "Given accessibility inspection, When color contrast and keyboard focus indicators are checked, Then text-to-background contrast exceeds 4.5:1 and all controls are tabbable."),
            ("Live Search Feedback", "Given user typing in the search bar, When queries are submitted, Then loading skeletons and clear availability badges (Available / Checked Out) are rendered.")
        ],
        "qa_test": "TC-UX-01 in tests/test_system_e2e.py",
        "coverage": "UI templates and responsive styling validation",
        "quality_gate": "100% keyboard accessibility and Lighthouse accessibility score >= 95."
    },

    "DCLRG-14": {
        "sprint_id": 3,
        "sprint_name": "Sprint 1",
        "epic": EPIC_QA,
        "points": 3,
        "summary": "[Dhareen G - PES1UG24AM084] LRG-106: Baseline Unit Tests for Search & Authentication",
        "owner": "Dhareen G",
        "srn": "PES1UG24AM084",
        "role": "QA Lead & Scrum Master",
        "component": COMP_AUTH,
        "labels": ["PES1UG24AM084", "Dhareen_G", "Sprint_1", "QA", "Pytest", "UnitTests"],
        "assign_to_dharshini": False,
        "as_a": "QA Engineer and Agile Scrum Master",
        "i_want": "an automated, hermetic pytest test suite for all Sprint 1 catalog search and authentication logic",
        "so_that": "code regressions are trapped immediately and the development team maintains a zero-broken-window policy from Day 1.",
        "scenarios": [
            ("Automated Test Discovery", "Given pytest is invoked from the project root, When discovery executes, Then all Sprint 1 test modules are identified and executed without manual configuration."),
            ("Network Isolation Verification", "Given network connectivity is disabled, When tests execute against temporary in-memory database fixtures, Then all tests execute and pass in under 2.0 seconds."),
            ("Coverage Assertion Baseline", "Given pytest-cov execution, When baseline metrics are computed, Then test coverage exceeds 85% with zero unhandled exceptions.")
        ],
        "qa_test": "Baseline pytest test runner across tests/test_catalog_search.py and tests/test_auth.py",
        "coverage": "100% pass rate across baseline test suite",
        "quality_gate": "Zero test failures, isolated tempfile/in-memory SQLite fixtures."
    },

    # -------------------------------------------------------------------------
    # SPRINT 2 (ID: 4) STORIES
    # -------------------------------------------------------------------------
    "DCLRG-15": {
        "sprint_id": 4,
        "sprint_name": "Sprint 2",
        "epic": EPIC_HOLD,
        "points": 5,
        "summary": "[Dharshini V - PES1UG24AM428] LRG-201: Place Hold on Checked-Out Book (LRG-F-020)",
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": COMP_FINE,
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_2", "UC-03", "Holds", "Reservation"],
        "assign_to_dharshini": True,
        "as_a": "Authenticated Student Member",
        "i_want": "to place a reservation hold on a book whose shelf copies are currently all checked out",
        "so_that": "I am placed into the FIFO reservation queue and reserved the next returned copy in sequential order.",
        "scenarios": [
            ("Successful Queue Allocation", "Given a book with 0 available shelf copies and 2 active holds, When an authenticated student places a hold, Then the hold record is created with status 'WAITING' and queue_position = 3."),
            ("Concurrency Protection", "Given two students placing a hold on the same title simultaneously, When database commits occur, Then atomic transactions guarantee gapless, distinct sequential positions."),
            ("Confirmation Receipt", "Given a successful hold placement, When the response returns, Then the student receives estimated wait position and hold reference ID.")
        ],
        "qa_test": "TC-HOLD-01 in tests/test_reservation_manager.py",
        "coverage": "95% statement coverage in reservation_manager.py",
        "quality_gate": "ACID transactional consistency with immediate audit logging."
    },

    "DCLRG-16": {
        "sprint_id": 4,
        "sprint_name": "Sprint 2",
        "epic": EPIC_HOLD,
        "points": 3,
        "summary": "[Dharshini V - PES1UG24AM428] LRG-202: Prevent Duplicate & Available Holds (LRG-F-021)",
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": COMP_FINE,
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_2", "UC-03", "Validation", "BusinessRules"],
        "assign_to_dharshini": True,
        "as_a": "Library System Business Logic Engine",
        "i_want": "to validate hold requests and reject submissions if copies are currently available on shelves or if the student already holds an active reservation on that title",
        "so_that": "queue hoarding is strictly prevented and students are directed to borrow physical copies immediately when available.",
        "scenarios": [
            ("Rejection on Shelf Available", "Given a title with available_copies > 0 on shelves, When a student attempts to place a hold, Then the request is rejected with HTTP 400 and message 'Copies are available on shelf for immediate checkout.'"),
            ("Duplicate Hold Prevention", "Given a student with an active WAITING hold on ISBN '978-0132350884', When they attempt to place another hold on the same ISBN, Then the system returns HTTP 400 'Duplicate hold already active.'"),
            ("Database Integrity Invariant", "Given rejected hold requests, When checked against the holds table, Then no new rows or position changes are committed.")
        ],
        "qa_test": "TC-HOLD-02, TC-HOLD-03 in tests/test_reservation_manager.py",
        "coverage": "100% validation path coverage",
        "quality_gate": "Strict adherence to Library Business Rule BR-HOLD-02."
    },

    "DCLRG-17": {
        "sprint_id": 4,
        "sprint_name": "Sprint 2",
        "epic": EPIC_HOLD,
        "points": 3,
        "summary": "[Divyansh - PES1UG24AM094] LRG-203: View & Cancel Active Holds (LRG-F-022)",
        "owner": "Divyansh",
        "srn": "PES1UG24AM094",
        "role": "Backend & Catalog Lead",
        "component": COMP_CATALOG,
        "labels": ["PES1UG24AM094", "Divyansh", "Sprint_2", "UC-04", "Cancellation", "MemberPortal"],
        "assign_to_dharshini": False,
        "as_a": "Student Member with active reservation holds",
        "i_want": "to view all my active holds with current queue positions and cancel any hold that I no longer require",
        "so_that": "I can release the reserved book for subsequent students in the waiting queue without unnecessary delay.",
        "scenarios": [
            ("Hold Dashboard Listing", "Given a student logged into the portal with 2 active holds, When they view the holds tab, Then each hold is rendered with title, author, queue position, and date requested."),
            ("Authorized Self-Cancellation", "Given an active hold owned by student 'PES1UG24AM428', When the student submits cancellation, Then hold status is updated to 'CANCELLED' and queue progression is triggered."),
            ("Unauthorized Cancellation Prevention", "Given student A attempting to cancel a hold belonging to student B, When the request is processed, Then authorization fails with HTTP 403 Forbidden.")
        ],
        "qa_test": "TC-HOLD-04 in tests/test_reservation_manager.py",
        "coverage": "92% statement coverage on cancellation logic",
        "quality_gate": "Zero cross-student data access; strict RBAC ownership."
    },

    "DCLRG-18": {
        "sprint_id": 4,
        "sprint_name": "Sprint 2",
        "epic": EPIC_HOLD,
        "points": 5,
        "summary": "[Dhruv Talavat - PES1UG24AM087] LRG-204: Dynamic FIFO Queue Position Progression (LRG-F-023)",
        "owner": "Dhruv Talavat",
        "srn": "PES1UG24AM087",
        "role": "Database & Security Lead",
        "component": COMP_DB,
        "labels": ["PES1UG24AM087", "Dhruv_Talavat", "Sprint_2", "UC-03", "FIFO", "Queue", "Cascade"],
        "assign_to_dharshini": False,
        "as_a": "Hold Queue Management Subsystem",
        "i_want": "to automatically recalculate and advance subsequent hold queue positions in gapless sequential order whenever an active hold is cancelled or fulfilled",
        "so_that": "every waiting student moves up accurately in line (e.g. position 3 becomes 2, position 2 becomes 1) without orphan gaps.",
        "scenarios": [
            ("Middle-of-Queue Cancellation", "Given holds at positions 1, 2, 3, and 4, When position 2 cancels their hold, Then positions 3 and 4 decrement atomically to positions 2 and 3."),
            ("Head-of-Queue Cancellation", "Given holds at positions 1 and 2, When position 1 cancels, Then position 2 advances to position 1 and becomes eligible for the next returned copy."),
            ("Atomic Shift Transaction", "Given concurrent queue adjustments, When the update query executes, Then the entire queue re-sequencing commits in a single ACID transaction block.")
        ],
        "qa_test": "TC-HOLD-05 in tests/test_reservation_manager.py",
        "coverage": "98% statement coverage on queue re-indexing",
        "quality_gate": "Zero deadlocks under simulated concurrent cancellations."
    },

    "DCLRG-19": {
        "sprint_id": 4,
        "sprint_name": "Sprint 2",
        "epic": EPIC_HOLD,
        "points": 5,
        "summary": "[Dhareen G - PES1UG24AM084] LRG-205: Return Title & Hold Promotion to Ready (LRG-F-040)",
        "owner": "Dhareen G",
        "srn": "PES1UG24AM084",
        "role": "QA Lead & Scrum Master",
        "component": COMP_AUTH,
        "labels": ["PES1UG24AM084", "Dhareen_G", "Sprint_2", "UC-06", "Circulation", "Librarian"],
        "assign_to_dharshini": False,
        "as_a": "Librarian processing physical book returns at the circulation desk",
        "i_want": "to record book returns and have the system automatically promote the position-1 waiting hold to 'READY' with a 72-hour pickup reservation window",
        "so_that": "the returned copy is immediately staged for pickup and the waiting student is formally notified.",
        "scenarios": [
            ("Return with Active Waiting Holds", "Given a checked-out book returned with waiting holds in queue, When librarian clicks Return, Then book status becomes RESERVED, hold position 1 transitions to READY, and pickup_expires_at is set to current_time + 72 hours."),
            ("Return with Zero Waiting Holds", "Given a returned book with 0 waiting holds, When recorded, Then copy status transitions directly to AVAILABLE on shelf."),
            ("Audit Trail Generation", "Given any processed return, When completed, Then an immutable return record is inserted into audit_log with librarian ID and timestamp.")
        ],
        "qa_test": "TC-ADM-01 in tests/test_admin.py",
        "coverage": "96% statement coverage in circulation_service.py",
        "quality_gate": "Timestamp precision to second; automated 72h window calculation."
    },

    "DCLRG-20": {
        "sprint_id": 4,
        "sprint_name": "Sprint 2",
        "epic": EPIC_HOLD,
        "points": 3,
        "summary": "[Divyansh - PES1UG24AM094] LRG-206: Hold Demand Report for Librarian (LRG-F-041)",
        "owner": "Divyansh",
        "srn": "PES1UG24AM094",
        "role": "Backend & Catalog Lead",
        "component": COMP_CATALOG,
        "labels": ["PES1UG24AM094", "Divyansh", "Sprint_2", "UC-09", "Reporting", "Analytics"],
        "assign_to_dharshini": False,
        "as_a": "Chief Librarian and Acquisitions Officer",
        "i_want": "to view an aggregated Hold Demand Report ranking catalog titles by total hold requests and average wait duration",
        "so_that": "our department can make data-driven purchasing decisions to acquire additional copies of high-demand academic textbooks.",
        "scenarios": [
            ("Aggregated Demand Ranking", "Given multiple titles with varying queue lengths, When the librarian loads the demand report, Then titles are listed sorted descending by active hold count alongside total inventory."),
            ("Zero Demand Filtering", "Given titles with 0 holds, When the high-demand threshold is applied, Then only titles with >= 1 pending hold are included in the primary report."),
            ("Librarian-Only Authorization", "Given an unauthorized student user attempting to query /api/admin/reports/demand, When evaluated, Then RBAC middleware rejects with HTTP 403 Forbidden.")
        ],
        "qa_test": "TC-ADM-02 in tests/test_admin.py",
        "coverage": "94% statement coverage in admin_reporting.py",
        "quality_gate": "Sub-50ms query aggregation utilizing SQL GROUP BY and indexes."
    },

    # -------------------------------------------------------------------------
    # SPRINT 3 (ID: 37) STORIES - UC-04 FINES, PAYMENTS & SPILL-OVERS
    # -------------------------------------------------------------------------
    "DCLRG-2": {
        "sprint_id": 37,
        "sprint_name": "Sprint 3",
        "epic": EPIC_FINE,
        "points": 3,
        "summary": "[Dharshini V - PES1UG24AM428] LRG-001: View Outstanding Fine Balance & Itemized Breakdown",
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": COMP_FINE,
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_3", "UC-04b", "Fines", "Portal"],
        "assign_to_dharshini": True,
        "as_a": "Student Member with overdue borrowed titles",
        "i_want": "to view my aggregate outstanding fine balance and an itemized breakdown of fines per overdue book on the student portal",
        "so_that": "I have complete transparency into my financial liabilities before initiating payment.",
        "scenarios": [
            ("Itemized Overdue Balance Display", "Given a student with 2 overdue books incurring $5.00 and $7.00 late fees, When they open their portal dashboard, Then the total balance displays $12.00 with itemized title, due date, and days overdue."),
            ("Good Standing Zero Balance", "Given a student with 0 overdue books and zero fines, When they navigate to the fines section, Then the screen displays 'No outstanding fines. Your account is in good standing.'"),
            ("Real-time Fine Refresh", "Given an overdue book incurring another calendar day, When the student refreshes the dashboard, Then the new daily fee is computed and reflected in the live total.")
        ],
        "qa_test": "TC-FINE-01 in tests/test_fine_manager.py",
        "coverage": "100% statement coverage on fine balance calculation",
        "quality_gate": "Currency precision to 2 decimal places ($X.XX)."
    },

    "DCLRG-3": {
        "sprint_id": 37,
        "sprint_name": "Sprint 3",
        "epic": EPIC_FINE,
        "points": 2,
        "summary": "[Dharshini V - PES1UG24AM428] LRG-002: Select Fine Payment Settlement Method",
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": COMP_FINE,
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_3", "UC-04b", "Payments", "Wallet"],
        "assign_to_dharshini": True,
        "as_a": "Student Member initiating a fine settlement",
        "i_want": "to choose between Campus Wallet and UPI gateway payment channels on the checkout screen",
        "so_that": "I can settle my outstanding balance using my preferred payment instrument.",
        "scenarios": [
            ("Campus Wallet Selection", "Given an outstanding fine of $10.00, When the student selects Campus Wallet, Then the interface queries their linked wallet balance and previews the post-deduction balance."),
            ("UPI Gateway Selection", "Given payment via UPI, When selected, Then a Virtual Payment Address (VPA) field is displayed with client-side syntax validation (e.g. username@bank)."),
            ("Pre-payment Validation", "Given an invalid or empty payment method selection, When submission is attempted, Then form validation prompts the user to select an active payment channel.")
        ],
        "qa_test": "TC-FINE-02 in tests/test_fine_manager.py",
        "coverage": "98% statement coverage on payment selector logic",
        "quality_gate": "Secure token generation with CSRF token verification."
    },

    "DCLRG-4": {
        "sprint_id": 37,
        "sprint_name": "Sprint 3",
        "epic": EPIC_FINE,
        "points": 5,
        "summary": "[Dharshini V - PES1UG24AM428] LRG-003: Process Overdue Fine Settlement Transaction",
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": COMP_FINE,
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_3", "UC-04b", "Transactions", "ACID"],
        "assign_to_dharshini": True,
        "as_a": "Student Member executing fine settlement",
        "i_want": "the payment engine to debit my selected payment channel and transition my fine status to 'PAID' atomically",
        "so_that": "my overdue fine liability is cleared immediately in the central library database without discrepancies.",
        "scenarios": [
            ("Successful Transaction Execution", "Given an outstanding fine of $15.00 and sufficient wallet balance, When payment is confirmed, Then $15.00 is debited, fine status transitions to 'PAID', and outstanding balance resets to $0.00."),
            ("Atomic Record Commitment", "Given payment processing, When database updates occur, Then fine record, payment ledger, and audit log commit inside a single atomic ACID transaction."),
            ("Double-Payment Idempotency", "Given rapid duplicate submission of the same payment form, When received by server, Then idempotency keys ensure only one debit is processed.")
        ],
        "qa_test": "TC-FINE-02 in tests/test_fine_manager.py",
        "coverage": "96% statement coverage in fine_manager.py",
        "quality_gate": "ACID transaction isolation level; zero partial debit states."
    },

    "DCLRG-5": {
        "sprint_id": 37,
        "sprint_name": "Sprint 3",
        "epic": EPIC_FINE,
        "points": 3,
        "summary": "[Dharshini V - PES1UG24AM428] LRG-004: Issue Cryptographic Payment Receipt (SHA-256)",
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": COMP_FINE,
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_3", "UC-04b", "Receipts", "SHA256", "Security"],
        "assign_to_dharshini": True,
        "as_a": "Student Member who has just completed a fine payment",
        "i_want": "to receive a cryptographically signed digital payment receipt featuring an immutable SHA-256 transaction signature",
        "so_that": "I have verifiable, tamper-evident proof of payment for semester clearance and financial audits.",
        "scenarios": [
            ("Receipt Generation with SHA-256", "Given a successful fine settlement transaction, When completed, Then a receipt object containing transaction_id, student_id, amount, timestamp, and SHA-256 hash is generated."),
            ("Cryptographic Verification", "Given an issued receipt hash, When validated against the transaction payload parameters, Then SHA-256 digest recalculation matches exactly confirming zero tampering."),
            ("Printable Receipt Presentation", "Given receipt viewing, When rendered in UI, Then itemized transaction metadata and reference ID are presented with a 1-click download/print option.")
        ],
        "qa_test": "TC-FINE-02 in tests/test_fine_manager.py",
        "coverage": "100% cryptographic hashing validation",
        "quality_gate": "Deterministic SHA-256 payload hashing with timestamp."
    },

    "DCLRG-6": {
        "sprint_id": 37,
        "sprint_name": "Sprint 3",
        "epic": EPIC_FINE,
        "points": 3,
        "summary": "[Dharshini V - PES1UG24AM428] LRG-005: Handle Declined & Insufficient Fund Payments",
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": COMP_FINE,
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_3", "UC-04b", "Errors", "ExceptionHandling"],
        "assign_to_dharshini": True,
        "as_a": "Student Member encountering a failed payment attempt",
        "i_want": "the system to return a clear, user-friendly error message indicating the specific cause (e.g. Insufficient Balance, Gateway Timeout)",
        "so_that": "I understand why the transaction did not succeed and can rectify the issue without panicking.",
        "scenarios": [
            ("Insufficient Funds Notification", "Given a wallet balance of $4.00 and an overdue fine of $10.00, When payment is attempted, Then the server returns HTTP 400 with error 'Insufficient wallet balance ($4.00 available). Please top up.'"),
            ("Gateway Timeout Handling", "Given a simulated network timeout during UPI gateway handshake, When timeout threshold (5000ms) elapses, Then server returns HTTP 504 with prompt to retry."),
            ("Zero Balance Discrepancy", "Given a declined transaction, When inspecting member account balances, Then wallet balance and fine balance remain identical to pre-transaction values.")
        ],
        "qa_test": "TC-FINE-04 in tests/test_fine_manager.py",
        "coverage": "100% error path and boundary condition coverage",
        "quality_gate": "Clean exception bubbling without unhandled 500 server crashes."
    },

    "DCLRG-7": {
        "sprint_id": 37,
        "sprint_name": "Sprint 3",
        "epic": EPIC_FINE,
        "points": 3,
        "summary": "[Dharshini V - PES1UG24AM428] LRG-006: Atomic Rollback & Balance Preservation on Failure",
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": COMP_FINE,
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_3", "UC-04b", "Rollback", "ACID", "Audit"],
        "assign_to_dharshini": True,
        "as_a": "Financial Auditor and Database Administrator",
        "i_want": "the payment subsystem to automatically issue a database transaction rollback upon any processing failure",
        "so_that": "fines never enter inconsistent intermediate states and funds are never debited without marking the fine as settled.",
        "scenarios": [
            ("Mid-transaction Failure Rollback", "Given a transaction encountering an unexpected exception after checking balances, When the exception is trapped, Then DB rollback executes restoring the fine status to 'UNPAID'."),
            ("Audit Logging of Failure Events", "Given a transaction rollback event, When the error handler runs, Then a detailed audit row is written to audit_log with failure reason, student ID, and timestamp."),
            ("Zero Financial Loss Guarantee", "Given automated stress tests simulating network breaks during settlement, When database audit runs, Then zero orphaned payments or phantom credits exist.")
        ],
        "qa_test": "TC-FINE-04 in tests/test_fine_manager.py",
        "coverage": "98% exception rollback coverage",
        "quality_gate": "Strict ACID Rollback verification in SQLite."
    },

    "DCLRG-8": {
        "sprint_id": 37,
        "sprint_name": "Sprint 3",
        "epic": EPIC_FINE,
        "points": 5,
        "summary": "[Dharshini V - PES1UG24AM428] LRG-301: UC-04 Overdue Fine Assessment & Balance Engine",
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": COMP_FINE,
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_3", "UC-04b", "FineEngine", "LateFees"],
        "assign_to_dharshini": True,
        "as_a": "Library Circulation Administrator",
        "i_want": "an automated fine assessment engine that evaluates overdue loans daily at $1.00 per calendar day from scheduled due date",
        "so_that": "borrowing durations are strictly enforced and overdue penalties are calculated objectively and automatically.",
        "scenarios": [
            ("Overdue Calendar Calculation", "Given a loaned title with scheduled due date 5 days in the past, When the fine assessment routine evaluates the loan, Then an itemized fine of $5.00 ($1.00 x 5 days) is generated."),
            ("On-time Return Zero Penalty", "Given a book returned on or prior to its scheduled due date, When processed, Then the overdue duration evaluates to 0 days and assessed fine is $0.00."),
            ("Multi-loan Aggregation", "Given a student with 3 books overdue by 2, 4, and 7 days respectively, When aggregated balance is queried, Then total balance evaluates to $13.00 with itemized linkage.")
        ],
        "qa_test": "TC-FINE-01 in tests/test_fine_manager.py",
        "coverage": "98% statement coverage in fine_manager.py",
        "quality_gate": "Calendar-day math timezone-invariant (UTC)."
    },

    "DCLRG-21": {
        "sprint_id": 37,
        "sprint_name": "Sprint 3",
        "epic": EPIC_FINE,
        "points": 5,
        "summary": "[Dharshini V - PES1UG24AM428] LRG-302: UC-04 Campus Wallet / UPI Settlement & Digital Receipt",
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": COMP_FINE,
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_3", "UC-04b", "CampusWallet", "UPI", "DigitalReceipt"],
        "assign_to_dharshini": True,
        "as_a": "Student Member settling an overdue fine online",
        "i_want": "to process instantaneous payment via Campus Wallet or UPI and receive an authenticated cryptographic digital receipt",
        "so_that": "my library hold privileges are restored immediately without visiting circulation desk in person.",
        "scenarios": [
            ("End-to-End Wallet Settlement", "Given an outstanding fine balance of $8.00 and wallet balance of $25.00, When student submits payment, Then wallet is debited $8.00, fine is marked PAID, and digital receipt with SHA-256 signature is returned."),
            ("End-to-End UPI Settlement", "Given payment via UPI with valid gateway transaction reference, When confirmed by callback, Then fine status transitions to PAID and audit event is logged."),
            ("Immediate Privilege Restoration", "Given student previously blocked by fine threshold, When payment brings balance below $20.00, Then reservation hold capabilities are restored instantaneously.")
        ],
        "qa_test": "TC-FINE-02 in tests/test_fine_manager.py",
        "coverage": "96% statement coverage across wallet and UPI settlement pathways",
        "quality_gate": "Sub-500ms settlement turn-around with digital signature."
    },

    "DCLRG-22": {
        "sprint_id": 37,
        "sprint_name": "Sprint 3",
        "epic": EPIC_FINE,
        "points": 3,
        "summary": "[Dharshini V - PES1UG24AM428] LRG-303: UC-04 Hold Restriction when Unpaid Fines >= $20",
        "owner": "Dharshini V",
        "srn": "PES1UG24AM428",
        "role": "Dev Lead & Financial Subsystem Lead",
        "component": COMP_FINE,
        "labels": ["PES1UG24AM428", "Dharshini_V", "Sprint_3", "UC-04b", "BusinessRule", "Restriction"],
        "assign_to_dharshini": True,
        "as_a": "Library Circulation Policy Engine",
        "i_want": "to automatically restrict student members with aggregate unpaid fines >= $20.00 from placing new reservation holds",
        "so_that": "students settle their outstanding debts before incurring additional book holds.",
        "scenarios": [
            ("Restriction Enforced at Threshold", "Given a student member with $22.00 in unpaid fines, When they attempt to place a reservation hold, Then the request is rejected with HTTP 403 Forbidden and message 'Account restricted: Unpaid fines ($22.00) meet or exceed the $20.00 limit.'"),
            ("Hold Permitted Below Threshold", "Given a student member with $18.00 in unpaid fines, When they submit a hold, Then the hold is accepted and queued normally."),
            ("Immediate Unblocking After Settlement", "Given a student with $22.00 fines who settles $10.00 bringing balance to $12.00, When they immediately retry hold placement, Then hold is placed successfully.")
        ],
        "qa_test": "TC-FINE-03 in tests/test_fine_manager.py",
        "coverage": "100% boundary testing around $20.00 threshold ($19.99, $20.00, $20.01)",
        "quality_gate": "Enforcement executed prior to queue locking."
    },

    "DCLRG-23": {
        "sprint_id": 37,
        "sprint_name": "Sprint 3",
        "epic": EPIC_HOLD,
        "points": 5,
        "summary": "[Dhruv Talavat - PES1UG24AM087] LRG-304: 72-Hour Ready Hold Auto-Expiration & Cascade Promotion",
        "owner": "Dhruv Talavat",
        "srn": "PES1UG24AM087",
        "role": "Database & Security Lead",
        "component": COMP_DB,
        "labels": ["PES1UG24AM087", "Dhruv_Talavat", "Sprint_3", "UC-03", "AutoExpire", "Cascade", "SpillOver"],
        "assign_to_dharshini": False,
        "as_a": "Automated Background Daemon Worker",
        "i_want": "to periodically scan the holds table for unclaimed 'READY' holds that have exceeded their 72-hour pickup window, cancel them, and cascade promotion to the next waiting student",
        "so_that": "reserved books do not sit idle on physical pickup shelves when a student fails to collect them.",
        "scenarios": [
            ("Unclaimed Hold Expiration", "Given a hold marked READY whose pickup_expires_at is in the past, When the auto-expiration worker runs, Then the hold status is transitioned to 'CANCELLED_EXPIRED'."),
            ("Sequential Cascade Promotion", "Given an expired hold and a subsequent student waiting at position 2, When cascade runs, Then position 2 advances to position 1, status becomes 'READY', and a fresh 72-hour pickup window is established."),
            ("Reversion to Shelf When Queue Empty", "Given an expired READY hold with 0 subsequent waiting students, When auto-expire executes, Then the book's shelf status reverts to 'AVAILABLE'.")
        ],
        "qa_test": "TC-HOLD-06 in tests/test_reservation_manager.py",
        "coverage": "98% statement coverage on expiration cron routine",
        "quality_gate": "Zero missed expirations; atomic cascade state update."
    },

    "DCLRG-24": {
        "sprint_id": 37,
        "sprint_name": "Sprint 3",
        "epic": EPIC_QA,
        "points": 3,
        "summary": "[Divyansh - PES1UG24AM094] LRG-305: Notification Retry Engine & Failure Audit Logging",
        "owner": "Divyansh",
        "srn": "PES1UG24AM094",
        "role": "Backend & Catalog Lead",
        "component": COMP_CATALOG,
        "labels": ["PES1UG24AM094", "Divyansh", "Sprint_3", "UC-07", "Retry", "Notifications", "SpillOver"],
        "assign_to_dharshini": False,
        "as_a": "Notification Dispatcher Subsystem",
        "i_want": "an exponential-backoff retry engine (3 attempts: 1s, 2s, 4s) for email/SMS dispatch and a dead-letter audit log for permanent delivery failures",
        "so_that": "transient network blips do not prevent students from receiving critical pickup notifications.",
        "scenarios": [
            ("Successful Retry on Network Blip", "Given an SMTP dispatch that fails with a transient network socket timeout on attempt 1, When retry logic executes, Then attempt 2 succeeds and email is marked DELIVERED."),
            ("Dead-Letter Queue Logging on Exhaustion", "Given 3 consecutive SMTP dispatch failures, When retry attempts are exhausted, Then notification status becomes 'FAILED' and recipient/error details are written to audit_log."),
            ("Non-blocking Dispatch", "Given notification dispatch in progress, When user interacts with UI, Then notifications run asynchronously without blocking web responses.")
        ],
        "qa_test": "TC-NOTF-03 in tests/test_notification.py",
        "coverage": "96% statement coverage in notification_service.py",
        "quality_gate": "Exponential backoff adhering to RFC 2616 retry strategy."
    },

    "DCLRG-25": {
        "sprint_id": 37,
        "sprint_name": "Sprint 3",
        "epic": EPIC_AUTH,
        "points": 3,
        "summary": "[Dhruv Talavat - PES1UG24AM087] LRG-306: Sliding-Window Rate Limiter & Cookie Security (LRG-SR-007)",
        "owner": "Dhruv Talavat",
        "srn": "PES1UG24AM087",
        "role": "Database & Security Lead",
        "component": COMP_DB,
        "labels": ["PES1UG24AM087", "Dhruv_Talavat", "Sprint_3", "Security", "RateLimit", "SpillOver"],
        "assign_to_dharshini": False,
        "as_a": "Library Gateway Security Middleware",
        "i_want": "an in-memory sliding-window rate limiter enforcing a 60 requests/minute per IP quota and strict session cookie security attributes (HttpOnly, Secure, SameSite=Strict)",
        "so_that": "the gateway is immune to automated credential stuffing, catalog scraping, and session hijacking.",
        "scenarios": [
            ("Rate Limit Enforced at 60 req/min", "Given an IP client submitting 61 requests within a rolling 60-second window, When request 61 arrives, Then server responds with HTTP 429 Too Many Requests and Retry-After header."),
            ("Quota Recovery After Window Closes", "Given an IP client throttled by HTTP 429, When 60 seconds elapse, Then subsequent requests are processed normally."),
            ("Hardened Cookie Attributes", "Given session authentication cookies issued by server, When inspected, Then cookies feature HttpOnly=True, Secure=True, and SameSite=Strict flags.")
        ],
        "qa_test": "TC-SEC-03, TC-SEC-07 in tests/test_security_audit.py",
        "coverage": "100% rate limiting and cookie inspection coverage",
        "quality_gate": "OWASP Security Verification Standard Level 2 compliance."
    },

    "DCLRG-26": {
        "sprint_id": 37,
        "sprint_name": "Sprint 3",
        "epic": EPIC_QA,
        "points": 3,
        "summary": "[Dhareen G - PES1UG24AM084] LRG-307: Automated GitHub Actions CI/CD Pipeline (ci.yml)",
        "owner": "Dhareen G",
        "srn": "PES1UG24AM084",
        "role": "QA Lead & Scrum Master",
        "component": COMP_AUTH,
        "labels": ["PES1UG24AM084", "Dhareen_G", "Sprint_3", "CI_CD", "GitHubActions", "Automation"],
        "assign_to_dharshini": False,
        "as_a": "Agile Scrum Master and DevOps Engineer",
        "i_want": "a robust multi-stage GitHub Actions CI/CD pipeline (.github/workflows/ci.yml) that executes flake8 linting, hermetic pytest execution, and automated 70% coverage gating on every push and PR",
        "so_that": "broken code, lint violations, or coverage regressions are trapped and prevented from entering the main codebase.",
        "scenarios": [
            ("Successful Pipeline Run", "Given code pushed to main or pull request with all tests passing and coverage >= 70%, When GitHub Actions workflow triggers, Then linting, testing, and coverage stages pass with a green build badge."),
            ("Failing Build on Test Failure", "Given a commit with a broken unit test, When CI executes, Then the test step exits non-zero, build status becomes red, and PR merge is blocked."),
            ("Coverage Threshold Enforcement", "Given code pushed with test coverage dropping below 70%, When pytest-cov evaluates, Then the workflow fails the build with threshold error.")
        ],
        "qa_test": "GitHub Actions workflow run logs (.github/workflows/ci.yml)",
        "coverage": "End-to-end automation of all 117 tests in pipeline",
        "quality_gate": "Clean flake8 run with zero lint warnings; > 70% coverage threshold."
    },

    "DCLRG-27": {
        "sprint_id": 37,
        "sprint_name": "Sprint 3",
        "epic": EPIC_QA,
        "points": 5,
        "summary": "[Dhareen G & Dharshini V] LRG-308: Execute Full Test Plan & Generate 4 Mandatory Test Reports",
        "owner": "Dhareen G & Dharshini V",
        "srn": "PES1UG24AM084 / PES1UG24AM428",
        "role": "QA Lead & Dev Lead",
        "component": COMP_FINE,
        "labels": ["PES1UG24AM428", "PES1UG24AM084", "Sprint_3", "Deliverable_3", "QAReports", "Coverage"],
        "assign_to_dharshini": True,
        "as_a": "Lead Development & QA Team",
        "i_want": "to execute the comprehensive test plan across all 117 automated test cases and compile all 4 formal reports (Unit Test, System Validation, Statement Coverage 94%, Branch Coverage 82.6%)",
        "so_that": "Deliverable 3 academic and industry quality certification is fully achieved, documented, and signed off in the repository.",
        "scenarios": [
            ("100% Automated Test Pass Execution", "Given the complete test suite of 117 automated tests, When executed via run_all_tests.py, Then 117/117 tests pass (100% pass rate) in under 2.0 seconds with zero flakiness."),
            ("Statement Coverage > 85% & Branch > 80%", "Given pytest-cov execution, When coverage is measured, Then statement coverage achieves 94% (exceeding 85% requirement) and branch coverage achieves 82.6% (exceeding 80% requirement)."),
            ("Formal Signed Deliverable 3 Documentation", "Given the test run outputs, When reports are compiled, Then 4 formal markdown reports (Unit Test, System Test, Statement Coverage, Branch Coverage) are authored and uploaded to docs/.")
        ],
        "qa_test": "docs/01_UNIT_TEST_REPORT.md, docs/02_SYSTEM_VALIDATION_REPORT.md, docs/03_CODE_COVERAGE_REPORT.md, docs/04_BRANCH_COVERAGE_REPORT.md",
        "coverage": "94.0% statement coverage (855/910 lines), 82.6% branch coverage (176/213 branches)",
        "quality_gate": "Zero open P1/P2 defects; all 4 mandatory reports committed."
    }
}


def make_adf_description(meta):
    """Builds a rich Atlassian Document Format (ADF) document for a User Story."""
    scenario_items = []
    for title, text in meta["scenarios"]:
        scenario_items.append({
            "type": "listItem",
            "content": [{
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": f"{title}: ", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": text}
                ]
            }]
        })

    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            # 1. Info Panel: Standard User Story Narrative
            {
                "type": "panel",
                "attrs": {"panelType": "info"},
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "USER STORY STATEMENT\n", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": "As a ", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": f"{meta['as_a']},\n"},
                            {"type": "text", "text": "I want to ", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": f"{meta['i_want']},\n"},
                            {"type": "text", "text": "So that ", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": f"{meta['so_that']}"}
                        ]
                    }
                ]
            },

            # 2. Acceptance Criteria Heading & Bullet List
            {
                "type": "heading",
                "attrs": {"level": 3},
                "content": [{"type": "text", "text": "Acceptance Criteria (Given / When / Then)"}]
            },
            {
                "type": "bulletList",
                "content": scenario_items
            },

            # 3. Success Panel: Definition of Done & Verification
            {
                "type": "panel",
                "attrs": {"panelType": "success"},
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "DEFINITION OF DONE (DoD) & AUTOMATED VERIFICATION\n", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": "Automated Test Case: ", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": f"{meta['qa_test']}\n"},
                            {"type": "text", "text": "Coverage Metric: ", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": f"{meta['coverage']}\n"},
                            {"type": "text", "text": "Quality Gate: ", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": f"{meta['quality_gate']}"}
                        ]
                    }
                ]
            },

            # 4. Note Panel: Team Member Attribution & Agile Meta
            {
                "type": "panel",
                "attrs": {"panelType": "note"},
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "TEAM MEMBER ATTRIBUTION & SPRINT SCOPE\n", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": "Assigned Owner: ", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": f"{meta['owner']} ("},
                            {"type": "text", "text": meta['srn'], "marks": [{"type": "code"}]},
                            {"type": "text", "text": f") - {meta['role']}\n"},
                            {"type": "text", "text": "Subsystem Component: ", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": f"{meta['component']}\n"},
                            {"type": "text", "text": "Sprint Assignment: ", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": f"{meta['sprint_name']} | Story Points: {meta['points']} (Fibonacci Scale)"}
                        ]
                    }
                ]
            }
        ]
    }
    return doc


def jira_api(path, data=None, method="GET"):
    url = f"{BASE_URL}{path}"
    headers = {
        "Authorization": AUTH,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Antigravity-Agile-Formatter/2.0"
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            c = r.read().decode("utf-8")
            return r.status, json.loads(c) if c else {}
    except urllib.error.HTTPError as e:
        c = e.read().decode("utf-8")
        try:
            return e.code, json.loads(c)
        except Exception:
            return e.code, {"error": c}


def update_epic_descriptions():
    print("\n--- Updating Epic Descriptions ---")
    epics_meta = {
        EPIC_FINE: {
            "summary": "Overdue Fine Payment & Settlement",
            "desc": "Epic encompassing complete UC-04 overdue fine computation ($1/day), itemized fine inspection, multi-channel payment settlement (Campus Wallet & UPI), SHA-256 digital receipt issuance, and automated $20 hold restriction threshold."
        },
        EPIC_CATALOG: {
            "summary": "Core Catalog Search & Discovery Engine",
            "desc": "Epic encompassing high-speed indexed catalog search across titles, authors, and ISBN-10/13, strict input validation and SQL injection sanitization, and responsive WCAG 2.1 AA accessible web UI."
        },
        EPIC_AUTH: {
            "summary": "Campus SSO Authentication & Security Shield",
            "desc": "Epic encompassing OpenID Connect campus SSO authentication, session state management, 5-attempt brute-force lockout middleware, in-memory sliding-window rate limiting (60 req/min), and hardened cookie security."
        },
        EPIC_HOLD: {
            "summary": "Hold Reservation & Queue Progression Engine",
            "desc": "Epic encompassing reservation hold placement on checked-out books, duplicate/available hold validation, student hold cancellation, gapless FIFO queue advancement, circulation return processing, hold demand reporting, and 72-hour auto-expiration cascade."
        },
        EPIC_QA: {
            "summary": "Automated Testing, CI/CD & Quality Assurance",
            "desc": "Epic encompassing relational SQLite schema testing, baseline unit test fixtures, notification retry engine with exponential backoff, automated GitHub Actions CI/CD pipeline, and full test plan execution across 4 mandatory test reports."
        }
    }

    for key, info in epics_meta.items():
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "panel",
                    "attrs": {"panelType": "info"},
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": "EPIC OBJECTIVE & SCOPE\n", "marks": [{"type": "strong"}]},
                                {"type": "text", "text": info["desc"]}
                            ]
                        }
                    ]
                }
            ]
        }
        st, res = jira_api(f"/rest/api/3/issue/{key}", data={"fields": {"summary": info["summary"], "description": doc}}, method="PUT")
        print(f"  Epic {key} [{info['summary'][:40]}]: HTTP {st}")


def move_stories_to_sprints():
    print("\n--- Assigning Issues to Sprints ---")
    sprint_groups = {
        3: ["DCLRG-9", "DCLRG-10", "DCLRG-11", "DCLRG-12", "DCLRG-13", "DCLRG-14"],
        4: ["DCLRG-15", "DCLRG-16", "DCLRG-17", "DCLRG-18", "DCLRG-19", "DCLRG-20"],
        37: ["DCLRG-2", "DCLRG-3", "DCLRG-4", "DCLRG-5", "DCLRG-6", "DCLRG-7", "DCLRG-8",
             "DCLRG-21", "DCLRG-22", "DCLRG-23", "DCLRG-24", "DCLRG-25", "DCLRG-26", "DCLRG-27"]
    }
    for sid, issues in sprint_groups.items():
        st, res = jira_api(f"/rest/agile/1.0/sprint/{sid}/issue", data={"issues": issues}, method="POST")
        print(f"  Sprint {sid}: Moved {len(issues)} issues -> HTTP {st}")


def main():
    print("=" * 75)
    print("FORMATTING ALL STORIES & EPICS IN LIVE JIRA CLOUD")
    print(f"Site: {BASE_URL} | Project: DCLRG")
    print("=" * 75)

    update_epic_descriptions()

    print("\n--- Updating 26 User Stories (ADF Format, Parent Epics, Points, Owners) ---")
    success_count = 0

    for key, meta in STORIES.items():
        desc = make_adf_description(meta)

        fields = {
            "summary": meta["summary"],
            "description": desc,
            "customfield_10037": meta["points"],  # Board Estimation Field
            "customfield_10016": meta["points"],  # Story point estimate field
            "parent": {"key": meta["epic"]},       # Epic Linkage
            "components": [{"name": meta["component"]}],
            "labels": meta["labels"]
        }

        if meta["assign_to_dharshini"]:
            fields["assignee"] = {"accountId": DHARSHINI_ACCOUNT_ID}

        st, res = jira_api(f"/rest/api/3/issue/{key}", data={"fields": fields}, method="PUT")
        if st in (200, 204):
            success_count += 1
            print(f"  + [{key}] Formatted Story: {meta['summary'][:65]}")
        else:
            print(f"  - [{key}] Failed (HTTP {st}): {res}")
        time.sleep(0.2)

    move_stories_to_sprints()

    print("\n" + "=" * 75)
    print(f"COMPLETED: Formatted {success_count} user stories with full ADF structure!")
    print(f"Active Board:   {BASE_URL}/jira/software/projects/DCLRG/boards/2")
    print(f"Backlog View:   {BASE_URL}/jira/software/projects/DCLRG/boards/2/backlog")
    print(f"Timeline View:  {BASE_URL}/jira/software/projects/DCLRG/boards/2/timeline")
    print(f"Reports:        {BASE_URL}/jira/software/projects/DCLRG/boards/2/reports/velocity-chart")
    print("=" * 75)


if __name__ == "__main__":
    main()
