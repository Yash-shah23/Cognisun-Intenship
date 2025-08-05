import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { FaMicrophone, FaPlus, FaTrash, FaEdit, FaPaperPlane } from "react-icons/fa";
import ReactMarkdown from "react-markdown";
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
      const filtered = res.data.filter((s) => !s.is_deleted);
      setSessions(filtered);

      if (filtered.length > 0 && !selectedSessionId) {
        setSelectedSessionId(filtered[0].id);
        loadSessionMessages(filtered[0].id);
      }
    } catch (err) {
      console.error("Failed to load sessions:", err);
      // Handle case when backend is not available
      setSessions([]);
      setSelectedSessionId(null);
      setMessages([]);
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
      alert("Unable to create session. Please ensure the backend server is running.");
    }
  };

  const loadSessionMessages = async (sessionId) => {
    try {
      const res = await axios.get(`${API_URL}/session/${sessionId}`);
      setSelectedSessionId(sessionId);
      setMessages(res.data.messages || []);
    } catch (err) {
      console.error("Failed to load session messages:", err);
      setMessages([]);
    }
  };

  const deleteSession = async (sessionId) => {
    try {
      await axios.put(`${API_URL}/delete-session/${sessionId}`);
      await fetchSessions();

      if (selectedSessionId === sessionId) {
        setMessages([]);
        setSelectedSessionId(null);

        const remaining = sessions.filter(s => s.id !== sessionId);
        if (remaining.length > 0) {
          setSelectedSessionId(remaining[0].id);
          loadSessionMessages(remaining[0].id);
        }
      }
    } catch (err) {
      console.error("Failed to delete session:", err);
      alert("Unable to delete session. Please ensure the backend server is running.");
    }
  };

  const renameSession = async (sessionId) => {
    const newName = prompt("Enter new session name:");
    if (!newName) return;
    try {
      await axios.put(`${API_URL}/rename-session/${sessionId}`, {
        new_name: newName,
      });
      await fetchSessions();
    } catch (err) {
      console.error("Failed to rename session:", err);
      alert("Unable to rename session. Please ensure the backend server is running.");
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
      setMessages((prev) => [
        ...prev,
        { role: "user", text: query },
        { role: "bot", text: "Sorry, I cannot respond right now. Please ensure the backend server is running.", outOfContext: true },
      ]);
      setQuery("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-header">
          <h2 className="sidebar-title">Conversations</h2>
          <button onClick={createSession} className="new-chat-btn">
            <FaPlus className="icon" />
            <span>New Chat</span>
          </button>
        </div>
        
        <div className="chat-list">
          {sessions.map((s) => (
            <div
              key={s.id}
              className={`chat-item ${selectedSessionId === s.id ? "active" : ""}`}
              onClick={() => loadSessionMessages(s.id)}
            >
              <div className="chat-item-content">
                <span className="chat-name">{s.name}</span>
                <div className="chat-actions">
                  <button 
                    className="action-btn edit-btn"
                    onClick={(e) => { e.stopPropagation(); renameSession(s.id); }}
                    title="Rename"
                  >
                    <FaEdit />
                  </button>
                  <button 
                    className="action-btn delete-btn"
                    onClick={(e) => { e.stopPropagation(); deleteSession(s.id); }}
                    title="Delete"
                  >
                    <FaTrash />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="main-content">
        <div className="chat-header">
          <h1 className="chat-title">AI Assistant</h1>
          <div className="lang-selector">
            <button 
              onClick={() => setSpeechLang("en-US")} 
              className={`lang-btn ${speechLang === "en-US" ? "active" : ""}`}
            >
              English
            </button>
            <button 
              onClick={() => setSpeechLang("hi-IN")} 
              className={`lang-btn ${speechLang === "hi-IN" ? "active" : ""}`}
            >
              हिंदी
            </button>
            <button 
              onClick={() => setSpeechLang("gu-IN")} 
              className={`lang-btn ${speechLang === "gu-IN" ? "active" : ""}`}
            >
              ગુજરાતી
            </button>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="chat-container">
          <div className="chat-box" ref={chatBoxRef}>
            {messages.length === 0 && (
              <div className="welcome-message">
                <div className="welcome-content">
                  <h3>Welcome to AI Assistant</h3>
                  <p>Start a conversation by typing your question below or use voice input.</p>
                </div>
              </div>
            )}
            
            {messages.map((msg, i) => (
              <div key={i} className={`message-wrapper ${msg.role}`}>
                <div className={`message ${msg.role} ${msg.outOfContext ? "out-of-context" : ""}`}>
                  <div className="message-content">
                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                  </div>
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="message-wrapper bot">
                <div className="message bot loading-message">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="input-area">
            <div className="input-container">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Type your message here..."
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                  }
                }}
                disabled={loading}
              />
              <div className="input-actions">
                <button 
                  className={`mic-btn ${recording ? "recording" : ""}`} 
                  onClick={handleSpeech}
                  title="Voice input"
                  disabled={loading}
                >
                  <FaMicrophone />
                </button>
                <button 
                  className="send-btn" 
                  onClick={sendMessage}
                  disabled={!query.trim() || loading}
                  title="Send message"
                >
                  <FaPaperPlane />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;