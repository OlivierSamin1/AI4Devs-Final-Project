import React from 'react';
import ChatInterface from './ChatInterface';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Personal Database Assistant</h1>
        <p>Ask questions about your health symptoms</p>
      </header>
      <main className="app-main">
        <ChatInterface />
      </main>
      <footer className="app-footer">
        <p>&copy; {new Date().getFullYear()} Personal Database Assistant</p>
      </footer>
    </div>
  );
}

export default App; 