// src/components/TypingIndicator.js
import React from 'react';
import '../styles/Chat.css'; // Import the CSS for styling

const TypingIndicator = () => {
  return (
    <div className="message-wrapper"> {/* Wrap for consistent alignment */}
      <div className="typing-indicator">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  );
};

export default TypingIndicator;