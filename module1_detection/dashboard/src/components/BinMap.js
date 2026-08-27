import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import React from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';

delete L.Icon.Default.prototype._getIconUrl;

const fillColor = (fill, type) => {
  if (type === 'hazardous') return '#ef4444';
  if (fill >= 0.85) return '#f59e0b';
  if (fill >= 0.5)  return '#3b82f6';
  return '#22c55e';
};

export default function BinMap({ bins }) {
  return (
    <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
      <MapContainer
        center={[31.5204, 74.3587]}
        zoom={13}
        style={{ height: '420px', width: '100%', borderRadius: 12 }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="© OpenStreetMap"
        />
        {bins.map(bin => (
          <CircleMarker
            key={bin.id}
            center={[bin.lat, bin.lng]}
            radius={14}
            fillColor={fillColor(bin.fill, bin.type)}
            color="#0f172a"
            weight={2}
            fillOpacity={0.9}
          >
            <Popup>
              <strong>{bin.id}</strong><br />
              Zone: {bin.zone}<br />
              Type: {bin.type}<br />
              Fill: {Math.round(bin.fill * 100)}%
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}