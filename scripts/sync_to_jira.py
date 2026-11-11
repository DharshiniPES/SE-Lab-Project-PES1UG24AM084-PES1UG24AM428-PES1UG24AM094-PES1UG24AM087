"""
Automated Jira Cloud REST API Synchronizer for LRG Project.
Takes Atlassian Jira Cloud domain, email, and API token to create
Epics, User Stories, Sprints, and transitions via Jira REST API v3.
Robust URL normalization, error handling, and project discovery.
"""

import os
import sys
import re
import json
import base64
import urllib.request
import urllib.error

# Ensure UTF-8 output encoding for Windows PowerShell/CMD
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

JIRA_ISSUES_DATA = [
    # Epics
    {"type": "Epic", "summary": "EPIC-1: Catalog & Discovery Engine", "desc": "High-speed indexed catalog search by Title, Author, ISBN with query sanitization (LRG-F-001, LRG-F-002).", "points": 16},
    {"type": "Epic", "summary": "EPIC-2: Member Circulation, Holds & Fines", "desc": "FIFO hold queueing, 72h auto-expiry cascade, and UC-04 overdue fine settlement with Campus Wallet (LRG-F-020 to 031).", "points": 32},
    {"type": "Epic", "summary": "EPIC-3: Librarian Administration & Reporting", "desc": "Librarian returns, book inventory management, and hold demand analytics (LRG-F-040, LRG-F-041).", "points": 14},
    {"type": "Epic", "summary": "EPIC-4: Infrastructure, Security & QA", "desc": "Campus SSO authentication, sliding-window rate limiting, GitHub Actions CI/CD, and 85%+ test coverage (LRG-SR-001 to 007).", "points": 23},

    # Sprint 1 Stories
    {"type": "Story", "summary": "LRG-101: Relational SQLite Schema & Initial Seed Data", "desc": "SQLite database schema with foreign keys, unique constraints, and seed titles.", "points": 5, "sprint": "Sprint 1"},
    {"type": "Story", "summary": "LRG-102: Catalog Search by Title, Author, ISBN (LRG-F-001)", "desc": "Sub-second catalog search across 100,000 titles with normalized ISBN matching.", "points": 5, "sprint": "Sprint 1"},
    {"type": "Story", "summary": "LRG-103: Search Input Validation & Sanitization (LRG-F-002)", "desc": "Input sanitization against SQL injection and XSS.", "points": 3, "sprint": "Sprint 1"},
    {"type": "Story", "summary": "LRG-104: Campus SSO Authentication & Session Engine (LRG-F-010)", "desc": "OpenID Connect SSO token verification and brute-force lockout after 5 attempts.", "points": 5, "sprint": "Sprint 1"},
    {"type": "Story", "summary": "LRG-105: Responsive Catalog Search Web UI", "desc": "Mobile-responsive web interface meeting WCAG 2.1 AA standards.", "points": 3, "sprint": "Sprint 1"},
    {"type": "Story", "summary": "LRG-106: Baseline Unit Tests for Search & Authentication", "desc": "Automated hermetic pytest test suite for Sprint 1 foundation.", "points": 3, "sprint": "Sprint 1"},

    # Sprint 2 Stories
    {"type": "Story", "summary": "LRG-201: Place Hold on Checked-Out Book (LRG-F-020)", "desc": "Allows students to place holds on checked-out books with FIFO queue position.", "points": 5, "sprint": "Sprint 2"},
    {"type": "Story", "summary": "LRG-202: Prevent Duplicate & Available Holds (LRG-F-021)", "desc": "Validation rules rejecting duplicate holds and holds on Available titles.", "points": 3, "sprint": "Sprint 2"},
    {"type": "Story", "summary": "LRG-203: View & Cancel Active Holds (LRG-F-022)", "desc": "Student portal view of active holds with instant cancellation authorization.", "points": 3, "sprint": "Sprint 2"},
    {"type": "Story", "summary": "LRG-204: Dynamic FIFO Queue Position Progression (LRG-F-023)", "desc": "Gapless queue re-sequencing upon cancellation or fulfillment.", "points": 5, "sprint": "Sprint 2"},
    {"type": "Story", "summary": "LRG-205: Return Title & Hold Promotion to Ready (LRG-F-040)", "desc": "Librarian returns title, promotes position-1 to Ready with 72h window.", "points": 5, "sprint": "Sprint 2"},
    {"type": "Story", "summary": "LRG-206: Hold Demand Report for Librarian (LRG-F-041)", "desc": "High-demand title ranking report sorted by queue length.", "points": 3, "sprint": "Sprint 2"},

    # Sprint 3 Stories
    {"type": "Story", "summary": "LRG-301: UC-04 Overdue Fine Assessment & Balance Engine", "desc": "Calculate daily late fees at $1/day from due date; track itemized fines.", "points": 5, "sprint": "Sprint 3"},
    {"type": "Story", "summary": "LRG-302: UC-04 Campus Wallet / UPI Settlement & Digital Receipt", "desc": "Payment settlement through Campus Wallet and cryptographically verifiable digital receipts.", "points": 5, "sprint": "Sprint 3"},
    {"type": "Story", "summary": "LRG-303: UC-04 Hold Restriction when Unpaid Fines >= $20", "desc": "Automated restriction blocking hold requests if student has outstanding fines >= $20.", "points": 3, "sprint": "Sprint 3"},
    {"type": "Story", "summary": "LRG-304: 72-Hour Ready Hold Auto-Expiration & Cascade Promotion", "desc": "Automated worker expiring unclaimed Ready holds after 72 hours and cascading to next member.", "points": 5, "sprint": "Sprint 3"},
    {"type": "Story", "summary": "LRG-305: Notification Retry Engine & Failure Audit Logging", "desc": "Exponential backoff retry queue (3 attempts) on SMTP dispatch failure with dead-letter logging.", "points": 3, "sprint": "Sprint 3"},
    {"type": "Story", "summary": "LRG-306: Sliding-Window Rate Limiter & Cookie Security (LRG-SR-007)", "desc": "Sliding-window rate limiter (60 req/min) and HTTP cookie security attributes.", "points": 3, "sprint": "Sprint 3"},
    {"type": "Story", "summary": "LRG-307: Automated GitHub Actions CI/CD Pipeline (ci.yml)", "desc": "Automated workflow executing linting hermetic tests and 70% coverage threshold gating.", "points": 3, "sprint": "Sprint 3"},
    {"type": "Story", "summary": "LRG-308: Execute Full Test Plan & Generate 4 Mandatory Test Reports", "desc": "Execution of 117 automated tests and generation of Unit System Coverage and Branch reports.", "points": 5, "sprint": "Sprint 3"}
]


