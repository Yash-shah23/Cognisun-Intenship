// src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/ask', { query });
      setResponse(res.data.answer);
    } catch (error) {
      console.error('❌ Error:', error.message);
      setResponse('Error connecting to backend.');
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>🧠 AI PDF Chatbot</h1>
      <textarea
        placeholder="Ask a question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSend} disabled={loading}>
        {loading ? 'Loading...' : 'Send'}
      </button>

      {response && (
        <div className="response-box">
          <h3>Answer:</h3>
          <ReactMarkdown>{response}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}

export default App;
