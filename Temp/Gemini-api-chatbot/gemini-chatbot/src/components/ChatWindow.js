import React from 'react';
import Message from './Message';

function ChatWindow({ messages, isLoading }) {
  return (
    <div className="chat-window">
      {messages.map((msg, index) => (
        <Message key={index} text={msg.text} sender={msg.sender} />
      ))}
      {isLoading && <Message text="Typing..." sender="bot" />}
    </div>
  );
}

export default ChatWindow;