def normalize_domain(raw_input_domain: str) -> str:
    """Normalize input domain to a clean https://<subdomain>.atlassian.net URL."""
    d = raw_input_domain.strip()
    # Strip any leading http/https and any colon or slashes
    d = re.sub(r'^https?[:/]+', '', d, flags=re.I)
    # Strip trailing slashes and paths (e.g. /jira/your-work)
    d = d.split('/')[0].strip()
    # Replace underscores with hyphens if user typed underscores for domain name
    if '_' in d and not d.endswith('.atlassian.net'):
        d = d.replace('_', '-')
    # If user only typed the subdomain (e.g. "my-team"), append .atlassian.net
    if '.' not in d:
        d = f"{d}.atlassian.net"
    return f"https://{d}"


def jira_request(url, auth_header, method="GET", data=None):
    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Antigravity-LRG-Jira-Sync/2.0"
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read().decode("utf-8")
            return resp.status, json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        try:
            parsed = json.loads(err_msg)
            return e.code, parsed
        except Exception:
            return e.code, {"error": err_msg}
    except urllib.error.URLError as e:
        return 0, {"error": f"Network / DNS Error: {e.reason}"}
    except Exception as e:
        return 0, {"error": str(e)}


def main():
    print("=" * 70)
    print("ATLASSIAN JIRA CLOUD REST API SYNCHRONIZER (LRG PROJECT)")
    print("=" * 70)

    raw_domain = os.environ.get("JIRA_DOMAIN") or input(
        "Enter Jira Domain (e.g. my-team.atlassian.net or https://my-team.atlassian.net): "
    ).strip()
    
    jira_domain = normalize_domain(raw_domain)
    email = os.environ.get("JIRA_EMAIL") or input("Enter Jira Account Email: ").strip()
    api_token = os.environ.get("JIRA_API_TOKEN") or input("Enter Atlassian API Token: ").strip()

    auth_str = f"{email}:{api_token}"
    auth_header = f"Basic {base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')}"

    print(f"\n[1/4] Connecting to {jira_domain} as {email}...")
    status, res = jira_request(f"{jira_domain}/rest/api/3/myself", auth_header)
    if status != 200:
        print(f"\nAuthentication Failed (HTTP {status})!")
        print(f"Error Details: {res.get('error', res.get('errorMessages', 'Check credentials or domain'))}")
        print("\nTroubleshooting Tips:")
        print("1. Check that the domain is your exact Atlassian subdomain (e.g. yourname.atlassian.net).")
        print("2. Ensure your email matches your Atlassian account login.")
        print("3. Ensure the API token was generated at: https://id.atlassian.com/manage-profile/security/api-tokens")
        return

    user_name = res.get('displayName', email)
    print(f"Successfully authenticated as: {user_name}")

    # [2/4] Fetch available projects
    print("\n[2/4] Discovering Jira projects on your account...")
    status, projects = jira_request(f"{jira_domain}/rest/api/3/project", auth_header)
    if status != 200 or not isinstance(projects, list):
        print(f"Could not retrieve projects (HTTP {status}): {projects}")
        return

    if not projects:
        print("\nNo projects found on this Jira site!")
        print("Please open Jira in your browser, click 'Projects' -> 'Create project' -> 'Scrum', name it 'Library Reservation Gateway' (Key: LRG), then run this script again.")
        return

    print("Found existing Jira projects:")
    for p in projects:
        print(f"  - [{p.get('key')}] {p.get('name')} (id: {p.get('id')})")

    # Prompt or auto-match project
    default_key = projects[0].get('key')
    match_lrg = next((p.get('key') for p in projects if p.get('key') in ('LRG', 'DCLRG', 'LIB')), default_key)
    
    project_key = os.environ.get("JIRA_PROJECT_KEY") or input(
        f"\nEnter Target Project Key [press Enter for '{match_lrg}']: "
    ).strip() or match_lrg

    # [3/4] Verify project issue types
    print(f"\n[3/4] Fetching issue types for project '{project_key}'...")
    status, proj_details = jira_request(f"{jira_domain}/rest/api/3/project/{project_key}", auth_header)
    if status != 200:
        print(f"Could not fetch details for project '{project_key}' (HTTP {status})")
        return

    valid_types = [it.get('name') for it in proj_details.get('issueTypes', [])]
    print(f"Available Issue Types: {', '.join(valid_types)}")

    # Prefer 'Task' or 'Story' or first non-subtask
    story_type_name = "Task"
    if "Story" in valid_types:
        story_type_name = "Story"
    elif "Task" in valid_types:
        story_type_name = "Task"
    elif valid_types:
        story_type_name = valid_types[0]

    epic_type_name = "Epic" if "Epic" in valid_types else story_type_name

    # [4/4] Create issues
    print(f"\n[4/4] Creating {len(JIRA_ISSUES_DATA)} issues in project '{project_key}'...")
    created_count = 0

    for item in JIRA_ISSUES_DATA:
        target_type = epic_type_name if item["type"] == "Epic" else story_type_name
        issue_payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": item["summary"],
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": item["desc"]}]
                        }
                    ]
                },
                "issuetype": {"name": target_type}
            }
        }
        st, created = jira_request(f"{jira_domain}/rest/api/3/issue", auth_header, method="POST", data=issue_payload)
        if st in (200, 201):
            created_count += 1
            print(f"  + [{created.get('key')}] {item['summary']}")
        else:
            err_details = created.get('errors') or created.get('errorMessages') or created.get('error')
            print(f"  - Failed for {item['summary']} (HTTP {st}): {err_details}")

    print("\n" + "=" * 70)
    print(f"SUCCESS: Created {created_count} issues in Jira project '{project_key}'!")
    print(f"Open your Jira board here:")
    print(f"{jira_domain}/jira/software/projects/{project_key}/boards")
    print("=" * 70)


if __name__ == "__main__":
    main()
