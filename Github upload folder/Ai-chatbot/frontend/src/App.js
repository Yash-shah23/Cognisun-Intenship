import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Auto scroll on new message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chat, loading]);

  // Auto grow textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [question]);

  const handleAsk = async () => {
    if (!question.trim()) return;

    const userMsg = { sender: 'user', text: question };
    setChat((prev) => [...prev, userMsg]);
    setLoading(true);
    setQuestion('');

    try {
      const res = await axios.post('http://localhost:8000/ask', { question });
      const botMsg = { sender: 'bot', text: res.data.answer };
      setChat((prev) => [...prev, botMsg]);
    } catch (err) {
      setChat((prev) => [...prev, { sender: 'bot', text: '⚠️ Error getting response.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  return (
    <div className="chat-container">
      <header className="chat-header">YASH AI</header>

      <div className="chat-window">
        {chat.map((msg, i) => (
          <div key={i} className={`message ${msg.sender}`}>
            <div className="bubble">{msg.text}</div>
          </div>
        ))}

        {loading && (
          <div className="message bot">
            <div className="bubble typing-indicator">Yash AI is typing...</div>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      <div className="input-area">
        <textarea
          ref={textareaRef}
          rows="1"
          placeholder="Ask something..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button onClick={handleAsk}>Send</button>
      </div>
    </div>
  );
}

export default App;
