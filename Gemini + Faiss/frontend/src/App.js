import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { FaMicrophone } from "react-icons/fa";
import ReactMarkdown from "react-markdown";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [recording, setRecording] = useState(false);
  const [speechLang, setSpeechLang] = useState("en-US"); // ✅ Default English
  const recognitionRef = useRef(null);
  const chatBoxRef = useRef(null);

  // ✅ Auto-scroll to latest message
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]);

  // ✅ Initialize speech recognition
  useEffect(() => {
    if ("webkitSpeechRecognition" in window) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onresult = (event) => {
        const speechText = event.results[0][0].transcript;
        setQuery(speechText);
      };

      recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        setRecording(false);
      };

      recognition.onend = () => {
        setRecording(false);
      };

      recognitionRef.current = recognition;
    } else {
      alert("Your browser does not support speech recognition.");
    }
  }, []);

  // ✅ Start/stop recording
  const handleSpeech = () => {
    if (recognitionRef.current) {
      recognitionRef.current.lang = speechLang;
      if (!recording) {
        setRecording(true);
        recognitionRef.current.start();
      } else {
        recognitionRef.current.stop();
        setRecording(false);
      }
    }
  };

  // ✅ Send message to backend
  const sendMessage = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/ask`, { 
        query, 
        selected_lang: speechLang.startsWith("hi") ? "hi" : speechLang.startsWith("gu") ? "gu" : "en"
      });
      const answer = res.data.answer;
      const isOutOfContext = /cannot answer|out of context|no information/i.test(answer);

      setMessages((prev) => [
        ...prev,
        { question: query, answer, outOfContext: isOutOfContext },
      ]);
      setQuery("");
    } catch (err) {
      console.error(err);
      alert("Error connecting to backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <h1 className="chat-title">RAG Chatbot</h1>
      
      {/* ✅ Language selection buttons */}
      <div className="lang-buttons">
        <button onClick={() => setSpeechLang("en-US")} className={speechLang === "en-US" ? "active" : ""}>
          English
        </button>
        <button onClick={() => setSpeechLang("hi-IN")} className={speechLang === "hi-IN" ? "active" : ""}>
          Hindi
        </button>
        <button onClick={() => setSpeechLang("gu-IN")} className={speechLang === "gu-IN" ? "active" : ""}>
          Gujarati
        </button>
      </div>

      <div className="chat-box" ref={chatBoxRef}>
        {messages.map((msg, i) => (
          <div key={i} className="chat-message">
            <div className="chat-question">Q: {msg.question}</div>
            <div className={`chat-answer ${msg.outOfContext ? "out-of-context" : ""}`}>
              <ReactMarkdown>{msg.answer}</ReactMarkdown>
            </div>
          </div>
        ))}
        {loading && <div className="loading">BotThinking...</div>}
      </div>

      <div className="input-container">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Type your question or use speech..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
        <button className={`mic-btn ${recording ? "recording" : ""}`} onClick={handleSpeech}>
          <FaMicrophone />
        </button>
      </div>
    </div>
  );
}

export default App;
