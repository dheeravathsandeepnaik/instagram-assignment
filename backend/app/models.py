from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Influencer(Base):
    __tablename__ = "influencers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    profile_picture_url = Column(String, nullable=True)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship("Post", back_populates="influencer", cascade="all, delete-orphan")
    reels = relationship("Reel", back_populates="influencer", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    influencer_id = Column(Integer, ForeignKey("influencers.id"))
    post_id = Column(String, index=True)
    image_url = Column(String)
    caption = Column(String)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)

    influencer = relationship("Influencer", back_populates="posts")
    analysis = relationship("PostAnalysis", back_populates="post", uselist=False, cascade="all, delete-orphan")

class PostAnalysis(Base):
    __tablename__ = "post_analyses"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), unique=True)
    tags = Column(String)  # comma-separated tags
    vibe = Column(String)
    quality_lighting = Column(Float, default=0.0)
    quality_visual = Column(Float, default=0.0)

    post = relationship("Post", back_populates="analysis")

class Reel(Base):
    __tablename__ = "reels"

    id = Column(Integer, primary_key=True, index=True)
    influencer_id = Column(Integer, ForeignKey("influencers.id"))
    reel_id = Column(String, index=True)
    thumbnail_url = Column(String)
    caption = Column(String)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)

    influencer = relationship("Influencer", back_populates="reels")
    analysis = relationship("ReelAnalysis", back_populates="reel", uselist=False, cascade="all, delete-orphan")

class ReelAnalysis(Base):
    __tablename__ = "reel_analyses"

    id = Column(Integer, primary_key=True, index=True)
    reel_id = Column(Integer, ForeignKey("reels.id"), unique=True)
    tags = Column(String)
    vibe = Column(String)

    reel = relationship("Reel", back_populates="analysis")
