import { NavLink } from 'react-router-dom';

const tabs = [
  { to: '/',            icon: '🏠', label: 'Home'   },
  { to: '/scan',        icon: '📷', label: 'Scan'   },
  { to: '/rewards',     icon: '⭐', label: 'Rewards' },
  { to: '/leaderboard', icon: '🏆', label: 'Ranks'  },
];

export default function NavBar() {
  return (
    <nav style={{
      position: 'fixed', bottom: 0, left: '50%', transform: 'translateX(-50%)',
      width: '100%', maxWidth: 430,
      background: '#1E293B', borderTop: '1px solid #334155',
      display: 'flex', padding: '8px 0 12px',
    }}>
      {tabs.map(t => (
        <NavLink key={t.to} to={t.to} style={({ isActive }) => ({
          flex: 1, display: 'flex', flexDirection: 'column',
          alignItems: 'center', gap: 2, textDecoration: 'none',
          color: isActive ? '#3B82F6' : '#64748B',
          fontSize: 11, fontWeight: 600,
        })}>
          <span style={{ fontSize: 22 }}>{t.icon}</span>
          {t.label}
        </NavLink>
      ))}
    </nav>
  );
}