import logging
from fastapi import FastAPI
from .database import engine, Base
from .config import settings

# import routers
from .routers import auth as auth_router
from .routers import users as users_router
from .routers import appointments as appt_router
from .routers import status as status_router

# Create DB tables (for dev/demo). In production use Alembic migrations.
Base.metadata.create_all(bind=engine)

# Configure logging
LOG_LEVEL = getattr(logging, getattr(settings, "LOG_LEVEL", "INFO").upper(), logging.INFO)
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("telemed")

app = FastAPI(title="Telemedicine API", version="1.0.0")

# Register routers
app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(appt_router.router)
app.include_router(status_router.router)

@app.get("/api/health")
def health():
    return {"status": "ok"}
