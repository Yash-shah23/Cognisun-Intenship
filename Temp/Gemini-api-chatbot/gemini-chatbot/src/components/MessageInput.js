import React, { useState } from 'react';

function MessageInput({ onSendMessage, isLoading }) {
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (inputValue.trim() === '') return;
    onSendMessage(inputValue);
    setInputValue('');
  };

  return (
    <div className="input-container">
      <input
        className="input-box"
        type="text"
        placeholder="Ask a question..."
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        disabled={isLoading}
      />
      <button className="send-button" onClick={handleSend} disabled={isLoading}>
        Send
      </button>
    </div>
  );
}

export default MessageInput;
