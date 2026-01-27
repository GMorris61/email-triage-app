
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

## 🖼️ Screenshots

Add screenshots to `docs/` and they’ll render here on GitHub.

Suggested filenames:

- `docs/search.png` — search screen
- `docs/results.png` — results + action buttons

Once you add them, these links will work:

![Search UI](docs/search.png)
![Results UI](docs/results.png)

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

## ☁️ Deployment (EC2)

This project is deployed on an AWS EC2 instance running Amazon Linux 2023.
The backend is publicly accessible via port 8080 and securely loads Gmail credentials from AWS Secrets Manager.

---

## 🔧 EC2 Setup Steps

### 1) Launch EC2 Instance

- AMI: Amazon Linux 2023
- Instance type: t2.micro (Free Tier eligible)
- Name: email-triage-backend
- Enable Auto-assign Public IP
- Open port 8080 in the security group
- Attach IAM role with SecretsManagerReadOnly access

### 2) Create IAM Role

- Name: EmailTriageEC2Role
- Trusted entity: ec2.amazonaws.com
- Permissions: SecretsManagerReadOnly
- Attach this role during EC2 launch

### 3) Create Key Pair

- Format: .pem
- Name: email-triage-key
- Download and store securely

---

## 🖥️ Connect to EC2

### Option A: EC2 Instance Connect

- Use AWS Console → EC2 → Connect → Instance Connect

### Option B: SSH from Terminal

```bash
chmod 400 email-triage-key.pem
ssh -i email-triage-key.pem ec2-user@<your-public-ip>
```

## ⚙️ Backend Setup on EC2

```bash
# Update packages
sudo yum update -y

# Install Python and Git
sudo yum install python3 git -y

# Clone the repo
git clone https://github.com/GMorris61/email-triage-app.git
cd email-triage-app/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
uvicorn main:app --host 0.0.0.0 --port 8080
```

## 🌐 Test the Backend

Visit:

`http://<your-ec2-public-ip>:8080/docs`

You’ll see the FastAPI Swagger UI.
Try a search keyword to confirm Gmail API access is working.

---

## 🔐 Secrets Manager Integration

- Gmail OAuth refresh token is stored in AWS Secrets Manager
- EC2 instance uses IAM role to retrieve the secret securely
- No hardcoded credentials or environment variables required

---

## 📸 Deployment Screenshots

Add screenshots of:

- EC2 instance running
- Swagger UI response
- Gmail search results
- AWS Secrets Manager (redacted)

---

## 🛡️ Security notes

- Do **not** commit credentials/tokens.
- This repo includes a `.gitignore` that excludes common secret file patterns.
- CORS is currently wide open for local development; tighten it before production.


