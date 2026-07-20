import SuggestionButton from "./SuggestionButton.jsx";
import { FoodPlateIcon } from "../icons/Icons.jsx";

function EmptyChat({ onPick }) {
  const suggestions = [
    "Jajka, ser i pomidory",
    "Kurczak i ryż",
    "Tylko makaron i czosnek",
    "Ogórek, jogurt naturalny i koperek",
  ];

  return (
    <div className="emptychat">
      <div className="emptychat-icon">
        <FoodPlateIcon />
      </div>
      <div className="emptychat-header">
        <h1>Jakie masz składniki?</h1>
      </div>
      <div className="emptychat-text">
        <p>
          Napisz jakie składniki masz, a ja spróbuje Tobie zaproponować co
          możesz z nich upichcić!
        </p>
      </div>
      <div className="emptychat-suggestions">
        {suggestions.map((text) => (
          <SuggestionButton key={text} text={text} onClick={onPick} />
        ))}
      </div>
    </div>
  );
}

export default EmptyChat;
