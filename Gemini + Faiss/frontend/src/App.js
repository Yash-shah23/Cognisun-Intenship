

import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { FaMicrophone, FaPlus, FaTrash, FaEdit } from "react-icons/fa";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [recording, setRecording] = useState(false);
  const [speechLang, setSpeechLang] = useState("en-US");
  const [sessions, setSessions] = useState([]);
  const [selectedSessionId, setSelectedSessionId] = useState(null);
  const recognitionRef = useRef(null);
  const chatBoxRef = useRef(null);

  // Auto-scroll chat
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]);

  // Load sessions
  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const res = await axios.get(`${API_URL}/sessions`);
      const filtered = res.data.filter((s) => !s.is_deleted); // ✅ Filter deleted
      setSessions(filtered);

      // Auto-select first session
      if (filtered.length > 0 && !selectedSessionId) {
        setSelectedSessionId(filtered[0].id);
        loadSessionMessages(filtered[0].id);
      }
    } catch (err) {
      console.error("Failed to load sessions:", err);
    }
  };

  const createSession = async () => {
    try {
      const res = await axios.post(`${API_URL}/create-session`);
      const newSessionId = res.data.id;
      setSelectedSessionId(newSessionId);
      fetchSessions();
      setMessages([]);
    } catch (err) {
      console.error("Failed to create session:", err);
    }
  };

  const loadSessionMessages = async (sessionId) => {
    try {
      const res = await axios.get(`${API_URL}/session/${sessionId}`);
      setSelectedSessionId(sessionId);
      setMessages(res.data.messages || []);
    } catch (err) {
      console.error("Failed to load session messages:", err);
    }
  };

  const deleteSession = async (sessionId) => {
    try {
      await axios.put(`${API_URL}/delete-session/${sessionId}`);
      await fetchSessions(); // refresh sessions

      if (selectedSessionId === sessionId) {
        setMessages([]);
        setSelectedSessionId(null);

        // Auto-select first available session
        const remaining = sessions.filter(s => s.id !== sessionId);
        if (remaining.length > 0) {
          setSelectedSessionId(remaining[0].id);
          loadSessionMessages(remaining[0].id);
        }
      }
    } catch (err) {
      console.error("Failed to delete session:", err);
    }
  };

  const renameSession = async (sessionId) => {
    const newName = prompt("Enter new session name:");
    if (!newName) return;
    try {
      await axios.put(`${API_URL}/rename-session/${sessionId}`, {
        new_name: newName, // ✅ fixed
      });
      await fetchSessions(); // refresh sidebar
    } catch (err) {
      console.error("Failed to rename session:", err);
    }
  };

  // Speech recognition setup
  useEffect(() => {
    if ("webkitSpeechRecognition" in window) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.onresult = (event) => {
        const speechText = event.results[0][0].transcript;
        setQuery(speechText);
      };
      recognition.onerror = () => setRecording(false);
      recognition.onend = () => setRecording(false);
      recognitionRef.current = recognition;
    }
  }, []);

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

  const sendMessage = async () => {
    if (!query.trim() || !selectedSessionId) return;
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/ask`, {
        query,
        selected_lang:
          speechLang.startsWith("hi")
            ? "hi"
            : speechLang.startsWith("gu")
              ? "gu"
              : "en",
        session_id: selectedSessionId,
      });
      const answer = res.data.answer;
      const isOutOfContext = /cannot answer|out of context|no information/i.test(answer);

      setMessages((prev) => [
        ...prev,
        { role: "user", text: query },
        { role: "bot", text: answer, outOfContext: isOutOfContext },
      ]);
      setQuery("");
    } catch (err) {
      console.error("Error sending message:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <div className="sidebar">
        <button onClick={createSession} className="new-chat-btn">
          <FaPlus /> New Chat
        </button>
        <div className="chat-list">
          {sessions.map((s) => (
            <div
              key={s.id}
              className={`chat-item ${selectedSessionId === s.id ? "active" : ""}`}
              onClick={() => loadSessionMessages(s.id)}
            >
              <span>{s.name}</span>
              <div className="chat-actions">
                <FaEdit onClick={(e) => { e.stopPropagation(); renameSession(s.id); }} />
                <FaTrash onClick={(e) => { e.stopPropagation(); deleteSession(s.id); }} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat */}
      <div className="chat-container">
        <h1 className="chat-title">RAG Chatbot</h1>

        {/* Language buttons */}
        <div className="lang-buttons">
          <button onClick={() => setSpeechLang("en-US")} className={speechLang === "en-US" ? "active" : ""}>English</button>
          <button onClick={() => setSpeechLang("hi-IN")} className={speechLang === "hi-IN" ? "active" : ""}>Hindi</button>
          <button onClick={() => setSpeechLang("gu-IN")} className={speechLang === "gu-IN" ? "active" : ""}>Gujarati</button>
        </div>

        {/* Messages */}
        <div className="chat-box" ref={chatBoxRef}>
          {messages.map((msg, i) => (
            <div key={i} className={`chat-message ${msg.role}`}>
              <div className={`chat-answer ${msg.outOfContext ? "out-of-context" : ""}`}>
                <strong>{msg.role === "user" ? "You:" : "Bot:"}</strong>{" "}
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.text}
                </ReactMarkdown>
              </div>
            </div>
          ))}
          {loading && <div className="loading">Bot is thinking...</div>}
        </div>


        {/* Input */}
        <div className="input-container">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type your question or use speech..."
            onKeyDown={(e) => {
              if (e.key === "Enter") sendMessage();
            }}
          />
          <button onClick={sendMessage}>Send</button>
          <button className={`mic-btn ${recording ? "recording" : ""}`} onClick={handleSpeech}>
            <FaMicrophone />
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;


