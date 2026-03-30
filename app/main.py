from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import users, posts

# Create tables (dev convenience — use Alembic in prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BlogApp API",
    description="A simple open blog API",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router)
app.include_router(posts.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}