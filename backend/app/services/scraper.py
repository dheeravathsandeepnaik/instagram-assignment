from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
from .. import crud

MOCK_PFPS = [
    "https://images.unsplash.com/photo-1544005313-94ddf0286df2",
    "https://images.unsplash.com/photo-1547425260-76bcadfb4f2c",
    "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d",
]

MOCK_IMAGES = [
    "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330",
    "https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d",
    "https://images.unsplash.com/photo-1472214103451-9374bd1c798e",
    "https://images.unsplash.com/photo-1491553895911-0055eca6402d",
]

MOCK_THUMBS = [
    "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4",
    "https://images.unsplash.com/photo-1496307042754-b4aa456c4a2d",
    "https://images.unsplash.com/photo-1469474968028-56623f02e42e",
]

CAPTION_BANK = [
    "Sunset vibes at the beach #travel #sunset",
    "Brunch with the besties! #food #cafe #aesthetic",
    "Morning workout done. Feeling energetic! #fitness #gym",
    "Street fashion diaries. #fashion #style",
    "Dreaming of mountains and coffee. #travel #nature",
    "New skincare routine – glowing! #beauty #selfcare",
    "City lights at night ✨ #nightlife #urban",
]


def ingest_mock_influencer(db: Session, username: str):
    name = username.replace("_", " ").title()
    influencer = crud.upsert_influencer(
        db,
        {
            "name": name,
            "username": username,
            "profile_picture_url": random.choice(MOCK_PFPS),
            "followers": random.randint(50_000, 500_000),
            "following": random.randint(100, 1000),
            "posts_count": random.randint(100, 1500),
        },
    )

    # Generate posts
    posts = []
    now = datetime.utcnow()
    for i in range(15):
        posts.append(
            {
                "post_id": f"{username}_post_{i}",
                "image_url": random.choice(MOCK_IMAGES),
                "caption": random.choice(CAPTION_BANK),
                "likes": random.randint(1000, 20000),
                "comments": random.randint(20, 500),
                "timestamp": now - timedelta(days=i),
            }
        )
    crud.add_posts(db, influencer.id, posts)

    # Generate reels
    reels = []
    for i in range(8):
        reels.append(
            {
                "reel_id": f"{username}_reel_{i}",
                "thumbnail_url": random.choice(MOCK_THUMBS),
                "caption": random.choice(CAPTION_BANK),
                "views": random.randint(10_000, 1_000_000),
                "likes": random.randint(1000, 50000),
                "comments": random.randint(10, 1000),
                "timestamp": now - timedelta(days=i*2),
            }
        )
    crud.add_reels(db, influencer.id, reels)
    return influencer
