import React, { useEffect, useRef } from 'react';

function MessageList({ messages }) {
  const messagesEndRef = useRef(null);
  
  // Auto-scroll to the bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);
  
  // Format timestamp
  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };
  
  return (
    <div className="message-list">
      {messages.length === 0 ? (
        <div className="empty-state">
          <p>Ask me a question about your health symptoms.</p>
        </div>
      ) : (
        messages.map(message => (
          <div 
            key={message.id}
            className={`message ${message.sender} ${message.isError ? 'error' : ''}`}
          >
            <div className="message-content">
              <p>{message.text}</p>
            </div>
            <div className="message-timestamp">
              {formatTime(message.timestamp)}
            </div>
          </div>
        ))
      )}
      <div ref={messagesEndRef} />
    </div>
  );
}

export default MessageList; 