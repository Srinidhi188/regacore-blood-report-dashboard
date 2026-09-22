import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.reports import router as reports_router
from app.utils.logger import get_logger

logger = get_logger("regacore_main")

app = FastAPI(
    title="REGACORE — Blood Report Dashboard API",
    description="Backend API for AI-powered blood test PDF extraction, biomarker normalization, and historical tracking.",
    version="1.0.0"
)

# Configure CORS for local development and cloud deployment
allowed_origins_env = os.getenv("CORS_ORIGINS", "")
if allowed_origins_env and allowed_origins_env.strip() != "*":
    allowed_origins = [orig.strip() for orig in allowed_origins_env.split(",") if orig.strip()]
    allow_credentials = True
else:
    allowed_origins = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ]
    # In open dev / wildcard deployment
    if allowed_origins_env.strip() == "*":
        allowed_origins = ["*"]
        allow_credentials = False
    else:
        allow_credentials = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reports_router)

@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring uptime and readiness."""
    return {
        "status": "healthy",
        "service": "regacore-blood-report-backend",
        "version": "1.0.0"
    }

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the REGACORE Blood Report Extraction API.",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
