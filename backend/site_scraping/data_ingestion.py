import json
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from site_scraper import download_recipes
from cleaning_text import clean_recipe_text

load_dotenv()
INDEX_NAME = "recipes-index"

if "PINECONE_API_KEY" not in os.environ:
    print("PINECONE_API_KEY not set in .env file")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    model_kwargs={"device": "cuda"},
)

def upload_recipes_to_pinecone(scraped_recipes):
    if not scraped_recipes:
        print("No recipes to upload")
        return

    texts = []
    metadata = []

    for recipe in scraped_recipes:
        clean_ingredients = clean_recipe_text(recipe['ingredients'])

        full_text = f"Title: {recipe['title']}\nIngredients:\n{clean_ingredients}\nInstructions: {recipe['instructions']}"
        texts.append(full_text)

        nutrition = recipe.get('nutrition', {})

        metadata.append({
            'title': recipe['title'],
            'url': recipe['url'],
            'ingredients': clean_ingredients,
            'instructions': recipe['instructions'],
            'source_text': full_text,
            'time': recipe.get('time', ''),
            'cooking_time': recipe.get('cooking_time', ''),
            'servings': recipe.get('servings', ''),
            'diet': recipe.get('diet', ''),
            'calories': nutrition.get('calories', ''),
            'carbs': nutrition.get('carbs', ''),
            'sugar': nutrition.get('sugar', ''),
            'protein': nutrition.get('protein', ''),
            'fat': nutrition.get('fat', ''),
        })

    print(f"Sending {len(texts)} recipes to pinecone")

    vector_store = PineconeVectorStore.from_texts(
        texts=texts,
        embedding=embeddings,
        index_name=INDEX_NAME,
        metadatas=metadata
    )
    print("Successfully uploaded recipes to pinecone.")

if __name__ == "__main__":
    print("Scraping recipes")
    category_url = "https://aniagotuje.pl/pomysl-na/obiad"
    domain = "https://aniagotuje.pl"

    with open("recipes.json", encoding="utf-8") as f:
        recipes = json.load(f)
    print(f"Loaded {len(recipes)} recipes")
    upload_recipes_to_pinecone(recipes)