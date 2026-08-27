@echo off
echo ========================================
echo    SWOS - Smart Waste Operating System
echo    Starting all services...
echo ========================================

echo [1/7] Starting Docker...
docker compose up -d
timeout /t 5 /nobreak

echo [2/7] Starting Module 1 - Detection API (port 8001)...
start "Module1-Detection" cmd /k "conda activate swos && cd C:\SWOS\module1_detection && uvicorn api.main:app --port 8001 --host 0.0.0.0"
timeout /t 3 /nobreak

echo [3/7] Starting Module 2 - Rewards API (port 8002)...
start "Module2-Rewards" cmd /k "conda activate swos && cd C:\SWOS && uvicorn module2_segregation.api.main:app --port 8002 --host 0.0.0.0"
timeout /t 3 /nobreak

echo [4/7] Starting Module 3 - Routing API (port 8003)...
start "Module3-Routing" cmd /k "conda activate swos && cd C:\SWOS\module3_routing && uvicorn api.main:app --port 8003 --host 0.0.0.0"
timeout /t 3 /nobreak

echo [5/7] Starting Module 4 - Prediction API (port 8004)...
start "Module4-Prediction" cmd /k "conda activate swos && cd C:\SWOS\module4_prediction && uvicorn api.main:app --port 8004 --host 0.0.0.0"
timeout /t 3 /nobreak

echo [6/7] Starting Module 5 - Marketplace API (port 8005)...
start "Module5-Marketplace" cmd /k "conda activate swos && cd C:\SWOS\module5_marketplace && uvicorn api.main:app --port 8005 --host 0.0.0.0"
timeout /t 3 /nobreak

echo [7/7] Starting Module 6 - Government Dashboard (port 3000)...
start "Module6-Dashboard" cmd /k "cd C:\SWOS\module6_dashboard\government-dashboard && npm start"
timeout /t 3 /nobreak

echo ========================================
echo    All services started!
echo ========================================
echo    APIs:
echo    Module 1: http://127.0.0.1:8001/docs
echo    Module 2: http://127.0.0.1:8002/docs
echo    Module 3: http://127.0.0.1:8003/docs
echo    Module 4: http://127.0.0.1:8004/docs
echo    Module 5: http://127.0.0.1:8005/docs
echo    Dashboard: http://localhost:3000
echo ========================================
pause