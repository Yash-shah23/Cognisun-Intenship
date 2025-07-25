import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';
import './styles/Chat.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (userMessage) => {
    const userMsgObj = { text: userMessage, sender: 'user' };
    setMessages((prev) => [...prev, userMsgObj]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: userMessage }),
      });

      const data = await response.json();
      const botMsgObj = { text: data.answer, sender: 'bot' };
      setMessages((prev) => [...prev, botMsgObj]);
    } catch (error) {
      console.error('Error:', error);
      const errorMsg = {
        text: 'Error contacting server or getting response. Please try again later.',
        sender: 'bot',
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <h1 className="header">Gemini RAG Chatbot</h1>
      <ChatWindow messages={messages} isLoading={isLoading} />
      <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
}

export default App;
