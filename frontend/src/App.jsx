import "./App.css";
import ChatInput from "./components/ChatInput.jsx";
import Header from "./components/Header.jsx";
import EmptyChat from "./components/EmptyChat.jsx";
import ChatWindow from "./components/ChatWindow.jsx";
import { useState } from "react";

function App() {
  const [messages, setMessages] = useState([]);

  function sendMessage(text) {
    if (text.trim() === "") return;
    const userMessage = { id: crypto.randomUUID(), sender: "user", text: text };
    setMessages((prev) => [...prev, userMessage]);

    // TODO: ZMIENIC WIADOMOSC BOTA NA PRAWDZIWA PO ZROBIENIU BACKENDU
    const botMessage = {
      id: crypto.randomUUID(),
      sender: "bot",
      text: "Ooh, smakowite typy — zaraz coś wymyślę!",
    };
    setTimeout(() => {
      setMessages((prev) => [...prev, botMessage]);
    }, 500);
  }

  function resetChat() {
    setMessages([]);
  }

  return (
    <>
      <Header onReset={resetChat} />
      {messages.length === 0 ? (
        <EmptyChat onPick={sendMessage} />
      ) : (
        <ChatWindow messages={messages} />
      )}
      <div className="fullChat">
        <ChatInput onSend={sendMessage} />
      </div>
    </>
  );
}

export default App;
