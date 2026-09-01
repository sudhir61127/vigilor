import { useState, useRef, useEffect } from 'react';

export default function AssistantView({
  sendMessage,
  transcript,
  isListening,
  startListening,
  stopListening,
  clearTranscript,
  speak,
  agentLoading,
}) {
  const [messages, setMessages] = useState([
    {
      type: 'assistant',
      text: 'Welcome to VIGIL-OR AI Assistant. I can help you with patient information, medical reports, vital signs monitoring, surgical checklists, and medical knowledge queries. How can I assist you?',
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [localLoading, setLocalLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (text) => {
    const userText = text || inputValue;
    if (!userText.trim()) return;

    // Add user message to chat
    setMessages((prev) => [...prev, { type: 'user', text: userText }]);
    setInputValue('');
    setLocalLoading(true);

    // Send to agent
    const response = await sendMessage(userText);

    if (response) {
      setMessages((prev) => [
        ...prev,
        {
          type: 'assistant',
          text: response.response,
          intent: response.intent,
        },
      ]);

      // Speak the response (optional - you can comment out if not desired)
      // Limit speaking to first 500 chars to avoid long speeches
      const textToSpeak = response.response.replace(/[*#_`\[\]]/g, '').substring(0, 500);
      // speak(textToSpeak);
    } else {
      setMessages((prev) => [
        ...prev,
        {
          type: 'error',
          text: 'Failed to get response from the agent. Please try again.',
        },
      ]);
    }

    setLocalLoading(false);
  };

  const handleMicrophoneClick = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  const handleSendTranscript = () => {
    if (transcript) {
      handleSendMessage(transcript);
      clearTranscript();
    }
  };

  return (
    <div className="assistant-container" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="card" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflowY: 'hidden' }}>
        <h2>🤖 AI Medical Assistant</h2>

        <div className="chat-messages" style={{ flex: 1, marginTop: '15px', overflowY: 'auto' }}>
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.type}`}>
              {msg.text}
            </div>
          ))}
          {(agentLoading || localLoading) && (
            <div className="message assistant">
              <span className="loading"></span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="assistant-input" style={{ marginTop: '20px', display: 'flex', gap: '10px', alignItems: 'flex-end' }}>
          <button
            className={`button mic ${isListening ? 'listening' : ''}`}
            onClick={handleMicrophoneClick}
            title={isListening ? 'Stop listening' : 'Start listening'}
          >
            🎤
          </button>

          <div className="input-area" style={{ flex: 1 }}>
            {(transcript || isListening) && (
              <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', padding: '8px', background: 'rgba(0, 217, 255, 0.05)', borderRadius: '4px' }}>
                {isListening && <span>🎤 Listening...</span>}
                {transcript && <span>Transcript: {transcript}</span>}
              </div>
            )}

            <div style={{ display: 'flex', gap: '10px' }}>
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !agentLoading && !localLoading) {
                    handleSendMessage();
                  }
                }}
                placeholder="Type a message or use microphone..."
                className="text-input"
                disabled={agentLoading || localLoading}
              />
              <button
                className="button primary"
                onClick={() => handleSendMessage()}
                disabled={(!inputValue.trim() && !transcript) || agentLoading || localLoading}
              >
                Send
              </button>
            </div>

            {transcript && (
              <div style={{ marginTop: '8px', display: 'flex', gap: '8px' }}>
                <button className="button" onClick={handleSendTranscript} disabled={agentLoading || localLoading}>
                  ✓ Send Transcript
                </button>
                <button className="button" onClick={clearTranscript}>
                  ✕ Clear
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="card" style={{ marginTop: '20px' }}>
        <h3>💡 Quick Examples</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px', marginTop: '10px' }}>
          {[
            'Show patient P001',
            'Show MRI report for P001',
            'Show current vitals',
            'Show surgical checklist',
            'What are surgical precautions?',
          ].map((example) => (
            <button
              key={example}
              className="button"
              onClick={() => handleSendMessage(example)}
              disabled={agentLoading || localLoading}
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
