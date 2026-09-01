import { useState } from 'react';

export default function PatientView({ sendMessage }) {
  const [patientId, setPatientId] = useState('P001');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    const response = await sendMessage(`Show patient ${patientId}`);
    if (response) {
      setResult(response.response);
    }
    setLoading(false);
  };

  return (
    <div>
      <div className="card">
        <h2>👤 Patient Information</h2>
        <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
          <input
            type="text"
            value={patientId}
            onChange={(e) => setPatientId(e.target.value)}
            placeholder="Enter patient ID (e.g., P001, PAT001)"
            className="text-input"
            style={{ flex: 1 }}
          />
          <button className="button primary" onClick={handleSearch} disabled={loading}>
            {loading ? 'Loading...' : 'Search'}
          </button>
        </div>
      </div>

      {result && (
        <div className="card">
          <h3>Patient Details</h3>
          <div style={{ marginTop: '15px', whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: '0.9rem' }}>
            {result}
          </div>
        </div>
      )}
    </div>
  );
}
