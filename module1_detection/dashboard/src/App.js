import React, { useState, useEffect } from 'react';
import BinMap from './components/BinMap';
import StatCards from './components/StatCards';
import AlertPanel from './components/AlertPanel';
import DetectionUpload from './components/DetectionUpload';
import './App.css';

function App() {
  const [bins, setBins]       = useState([]);
  const [alerts, setAlerts]   = useState([]);
  const [stats, setStats]     = useState({
    total_bins: 0,
    full_bins: 0,
    hazardous_bins: 0,
    collection_rate: 0,
  });

  // Simulate live bin data
  useEffect(() => {
    const mockBins = [
      { id: 'BIN-001', lat: 31.5204, lng: 74.3587, fill: 0.92, type: 'plastic',   zone: 'Gulberg III' },
      { id: 'BIN-002', lat: 31.5134, lng: 74.3290, fill: 0.45, type: 'organic',   zone: 'DHA Phase 1' },
      { id: 'BIN-003', lat: 31.5320, lng: 74.3450, fill: 0.78, type: 'metal',     zone: 'Model Town' },
      { id: 'BIN-004', lat: 31.5410, lng: 74.3600, fill: 0.21, type: 'glass',     zone: 'Johar Town' },
      { id: 'BIN-005', lat: 31.5250, lng: 74.3700, fill: 0.88, type: 'hazardous', zone: 'Gulberg III' },
      { id: 'BIN-006', lat: 31.5180, lng: 74.3400, fill: 0.60, type: 'plastic',   zone: 'Garden Town' },
      { id: 'BIN-007', lat: 31.5380, lng: 74.3520, fill: 0.15, type: 'organic',   zone: 'Bahria Town' },
      { id: 'BIN-008', lat: 31.5090, lng: 74.3650, fill: 0.95, type: 'hazardous', zone: 'DHA Phase 5' },
    ];
    setBins(mockBins);

    const full      = mockBins.filter(b => b.fill >= 0.85).length;
    const hazardous = mockBins.filter(b => b.type === 'hazardous').length;
    setStats({
      total_bins     : mockBins.length,
      full_bins      : full,
      hazardous_bins : hazardous,
      collection_rate: 78,
    });

    setAlerts([
      { id: 1, bin_id: 'BIN-008', type: 'hazardous', severity: 'high',
        message: '⚠️ Hazardous waste detected', zone: 'DHA Phase 5', time: '2 min ago' },
      { id: 2, bin_id: 'BIN-001', type: 'bin_full',  severity: 'medium',
        message: '🗑️ Bin nearly full (92%)',    zone: 'Gulberg III',  time: '5 min ago' },
      { id: 3, bin_id: 'BIN-005', type: 'hazardous', severity: 'high',
        message: '⚠️ Hazardous waste detected', zone: 'Gulberg III',  time: '8 min ago' },
    ]);

    // Simulate live updates every 5 seconds
    const interval = setInterval(() => {
      setBins(prev => prev.map(bin => ({
        ...bin,
        fill: Math.min(1, bin.fill + (Math.random() * 0.02 - 0.005)),
      })));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">
      <header className="header">
        <div className="header-left">
          <h1>🗑️ SWOS</h1>
          <span>Smart Waste Operating System</span>
        </div>
        <div className="header-right">
          <span className="live-badge">● LIVE</span>
          <span>Lahore, Pakistan</span>
        </div>
      </header>

      <div className="main">
        <StatCards stats={stats} />
        <div className="middle-row">
          <BinMap bins={bins} />
          <AlertPanel alerts={alerts} />
        </div>
        <DetectionUpload />
      </div>
    </div>
  );
}

export default App;