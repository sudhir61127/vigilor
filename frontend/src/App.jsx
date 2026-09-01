import { useState, useEffect } from 'react';
import { useAgent, useMonitor, useSpeechRecognition, useSpeechSynthesis } from './hooks/useVoice';
import OverviewView from './pages/OverviewView';
import PatientView from './pages/PatientView';
import ReportsView from './pages/ReportsView';
import MonitorView from './pages/MonitorView';
import ChecklistView from './pages/ChecklistView';
import AssistantView from './pages/AssistantView';

export default function App() {
  const [currentView, setCurrentView] = useState('overview');
  const { sendMessage, loading: agentLoading } = useAgent();
  const { vitals, fetchVitals } = useMonitor();
  const { transcript, isListening, startListening, stopListening, clearTranscript } = useSpeechRecognition();
  const { speak } = useSpeechSynthesis();

  // Auto-fetch vitals when monitor view is active or periodically
  useEffect(() => {
    if (currentView === 'monitor') {
      fetchVitals();
      const interval = setInterval(fetchVitals, 3000); // Update every 3 seconds
      return () => clearInterval(interval);
    }
  }, [currentView, fetchVitals]);

  const renderView = () => {
    switch (currentView) {
      case 'overview':
        return <OverviewView vitals={vitals} />;
      case 'patient':
        return <PatientView sendMessage={sendMessage} />;
      case 'reports':
        return <ReportsView sendMessage={sendMessage} />;
      case 'monitor':
        return <MonitorView vitals={vitals} fetchVitals={fetchVitals} />;
      case 'checklist':
        return <ChecklistView sendMessage={sendMessage} />;
      case 'assistant':
        return (
          <AssistantView
            sendMessage={sendMessage}
            transcript={transcript}
            isListening={isListening}
            startListening={startListening}
            stopListening={stopListening}
            clearTranscript={clearTranscript}
            speak={speak}
            agentLoading={agentLoading}
          />
        );
      default:
        return <OverviewView vitals={vitals} />;
    }
  };

  return (
    <div className="dashboard">
      <div className="top-bar">
        <h1>⚕️ VIGIL-OR</h1>
        <div className="status">
          <div className="status-indicator">
            <div className={`status-dot${vitals ? '' : ' warning'}`}></div>
            <span>{vitals ? 'System Online' : 'Initializing'}</span>
          </div>
        </div>
      </div>

      <div className="sidebar">
        <div
          className={`sidebar-item${currentView === 'overview' ? ' active' : ''}`}
          onClick={() => setCurrentView('overview')}
        >
          📊 Overview
        </div>
        <div
          className={`sidebar-item${currentView === 'patient' ? ' active' : ''}`}
          onClick={() => setCurrentView('patient')}
        >
          👤 Patient
        </div>
        <div
          className={`sidebar-item${currentView === 'reports' ? ' active' : ''}`}
          onClick={() => setCurrentView('reports')}
        >
          📋 Reports
        </div>
        <div
          className={`sidebar-item${currentView === 'monitor' ? ' active' : ''}`}
          onClick={() => setCurrentView('monitor')}
        >
          ❤️ Monitor
        </div>
        <div
          className={`sidebar-item${currentView === 'checklist' ? ' active' : ''}`}
          onClick={() => setCurrentView('checklist')}
        >
          ✓ Checklist
        </div>
        <div
          className={`sidebar-item${currentView === 'assistant' ? ' active' : ''}`}
          onClick={() => setCurrentView('assistant')}
        >
          🤖 Assistant
        </div>
      </div>

      <div className="main-content">{renderView()}</div>
    </div>
  );
}

function Metric({ label, value }) { return <article className="metric"><span>{label}</span><strong>{value}</strong></article>; }
