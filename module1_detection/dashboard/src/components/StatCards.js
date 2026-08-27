import React from 'react';

export default function StatCards({ stats }) {
  const cards = [
    { label: 'Total Bins',      value: stats.total_bins,     icon: '🗑️', color: '#38bdf8' },
    { label: 'Full Bins',       value: stats.full_bins,      icon: '⚠️', color: '#f59e0b' },
    { label: 'Hazardous',       value: stats.hazardous_bins, icon: '☣️', color: '#ef4444' },
    { label: 'Collection Rate', value: `${stats.collection_rate}%`, icon: '✅', color: '#22c55e' },
  ];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '1rem' }}>
      {cards.map(c => (
        <div key={c.label} className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2rem' }}>{c.icon}</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: c.color }}>{c.value}</div>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: 4 }}>{c.label}</div>
        </div>
      ))}
    </div>
  );
}