from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

from generate_dataset import DATA_FILE, generate_dataset
from translations import translate


class RecommendRequest(BaseModel):
    education: str = Field(..., min_length=1)
    skills: List[str] = Field(default_factory=list)
    sector: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    language: str | None = "en"

    @validator("skills", pre=True)
    def ensure_list(cls, value):  # type: ignore[override]
        if value is None:
            return []
        if isinstance(value, str):
            if not value.strip():
                return []
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @validator("skills")
    def normalize_skills(cls, value):  # type: ignore[override]
        return [skill.strip() for skill in value if skill.strip()]


class Recommendation(BaseModel):
    id: int
    title: str
    organization: str
    sector: str
    location: str
    duration: str
    stipend: int
    type: str
    mode: str
    reasons: List[str]


app = FastAPI(title="Smart Internship Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DATA_PATH = DATA_FILE
_vectorizer: TfidfVectorizer | None = None
_knn: NearestNeighbors | None = None
_matrix = None
_dataset: pd.DataFrame | None = None

_EDUCATION_FOCUS = {
    "b.tech": {"IT", "Cybersecurity", "Data Analytics", "Renewable Energy", "Logistics", "GIS"},
    "b.e": {"IT", "Renewable Energy", "Logistics", "GIS"},
    "b.sc": {"Healthcare", "Agriculture", "Data Analytics", "Education"},
    "b.com": {"Finance", "Public Policy", "Logistics"},
    "bba": {"Finance", "Tourism", "Public Policy", "Media"},
    "mba": {"Finance", "Tourism", "Public Policy", "Logistics"},
    "ba": {"Public Policy", "Education", "Media", "Law"},
    "law": {"Law", "Public Policy"},
    "design": {"Design", "Media"},
}


def _ensure_dataset() -> None:
    if not DATA_PATH.exists():
        generate_dataset(DATA_PATH)


def _prepare_model() -> None:
    global _vectorizer, _knn, _matrix, _dataset

    _ensure_dataset()

    _dataset = pd.read_csv(DATA_PATH)
    if _dataset.empty:
        raise RuntimeError("Dataset is empty after loading.")

    corpus = (
        _dataset["skills"].fillna("")
        + " "
        + _dataset["sector"].fillna("")
        + " "
        + _dataset["location"].fillna("")
        + " "
        + _dataset["type"].fillna("")
        + " "
        + _dataset["mode"].fillna("")
    )

    _vectorizer = TfidfVectorizer()
    _matrix = _vectorizer.fit_transform(corpus)

    _knn = NearestNeighbors(metric="cosine", n_neighbors=10)
    _knn.fit(_matrix)


@app.on_event("startup")
def startup_event() -> None:
    _prepare_model()


def _build_query_text(payload: RecommendRequest) -> str:
    pieces = [
        " ".join(payload.skills),
        payload.sector,
        payload.location,
        payload.education,
    ]
    return " ".join(part.strip() for part in pieces if part.strip())


def _skill_reason(user_skills: list[str], internship_skills: list[str], lang: str = "en") -> str:
    if not user_skills:
        preview = ", ".join(internship_skills[:3])
        return translate("skillNoList", lang, skills=preview)

    normalized = {s.lower(): s for s in internship_skills}
    matched_originals = [normalized[s.lower()] for s in user_skills if s.lower() in normalized]
    if matched_originals:
        summary = ", ".join(matched_originals[:4])
        return translate("skillMatch", lang, count=len(matched_originals), total=len(user_skills), skills=summary)
    preview = ", ".join(internship_skills[:3])
    return translate("skillNoMatch", lang, skills=preview)


def _sector_reason(user_sector: str, internship_sector: str, lang: str = "en") -> str:
    if user_sector.strip().lower() == internship_sector.strip().lower():
        return translate("sectorMatch", lang, sector=internship_sector)
    return translate("sectorRelated", lang, sector=internship_sector, userSector=user_sector)


def _location_reason(user_location: str, internship_location: str, mode: str, lang: str = "en") -> str:
    user_loc = user_location.strip().lower()
    internship_loc = internship_location.strip().lower()
    if user_loc in {"any", "all"}:
        return translate("locationFlexible", lang, location=internship_location, mode=mode)
    if user_loc == internship_loc:
        return translate("locationMatch", lang, location=internship_location)
    if user_loc == "remote" and (internship_loc == "remote" or mode.lower() == "online"):
        return translate("locationRemote", lang, location=internship_location, mode=mode)
    return translate("locationOther", lang, location=internship_location, mode=mode)


def _education_reason(education: str, sector: str, lang: str = "en") -> str:
    edu_lower = education.strip().lower()
    for key, sectors in _EDUCATION_FOCUS.items():
        if key in edu_lower:
            if sector in sectors:
                return translate("educationSuitable", lang, education=education)
            return translate("educationComplements", lang, education=education, sector=sector)
    return translate("educationSuitable", lang, education=education)


def _format_recommendation(index: int, payload: RecommendRequest) -> Recommendation:
    if _dataset is None:
        raise RuntimeError("Dataset not loaded")

    lang = payload.language or "en"
    row = _dataset.iloc[index]
    internship_skills = [s.strip() for s in str(row["skills"]).split("|") if s.strip()]
    reasons = [
        _skill_reason(payload.skills, internship_skills, lang),
        _sector_reason(payload.sector, row["sector"], lang),
        _location_reason(payload.location, row["location"], row["mode"], lang),
        _education_reason(payload.education, row["sector"], lang),
    ]

    return Recommendation(
        id=int(row["id"]),
        title=str(row["title"]),
        organization=str(row["organization"]),
        sector=str(row["sector"]),
        location=str(row["location"]),
        duration=str(row["duration"]),
        stipend=int(row["stipend"]),
        type=str(row["type"]),
        mode=str(row["mode"]),
        reasons=reasons,
    )


@app.get("/health")
def healthcheck() -> dict[str, str | int]:
    if _dataset is None:
        _prepare_model()
    assert _dataset is not None
    return {"status": "ok", "items": int(len(_dataset))}


@app.post("/recommend", response_model=List[Recommendation])
def recommend(payload: RecommendRequest) -> List[Recommendation]:
    if _vectorizer is None or _knn is None or _matrix is None or _dataset is None:
        _prepare_model()
    assert _vectorizer is not None and _knn is not None and _matrix is not None and _dataset is not None

    if _dataset.empty:
        raise HTTPException(status_code=500, detail="Dataset unavailable")

    query_text = _build_query_text(payload)
    if not query_text.strip():
        raise HTTPException(status_code=400, detail="At least one preference is required")

    query_vec = _vectorizer.transform([query_text])
    distances, indices = _knn.kneighbors(query_vec, n_neighbors=min(10, len(_dataset)))

    seen = set()
    recommendations: List[Recommendation] = []
    for idx in indices[0]:
        if idx in seen:
            continue
        seen.add(idx)
        recommendations.append(_format_recommendation(int(idx), payload))
        if len(recommendations) == 5:
            break

    # Fallback if fewer than 5 found (unlikely but safe)
    if len(recommendations) < 5:
        remaining = _dataset.index.difference(list(seen))
        for idx in remaining[: 5 - len(recommendations)]:
            recommendations.append(_format_recommendation(int(idx), payload))

    return recommendations

