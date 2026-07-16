import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel, Field
from config import settings
from langchain_pinecone import PineconeVectorStore
from model import generate_steps_and_tips

os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    model_kwargs={"device": "cuda"},
)

vector_store = PineconeVectorStore.from_existing_index(
    index_name="recipes-index",
    embedding=embeddings
)
app = FastAPI(
    title="Conaobiad API",
    description="api to create nice dinner ideas",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class Recipe(BaseModel):
    title: str = Field(description="Nazwa dania")
    time: str = Field(description="Czas wykonania, np. '30 min'")
    cooking_time: str = Field(description="Czas gotowania, np. '30 min'")
    servings: str = Field(description="Liczba porcji, np. '2 porcje'")
    diet: str = Field(description="Dieta")
    calories: str = Field(description="Wartości odżywcze")
    protein: str = Field(description="Białko")
    carbs: str = Field(description="Węglowodany")
    fat: str = Field(description="Tłuszcze")
    sugar: str = Field(description="Cukry")
    ingredients: list[str] = Field(description="Lista składników")
    steps: list[str] = Field(description="Kroki przygotowania, po kolei")
    tip: str = Field(default="", description="Wskazówka")

def doc_to_recipe(doc):
    m = doc.metadata
    ingredients = [line.strip() for line in m.get("ingredients", "").split("\n") if line.strip()]
    steps = [line.strip() for line in m.get("instructions", "").split("\n") if line.strip()]

    return Recipe(
        title=m.get("title", ""),
        time=m.get("time", ""),
        cooking_time=m.get("cooking_time", ""),
        servings=m.get("servings", ""),
        diet=m.get("diet", ""),
        calories=m.get("calories", ""),
        protein=m.get("protein", ""),
        carbs=m.get("carbs", ""),
        fat=m.get("fat", ""),
        sugar=m.get("sugar", ""),
        ingredients=ingredients,
        steps=steps,
    )
@app.post("/chat", response_model=Recipe)
def chat(request: ChatRequest):
    results = vector_store.similarity_search(request.message, k=1)
    context = "\n\n".join(doc.page_content for doc in results)
    recipe = doc_to_recipe(results[0])
    extras = generate_steps_and_tips(context, request.message)
    recipe.steps = extras.steps
    recipe.tip = extras.tip

    return recipe

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
