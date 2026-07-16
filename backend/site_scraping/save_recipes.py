import json

from site_scraper import download_recipes

category_url = "https://aniagotuje.pl/pomysl-na/obiad"
domain = "https://aniagotuje.pl"

recipes = download_recipes(category_url, domain)

with open("recipes.json", "w", encoding="utf-8") as f:
    json.dump(recipes, f, ensure_ascii=False, indent=2)

print(f"Found {len(recipes)} recipes!")
