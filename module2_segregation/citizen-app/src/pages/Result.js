import { useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import toast from 'react-hot-toast';

export default function Result() {
  const { state } = useLocation();
  const nav = useNavigate();
  const [submitted, setSubmitted] = useState(false);

  if (!state) { nav('/scan'); return null; }
  const { detected, info, image } = state;

  const submitDisposal = async () => {
    // Will connect to FastAPI rewards endpoint in Week 6
    await new Promise(r => setTimeout(r, 800));
    setSubmitted(true);
    toast.success(`+${info.points} points earned! 🎉`);
  };

  return (
    <div style={{ padding: '48px 20px 100px' }}>
      <h1 style={{ fontSize: 22, fontWeight: 800, marginBottom: 20 }}>
        🔍 Detection Result
      </h1>

      {/* Captured image */}
      {image && (
        <img src={image} alt="waste"
          style={{ width: '100%', borderRadius: 16, marginBottom: 20, maxHeight: 240, objectFit: 'cover' }}
        />
      )}

      {/* Result card */}
      <div style={{
        background: '#1E293B', border: `2px solid ${info.color}`,
        borderRadius: 20, padding: 24, marginBottom: 20,
        textAlign: 'center',
      }}>
        <div style={{ fontSize: 64, marginBottom: 12 }}>{info.icon}</div>
        <h2 style={{ fontSize: 28, fontWeight: 800, color: info.color, textTransform: 'capitalize' }}>
          {detected}
        </h2>
        <p style={{ color: '#94A3B8', marginTop: 4 }}>Waste type detected</p>

        <div style={{
          margin: '20px 0', padding: '16px', borderRadius: 14,
          background: info.color + '18', border: `1px solid ${info.color}44`,
        }}>
          <p style={{ fontSize: 13, color: '#94A3B8' }}>Dispose in</p>
          <p style={{ fontSize: 22, fontWeight: 800, color: info.color }}>{info.bin}</p>
        </div>

        <div style={{
          background: '#0F172A', borderRadius: 12, padding: '12px 20px',
          display: 'inline-block',
        }}>
          <p style={{ fontSize: 13, color: '#94A3B8' }}>You'll earn</p>
          <p style={{ fontSize: 24, fontWeight: 800, color: '#22C55E' }}>+{info.points} pts</p>
        </div>
      </div>

      {/* Instructions */}
      <div style={{
        background: '#1E293B', border: '1px solid #334155',
        borderRadius: 16, padding: 16, marginBottom: 20,
      }}>
        <p style={{ fontWeight: 700, marginBottom: 10 }}>📋 Disposal Instructions</p>
        {detected === 'hazardous' ? (
          <p style={{ fontSize: 13, color: '#EF4444' }}>
            ⚠️ Do NOT mix with regular waste. Take to the nearest hazardous waste collection point. Contact municipal services if unsure.
          </p>
        ) : (
          ['Remove any food residue before disposal',
           'Flatten boxes and containers if possible',
           'Check item is dry before placing in bin'].map(i => (
            <p key={i} style={{ fontSize: 13, color: '#94A3B8', marginBottom: 6 }}>✓ {i}</p>
          ))
        )}
      </div>

      {/* Buttons */}
      {!submitted ? (
        <button onClick={submitDisposal} style={{
          width: '100%', background: '#22C55E', color: '#fff',
          border: 'none', borderRadius: 16, padding: '16px',
          fontSize: 16, fontWeight: 700, marginBottom: 12,
        }}>
          ✅ I disposed it correctly
        </button>
      ) : (
        <div style={{
          background: '#14532D', border: '1px solid #22C55E',
          borderRadius: 16, padding: 16, textAlign: 'center', marginBottom: 12,
        }}>
          <p style={{ fontSize: 20 }}>🎉</p>
          <p style={{ fontWeight: 700, color: '#22C55E' }}>+{info.points} points added!</p>
        </div>
      )}

      <button onClick={() => nav('/scan')} style={{
        width: '100%', background: '#1E293B', color: '#94A3B8',
        border: '1px solid #334155', borderRadius: 16, padding: '14px',
        fontSize: 15, fontWeight: 600,
      }}>
        📷 Scan Another
      </button>
    </div>
  );
}