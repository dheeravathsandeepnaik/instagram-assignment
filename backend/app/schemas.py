from typing import List, Optional
from pydantic import BaseModel, field_validator
from datetime import datetime

class PostAnalysis(BaseModel):
    tags: List[str]
    vibe: str
    quality_lighting: float
    quality_visual: float

    @field_validator("tags", mode="before")
    @classmethod
    def split_tags(cls, v):
        if isinstance(v, str):
            return [t for t in v.split(".") if t] if "," not in v and "." in v else [t for t in v.split(",") if t]
        return v or []

class ReelAnalysis(BaseModel):
    tags: List[str]
    vibe: str

    @field_validator("tags", mode="before")
    @classmethod
    def split_tags(cls, v):
        if isinstance(v, str):
            return [t for t in v.split(".") if t] if "," not in v and "." in v else [t for t in v.split(",") if t]
        return v or []

class Post(BaseModel):
    id: int
    image_url: str
    caption: Optional[str]
    likes: int
    comments: int
    timestamp: datetime
    analysis: Optional[PostAnalysis]

    class Config:
        from_attributes = True

class Reel(BaseModel):
    id: int
    thumbnail_url: str
    caption: Optional[str]
    views: int
    likes: int
    comments: int
    timestamp: datetime
    analysis: Optional[ReelAnalysis]

    class Config:
        from_attributes = True

class Influencer(BaseModel):
    id: int
    name: str
    username: str
    profile_picture_url: Optional[str]
    followers: int
    following: int
    posts_count: int

    class Config:
        from_attributes = True

class ProfileResponse(BaseModel):
    influencer: Influencer
    avg_likes: float
    avg_comments: float
    engagement_rate: float

class PostsResponse(BaseModel):
    posts: List[Post]

class ReelsResponse(BaseModel):
    reels: List[Reel]
