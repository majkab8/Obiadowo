from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from config import settings
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

class ChatResponse(BaseModel):
    reply: str
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    #request.message skladniki od uzytkownika
    return {"reply": "..."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# class Recipe(BaseModel):
#     id: str
#     ingredients: list
#     instructions: str
#     source_text: str
#     text: str
#     title: str
#     url: str
#
# class Recipes(BaseModel):
#     recipes: List[Recipe]
#
# @app.get("/recipes", response_model=Recipes)
# def get_recipes():
#     return {"message": "Hello World!"}