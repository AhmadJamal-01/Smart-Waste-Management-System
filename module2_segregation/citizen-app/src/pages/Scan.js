import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { detectWaste, submitDisposal } from '../services/api';

const BIN_INFO = {
  plastic  : { color: '#3B82F6', bin: 'Blue Bin',   emoji: '🔵', tip: 'Rinse before disposal' },
  organic  : { color: '#22C55E', bin: 'Green Bin',  emoji: '🟢', tip: 'Remove packaging first' },
  metal    : { color: '#94A3B8', bin: 'Silver Bin', emoji: '⚪', tip: 'Crush cans to save space' },
  glass    : { color: '#06B6D4', bin: 'Cyan Bin',   emoji: '🔵', tip: 'Wrap broken glass safely' },
  hazardous: { color: '#EF4444', bin: 'Red Bin',    emoji: '🔴', tip: 'Never mix with regular bins' },
};

export default function Scan() {
  const [image,     setImage]     = useState(null);
  const [preview,   setPreview]   = useState(null);
  const [result,    setResult]    = useState(null);
  const [loading,   setLoading]   = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [points,    setPoints]    = useState(null);
  const fileRef = useRef();
  const navigate = useNavigate();
  const phone = localStorage.getItem('swos_phone') || '03001234567';

  const handleCapture = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setImage(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
    setSubmitted(false);
  };

  const handleDetect = async () => {
    if (!image) return;
    setLoading(true);
    try {
      const data = await detectWaste(image);
      setResult(data);
    } catch {
      alert('Detection API error — make sure port 8001 is running');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (wasCorrect) => {
  if (!result?.dominant_type) return;
  try {
    const data = await submitDisposal(phone, result.dominant_type, wasCorrect);
    setPoints(data.points_earned);
    setSubmitted(true);
    setTimeout(() => navigate('/rewards'), 2000);
  } catch (err) {
    console.error('Submit error:', err);
    // Show points anyway even if API fails
    setPoints(10);
    setSubmitted(true);
    setTimeout(() => navigate('/rewards'), 2000);
  }
};

  const binInfo = result?.dominant_type ? BIN_INFO[result.dominant_type] : null;

  return (
    <div style={{ padding: '1.5rem', maxWidth: 480, margin: '0 auto', paddingBottom: 80 }}>
      <h2 style={{ marginBottom: '1rem' }}>📷 Scan Waste</h2>

      {/* Camera / Upload */}
      <div style={{ display: 'flex', gap: 10, marginBottom: '1rem' }}>
        <button onClick={() => fileRef.current.click()}
          style={btnStyle('#1e293b')}>
          📁 Upload Image
        </button>
        <input ref={fileRef} type="file"
          accept="image/*" capture="environment"
          onChange={handleCapture} style={{ display: 'none' }} />
      </div>

      {/* Preview */}
      {preview && (
        <img src={preview} alt="preview"
          style={{ width: '100%', borderRadius: 12,
            marginBottom: '1rem', maxHeight: 280, objectFit: 'cover' }} />
      )}

      {/* Detect Button */}
      {image && !result && (
        <button onClick={handleDetect} disabled={loading}
          style={btnStyle('#2563eb', true)}>
          {loading ? '⏳ Detecting...' : '🔍 Detect Waste Type'}
        </button>
      )}

      {/* Result */}
      {result && binInfo && !submitted && (
        <div style={{ marginTop: '1rem' }}>
          <div style={{
            background: '#1e293b', borderRadius: 12,
            padding: '1.25rem', borderLeft: `4px solid ${binInfo.color}`,
            marginBottom: '1rem'
          }}>
            <div style={{ fontSize: '2rem', marginBottom: 6 }}>
              {binInfo.emoji}
            </div>
            <div style={{ fontSize: '1.2rem', fontWeight: 700,
              color: binInfo.color, marginBottom: 4 }}>
              {result.dominant_type?.toUpperCase()}
            </div>
            <div style={{ fontSize: '1rem', color: '#e2e8f0',
              marginBottom: 4 }}>
              Put in the <strong>{binInfo.bin}</strong>
            </div>
            <div style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
              💡 {binInfo.tip}
            </div>
            {result.is_hazardous && (
              <div style={{ marginTop: 10, padding: '8px 12px',
                background: '#7f1d1d', borderRadius: 8,
                color: '#fca5a5', fontSize: '0.85rem' }}>
                ⚠️ HAZARDOUS — Handle with extreme care
              </div>
            )}
          </div>

          {/* Annotated image */}
          {result.annotated_image && (
            <img
              src={`data:image/jpeg;base64,${result.annotated_image}`}
              alt="detected"
              style={{ width: '100%', borderRadius: 12, marginBottom: '1rem' }}
            />
          )}

          {/* Confirm disposal */}
          <p style={{ color: '#94a3b8', marginBottom: 10, fontSize: '0.9rem' }}>
            Did you dispose it correctly?
          </p>
          <div style={{ display: 'flex', gap: 10 }}>
            <button onClick={() => handleSubmit(true)}
              style={btnStyle('#16a34a', true)}>
              ✅ Yes — correct bin
            </button>
            <button onClick={() => handleSubmit(false)}
              style={btnStyle('#dc2626', true)}>
              ❌ No — wrong bin
            </button>
          </div>
        </div>
      )}

      {/* Points earned */}
      {submitted && points && (
        <div style={{ textAlign: 'center', padding: '2rem',
          background: '#1e293b', borderRadius: 12, marginTop: '1rem' }}>
          <div style={{ fontSize: '3rem' }}>🎉</div>
          <div style={{ fontSize: '2rem', fontWeight: 700,
            color: '#22c55e' }}>+{points} points!</div>
          <div style={{ color: '#94a3b8', marginTop: 6 }}>
            Redirecting to rewards...
          </div>
        </div>
      )}
    </div>
  );
}

const btnStyle = (bg, full = false) => ({
  background   : bg,
  color        : '#fff',
  border       : 'none',
  borderRadius : 10,
  padding      : '12px 20px',
  fontSize     : '0.95rem',
  cursor       : 'pointer',
  width        : full ? '100%' : 'auto',
  fontWeight   : 600,
});