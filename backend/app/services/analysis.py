from sqlalchemy.orm import Session
from typing import List
from .. import models, crud

KEYWORD_MAP = {
    "beach": ["travel", "beach", "sunset", "outdoor"],
    "sunset": ["sunset", "aesthetic", "golden hour"],
    "food": ["food", "cafe", "brunch"],
    "fitness": ["fitness", "gym", "energetic"],
    "fashion": ["fashion", "style", "streetwear"],
    "night": ["nightlife", "urban", "neon"],
    "beauty": ["beauty", "selfcare", "glow"],
    "travel": ["travel", "adventure", "scenic"],
}

VIBE_RULES = [
    ("luxury", ["neon", "urban", "nightlife"]),
    ("aesthetic", ["aesthetic", "sunset", "golden hour", "cafe"]),
    ("energetic", ["fitness", "gym", "energetic"]),
    ("casual", ["food", "brunch", "streetwear"]),
    ("travel", ["travel", "beach", "scenic", "adventure"]),
]


def extract_tags_from_caption(caption: str) -> List[str]:
    caption_l = (caption or "").lower()
    tags: List[str] = []
    for key, kws in KEYWORD_MAP.items():
        if key in caption_l:
            tags.extend(kws)
    # Fallback: add some hash words
    for token in caption_l.split():
        if token.startswith("#"):
            tags.append(token[1:])
    # Deduplicate and keep top N
    uniq = []
    for t in tags:
        if t not in uniq:
            uniq.append(t)
    return uniq[:6] if uniq else ["general"]


def infer_vibe(tags: List[str]) -> str:
    for vibe, triggers in VIBE_RULES:
        if any(t in tags for t in triggers):
            return vibe
    return "casual"


def estimate_quality(tags: List[str]):
    # Very naive proxies
    lighting = 0.7 if ("sunset" in tags or "golden hour" in tags) else 0.5
    visual = 0.8 if ("aesthetic" in tags or "style" in tags) else 0.6
    return lighting, visual


def analyze_all(db: Session, influencer_id: int):
    posts = db.query(models.Post).filter(models.Post.influencer_id == influencer_id).all()
    for p in posts:
        tags = extract_tags_from_caption(p.caption or "")
        vibe = infer_vibe(tags)
        lighting, visual = estimate_quality(tags)
        crud.set_post_analysis(
            db,
            post_id=p.id,
            data={
                "tags": ",".join(tags),
                "vibe": vibe,
                "quality_lighting": float(lighting),
                "quality_visual": float(visual),
            },
        )

    reels = db.query(models.Reel).filter(models.Reel.influencer_id == influencer_id).all()
    for r in reels:
        tags = extract_tags_from_caption(r.caption or "")
        vibe = infer_vibe(tags)
        crud.set_reel_analysis(
            db,
            reel_id=r.id,
            data={
                "tags": ",".join(tags),
                "vibe": vibe,
            },
        )
