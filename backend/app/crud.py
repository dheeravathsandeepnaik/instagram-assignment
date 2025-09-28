from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models
from typing import List, Optional

# Influencer

def get_influencer_by_username(db: Session, username: str) -> Optional[models.Influencer]:
    return db.query(models.Influencer).filter(models.Influencer.username == username).first()

def upsert_influencer(db: Session, data: dict) -> models.Influencer:
    inst = get_influencer_by_username(db, data["username"]) 
    if inst:
        for k, v in data.items():
            setattr(inst, k, v)
    else:
        inst = models.Influencer(**data)
        db.add(inst)
    db.commit()
    db.refresh(inst)
    return inst

# Posts

def add_posts(db: Session, influencer_id: int, posts: List[dict]):
    for p in posts:
        post = models.Post(**p, influencer_id=influencer_id)
        db.add(post)
    db.commit()

def list_posts(db: Session, influencer_id: int, limit: int = 10) -> List[models.Post]:
    return db.query(models.Post).filter(models.Post.influencer_id == influencer_id).order_by(models.Post.timestamp.desc()).limit(limit).all()

# Reels

def add_reels(db: Session, influencer_id: int, reels: List[dict]):
    for r in reels:
        reel = models.Reel(**r, influencer_id=influencer_id)
        db.add(reel)
    db.commit()

def list_reels(db: Session, influencer_id: int, limit: int = 5) -> List[models.Reel]:
    return db.query(models.Reel).filter(models.Reel.influencer_id == influencer_id).order_by(models.Reel.timestamp.desc()).limit(limit).all()

# Analysis

def set_post_analysis(db: Session, post_id: int, data: dict):
    existing = db.query(models.PostAnalysis).filter(models.PostAnalysis.post_id == post_id).first()
    if existing:
        for k, v in data.items():
            setattr(existing, k, v)
    else:
        obj = models.PostAnalysis(post_id=post_id, **data)
        db.add(obj)
    db.commit()

def set_reel_analysis(db: Session, reel_id: int, data: dict):
    existing = db.query(models.ReelAnalysis).filter(models.ReelAnalysis.reel_id == reel_id).first()
    if existing:
        for k, v in data.items():
            setattr(existing, k, v)
    else:
        obj = models.ReelAnalysis(reel_id=reel_id, **data)
        db.add(obj)
    db.commit()

# Aggregations

def avg_likes_comments(db: Session, influencer_id: int):
    avg_likes, avg_comments = db.query(func.avg(models.Post.likes), func.avg(models.Post.comments)).filter(models.Post.influencer_id == influencer_id).one()
    return float(avg_likes or 0), float(avg_comments or 0)
