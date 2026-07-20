import json
from pathlib import Path
import torch
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM

device = "cuda" if torch.cuda.is_available() else "cpu"
path = "Mijuub/conaobiad-polka"
model = AutoModelForCausalLM.from_pretrained(path, dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained(path)

class RecipeAIExtras(BaseModel):
    steps: list[str]
    tip: str

def generate_steps_and_tips(title, ingredients, instructions):
    prompt = f"""Oto przepis:

Tytuł: {title}

Składniki: {ingredients}

Instrukcje (mogą być chaotyczne i powtórzone):
{instructions}

Przepisz kroki własnymi słowami, krótko i po kolei uwzględniając ważne szczegóły.
Na końcu dodaj jedną krótką wskazówkę. Odpowiadaj wyłącznie po polsku. Odpowiedz wyłącznie w formacie JSON, bez dodatkowego tekstu i bez ```:
{{"steps": ["pierwszy krok", "drugi krok"], "tip": "krótka wskazówka"}}"""

    messages = [
        {"role": "system", "content": "Jesteś pomocnym polskim kucharzem. Odpowiadasz wyłącznie po polsku."},
        {"role": "user", "content": prompt},
    ]

    model_inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt",
                                                 return_dict=True).to(device)
    generated_ids = model.generate(**model_inputs, max_new_tokens=512, do_sample=False)

    input_len = model_inputs["input_ids"].shape[-1]
    answer = tokenizer.decode(generated_ids[0][input_len:], skip_special_tokens=True)
    start = answer.find("{")
    end = answer.rfind("}") + 1
    data = json.loads(answer[start:end])

    return RecipeAIExtras(**data)