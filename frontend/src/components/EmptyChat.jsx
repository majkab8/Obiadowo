import { CookingPotIcon } from "../icons/Icons.jsx";
import SuggestionButton from "./SuggestionButton.jsx";

function EmptyChat({ onPick }) {
  const suggestions = [
    "Jajka, ser i pomidory",
    "Kurczak i ryż",
    "Tylko makaron i czosnek",
    "Ogórek, jogurt naturalny i koperek",
  ];

  return (
    <div className="emptyChat">
      <div className="emptyChat-icon">
        <CookingPotIcon />
      </div>
      <div className="emptyChat-header">
        <h1>Jakie masz składniki?</h1>
      </div>
      <div className="emptyChat-text">
        <p>
          Napisz jakie składniki masz, a ja spróbuje zaproponować Ci co możesz z
          nich upichcić!
        </p>
      </div>
      <div className="emptyChat-suggestions">
        {suggestions.map((text) => (
          <SuggestionButton key={text} text={text} onClick={onPick} />
        ))}
      </div>
    </div>
  );
}

export default EmptyChat;
