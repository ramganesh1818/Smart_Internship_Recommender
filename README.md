# Smart Internship Recommender

A lightweight full-stack web application that recommends the top 5 internships tailored to a learner’s background. Recommendations are driven by a TF-IDF + KNN similarity pipeline and each result explains why it was suggested.

## Project Structure

```
smart-internship-recommender/
├── backend/                # FastAPI service and dataset generator
├── frontend/               # React + Vite + Tailwind client
├── data/                   # Internship dataset (1000 rows)
└── README.md
```

## Dataset

- Location: `data/internships_1000.csv`
- 1000 realistic internship records
- Automatically generated at startup if missing via `backend/generate_dataset.py`

## Backend

- Stack: FastAPI, pandas, scikit-learn
- Model: TF-IDF vectorizer + Nearest Neighbors (cosine)
- Endpoints:
  - `GET /health` → returns `{ "status": "ok", "items": 1000 }`
  - `POST /recommend` → returns exactly 5 internships with reasons

### Run locally

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # PowerShell (use source .venv/bin/activate on bash)
pip install -r requirements.txt
uvicorn main:app --reload
```

The API listens on `http://localhost:8000` and enables CORS for the Vite dev server.

## Frontend

- Stack: React, Vite, Tailwind CSS, React Router, Axios
- Pages:
  - `/` Home
  - `/form` Preference form
  - `/results` Recommendation cards with reasons

### Run locally

```bash
cd frontend
npm install
npm run dev
```

The app runs at `http://localhost:5173`.

## Usage Flow

1. Start the backend server.
2. Start the frontend dev server.
3. Open the frontend URL and complete the form (education, skills, sector, location).
4. Submit to view the top 5 internships, each with four explanation bullets: skills, sector, location, and education fit.

## Notes

- No external database or GPU required; everything runs locally.
- Dataset auto-regenerates if the CSV is missing.
- Responses exclude explicit similarity scores and provide narrative reasons instead.

