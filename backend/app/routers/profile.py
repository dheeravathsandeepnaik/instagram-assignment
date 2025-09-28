from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, models, schemas

router = APIRouter()

@router.get("/profile/{username}", response_model=schemas.ProfileResponse)
def get_profile(username: str, db: Session = Depends(get_db)):
    inst = crud.get_influencer_by_username(db, username)
    if not inst:
        raise HTTPException(status_code=404, detail="Influencer not found. Try /api/scrape/{username} to ingest mock data.")
    avg_likes, avg_comments = crud.avg_likes_comments(db, inst.id)
    # Engagement rate ~ (avg likes + avg comments) / followers
    engagement_rate = 0.0
    if inst.followers:
        engagement_rate = ((avg_likes + avg_comments) / inst.followers) * 100
    return {
        "influencer": inst,
        "avg_likes": round(avg_likes, 2),
        "avg_comments": round(avg_comments, 2),
        "engagement_rate": round(engagement_rate, 2),
    }
