import { ChefHatIcon } from "../icons/Icons.jsx";

function ChatMessage({ message, sender }) {
  return (
    <div className={`message-row message-row--${sender}`}>
      {sender === "bot" && (
        <div className="botmessage-avatar">
          <ChefHatIcon />
        </div>
      )}
      <div className={`message message--${sender}`}>{message}</div>
    </div>
  );
}

export default ChatMessage;
