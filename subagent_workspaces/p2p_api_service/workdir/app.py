from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from routes.api import router as api_router
from db import engine, Base
import models

# Initialize SQLite database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="P2P API Service",
    description="Data scraping/analysis service with Direct P2P monetization",
    version="1.0.0"
)

# Custom exception handler for 402 Payment Required to ensure exact schema matches
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_402_PAYMENT_REQUIRED:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

app.include_router(api_router)

@app.get("/")
async def root():
    return {
        "status": "success",
        "data": {},
        "message": "Welcome to P2P API Service. Check /docs for endpoints. A valid X-API-Key header is required for protected routes."
    }
