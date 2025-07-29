import os
import logging
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from models import *
from seed_data import create_seed_data
from routers import auth, patients, providers, appointments, ui

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fake_carecloud.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("fake_carecloud")

# Configure uvicorn access logging to use our handlers
uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.handlers = []
for handler in logging.getLogger().handlers:
    uvicorn_logger.addHandler(handler)

uvicorn_error_logger = logging.getLogger("uvicorn.error")
uvicorn_error_logger.handlers = []
for handler in logging.getLogger().handlers:
    uvicorn_error_logger.addHandler(handler)

# Create database tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables created")

# Initialize seed data
db = SessionLocal()
create_seed_data(db)
db.close()
logger.info("Seed data initialized")

app = FastAPI(
    title=os.getenv("API_TITLE", "Fake CareCloud API"),
    description="A mock implementation of the CareCloud API for testing purposes",
    version=os.getenv("API_VERSION", "1.0.0"),
)

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application startup completed")
    logger.info(f"API Title: {app.title}")
    logger.info(f"API Version: {app.version}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI application shutting down")
    logger.info("Goodbye!")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["Authentication"])  # OAuth endpoint has no /v2 prefix
app.include_router(patients.router, prefix="/v2", tags=["Patients"])
app.include_router(providers.router, prefix="/v2", tags=["Providers"])
app.include_router(appointments.router, prefix="/v2", tags=["Appointments"])
app.include_router(ui.router, tags=["UI"])

@app.get("/")
async def root():
    return {
        "message": "Fake CareCloud API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "endpoints": {
            "authentication": "/oauth2/access_token",
            "patients": "/v2/patients",
            "providers": "/v2/providers",
            "locations": "/v2/locations",
            "appointment_resources": "/v2/appointment_resources",
            "visit_reasons": "/v2/visit_reasons",
            "appointments": "/v2/appointments"
        },
        "ui": {
            "home": "/ui",
            "patients": "/ui/patients",
            "appointments": "/ui/appointments"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("FAKE_CARECLOUD_HOST", "0.0.0.0")
    port = int(os.getenv("FAKE_CARECLOUD_PORT", "8000"))
    debug = os.getenv("FAKE_CARECLOUD_DEBUG", "false").lower() == "true"
    
    logger.info(f"Starting Fake CareCloud API server on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Log file: fake_carecloud.log")
    
    # Create custom log config to ensure access logs go to our handlers
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": "fake_carecloud.log",
                "formatter": "default",
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["file", "console"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["file", "console"], 
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["file", "console"],
                "level": "INFO", 
                "propagate": False,
            },
        },
    }
    
    if debug:
        uvicorn.run("app:app", host=host, port=port, reload=True, log_config=log_config)
    else:
        uvicorn.run(app, host=host, port=port, reload=False, log_config=log_config)