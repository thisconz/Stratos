from .api.dependencies import get_current_admin
from fastapi import FastAPI, Depends
from .api.routes.core_routes import router as core_router
from .api.routes.auth_routes import router as auth_router
from .api.routes.admin_routes import router as admin_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API is running"}

app.include_router(auth_router, tags=["auth"])
app.include_router(core_router, tags=["core"])
app.include_router(
    admin_router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)]
)
