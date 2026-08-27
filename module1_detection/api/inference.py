from ultralytics import YOLO
from pathlib import Path
import numpy as np
import cv2
import base64
import torch

CLASS_NAMES = ["plastic", "organic", "metal", "glass", "hazardous"]
CLASS_COLORS = {
    "plastic"  : "#3B82F6",
    "organic"  : "#22C55E",
    "metal"    : "#94A3B8",
    "glass"    : "#06B6D4",
    "hazardous": "#EF4444",
}

MODEL_PATH = Path(r"C:\SWOS\module1_detection\models\swos_v3_best.pt")

_model = None

def get_model():
    global _model
    if _model is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading model on {device}...")
        _model = YOLO(str(MODEL_PATH))
        print("✅ Model loaded")
    return _model

def run_inference(image_bytes: bytes, conf):
    nparr  = np.frombuffer(image_bytes, np.uint8)
    img    = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image")

    h, w  = img.shape[:2]
    model = get_model()
    results = model(img, conf=conf, verbose=False)[0]

    detections   = []
    class_counts = {c: 0 for c in CLASS_NAMES}

    for box in results.boxes:
        cls_id     = int(box.cls[0])
        confidence = float(box.conf[0])
        cls_name   = CLASS_NAMES[cls_id]
        x1, y1, x2, y2 = box.xyxy[0].tolist()

        detections.append({
            "class_id"  : cls_id,
            "class_name": cls_name,
            "confidence": round(confidence, 4),
            "bbox"      : {
                "x1": round(x1), "y1": round(y1),
                "x2": round(x2), "y2": round(y2),
            },
            "color": CLASS_COLORS[cls_name],
        })
        class_counts[cls_name] += 1

    dominant     = max(class_counts, key=class_counts.get) \
                   if any(class_counts.values()) else None
    is_hazardous = class_counts["hazardous"] > 0

    annotated    = results.plot()
    _, buf       = cv2.imencode(".jpg", annotated)
    annotated_b64= base64.b64encode(buf).decode("utf-8")

    return {
        "detections"     : detections,
        "total_objects"  : len(detections),
        "dominant_type"  : dominant,
        "is_hazardous"   : is_hazardous,
        "class_counts"   : class_counts,
        "image_size"     : {"width": w, "height": h},
        "annotated_image": annotated_b64,
    }