import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.core.config import settings
from app.core.s3 import init_bucket
from app.api import deps
from app.api.v1 import (auth, user, objects, documents)

app = FastAPI(
    title="StratosCore API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Root health check ---
@app.get("/")
async def root():
    return {"message": "Stratos API is running"}

# --- Route Registration ---
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(objects.router, prefix="/api/v1/objects", tags=["Objects"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])

# --- Startup Events ---
@app.on_event("startup")
async def startup_event():
    await init_bucket()

# --- Shutdown Events ---
@app.on_event("shutdown")
async def shutdown_event():
    pass

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
