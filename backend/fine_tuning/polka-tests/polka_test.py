import json
from pathlib import Path
import torch
from peft import PeftModel
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda"
model_name = "speakleash/Bielik-1.5B-v3.0-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map={"": 0}, dtype=torch.bfloat16)
model = PeftModel.from_pretrained(model, str(Path(__file__).parent / "polka-lora" / "checkpoint-81"))


clean_recipes = json.load(open(Path(__file__).parent / "recipes_clean.json", encoding="utf-8"))
recipe = clean_recipes[5]

prompt = f"""Oto przepis:

Tytuł: {recipe["title"]}

Składniki: {recipe["ingredients"]}

Instrukcje (mogą być chaotyczne i powtórzone):
{recipe["instructions"]}

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
print(answer)