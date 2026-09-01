import { useSpeechRecognition } from "../hooks/useSpeechRecognition";

function VoiceInput({ onTranscript }) {
  const {
    transcript,
    isListening,
    error,
    startListening,
    stopListening,
  } = useSpeechRecognition();

  const handleVoiceInput = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  if (transcript) {
    onTranscript(transcript);
  }

  return (
    <div>
      <button type="button" onClick={handleVoiceInput}>
        {isListening ? "🛑 Stop Listening" : "🎤 Start Speaking"}
      </button>

      {isListening && <p>Listening...</p>}

      {transcript && (
        <p>
          <strong>You said:</strong> {transcript}
        </p>
      )}

      {error && <p>{error}</p>}
    </div>
  );
}

export default VoiceInput;