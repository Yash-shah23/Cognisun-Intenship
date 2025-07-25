import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);
  const textareaRef = useRef(null); // Ref for the textarea

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chat, loading]);

  // Effect to adjust textarea height
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'; // Reset height
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px'; // Set to scroll height
    }
  }, [question]); // Re-run when question changes

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
    } catch {
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
      <header className="chat-header">🤖 AI Chat Assistant</header>
      <div className="chat-window">
        {chat.map((msg, i) => (
          <div key={i} className={`message ${msg.sender}`}>
            <div className="bubble">{msg.text}</div>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <div className="bubble">Typing...</div>
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
