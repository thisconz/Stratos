from .api.dependencies import get_current_admin
from fastapi import FastAPI, Depends
from .api.routes.core_routes import router as core_router
from .api.routes.auth_routes import router as auth_router
from .api.routes.admin_routes import router as admin_router
from .api.routes.locations import router as locations
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

origins = [
    "http://localhost:3000",
    # Add other frontend URLs if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API is running"}

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(core_router, tags=["core"])
app.include_router(admin_router, prefix="/admin", tags=["admin"], dependencies=[Depends(get_current_admin)])
app.include_router(locations, prefix="/locations", tags=["locations"])
