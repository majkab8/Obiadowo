import { ArrowUpIcon } from "../icons/Icons.jsx";
import { useState } from "react";

function ChatInput({ onSend, loading }) {
  const [text, setText] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (loading) return;
    const trimmed = text.trim();
    if (trimmed === "") return;
    onSend(trimmed);
    setText("");
  }

  return (
    <form className="chatinput" onSubmit={handleSubmit}>
      <input
        type="text"
        className="chatinput-text"
        placeholder="Wypisz składniki..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button className="chatinput-button" type="submit">
        <ArrowUpIcon />
      </button>
    </form>
  );
}

export default ChatInput;
