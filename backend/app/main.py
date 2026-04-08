from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.middleware.audit import AuditMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="CompassCHW API",
    version="0.1.0",
    description="Backend API for CompassCHW",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuditMiddleware)

# Register all routers
from app.routers.auth import router as auth_router
from app.routers.chw import router as chw_router
from app.routers.member import router as member_router
from app.routers.sessions import router as sessions_router
from app.routers.requests import router as requests_router
from app.routers.matching import router as matching_router
from app.routers.conversations import router as conversations_router
from app.routers.credentials import router as credentials_router
from app.routers.upload import router as upload_router
from app.routers.health import router as health_router

app.include_router(auth_router)
app.include_router(chw_router)
app.include_router(member_router)
app.include_router(sessions_router)
app.include_router(requests_router)
app.include_router(matching_router)
app.include_router(conversations_router)
app.include_router(credentials_router)
app.include_router(upload_router)
app.include_router(health_router)
