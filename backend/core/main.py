import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from config import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.output_parsers import PydanticOutputParser


os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = settings.GEMINI_API_KEY

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    output_dimensionality=768
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

llm_endpoint = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    max_new_tokens=1024,
    huggingfacehub_api_token=settings.HF_TOKEN,
    temperature=0.3
)

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

class RecipeAIExtras(BaseModel):
    steps: list[str]
    tip: str

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

llm = ChatHuggingFace(llm=llm_endpoint)
parser = PydanticOutputParser(pydantic_object=RecipeAIExtras)
@app.post("/chat", response_model=Recipe)
def chat(request: ChatRequest):
    results = vector_store.similarity_search(request.message, k=1)
    context = "\n\n".join(doc.page_content for doc in results)
    prompt =f"""Jesteś polskim pomocnym kucharzem. Odpowiadaj wyłącznie po polsku. Użytkownik ma składniki: {request.message}

To przepis z bazy:
{context}

Przepisz kroki własnymi słowami, krócej (nie kopiuj dosłownie) i dodaj krótką wskazówkę, jak wpleść jego składniki, które zostały. Kroki i wskazówka muszą być po polsku. Nie używaj innych języków.
{parser.get_format_instructions()}"""

    recipe = doc_to_recipe(results[0])
    response = llm.invoke(prompt)
    out = parser.parse(response.content)
    recipe.steps = out.steps
    recipe.tip = out.tip
    return recipe

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
