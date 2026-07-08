function SuggestionButton({ text, onClick }) {
  return (
    <button className="suggestion-button" onClick={() => onClick(text)}>
      {text}
    </button>
  );
}

export default SuggestionButton;
