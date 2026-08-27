import React, { useEffect, useState } from 'react';
import { getRewards } from '../services/api';

const BADGE_ICONS = {
  starter  : '♻️',
  recycler : '🌱',
  champion : '🏆',
  hero     : '🌍',
  legend   : '⭐',
};

export default function Rewards() {
  const [data,    setData]    = useState(null);
  const [loading, setLoading] = useState(true);
  const phone = localStorage.getItem('swos_phone') || '03001234567';

  useEffect(() => {
    getRewards(phone)
      .then(setData)
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [phone]);

  if (loading) return <div style={{ padding: '2rem', color: '#94a3b8' }}>Loading...</div>;

  if (!data) return (
    <div style={{ padding: '2rem', color: '#94a3b8' }}>
      No rewards yet — scan some waste first! 🗑️
    </div>
  );

  return (
    <div style={{ padding: '1.5rem', maxWidth: 480,
      margin: '0 auto', paddingBottom: 80 }}>
      <h2 style={{ marginBottom: '1rem' }}>🏆 Your Rewards</h2>

      {/* Points card */}
      <div style={{ background: 'linear-gradient(135deg,#2563eb,#7c3aed)',
        borderRadius: 16, padding: '1.5rem', marginBottom: '1.5rem' }}>
        <div style={{ color: '#bfdbfe', fontSize: '0.85rem' }}>Total Points</div>
        <div style={{ fontSize: '3rem', fontWeight: 800, color: '#fff' }}>
          {data.user.total_points.toLocaleString()}
        </div>
        <div style={{ color: '#bfdbfe', fontSize: '0.85rem', marginTop: 4 }}>
          Accuracy: {data.user.accuracy}% · {data.user.total_disposals} disposals
        </div>
      </div>

      {/* Badges */}
      <h3 style={{ marginBottom: '0.75rem', color: '#94a3b8',
        fontSize: '0.85rem', textTransform: 'uppercase' }}>
        Badges Earned
      </h3>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr',
        gap: 10, marginBottom: '1.5rem' }}>
        {data.badges.length === 0 && (
          <div style={{ color: '#64748b', gridColumn: 'span 2' }}>
            No badges yet — keep scanning!
          </div>
        )}
        {data.badges.map(b => (
          <div key={b.id} style={{ background: '#1e293b',
            borderRadius: 12, padding: '1rem', textAlign: 'center' }}>
            <div style={{ fontSize: '2rem' }}>{b.icon}</div>
            <div style={{ fontWeight: 600, marginTop: 4 }}>{b.name}</div>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
              {b.desc}
            </div>
          </div>
        ))}
      </div>

      {/* History */}
      <h3 style={{ marginBottom: '0.75rem', color: '#94a3b8',
        fontSize: '0.85rem', textTransform: 'uppercase' }}>
        Recent Activity
      </h3>
      {data.history.map((h, i) => (
        <div key={i} style={{ display: 'flex', justifyContent: 'space-between',
          alignItems: 'center', padding: '10px 0',
          borderBottom: '1px solid #1e293b' }}>
          <div>
            <span style={{ fontWeight: 600 }}>{h.waste_type}</span>
            <span style={{ marginLeft: 8, fontSize: '0.8rem',
              color: h.was_correct ? '#22c55e' : '#ef4444' }}>
              {h.was_correct ? '✅ Correct' : '❌ Wrong bin'}
            </span>
          </div>
          <span style={{ color: '#22c55e', fontWeight: 700 }}>
            +{h.points}
          </span>
        </div>
      ))}
    </div>
  );
}