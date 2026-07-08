function ChatMessage({ message, sender }) {
  return <div className={`message message--${sender}`}>{message}</div>;
}

export default ChatMessage;
