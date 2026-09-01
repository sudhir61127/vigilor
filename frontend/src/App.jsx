import React from "react";
import VoiceInput from "./components/VoiceInput";

function App() {
  return (
    <div>
      <h1>VIGIL-OR</h1>

      <VoiceInp                                                                               ut
        onTranscript={(text) => {
          console.log("Voice transcript:", text);
        }}
      />
    </div>
  );
}

export default App;