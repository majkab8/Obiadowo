import RecipeCard from "./RecipeCard.jsx";
import { ChefHatIcon } from "../icons/Icons.jsx";

function ChatMessage({ message, sender, recipe }) {
  return (
    <div className={`message-row message-row--${sender}`}>
      {sender === "bot" && (
        <div className="botmessage-avatar">
          <ChefHatIcon />
        </div>
      )}
      {recipe ? (
        <RecipeCard recipe={recipe} />
      ) : (
        <div className={`message message--${sender}`}>{message}</div>
      )}
    </div>
  );
}

export default ChatMessage;
