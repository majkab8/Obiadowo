import { ChefHatIcon } from "../icons/Icons.jsx";

function TypingIndicator({}) {
  return (
    <div className="message-row message-row--bot">
      <div className="botmessage-avatar">
        <ChefHatIcon />
      </div>
      <div className="message message--bot typing-bubble">
        <span className="typing-dot"></span>
        <span className="typing-dot"></span>
        <span className="typing-dot"></span>
      </div>
    </div>
  );
}

export default TypingIndicator;
