from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, models, schemas

router = APIRouter()

@router.get("/reels/{username}", response_model=schemas.ReelsResponse)
def get_reels(username: str, db: Session = Depends(get_db)):
    inst = crud.get_influencer_by_username(db, username)
    if not inst:
        raise HTTPException(status_code=404, detail="Influencer not found. Try /api/scrape/{username} to ingest mock data.")
    reels = crud.list_reels(db, inst.id, limit=5)
    return {"reels": reels}
