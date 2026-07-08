import ChatMessage from "./ChatMessage.jsx";

function ChatWindow({ messages }) {
  return (
    <div className="chatwindow">
      <div className="chatwindow-messages">
        {messages.map((m) => (
          <ChatMessage key={m.id} sender={m.sender} message={m.text} />
        ))}
      </div>
    </div>
  );
}

export default ChatWindow;
