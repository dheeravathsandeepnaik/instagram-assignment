from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import profile, posts, reels, scrape

app = FastAPI(title="Instagram Influencer Profile API", version="0.1.0")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup (SQLite)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(profile.router, prefix="/api", tags=["profile"]) 
app.include_router(posts.router, prefix="/api", tags=["posts"]) 
app.include_router(reels.router, prefix="/api", tags=["reels"]) 
app.include_router(scrape.router, prefix="/api", tags=["scrape"]) 

@app.get("/api/health")
def health():
    return {"status": "ok"}
