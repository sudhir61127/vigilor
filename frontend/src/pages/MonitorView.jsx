import { useEffect, useRef } from 'react';

export default function MonitorView({ vitals, fetchVitals }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (canvasRef.current && vitals?.ecg?.waveform) {
      drawECG(canvasRef.current, vitals.ecg.waveform);
    }
  }, [vitals]);

  const drawECG = (canvas, waveformData) => {
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    // Clear canvas
    ctx.fillStyle = 'rgba(10, 14, 39, 0.5)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw grid
    ctx.strokeStyle = 'rgba(0, 217, 255, 0.1)';
    ctx.lineWidth = 0.5;
    const gridSize = 20;
    for (let x = 0; x < canvas.width; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvas.height);
      ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(canvas.width, y);
      ctx.stroke();
    }

    // Draw waveform
    if (waveformData && waveformData.length > 0) {
      ctx.strokeStyle = '#00d9ff';
      ctx.lineWidth = 2;
      ctx.beginPath();

      const minVoltage = Math.min(...waveformData.map((d) => d.voltage));
      const maxVoltage = Math.max(...waveformData.map((d) => d.voltage));
      const voltageRange = maxVoltage - minVoltage || 1;

      waveformData.forEach((point, index) => {
        const x = (index / waveformData.length) * canvas.width;
        const normalizedVoltage = (point.voltage - minVoltage) / voltageRange;
        const y = canvas.height - normalizedVoltage * canvas.height * 0.8 - canvas.height * 0.1;

        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });

      ctx.stroke();

      // Draw glow effect
      ctx.shadowColor = 'rgba(0, 217, 255, 0.5)';
      ctx.shadowBlur = 10;
      ctx.stroke();
      ctx.shadowBlur = 0;
    }
  };

  if (!vitals) {
    return (
      <div className="card">
        <h2>❤️ Live Monitor</h2>
        <p>Loading vitals...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="card">
        <h2>❤️ Live Vital Signs Monitor</h2>
        <div className="vitals-grid">
          {vitals.vitals && Object.entries(vitals.vitals).map(([key, vital]) => (
            <div key={key} className="vital-item">
              <div className="vital-label">{key.replace(/_/g, ' ')}</div>
              <div className="vital-value">
                {vital.value}
                <span className="vital-unit">{vital.unit}</span>
              </div>
              <div className={`vital-status ${vital.status}`}>{vital.status}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h2>🔴 ECG Waveform</h2>
        <div className="ecg-container">
          <canvas ref={canvasRef} className="ecg-waveform"></canvas>
        </div>
      </div>

      <div className="card">
        <button className="button primary" onClick={fetchVitals} style={{ width: '100%' }}>
          🔄 Refresh Vitals
        </button>
        <small style={{ marginTop: '15px', display: 'block', color: 'var(--text-secondary)' }}>
          {vitals.note}
        </small>
      </div>
    </div>
  );
}
