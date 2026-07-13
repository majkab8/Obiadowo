import ChatMessage from "./ChatMessage.jsx";
import TypingIndicator from "./TypingIndicator.jsx";
import { useEffect, useRef } from "react";

function ChatWindow({ messages, loading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="chatwindow">
      <div className="chatwindow-messages">
        {messages.map((m) => (
          <ChatMessage
            key={m.id}
            sender={m.sender}
            message={m.text}
            recipe={m.recipe}
          />
        ))}
        {loading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}

export default ChatWindow;
