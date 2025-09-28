from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.scraper import ingest_mock_influencer
from ..services.analysis import analyze_all

router = APIRouter()

@router.post("/scrape/{username}")
def scrape_username(username: str, db: Session = Depends(get_db)):
    inst = ingest_mock_influencer(db, username=username)
    analyze_all(db, influencer_id=inst.id)
    return {"status": "ok", "message": f"Mock data ingested and analyzed for @{username}"}
