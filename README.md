
# Email Triage App

A simple web app that pulls emails from Gmail, analyzes/triages them, and displays the results in a small frontend.

## What’s in this repo

- `backend/`: FastAPI backend (API endpoints, Gmail integration)
- `frontend/`: Static frontend (HTML/CSS/JS)

## Requirements

- Python 3.10+ (recommended)

## Run locally

### 1) Backend

From the `backend/` folder:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

Backend should be at `http://127.0.0.1:8080`.

### 2) Frontend

Open `frontend/index.html` in your browser.

If your browser blocks API calls due to CORS or `file://` restrictions, run a tiny static server from the repo root:

```bash
python -m http.server 5500
```

Then open `http://127.0.0.1:5500/frontend/index.html`.

## Notes on credentials

This project uses Gmail credentials/tokens. Do **not** commit secrets.
The repo includes a `.gitignore` that excludes common credential/token files.

