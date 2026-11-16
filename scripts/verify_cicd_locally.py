"""
verify_cicd_locally.py
Executes the full CI/CD pipeline verification stages locally to ensure 100% compliance
before pushing to GitHub Actions or submitting project deliverables.

Stages verified:
1. Syntax & Bytecode Compilation
2. Flake8 PEP 8 Code Quality Audit
3. Bandit DevSecOps Security AST (SAST) Scanner
4. Pytest Automated Test Suite & Coverage Threshold Gating (>= 70%)
5. Application Factory & Healthcheck Probing
6. Production Deployment Manifests Check (Dockerfile, docker-compose.yml, Procfile)
"""

import os
import subprocess
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(BASE_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def print_stage(title):
    print("\n" + "=" * 70)
    print(f"STAGE: {title}")
    print("=" * 70)


def run_command(cmd, desc):
    print(f"--> Executing: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    res = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[FAILED] {desc}")
        print("STDOUT:\n", res.stdout)
        print("STDERR:\n", res.stderr)
        return False
    print(f"[PASSED] {desc}")
    if res.stdout.strip():
        lines = res.stdout.strip().split("\n")
        if len(lines) > 5:
            print("Output preview:")
            for l in lines[-4:]:
                print(f"  {l}")
        else:
            print("Output:\n" + res.stdout.strip())
    return True


def main():
    print("=" * 70)
    print("LOCAL CI/CD PIPELINE VERIFICATION SUITE")
    print(f"Project: Digital Campus Library Reservation Gateway (DCLRG)")
    print(f"Directory: {BASE_DIR}")
    print("=" * 70)

    stages = []

    # 1. Bytecode Compilation Check
    print_stage("1. Python Syntax & Bytecode Pre-compilation")
    s1 = run_command([sys.executable, "-m", "py_compile", "src/app.py", "src/database.py", "src/fine_manager.py"], "Bytecode Compilation Check")
    stages.append(("Syntax & Bytecode", s1))

    # 2. Flake8 Style Audit
    print_stage("2. Flake8 Code Style & PEP 8 Standards Audit")
    s2 = run_command(["flake8", "src", "tests"], "Flake8 Quality Gate")
    stages.append(("Flake8 Code Style", s2))

    # 3. Bandit Security Scan
    print_stage("3. Bandit DevSecOps Security AST (SAST) Scanner")
    s3 = run_command(["bandit", "-r", "src", "-s", "B101"], "Bandit Security Scan (0 Vulnerabilities)")
    stages.append(("Bandit Security SAST", s3))

    # 4. Pytest & Coverage Threshold
    print_stage("4. Automated Hermetic Test Suite & 70% Coverage Gating")
    s4 = run_command(["pytest", "--cov=src", "--cov-branch", "--cov-fail-under=70", "-q"], "Pytest 118 Tests & Coverage Enforcement")
    stages.append(("Pytest & Coverage Gate", s4))

    # 5. App Factory & Health Probe
    print_stage("5. Application Factory & REST API Healthcheck Probe")
    try:
        from src.app import create_app
        app = create_app(db_path=":memory:")
        client = app.test_client()
        r = client.get("/health")
        data = r.get_json() or {}
        if r.status_code == 200 and data.get("status") in ("UP", "healthy") and data.get("db") == "CONNECTED":
            print(f"[PASSED] Healthcheck endpoint returned HTTP 200 with status={data.get('status')} and db={data.get('db')}")
            s5 = True
        else:
            print(f"[FAILED] Healthcheck returned HTTP {r.status_code}: {r.data}")
            s5 = False
    except Exception as e:
        print(f"[FAILED] App factory test encountered exception: {e}")
        s5 = False
    stages.append(("Healthcheck Probe", s5))

    # 6. Deployment Manifests Verification
    print_stage("6. Production Deployment Manifests Check")
    manifests = ["Dockerfile", "docker-compose.yml", "Procfile", "requirements.txt", ".dockerignore"]
    missing = [m for m in manifests if not os.path.exists(os.path.join(BASE_DIR, m))]
    if not missing:
        print("[PASSED] All production deployment manifests verified (Dockerfile, docker-compose.yml, Procfile, requirements.txt, .dockerignore)")
        s6 = True
    else:
        print(f"[FAILED] Missing deployment files: {missing}")
        s6 = False
    stages.append(("Deployment Manifests", s6))

    # Summary
    print("\n" + "=" * 70)
    print("CI/CD PIPELINE LOCAL VERIFICATION SUMMARY")
    print("=" * 70)
    all_passed = True
    for name, status in stages:
        status_text = "PASSED (100% OK)" if status else "FAILED"
        print(f"  Stage: {name.ljust(35)} -> {status_text}")
        if not status:
            all_passed = False

    print("=" * 70)
    if all_passed:
        print("ALL CI/CD STAGES PASSED SUCCESSFULLY!")
        print("Your repository is 100% ready for GitHub Actions CI/CD and final submission evaluation.")
        return 0
    else:
        print("SOME CI/CD STAGES FAILED. Please review the error logs above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
