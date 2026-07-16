import json
from pathlib import Path

BASE = Path(__file__).parent
src = BASE.parent / "site_scraping" / "recipes.json"
out = BASE / "recipes_clean.json"

with open(src, "r", encoding="utf-8") as json_file:
    recipes = json.load(json_file)
print(len(recipes))

recipes_clean = []
for recipe in recipes:
    if recipe["instructions"].strip() not in ("", "Brak.", "Brak"):
        recipes_clean.append(recipe)

with open(out, "w", encoding="utf-8") as clean_file:
    json.dump(recipes_clean, clean_file, ensure_ascii=False, indent=2)
print(len(recipes_clean))
