// src/components/Message.js (Already correct from previous update)
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import '../styles/Chat.css';

const Message = ({ text, sender }) => {
  const isUser = sender === 'user';
  return (
    // This wrapper div is key for the alignment
    <div className={`message-wrapper ${isUser ? 'user-message-wrapper' : 'bot-message-wrapper'}`}>
      <div className={`message ${isUser ? 'user-message' : 'bot-message'}`}>
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{text}</ReactMarkdown>
      </div>
    </div>
  );
};

export default Message;