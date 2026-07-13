import "./App.css";
import ChatInput from "./components/ChatInput.jsx";
import Header from "./components/Header.jsx";
import EmptyChat from "./components/EmptyChat.jsx";
import ChatWindow from "./components/ChatWindow.jsx";
import { useState } from "react";

function App() {
  const [messages, setMessages] = useState([]);

  async function sendMessage(text) {
    if (text.trim() === "") return;

    const userMessage = { id: crypto.randomUUID(), sender: "user", text: text };
    setMessages((prev) => [...prev, userMessage]);

    // TODO: ZMIENIC WIADOMOSC BOTA NA PRAWDZIWA PO ZROBIENIU BACKENDU
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    const data = await response.json();

    const botMessage = {
      id: crypto.randomUUID(),
      sender: "bot",
      recipe: data,
    };

    setMessages((prev) => [...prev, botMessage]);
  }

  function resetChat() {
    setMessages([]);
  }

  return (
    <div className="wholesite">
      <Header onReset={resetChat} />
      {messages.length === 0 ? (
        <EmptyChat onPick={sendMessage} />
      ) : (
        <ChatWindow messages={messages} />
      )}
      <hr className="divider" />
      <ChatInput onSend={sendMessage} />
    </div>
  );
}

export default App;
