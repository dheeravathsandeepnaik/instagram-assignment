# Instagram Influencer Profile – Full Stack Assignment

This repository contains a FastAPI backend and a React (Vite) frontend that together build an Influencer Profile page including analytics, posts, and reels. The backend provides endpoints and mock data ingestion with basic analysis. The frontend is a modern, responsive UI that consumes these APIs.

## Project Structure

- `backend/`
  - FastAPI app with SQLite via SQLAlchemy
  - Routers: `profile`, `posts`, `reels`, `scrape`
  - Services: `scraper.py` (mock data), `analysis.py` (tag/vibe/quality)
- `frontend/`
  - React + Vite app
  - Components for Profile, Posts, Reels, and Analytics

## Backend

### Requirements
- Python 3.10+

### Install and Run
```bash
# In a new terminal
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python backend/uvicorn_app.py
```
The backend will start at `http://localhost:8000`.

Available endpoints (prefixed with `/api`):
- `GET /api/health`
- `POST /api/scrape/{username}` – Ingests mock data and runs analysis
- `GET /api/profile/{username}` – Influencer profile with averages and engagement rate
- `GET /api/posts/{username}` – Last 10 posts with analysis
- `GET /api/reels/{username}` – Last 5 reels with analysis

Notes:
- Database file: `backend/db.sqlite3` (auto-created)
- CORS allows `http://localhost:5173` for the frontend

### Database
- Engine: SQLite via SQLAlchemy (`backend/app/database.py`)
- File location: `backend/db.sqlite3` (relative to repo). It is created automatically on app startup.
- For production, consider swapping to Postgres by changing `SQLALCHEMY_DATABASE_URL` in `backend/app/database.py`.

## Frontend

### Requirements
- Node.js 18+

### Install and Run
```bash
# In another terminal
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`.

On first load for a new username, if data is not found, the frontend will call `POST /api/scrape/{username}` to ingest mock data and then reload the profile automatically.

### Configuring API base URL
The frontend reads the backend base URL from `VITE_API_BASE` (default: `http://localhost:8000`).

Create `frontend/.env` for local overrides:
```bash
VITE_API_BASE=http://localhost:8000
```

## Assumptions
- Instagram real scraping is out of scope for a take-home; we simulate with `services/scraper.py` using public Unsplash images and randomized metrics.
- Image/video “analysis” is rule-based keyword extraction from captions (`services/analysis.py`). This can be swapped for real CV/ML later.
- Engagement rate formula: `(avg_likes + avg_comments) / followers * 100`.

## Bonus Ideas (not fully implemented)
- Audience demographics inference via external datasets or ML models.
- Deeper CV-based classification using Torch models already listed in `requirements.txt`.

## Troubleshooting
- If the frontend cannot reach the backend, ensure FastAPI is running at `http://localhost:8000` and that CORS is configured (it is by default in `app/main.py`).
- If you change the frontend port, update `origins` in `backend/app/main.py` accordingly and restart the server.

## Deploy to Render

### Backend (FastAPI)
1. Push this repo to GitHub.
2. In Render, create a new Web Service.
   - Repository: this repo
   - Runtime: Python
   - Build Command:
     ```bash
     pip install -r backend/requirements.txt
     ```
   - Start Command:
     ```bash
     python backend/uvicorn_app.py
     ```
   - Environment:
     - `PORT` is provided by Render automatically.
     - Optionally set `RELOAD=false` in production.
3. After deploy, note the Render URL, e.g. `https://your-backend.onrender.com`.

SQLite note: Render’s ephemeral filesystem resets on redeploys. For persistent data, switch to a managed Postgres and update `backend/app/database.py` accordingly.

### Frontend (Vite React)
Option A: Deploy as a Static Site
1. Build step and publish dir:
   - Build Command:
     ```bash
     npm ci && npm run build
     ```
   - Publish Directory: `frontend/dist`
   - Environment Variables:
     - `VITE_API_BASE=https://your-backend.onrender.com`
2. Create a Static Site on Render pointing to this repo. Set Root Directory to `frontend/`.

Option B: Keep frontend local
Set `VITE_API_BASE` in `frontend/.env` to your Render backend URL and run `npm run dev` locally.

## About `__init__.py`
- Python 3.11+ supports implicit namespace packages, so empty `__init__.py` files in subfolders like `app/routers/` or `app/services/` are not strictly required.
- Keeping `app/__init__.py` is harmless and ensures `app` is a proper package for all tooling.
- You may delete empty `__init__.py` in `app/routers/` and `app/services/` without changing imports.

## Screens
- Profile header with follower stats
- Analytics chart (likes/comments trend)
- Recent posts with tags, vibe, quality indicators
- Recent reels with tags and vibe
