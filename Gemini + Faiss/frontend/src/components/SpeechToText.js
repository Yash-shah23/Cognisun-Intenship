// components/SpeechToText.js
import React, { useState, useEffect } from "react";

const SpeechToText = ({ onTranscript }) => {
  const [listening, setListening] = useState(false);
  const recognition = useRef(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech Recognition not supported in this browser");
      return;
    }

    recognition.current = new SpeechRecognition();
    recognition.current.lang = "auto"; // auto-detect
    recognition.current.interimResults = false;

    recognition.current.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      onTranscript(transcript); // send result to parent
    };

    recognition.current.onend = () => {
      setListening(false);
    };
  }, []);

  const startListening = () => {
    if (recognition.current) {
      setListening(true);
      recognition.current.start();
    }
  };

  return (
    <button onClick={startListening} disabled={listening}>
      🎤 {listening ? "Listening..." : "Start Talking"}
    </button>
  );
};

export default SpeechToText;
