// src/components/ChatWindow.js
import React, { useRef, useEffect } from 'react';
import Message from './Message';
import TypingIndicator from './TypingIndicator'; // Import the new component
import '../styles/Chat.css';

const ChatWindow = ({ messages, isLoading }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]); // Scroll when messages change OR loading state changes

  return (
    <div className="chat-window">
      {messages.map((msg, index) => (
        <Message key={index} text={msg.text} sender={msg.sender} />
      ))}
      {isLoading && <TypingIndicator />} {/* Show typing indicator when loading */}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatWindow;