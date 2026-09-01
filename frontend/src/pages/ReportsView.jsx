import { useState } from 'react';

export default function ReportsView({ sendMessage }) {
  const [patientId, setPatientId] = useState('P001');
  const [reportType, setReportType] = useState('blood');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const reportTypes = ['blood', 'mri', 'ct', 'xray', 'ecg'];

  const handleFetchReport = async () => {
    setLoading(true);
    const response = await sendMessage(`Show ${reportType} report for ${patientId}`);
    if (response) {
      setResult(response.response);
    }
    setLoading(false);
  };

  return (
    <div>
      <div className="card">
        <h2>📋 Medical Reports</h2>
        <div style={{ marginTop: '15px', display: 'grid', gridTemplateColumns: '1fr 1fr auto', gap: '10px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '5px', color: 'var(--text-secondary)' }}>
              Patient ID
            </label>
            <input
              type="text"
              value={patientId}
              onChange={(e) => setPatientId(e.target.value)}
              placeholder="P001"
              className="text-input"
            />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '5px', color: 'var(--text-secondary)' }}>
              Report Type
            </label>
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="text-input"
            >
              {reportTypes.map((type) => (
                <option key={type} value={type}>
                  {type.toUpperCase()}
                </option>
              ))}
            </select>
          </div>
          <div style={{ alignSelf: 'flex-end' }}>
            <button className="button primary" onClick={handleFetchReport} disabled={loading}>
              {loading ? 'Loading...' : 'Fetch'}
            </button>
          </div>
        </div>
      </div>

      {result && (
        <div className="card">
          <h3>Report Content</h3>
          <div
            style={{
              marginTop: '15px',
              whiteSpace: 'pre-wrap',
              fontFamily: 'monospace',
              fontSize: '0.85rem',
              maxHeight: '600px',
              overflowY: 'auto',
            }}
          >
            {result}
          </div>
        </div>
      )}
    </div>
  );
}
