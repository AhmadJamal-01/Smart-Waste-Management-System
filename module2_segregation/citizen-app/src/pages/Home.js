import { useNavigate } from 'react-router-dom';

export default function Home() {
  const nav = useNavigate();
  // Mock user — will connect to API later
  const user = { name: 'Ahmed', points: 1240, zone: 'Zone A - Lahore' };

  return (
    <div style={{ padding: '48px 20px 100px' }}>
      {/* Header */}
      <div style={{ marginBottom: 28 }}>
        <p style={{ color: '#94A3B8', fontSize: 13 }}>Welcome back 👋</p>
        <h1 style={{ fontSize: 26, fontWeight: 800 }}>{user.name}</h1>
        <p style={{ color: '#94A3B8', fontSize: 13, marginTop: 4 }}>{user.zone}</p>
      </div>

      {/* Points card */}
      <div style={{
        background: 'linear-gradient(135deg, #1D4ED8, #7C3AED)',
        borderRadius: 20, padding: '24px 24px',
        marginBottom: 24,
      }}>
        <p style={{ fontSize: 13, opacity: 0.8 }}>Your Points</p>
        <p style={{ fontSize: 48, fontWeight: 800 }}>{user.points.toLocaleString()}</p>
        <p style={{ fontSize: 13, opacity: 0.8 }}>♻️ Keep recycling to earn more!</p>
      </div>

      {/* Quick actions */}
      <h2 style={{ fontSize: 16, fontWeight: 700, marginBottom: 14 }}>Quick Actions</h2>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 24 }}>
        {[
          { icon: '📷', label: 'Scan Waste',    color: '#3B82F6', path: '/scan'        },
          { icon: '🏆', label: 'Leaderboard',   color: '#EAB308', path: '/leaderboard' },
          { icon: '⭐', label: 'My Rewards',    color: '#22C55E', path: '/rewards'     },
          { icon: '📊', label: 'My History',    color: '#8B5CF6', path: '/rewards'     },
        ].map(a => (
          <button key={a.label} onClick={() => nav(a.path)} style={{
            background: '#1E293B', border: '1px solid #334155',
            borderRadius: 16, padding: '20px 16px',
            display: 'flex', flexDirection: 'column', gap: 8,
            alignItems: 'flex-start', color: '#F1F5F9',
          }}>
            <span style={{
              fontSize: 28, background: a.color + '22',
              borderRadius: 10, padding: '6px 8px',
            }}>{a.icon}</span>
            <span style={{ fontSize: 13, fontWeight: 600 }}>{a.label}</span>
          </button>
        ))}
      </div>

      {/* Waste guide */}
      <h2 style={{ fontSize: 16, fontWeight: 700, marginBottom: 14 }}>Bin Guide</h2>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        {[
          { color: '#3B82F6', name: 'Blue Bin',   types: 'Plastic, Paper, Cardboard'    },
          { color: '#22C55E', name: 'Green Bin',  types: 'Food, Organic, Garden waste'  },
          { color: '#EAB308', name: 'Yellow Bin', types: 'Metal, Tin cans, Foil'        },
          { color: '#8B5CF6', name: 'Purple Bin', types: 'Glass bottles & jars'         },
          { color: '#EF4444', name: 'Red Bin',    types: 'Hazardous, Batteries, Chemicals'},
        ].map(b => (
          <div key={b.name} style={{
            background: '#1E293B', border: `1px solid ${b.color}44`,
            borderLeft: `4px solid ${b.color}`,
            borderRadius: 12, padding: '12px 16px',
            display: 'flex', alignItems: 'center', gap: 14,
          }}>
            <div style={{
              width: 36, height: 36, borderRadius: 10,
              background: b.color, display: 'flex',
              alignItems: 'center', justifyContent: 'center',
              fontSize: 18, flexShrink: 0,
            }}>🗑️</div>
            <div>
              <p style={{ fontWeight: 700, fontSize: 14 }}>{b.name}</p>
              <p style={{ color: '#94A3B8', fontSize: 12 }}>{b.types}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}