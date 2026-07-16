import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from pathlib import Path
from tqdm import tqdm

device = "cuda"

model_name = "speakleash/Bielik-11B-v3.0-Instruct"

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=quant_config, device_map={"": 0})

clean_recipes = json.load(open(Path(__file__).parent / "recipes_clean.json", encoding="utf-8"))

results = []
failed = []
out = Path(__file__).parent / "recipes_bielik.jsonl"
with open(out, "w", encoding="utf-8") as f:
    for recipe in tqdm(clean_recipes):
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

        model_inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", return_dict=True).to(device)

        generated_ids = model.generate(**model_inputs, max_new_tokens=512, do_sample=False)

        input_len = model_inputs["input_ids"].shape[-1]
        answer = tokenizer.decode(generated_ids[0][input_len:], skip_special_tokens=True)

        try:
            start = answer.find("{")
            end = answer.rfind("}") + 1
            data = json.loads(answer[start:end])
            results.append({"prompt": prompt, "steps": data["steps"], "tip": data["tip"]})
            f.write(json.dumps(results[-1], ensure_ascii=False) + "\n")
            f.flush()
        except (json.JSONDecodeError, KeyError):
            failed.append(recipe["title"])

print(f"OK recipes: {len(results)}, failed recipes: {len(failed)}")