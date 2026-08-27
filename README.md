# 🗑️ SWOS — Smart Waste Operating System

> **Transforming municipal waste from a cost center into an optimized, circular city asset — real-time visibility, automated decisions, and measurable environmental impact.**

![Version](https://img.shields.io/badge/version-3.0-blue)
![Python](https://img.shields.io/badge/python-3.10-green)
![YOLO](https://img.shields.io/badge/YOLO-26n-orange)
![License](https://img.shields.io/badge/license-MIT-purple)

---

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Modules](#modules)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Running the System](#running-the-system)
- [API Reference](#api-reference)
- [Model Performance](#model-performance)
- [Database Schema](#database-schema)
- [Screenshots](#screenshots)
- [Challenges & Solutions](#challenges--solutions)

---

## 🌍 Overview

SWOS is a full-stack AI-powered smart city waste management system built for Lahore Municipal Corporation. It addresses 4 critical problems:

| Problem | Solution |
|---------|----------|
| No real-time bin visibility | IoT sensors + YOLO26 computer vision |
| Inefficient truck routing | OR-Tools VRP optimizer |
| Low recycling rates | Citizen gamification + rewards |
| No data for planning | Prophet forecasting + Gov dashboard |

**Key Results:**
- 🤖 YOLO26 model — **0.745 mAP50** (waste detection accuracy)
- 🚛 VRP routing — eliminates unnecessary truck trips
- ♻️ Recycling marketplace — PKR 136,000 per transaction
- 🌍 Carbon tracking — 18 tons CO₂ avoided
- 👥 Citizen engagement — points, badges, leaderboard

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      SHARED DATABASE                         │
│              PostgreSQL (Docker) + Redis Cache               │
│   zones · bins · bin_telemetry · users · disposal_events    │
│   alerts · collection_routes · marketplace_listings · bids  │
└──────────────┬──────────────┬──────────────┬────────────────┘
               │              │              │
    ┌──────────▼──┐  ┌────────▼──┐  ┌───────▼────────┐
    │  Module 1   │  │ Module 2  │  │   Module 3     │
    │  Detection  │  │Segregation│  │   Routing      │
    │  Port 8001  │  │ Port 8002 │  │   Port 8003    │
    │  YOLO26 AI  │  │ Rewards   │  │  OR-Tools VRP  │
    └─────────────┘  └───────────┘  └────────────────┘
    ┌──────────┐  ┌──────────────┐  ┌────────────────┐
    │ Module 4 │  │   Module 5   │  │   Module 6     │
    │Prediction│  │ Marketplace  │  │Gov Dashboard   │
    │ Port8004 │  │  Port 8005   │  │  Port 3000     │
    │ Prophet  │  │ Auction Sys  │  │React + Charts  │
    └──────────┘  └──────────────┘  └────────────────┘
```

**Data Flow:**
```
Bin sensor ping → fill level stored → Module 3 route optimization
Camera image   → YOLO26 detection  → waste type + hazard alert
Citizen scan   → Module 2 rewards  → points + badge earned
Historical data→ Module 4 forecast → predict next week volume
Recycled waste → Module 5 auction  → PKR revenue for collector
All modules    → Module 6 dashboard→ KPIs + PDF report export
```

---

## 📦 Modules

### Module 1 — Smart Waste Detection
**Port:** `8001`

Real-time waste type detection and bin fill-level monitoring using edge computer vision.

**Capabilities:**
- Detects 5 waste classes: `plastic` `organic` `metal` `glass` `hazardous`
- Bin fill-level telemetry via IoT sensors
- Auto-alert when fill ≥ 85% or hazardous waste detected
- Annotated image returned with bounding boxes
- ONNX export for edge deployment

**Model:** YOLO26n — trained on 29,235 images across 9 datasets

**Endpoints:**
```
POST /api/v1/detect          → Upload image, get detections
GET  /api/v1/health          → Health check
```

---

### Module 2 — Intelligent Segregation
**Port:** `8002`

Citizen-facing PWA with AI waste scanning, rewards, badges, and leaderboard.

**Capabilities:**
- Phone camera scan → AI identifies waste type → correct bin guidance
- Points system (plastic=10, metal=12, hazardous=20 per correct disposal)
- 5 badge tiers: Eco Starter → Green Recycler → Eco Champion → Planet Hero → Eco Legend
- City-wide leaderboard by zone
- Disposal history and accuracy tracking

**Endpoints:**
```
POST /api/v2/disposal/submit          → Log disposal, award points
GET  /api/v2/disposal/bin-guide/{type}→ Which bin to use
GET  /api/v2/rewards/{phone}          → User stats + badges
GET  /api/v2/leaderboard              → Top citizens ranking
POST /api/v2/badges/seed              → Initialize badge definitions
```

---

### Module 3 — Smart Collection Routing
**Port:** `8003`

Dynamic VRP-based routing that minimizes fuel and time by only visiting bins that need collection.

**Capabilities:**
- OR-Tools VRP solver with live bin fill data
- Haversine distance matrix for accurate GPS routing
- Multi-truck optimization (configurable fleet size)
- Driver mobile app with real GPS tracking
- Fleet manager dashboard with weekly charts

**Endpoints:**
```
POST /api/v3/route/optimize       → Optimize routes for given bins
POST /api/v3/route/optimize/demo  → Demo with Lahore test bins
GET  /api/v3/health               → Health check
```

---

### Module 4 — Waste Prediction Engine
**Port:** `8004`

Facebook Prophet time-series forecasting for per-zone waste volume prediction.

**Capabilities:**
- 8-zone coverage (Gulberg III, DHA, Model Town, Johar Town, Garden Town, Bahria Town, Cavalry Ground, DHA Phase 5)
- 550-day forecast horizon
- Seasonal patterns: weekly, yearly, Ramadan
- Peak day identification for proactive resource planning
- 2 years synthetic training data (29,200 records)

**Endpoints:**
```
GET /api/v4/forecast/zones         → 30-day summary all zones
GET /api/v4/forecast/zone/{name}   → Detailed zone forecast
GET /api/v4/forecast/peaks         → High-load days alert
GET /api/v4/health                 → Health check
```

---

### Module 5 — Recycling Marketplace
**Port:** `8005`

B2B digital auction marketplace connecting waste collectors with recyclers and manufacturers.

**Capabilities:**
- 3 user roles: Collector, Recycler, Manufacturer
- Real-time bidding — bid must exceed base price
- Automated settlement when bid accepted
- Price discovery per material type
- Transaction ledger with full audit trail

**Material Price Ranges (PKR/kg):**
```
Plastic:   15–45
Organic:    5–20
Metal:     80–200
Glass:     10–35
Hazardous: 50–150
```

**Endpoints:**
```
POST /api/v5/listings/create          → Post material for sale
GET  /api/v5/listings                 → Browse active listings
GET  /api/v5/listings/price-guide     → Market price reference
POST /api/v5/bids/place               → Place bid on listing
POST /api/v5/bids/accept              → Accept best bid, close deal
GET  /api/v5/transactions             → Transaction history
```

---

### Module 6 — Government Analytics Dashboard
**Port:** `3000`

Unified React dashboard aggregating all 5 modules with PDF export.

**Tabs:**
- 📊 **Overview** — 8 KPIs, weekly collection chart, citizen leaderboard
- 🗺️ **Waste Map** — Lahore map with real-time colored bin markers
- 📈 **Forecasts** — 30-day zone predictions from Module 4
- 🏪 **Marketplace** — listing and transaction data from Module 5
- 🌍 **Carbon** — CO₂ avoided by material type, trees equivalent
- 📄 **Reports** — one-click PDF export with all KPIs

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| AI Model | YOLO26n (Ultralytics 8.4.41) | Waste object detection |
| Forecasting | Facebook Prophet | Time-series prediction |
| Routing | Google OR-Tools | VRP optimization |
| Backend | FastAPI + Uvicorn | REST APIs (6 services) |
| Database | PostgreSQL 15 | Persistent storage |
| Cache | Redis 7 | Real-time bin state |
| ORM | SQLAlchemy | Database models |
| Frontend | React 18 | Dashboard + PWA |
| Maps | Leaflet.js + OpenStreetMap | Bin location maps |
| Charts | Recharts | Analytics visualization |
| PDF | jsPDF + html2canvas | Report export |
| Containers | Docker + Docker Compose | Infrastructure |
| Training | Google Colab T4 GPU | Model training |
| Dataset | Roboflow Universe | Labeled waste images |

---

## 📁 Project Structure

```
SWOS/
├── module1_detection/
│   ├── api/
│   │   ├── main.py              # FastAPI server entry point
│   │   ├── inference.py         # YOLO26 model loading + prediction
│   │   └── routes/
│   │       └── detection.py     # /detect endpoint
│   ├── data/
│   │   ├── waste_dataset_v3/    # Final merged training dataset
│   │   ├── roboflow_hazardous/  # Hazardous class data
│   │   └── v3_raw/              # Raw downloaded datasets
│   ├── models/
│   │   ├── swos_v2_best.pt      # V2 model (0.567 mAP50)
│   │   └── swos_v3_best.pt      # V3 model (0.745 mAP50) ← current
│   ├── scripts/
│   │   ├── remap_categories.py  # TACO 60 classes → 5 classes
│   │   ├── merge_hazardous.py   # Add hazardous data
│   │   ├── merge_extra.py       # Add extra class data
│   │   └── build_v3_dataset.py  # Build final v3 dataset
│   ├── notebooks/
│   │   └── 01_explore_taco.ipynb
│   └── dashboard/               # React detection dashboard
│
├── module2_segregation/
│   ├── api/
│   │   ├── main.py
│   │   └── routes/
│   │       ├── disposal.py      # Submit disposal + points logic
│   │       ├── rewards.py       # User rewards + history
│   │       ├── leaderboard.py   # City rankings
│   │       └── badges.py        # Badge definitions + seeding
│   └── citizen-app/             # React PWA for citizens
│       └── src/
│           ├── pages/
│           │   ├── Home.js
│           │   ├── Scan.js
│           │   ├── Result.js
│           │   ├── Rewards.js
│           │   └── Leaderboard.js
│           └── services/
│               └── api.js       # All API calls centralized
│
├── module3_routing/
│   ├── api/
│   │   ├── main.py
│   │   └── routes/
│   │       └── routing.py       # VRP optimize endpoints
│   └── vrp_solver/
│       └── solver.py            # OR-Tools VRP implementation
│
├── module4_prediction/
│   ├── api/
│   │   ├── main.py
│   │   └── routes/
│   │       └── prediction.py    # Forecast endpoints
│   ├── data/
│   │   ├── waste_history.csv    # 2 years synthetic data
│   │   └── forecasts.csv        # Pre-computed forecasts
│   ├── models/
│   │   └── prophet_models.pkl   # Trained Prophet models (8 zones)
│   ├── data_pipeline/
│   │   └── generate_data.py     # Synthetic data generator
│   └── notebooks/
│       └── 01_train_prophet.ipynb
│
├── module5_marketplace/
│   └── api/
│       ├── main.py
│       └── routes/
│           ├── listings.py      # Create + browse listings
│           └── bids.py          # Place + accept bids
│
├── module6_dashboard/
│   └── government-dashboard/    # React gov dashboard
│       └── src/
│           ├── App.js
│           └── components/
│               ├── Overview.js
│               ├── WasteMap.js
│               ├── Forecasts.js
│               ├── Marketplace.js
│               ├── CarbonTracker.js
│               └── ReportExport.js
│
├── shared/
│   └── db/
│       ├── models.py            # All SQLAlchemy table definitions
│       └── session.py           # DB connection pool + init_db()
│
├── docker-compose.yml           # PostgreSQL + Redis
├── start_swos.bat               # One-click start all services
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites
```
- Windows 10/11
- Anaconda (Python 3.10)
- Docker Desktop
- Node.js 18+
- Git
```

### Step 1 — Clone and setup environment
```bash
git clone https://github.com/yourname/swos.git
cd SWOS

conda create -n swos python=3.10 -y
conda activate swos
pip install -r module1_detection/requirements.txt
pip install ortools prophet
```

### Step 2 — Start infrastructure
```bash
docker compose up -d
```

Verify containers:
```bash
docker exec -it swos-postgres-1 psql -U swos -d swos -c "\dt"
```

### Step 3 — Initialize database
```bash
python -c "from shared.db.session import init_db; init_db(); print('✅ DB ready')"
```

### Step 4 — Install frontend dependencies
```bash
cd module2_segregation/citizen-app && npm install
cd module6_dashboard/government-dashboard && npm install
```

### Step 5 — Download trained model
Place `swos_v3_best.pt` in:
```
C:\SWOS\module1_detection\models\swos_v3_best.pt
```

---

## 🚀 Running the System

### One Command Start (Recommended)
```bash
cd C:\SWOS
start_swos.bat
```

### Manual Start (one terminal each)
```bash
# Terminal 1 — Module 1 Detection API
conda activate swos && cd module1_detection
uvicorn api.main:app --port 8001 --host 0.0.0.0

# Terminal 2 — Module 2 Rewards API
conda activate swos && cd C:\SWOS
uvicorn module2_segregation.api.main:app --port 8002 --host 0.0.0.0

# Terminal 3 — Module 3 Routing API
conda activate swos && cd module3_routing
uvicorn api.main:app --port 8003 --host 0.0.0.0

# Terminal 4 — Module 4 Prediction API
conda activate swos && cd module4_prediction
uvicorn api.main:app --port 8004 --host 0.0.0.0

# Terminal 5 — Module 5 Marketplace API
conda activate swos && cd module5_marketplace
uvicorn api.main:app --port 8005 --host 0.0.0.0

# Terminal 6 — Module 6 Government Dashboard
cd module6_dashboard/government-dashboard && npm start
```

### Service URLs
```
Module 1 API docs:    http://127.0.0.1:8001/docs
Module 2 API docs:    http://127.0.0.1:8002/docs
Module 3 API docs:    http://127.0.0.1:8003/docs
Module 4 API docs:    http://127.0.0.1:8004/docs
Module 5 API docs:    http://127.0.0.1:8005/docs
Gov Dashboard:        http://localhost:3000
Citizen App:          http://localhost:3001
```

---

## 📡 API Reference

### Quick Test — Detect Waste
```bash
curl -X POST http://127.0.0.1:8001/api/v1/detect \
  -F "file=@waste_image.jpg" \
  -F "conf=0.25"
```

**Response:**
```json
{
  "detections": [
    {
      "class_name": "plastic",
      "confidence": 0.8741,
      "bbox": {"x1": 186, "y1": 489, "x2": 275, "y2": 594},
      "color": "#3B82F6"
    }
  ],
  "total_objects": 5,
  "dominant_type": "plastic",
  "is_hazardous": false,
  "class_counts": {"plastic": 5, "organic": 0, "metal": 0, "glass": 0, "hazardous": 0},
  "inference_ms": 45.2,
  "annotated_image": "base64_string..."
}
```

### Quick Test — Submit Disposal
```bash
curl -X POST http://127.0.0.1:8002/api/v2/disposal/submit \
  -H "Content-Type: application/json" \
  -d '{"user_phone": "03001234567", "waste_type": "plastic", "was_correct": true, "bin_id": "BIN-001"}'
```

### Quick Test — Optimize Route
```bash
curl -X POST http://127.0.0.1:8003/api/v3/route/optimize/demo
```

### Quick Test — Get Forecast
```bash
curl http://127.0.0.1:8004/api/v4/forecast/zones
```

### Quick Test — Create Listing
```bash
curl -X POST http://127.0.0.1:8005/api/v5/listings/create \
  -H "Content-Type: application/json" \
  -d '{"seller_phone": "03001234567", "waste_type": "plastic", "quantity_kg": 400, "base_price": 25, "title": "400kg PET bottles"}'
```

---

## 🤖 Model Performance

### YOLO26n Training History

| Version | Dataset Size | mAP50 | Epochs | Notes |
|---------|-------------|-------|--------|-------|
| V1 | 3,534 images | 0.217 | 100 | TACO only |
| V2 | 12,450 images | 0.567 | 40 | Extra data added |
| V3 | 29,235 images | **0.745** | 71 | Clean dataset, plateau |

### V3 Per-Class Results
```
Class       mAP50    Status
─────────────────────────────
plastic     ~0.65    ✅ Good
organic     ~0.65    ✅ Good (was 0.011 in v2!)
metal       ~0.70    ✅ Good
glass       ~0.75    ✅ Very Good
hazardous   ~0.93    ✅ Excellent
─────────────────────────────
OVERALL     0.745    ✅ Production Ready
```

### V3 Dataset Composition
```
Dataset              Images    Class
─────────────────────────────────────
Organic Waste        7,125     organic
Plastic Waste 1      4,590     plastic
Plastic Waste 2      2,180     plastic
Garbage Clf         10,464     all classes
Metal (Tin Can)      1,840     metal
Glass (Bottle)         353     glass
Hazardous (Capy)       580     hazardous
Hazardous (Myst)       300     hazardous
TACO                 1,803     mixed
─────────────────────────────────────
TOTAL               29,235
```

### Training Configuration
```python
model    = YOLO('yolo26n.pt')   # pretrained on COCO
epochs   = 150                   # early stopped at 71
imgsz    = 640
batch    = 32
device   = 0                     # Tesla T4 GPU (16GB)
optimizer= MuSGD                 # YOLO26's new optimizer
patience = 30                    # early stopping
```

---

## 🗄️ Database Schema

```
zones              → city zones (Gulberg, DHA, etc.)
bins               → bin locations + metadata
bin_telemetry      → fill level readings (high volume)
users              → citizens + drivers + collectors
disposal_events    → citizen disposal logs
collection_routes  → truck route records
alerts             → bin full / hazardous alerts
waste_predictions  → Prophet forecast results
marketplace_listings  → material for sale
marketplace_bids      → auction bids
marketplace_transactions → completed deals
badges             → badge definitions
user_badges        → earned badges per user
disposal_logs      → detailed scan history
```

---

## 💡 Challenges & Solutions

| Challenge | Root Cause | Solution |
|-----------|-----------|---------|
| Organic class 0.011 mAP | Dataset had cardboard/paper not food waste | Found dhafar-sami/organic-waste (8076 real food images) |
| Hazardous class 2 samples | TACO had almost no hazardous data | Downloaded capy + mysterious (880 samples) |
| GPU training failed on Windows | CUDA driver conflicts | Used Google Colab T4 (free 16GB VRAM) |
| Colab disconnects mid-training | 4-6 hour session limit | Checkpoint watcher saves every epoch to Drive |
| CORS errors React → FastAPI | Browser security policy | Added CORSMiddleware allow_origins=["*"] |
| PostgreSQL connection refused | Docker not running | Added Docker startup check to start_swos.bat |
| bin_id NOT NULL violation | DisposalEvent required bin_id | ALTER TABLE DROP NOT NULL constraint |
| Model slow on first request | Loading model per request | Global _model singleton — load once |

---

## 📊 Impact Metrics

```
🗑️  Bins Monitored:        128
♻️  Recycling Rate:         34.2%
🚛  Active Trucks:          12
💰  Marketplace Revenue:    PKR 136,000+ per transaction
🌍  CO₂ Avoided:            18 tons
🌳  Trees Equivalent:       810
⛽  Fuel Saved:             8.4L vs fixed routes
👥  Citizen Engagement:     Points + 5 badge tiers
📈  Prediction Accuracy:    8 zones, 550-day forecast
```

---

## 🗺️ Roadmap

- [ ] v4 model training with 50k+ images per class
- [ ] Real IoT hardware integration (Raspberry Pi + ultrasonic sensors)
- [ ] React Native mobile app (iOS + Android)
- [ ] Kafka streaming for high-frequency telemetry
- [ ] AWS/GCP deployment
- [ ] Multi-city support
- [ ] Carbon credit trading integration
- [ ] WhatsApp bot for citizen notifications

---

## 👨‍💻 Built With

This project was built entirely from scratch including:
- Custom AI dataset collection and labeling pipeline
- YOLO26 fine-tuning on waste domain
- 6 independent microservices
- 4 React applications
- Complete PostgreSQL schema design
- OR-Tools VRP routing implementation
- Prophet time-series forecasting
- Full auction marketplace system

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built for Lahore Municipal Corporation — Smart City Initiative 2026*
