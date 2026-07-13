function RecipeCard({ recipe }) {
  return (
    <div className="recipe-card">
      <div className="recipe-card-title">
        <h3>{recipe.title}</h3>
      </div>
      <div className="recipe-card-info">
        {recipe.time && (
          <span className="recipe-card-time"> {recipe.time}</span>
        )}
        {recipe.servings && (
          <span className="recipe-card-servings"> {recipe.servings}</span>
        )}
        {recipe.diet && (
          <span className="recipe-card-diet"> {recipe.diet}</span>
        )}
        {recipe.calories && (
          <span className="recipe-card-calories"> {recipe.calories}</span>
        )}
      </div>
      <div className="recipe-card-ingredients">
        <ul>
          {recipe.ingredients.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      </div>
      <div className="recipe-card-steps">
        <ol>
          {recipe.steps.map((step, i) => (
            <li key={i}>{step}</li>
          ))}
        </ol>
      </div>
      <div className="recipe-card-tip">
        {recipe.tip && <p>💡 {recipe.tip}</p>}
      </div>
    </div>
  );
}

export default RecipeCard;
