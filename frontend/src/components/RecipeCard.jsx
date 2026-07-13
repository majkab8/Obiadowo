import { ClockIcon } from "../icons/Icons.jsx";
import { ServingsIcon } from "../icons/Icons.jsx";
import MacroBar from "./MacroBar.jsx";

function RecipeCard({ recipe }) {
  const [calNumber, calUnit] = recipe.calories.split(" ");

  return (
    <div className="recipe-card">
      <div className="recipe-card-title">
        <h3>{recipe.title}</h3>
      </div>
      <div className="recipe-card-info">
        {recipe.time && (
          <span className="recipe-card-time">
            <ClockIcon size={23} /> {recipe.time}
          </span>
        )}
        {recipe.servings && (
          <span className="recipe-card-servings">
            <ServingsIcon size={20} /> {recipe.servings}
          </span>
        )}
      </div>
      <div className="recipe-card-nutrition">
        {recipe.calories && (
          <div className="recipe-card-calories">
            <span className="recipe-card-calories-number"> {calNumber}</span>
            <span className="recipe-card-calories-unit"> {calUnit}</span>
            <span className="recipe-card-calories-label"> / 100g</span>
          </div>
        )}
        <div className="recipe-card-diets">
          {recipe.diet.split(",").map((d) => (
            <span key={d} className="recipe-card-diet">
              {d.trim()}
            </span>
          ))}
        </div>
      </div>
      <MacroBar
        protein={recipe.protein}
        carbs={recipe.carbs}
        fat={recipe.fat}
        sugar={recipe.sugar}
      />
      <div className="recipe-card-ingredients">
        <h4 className="recipe-card-ingredients-title">Składniki:</h4>
        <ul className="recipe-card-ingredients-list">
          {recipe.ingredients.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      </div>
      <div className="recipe-card-steps">
        <ul className="recipe-card-steps-list">
          {recipe.steps.map((step, i) => (
            <li className="recipe-card-step" key={i}>
              <span className="step-number">{i + 1}</span>
              {step}
            </li>
          ))}
        </ul>
      </div>
      <div className="recipe-card-tip">
        {recipe.tip && <p>💡 {recipe.tip}</p>}
      </div>
    </div>
  );
}

export default RecipeCard;
