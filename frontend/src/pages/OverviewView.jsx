export default function OverviewView({ vitals }) {
  return (
    <div>
      <div className="card">
        <h2>🏥 VIGIL-OR Status</h2>
        <p>Operating Room Management & Surgical Assistance System</p>
        
        <h3>System Status</h3>
        <div style={{ marginTop: '15px' }}>
          <div style={{ padding: '10px', background: 'rgba(0, 255, 65, 0.1)', border: '1px solid #00ff41', borderRadius: '4px', marginBottom: '10px' }}>
            ✅ Backend API: Connected
          </div>
          <div style={{ padding: '10px', background: 'rgba(0, 217, 255, 0.1)', border: '1px solid #00d9ff', borderRadius: '4px', marginBottom: '10px' }}>
            ✅ RAG Pipeline: Ready
          </div>
          <div style={{ padding: '10px', background: vitals ? 'rgba(0, 255, 65, 0.1)' : 'rgba(255, 165, 0, 0.1)', border: vitals ? '1px solid #00ff41' : '1px solid #ffa500', borderRadius: '4px' }}>
            {vitals ? '✅' : '⏳'} Monitor: {vitals ? 'Online' : 'Initializing'}
          </div>
        </div>
      </div>

      <div className="card">
        <h2>📋 Quick Actions</h2>
        <p>Select a section from the sidebar to begin:</p>
        <ul style={{ marginTop: '15px', lineHeight: '1.8' }}>
          <li><strong>👤 Patient</strong> - View patient information and details</li>
          <li><strong>📋 Reports</strong> - Access medical reports and imaging</li>
          <li><strong>❤️ Monitor</strong> - View real-time vital signs (simulated)</li>
          <li><strong>✓ Checklist</strong> - Pre-surgical safety checklist</li>
          <li><strong>🤖 Assistant</strong> - AI-powered medical assistant</li>
        </ul>
      </div>

      {vitals && (
        <div className="card">
          <h2>❤️ Current Vitals</h2>
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
          <small style={{ marginTop: '15px', color: 'var(--text-secondary)' }}>
            {vitals.note}
          </small>
        </div>
      )}
    </div>
  );
}
