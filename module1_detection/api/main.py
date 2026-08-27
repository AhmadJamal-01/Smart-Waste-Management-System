from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.detection import router as detection_router
from api.inference import get_model

app = FastAPI(
    title      = "SWOS Detection API",
    description= "Module 1: Real-time waste detection",
    version    = "1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins  = ["*"],
    allow_methods  = ["*"],
    allow_headers  = ["*"],
)

@app.on_event("startup")
async def startup():
    get_model()
    print("✅ SWOS Detection API ready")

app.include_router(detection_router)

@app.get("/")
async def root():
    return {
        "service": "SWOS Detection API",
        "docs"   : "/docs",
        "health" : "/api/v1/health",
    }

@app.get("/health")
def health():
    return {"status": "ok", "module": "module1_detection"}