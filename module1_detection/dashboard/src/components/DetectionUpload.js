import React, { useState } from 'react';
import axios from 'axios';

export default function DetectionUpload() {
  const [result,   setResult]   = useState(null);
  const [loading,  setLoading]  = useState(false);
  const [preview,  setPreview]  = useState(null);

  const handleFile = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setPreview(URL.createObjectURL(file));
    setLoading(true);

    const form = new FormData();
    form.append('file', file);

    try {
      const res = await axios.post(
        'http://127.0.0.1:8001/api/v1/detect?conf=0.25', form
      );
      setResult(res.data);
    } catch (err) {
      alert('API error — make sure the FastAPI server is running on port 8001');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3>Live Waste Detection — Upload Image</h3>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>

        <div>
          <input type="file" accept="image/*" onChange={handleFile}
            style={{ marginBottom: 12 }} />
          {preview && (
            <img src={preview} alt="preview"
              style={{ width: '100%', borderRadius: 8, maxHeight: 250, objectFit: 'cover' }} />
          )}
        </div>

        <div>
          {loading && <p style={{ color: '#38bdf8' }}>⏳ Detecting...</p>}
          {result && (
            <div>
              <p style={{ color: '#22c55e', marginBottom: 8 }}>
                ✅ {result.total_objects} objects detected
              </p>
              {result.is_hazardous && (
                <div style={{ background: '#7f1d1d', padding: '8px 12px',
                  borderRadius: 8, marginBottom: 8, color: '#fca5a5' }}>
                  ⚠️ HAZARDOUS WASTE DETECTED
                </div>
              )}
              <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginBottom: 8 }}>
                Dominant: <strong style={{ color: '#38bdf8' }}>{result.dominant_type}</strong>
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                {Object.entries(result.class_counts).map(([cls, cnt]) =>
                  cnt > 0 && (
                    <div key={cls} style={{ fontSize: '0.85rem',
                      display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: '#e2e8f0' }}>{cls}</span>
                      <span style={{ color: '#38bdf8', fontWeight: 600 }}>{cnt}</span>
                    </div>
                  )
                )}
              </div>
              {result.annotated_image && (
                <img
                  src={`data:image/jpeg;base64,${result.annotated_image}`}
                  alt="annotated"
                  style={{ width: '100%', borderRadius: 8, marginTop: 12 }}
                />
              )}
            </div>
          )}
        </div>

      </div>
    </div>
  );
}