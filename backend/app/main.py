from fastapi import FastAPI
from .api.routes.core_routes import router as core_router
from .api.routes.auth_routes import router as auth_router
from .api.routes.admin_routes import router as admin_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(auth_router)
app.include_router(core_router)
app.include_router(admin_router, prefix="/admin")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)