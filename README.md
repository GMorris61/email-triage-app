
# Email Triage Automation (FastAPI + Gmail API + AWS Secrets Manager)

A lightweight backend service that connects to Gmail, searches messages by **subject keyword**, and performs automated cleanup actions (**trash**, **archive**, **dry-run**).

The system uses **FastAPI** for the backend, **AWS Secrets Manager** for secure credential storage, and the **Gmail API** for email operations.

A simple **HTML/CSS/JavaScript** frontend provides a clean UI for interacting with the backend.

---

## 📌 Features

- Search Gmail messages by subject keyword
- Display sender + subject for each matching email
- Perform actions:
	- Trash
	- Archive
	- Dry-run (preview without modifying anything)
- Secure OAuth credential storage in AWS Secrets Manager
- Automatic access token refresh using Google OAuth refresh tokens
- FastAPI backend with CORS enabled (dev-friendly)
- Clean, minimal frontend UI (HTML + CSS + JS)

---

## 🧱 Architecture Overview

```text
Browser (frontend/index.html + app.js)
				|
				| HTTP (fetch)
				v
FastAPI Backend (backend/main.py)
				|
				| Gmail API (google-api-python-client)
				v
Gmail Account (search + actions)

FastAPI Backend
				|
				| AWS SDK (boto3)
				v
AWS Secrets Manager (stores Gmail OAuth JSON)
```

---

## 🔌 API Endpoints

### Search emails

- `GET /email/search?keyword=...`
- Returns up to 10 results (subject contains the keyword)

Example:

```bash
curl "http://localhost:8080/email/search?keyword=invoice"
```

### Perform an action

- `POST /email/action`
- Body:
	- `email_ids`: list of Gmail message IDs
	- `action`: `trash` | `archive` | `dry-run`

Example:

```bash
curl -X POST "http://localhost:8080/email/action" \
	-H "Content-Type: application/json" \
	-d '{"email_ids":["178c..."],"action":"dry-run"}'
```

---

## 🔐 Credentials & AWS Secrets Manager

This app expects a Secrets Manager secret containing a **Gmail OAuth authorized user JSON**.

### Environment variables

- `GMAIL_SECRET_NAME` (default: `gmail-credentials`)
- `AWS_REGION` or `AWS_DEFAULT_REGION` (default: `us-east-1`)

### Secret format

The secret value should be a JSON object compatible with `google.oauth2.credentials.Credentials.from_authorized_user_info(...)`.
It typically includes fields like:

- `client_id`
- `client_secret`
- `refresh_token`
- `token_uri`
- `scopes`

Important: the backend reads this secret in `backend/secrets_manager.py`.

---

## ▶️ Run locally

### 1) Backend (FastAPI)

From the `backend/` folder:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# optional
export GMAIL_SECRET_NAME="gmail-credentials"
export AWS_REGION="us-east-1"

uvicorn main:app --reload --port 8080
```

Backend runs at `http://127.0.0.1:8080`.

### 2) Frontend

Option A: open `frontend/index.html` directly.

Option B (recommended): serve it locally to avoid browser `file://` quirks:

```bash
python -m http.server 5500
```

Then open `http://127.0.0.1:5500/frontend/index.html`.

---

## 🛡️ Security notes

- Do **not** commit credentials/tokens.
- This repo includes a `.gitignore` that excludes common secret file patterns.
- CORS is currently wide open for local development; tighten it before production.


