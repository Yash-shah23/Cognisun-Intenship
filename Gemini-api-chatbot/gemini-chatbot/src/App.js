// src/App.js
import React, { useState, useEffect } from 'react';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';
import { getGeminiResponse } from './api/gemini';
import './styles/App.css';
import './styles/Chat.css';
// import geminiLogo from './assets/gemini-logo.png'; // If you add a logo
import { FaSun, FaMoon } from 'react-icons/fa'; // Install react-icons: npm install react-icons

function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      return savedTheme;
    }
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  });

  useEffect(() => {
    document.body.classList.toggle('dark-mode', theme === 'dark');
    localStorage.setItem('theme', theme);
  }, [theme]);

  useEffect(() => {
    setMessages([{ text: "Hello! I'm Gemini Chatbot. How can I help you today?", sender: 'bot' }]);
  }, []);

  const handleSendMessage = async (userMessage) => {
    const newMessage = { text: userMessage, sender: 'user' };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setIsLoading(true);

    try {
      const botResponse = await getGeminiResponse(userMessage);
      const newBotMessage = { text: botResponse, sender: 'bot' };
      setMessages((prevMessages) => [...prevMessages, newBotMessage]);
    } catch (error) {
      console.error('Failed to get bot response:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: `Error: Could not get a response from the AI. (${error.message || 'Unknown error'})`, sender: 'bot' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  return (
    <div className="app-container">
      <div className="chat-header">
        <div className="chat-header-title"> {/* NEW WRAPPER DIV */}
          {/* Uncomment and add a logo if you have one in src/assets */}
          {/* <img src={geminiLogo} alt="Gemini Logo" /> */}
          <span>Gemini Chatbot</span> {/* Wrapped in a span for direct text styling if needed */}
        </div>
        <button onClick={toggleTheme} className="theme-toggle-button" aria-label="Toggle dark mode">
          {theme === 'light' ? <FaMoon /> : <FaSun />}
        </button>
      </div>
      <div className="chat-container">
        <ChatWindow messages={messages} isLoading={isLoading} />
        <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
}

export default App;