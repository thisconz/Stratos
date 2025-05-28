from fastapi import FastAPI
from app.api.v1 import (
    auth, files, metadata, user, onboarding, sessions,
    mfa, analytics, product_tour, oauth
)
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI(title="Stratos API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "supersecretkey123"),
)

# Root health check
@app.get("/")
async def root():
    return {"message": "Stratos API is running"}

# Register routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(metadata.router, prefix="/metadata", tags=["metadata"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(onboarding.router, prefix="/onboarding", tags=["onboarding"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(mfa.router, prefix="/mfa", tags=["mfa"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(product_tour.router, prefix="/tour", tags=["product tour"])
app.include_router(oauth.router, prefix="/oauth", tags=["oauth"])
