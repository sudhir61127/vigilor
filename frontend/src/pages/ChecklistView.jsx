import { useState } from 'react';

export default function ChecklistView({ sendMessage }) {
  const [patientId, setPatientId] = useState('P001');
  const [checklist, setChecklist] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerateChecklist = async () => {
    setLoading(true);
    const response = await sendMessage(`Show surgical checklist for ${patientId}`);
    if (response) {
      setChecklist(response.response);
    }
    setLoading(false);
  };

  return (
    <div>
      <div className="card">
        <h2>✓ Surgical Safety Checklist</h2>
        <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
          <input
            type="text"
            value={patientId}
            onChange={(e) => setPatientId(e.target.value)}
            placeholder="Enter patient ID"
            className="text-input"
            style={{ flex: 1 }}
          />
          <button className="button primary" onClick={handleGenerateChecklist} disabled={loading}>
            {loading ? 'Generating...' : 'Generate'}
          </button>
        </div>
      </div>

      {checklist && (
        <div className="card">
          <h3>Pre-Surgical Checklist</h3>
          <div
            style={{
              marginTop: '15px',
              whiteSpace: 'pre-wrap',
              fontFamily: 'monospace',
              fontSize: '0.9rem',
            }}
          >
            {checklist}
          </div>
          <div style={{ marginTop: '20px', padding: '15px', background: 'rgba(0, 255, 65, 0.1)', border: '1px solid #00ff41', borderRadius: '4px' }}>
            <strong>✅ Ready for Surgery:</strong> All critical checklist items must be completed before proceeding to OR.
          </div>
        </div>
      )}
    </div>
  );
}
