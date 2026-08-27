import React, { useEffect, useState } from 'react';
import { getLeaderboard } from '../services/api';

const MEDALS = ['🥇', '🥈', '🥉'];

export default function Leaderboard() {
  const [data,    setData]    = useState([]);
  const [loading, setLoading] = useState(true);
  const phone = localStorage.getItem('swos_phone') || '03001234567';

  useEffect(() => {
    getLeaderboard()
      .then(res => setData(res.leaderboard || []))
      .catch(() => setData([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div style={{ padding: '2rem', color: '#94a3b8' }}>Loading...</div>
  );

  return (
    <div style={{ padding: '1.5rem', maxWidth: 480,
      margin: '0 auto', paddingBottom: 80 }}>
      <h2 style={{ marginBottom: '1.5rem' }}>🏆 Leaderboard</h2>

      {data.length === 0 && (
        <div style={{ color: '#64748b', textAlign: 'center',
          padding: '3rem' }}>
          No users yet — be the first to scan! 🌱
        </div>
      )}

      {data.map((u, i) => (
        <div key={i} style={{
          display        : 'flex',
          alignItems     : 'center',
          gap            : 12,
          padding        : '12px 16px',
          background     : i < 3 ? '#1e293b' : 'transparent',
          borderRadius   : 12,
          marginBottom   : 8,
          border         : i === 0 ? '1px solid #f59e0b' : '1px solid transparent',
        }}>
          <div style={{ fontSize: '1.5rem', minWidth: 36 }}>
            {MEDALS[i] || `#${u.rank}`}
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontWeight: 600 }}>{u.name}</div>
            <div style={{ fontSize: '0.8rem', color: '#64748b' }}>
              {u.badge} · {u.zone}
            </div>
          </div>
          <div style={{ fontWeight: 700, color: '#38bdf8',
            fontSize: '1.1rem' }}>
            {u.points.toLocaleString()}
          </div>
        </div>
      ))}
    </div>
  );
}