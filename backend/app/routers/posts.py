from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, models, schemas

router = APIRouter()

@router.get("/posts/{username}", response_model=schemas.PostsResponse)
def get_posts(username: str, db: Session = Depends(get_db)):
    inst = crud.get_influencer_by_username(db, username)
    if not inst:
        raise HTTPException(status_code=404, detail="Influencer not found. Try /api/scrape/{username} to ingest mock data.")
    posts = crud.list_posts(db, inst.id, limit=10)
    # Ensure analysis relationship is loaded
    return {"posts": posts}
