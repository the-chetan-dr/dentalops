# Dental Clinic CI/CD: GitHub Actions + Render

## Pipeline

1. Every push to `main`/`master` and every pull request runs the GitHub Actions workflow in `.github/workflows/ci.yml`.
2. CI compiles Python, runs Ruff, Django checks, migration drift checks, Django tests, static collection and Django deployment checks.
3. The security job runs `pip-audit`, Bandit and Trivy (dependency vulnerabilities, secrets and configuration findings).
4. Render's Blueprint deploys the Django web service and PostgreSQL database. `autoDeployTrigger: checksPass` means Render waits for GitHub checks before deploying.
5. Render runs `/healthz/` as its health check.

## First deployment

1. Push this project to a GitHub repository. Make sure the default production branch is named `main` (or change `branch` in `render.yaml`).
2. In GitHub, open **Settings → Actions → General** and ensure workflows are allowed to run.
3. In Render, choose **New → Blueprint**, connect the GitHub repository, review `render.yaml`, and apply it.
4. Render creates the PostgreSQL database and web service. It generates `SECRET_KEY` and injects `DATABASE_URL` automatically.
5. Open the service's **Settings → Auto-Deploy** and verify it is set to **After CI Checks Pass**. The Blueprint also requests `checksPass`.
6. Wait for the first deployment. Visit `https://YOUR-SERVICE.onrender.com/healthz/`; expected response: `{"status": "ok"}`.
7. Create an application user through the app's registration flow. If a Django admin/superuser is required, use Render Shell: `python manage.py createsuperuser`.

## Local verification

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py test
python manage.py runserver
```

## Important production notes

- The previous source contained a hardcoded Django `SECRET_KEY`. It has been removed from settings; Render generates a new key. If the old key was ever used on a public deployment, rotate it and invalidate existing sessions.
- SQLite is retained only for local development. Render uses PostgreSQL through `DATABASE_URL`.
- Render's filesystem is ephemeral. Do not rely on local `MEDIA_ROOT` for patient uploads; configure durable private object storage before storing any real records.
- This project should be treated as a demo until authentication, authorization, audit logging, backups, encryption, privacy controls and applicable healthcare compliance requirements have been reviewed. Do not upload real patient-identifiable data to a demo deployment.
- The free Render Postgres offering is intended for evaluation and may have time/availability limits. Check current Render plan terms and use a suitable paid database with backups for anything important.
- The current application test coverage is only a smoke-test baseline. Add business-flow tests for patient registration, appointments, prescriptions, invoices, role permissions and AI assistant routes before relying on automatic production deployment.

## Branch protection recommendation

In GitHub, open **Settings → Branches → Add branch protection rule** for `main`. Require pull requests and require both checks: `Django checks and tests` and `Dependency and source security scans`. This prevents merging until both jobs pass. Render's `checksPass` then prevents deployment until CI succeeds.
