from langchain_core.output_parsers import PydanticOutputParser
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from pydantic import BaseModel
from config import settings

llm_endpoint = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    max_new_tokens=1024,
    huggingfacehub_api_token=settings.HF_TOKEN,
    temperature=0.3
)

class RecipeAIExtras(BaseModel):
    steps: list[str]
    tip: str

llm = ChatHuggingFace(llm=llm_endpoint)
parser = PydanticOutputParser(pydantic_object=RecipeAIExtras)

def generate_steps_and_tips(context, ingredients):
    prompt = f"""Jesteś polskim pomocnym kucharzem. Odpowiadaj wyłącznie po polsku. Użytkownik ma składniki: {ingredients}

    To przepis z bazy:
    {context}

    Przepisz kroki własnymi słowami, krócej (nie kopiuj dosłownie) i dodaj krótką wskazówkę, jak wpleść jego składniki, które zostały. Kroki i wskazówka muszą być po polsku. Nie używaj innych języków.
    {parser.get_format_instructions()}"""

    response = llm.invoke(prompt)
    out = parser.parse(response.content)

    return out