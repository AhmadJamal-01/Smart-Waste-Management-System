import React from 'react';

const severityColor = s => s === 'high' ? '#ef4444' : '#f59e0b';

export default function AlertPanel({ alerts }) {
  return (
    <div className="card">
      <h3>Live Alerts</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        {alerts.map(a => (
          <div key={a.id} style={{
            padding: '10px 12px',
            borderRadius: 8,
            borderLeft: `3px solid ${severityColor(a.severity)}`,
            background: '#0f172a',
          }}>
            <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>{a.message}</div>
            <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: 4 }}>
              {a.bin_id} · {a.zone} · {a.time}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}