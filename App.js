import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');

  const sendMessage = async () => {
    if (inputText.trim() === '') return;

    setMessages([...messages, { text: inputText, sender: 'user' }]);
    setInputText('');

    try {
      const response = await axios.post('/api/send-message', { user_question: inputText });
      setMessages([...messages, { text: response.data, sender: 'bot' }]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        SkyFlareAI Chatbot
      </div>
      <div className="chatbot-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            {message.text}
          </div>
        ))}
      </div>
      <div className="chatbot-input">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') sendMessage();
          }}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;





  // return (
  //   <div className="App">
  //     <header className="App-header">
  //       {/*<img src={logo} className="App-logo" alt="logo" />*/}
  //       <p>
  //         SkyFlareAI Chatbot
  //       </p>
  //       <a
  //         className="App-link"
  //         href="https://react.dev/"
  //         target="_blank"
  //         rel="noopener noreferrer"
  //       >
         
  //       </a>
  //     </header>
  //   </div>
  // );