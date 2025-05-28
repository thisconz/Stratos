from fastapi import APIRouter
from . import (
    auth, onboarding, dashboard, files,
    sync, vision, viewer, sharing,
    settings, admin, analytics
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(onboarding.router, prefix="/onboarding", tags=["onboarding"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(sync.router, prefix="/sync", tags=["sync"])
api_router.include_router(vision.router, prefix="/vision", tags=["vision"])
api_router.include_router(viewer.router, prefix="/viewer", tags=["viewer"])
api_router.include_router(sharing.router, prefix="/sharing", tags=["sharing"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
