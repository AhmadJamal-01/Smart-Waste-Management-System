from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from api.inference import run_inference
import time

router = APIRouter(prefix="/api/v1", tags=["detection"])

@router.post("/detect")
async def detect_waste(
    file: UploadFile = File(...),
    # CHANGE default=0.25 :
    conf: float = Query(default=0.25, ge=0.1, le=0.9),
):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(400, "Only JPEG and PNG supported")

    start       = time.time()
    image_bytes = await file.read()
    result      = run_inference(image_bytes, conf=conf)
    result["inference_ms"] = round((time.time() - start) * 1000, 2)
    result["filename"]     = file.filename

    if result["is_hazardous"]:
        result["alert"] = {
            "type"    : "hazardous",
            "severity": "high",
            "message" : "⚠️ Hazardous waste detected — immediate action required",
        }

    return JSONResponse(content=result)

@router.get("/health")
async def health():
    return {"status": "ok", "model": "swos_v2", "version": "1.0"}