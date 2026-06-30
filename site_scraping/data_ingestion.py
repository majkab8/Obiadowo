import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from site_scraper import download_recipes
from cleaning_text import clean_recipe_text

load_dotenv()
GEMINI_KEY = os.environ["GEMINI_API_KEY"]
INDEX_NAME = "recipes-index"

if "PINECONE_API_KEY" not in os.environ:
    print("PINECONE_API_KEY not set in .env file")

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_KEY,
    output_dimensionality=768
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

        metadata.append({
            'title': recipe['title'],
            'url': recipe['url'],
            'ingredients': clean_ingredients,
            'instructions': recipe['instructions'],
            'source_text': full_text
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
    print("Scraping recipes Scraping -> Pinecone")
    category_url = "https://aniagotuje.pl/pomysl-na/obiad"
    domain = "https://aniagotuje.pl"

    recipes = download_recipes(category_url, domain)
    upload_recipes_to_pinecone(recipes)