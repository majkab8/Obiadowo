import "./App.css";
import ChatInput from "./components/ChatInput.jsx";
import Header from "./components/Header.jsx";
import EmptyChat from "./components/EmptyChat.jsx";
import ChatWindow from "./components/ChatWindow.jsx";
import { useState } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  async function sendMessage(text) {
    if (text.trim() === "") return;

    const userMessage = { id: crypto.randomUUID(), sender: "user", text: text };
    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();

      const botMessage = {
        id: crypto.randomUUID(),
        sender: "bot",
        recipe: data,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Fetch error:", error);
    } finally {
      setLoading(false);
    }
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
        <ChatWindow messages={messages} loading={loading} />
      )}
      <hr className="divider" />
      <ChatInput onSend={sendMessage} />
    </div>
  );
}

export default App;
