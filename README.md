# 🍽️ Obiadowo

**AI-powered Polish recipe assistant** — tell it what ingredients you have, and it suggests a dish with a full recipe card: ingredients, steps, macronutrients, and a tip.

🔗 **Live demo:** https://obiadowo.vercel.app
_(free-tier CPU hosting — the first request after the app has been idle may take ~30–60 s to warm up)_

<!-- TODO: add a screenshot or short GIF here — it's the single biggest boost to a portfolio README -->
<!-- ![Obiadowo screenshot](docs/screenshot.png) -->

---

## What it does
- 💬 **Chat interface** — describe the ingredients you have (in Polish)
- 🔎 **RAG** over ~200 real recipes scraped
- 🧾 **Rich recipe card** — title, time, servings, diet tags, calories, a macronutrient bar, ingredients, numbered steps, and a tip
- 🤖 Steps & tip written by **a custom fine-tuned Polish model**

## The highlight: my own fine-tuned model
General-purpose models write clumsy Polish. Instead of relying on one, I trained my own small Polish model via **knowledge distillation**:

- **Teacher** — [`Bielik-11B-v3.0-Instruct`](https://huggingface.co/speakleash): used offline to generate a 212-example dataset of clean, reworded recipe steps + tips (as JSON).
- **Student** — [`Bielik-1.5B-v3.0-Instruct`](https://huggingface.co/speakleash): fine-tuned with **LoRA** (peft + trl) on that dataset, then merged into a standalone model, **"polka"** → [`Mijuub/conaobiad-polka`](https://huggingface.co/Mijuub/conaobiad-polka).

The result: correct Polish from a model small enough to self-host.

| Model | Example step output |
|---|---|
| ❌ Generic model (Qwen) | _"Wgrzebaj cebulę… gotuj 15 minut na pomidziłku"_ — invented words, broken grammar |
| ✅ polka (fine-tuned) | _"Podsmaż cebulę i czosnek na oliwie przez ok. 10 minut"_ — correct, clean Polish |

## Architecture
```
React (Vite)              FastAPI                  Pinecone
  Vercel      ──POST /chat──▶  HF Spaces  ──search──▶  (recipe DB)
  frontend                     backend    ──generate──▶ polka (HF Hub)
```
1. User query → **local embedding** → **Pinecone** similarity search → retrieved recipe (real facts: kcal, time, diet).
2. **polka** rewords the steps in its own words + writes a tip.
3. Backend returns a structured `Recipe` (JSON) → frontend renders the card.
4. A simple **in-memory cache** returns repeated queries instantly.

## Tech stack
- **Frontend:** React, Vite, Chart.js (macro bar) — deployed on **Vercel**
- **Backend:** FastAPI — deployed on **Hugging Face Spaces** (Docker)
- **RAG:** `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` (local embeddings) + **Pinecone**
- **Model:** Bielik-1.5B fine-tuned with **LoRA** (peft, trl, transformers)
- **Scraping:** BeautifulSoup

## Run locally
### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate            # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
# create a .env file (see .env.example):
#   PINECONE_API_KEY=your_key
#   ALLOWED_ORIGINS=http://localhost:5173
cd core
uvicorn main:app --reload
```
The model is pulled automatically from the Hugging Face Hub (`Mijuub/conaobiad-polka`).

### Frontend
```bash
cd frontend
npm install
# optional .env:  VITE_API_URL=http://localhost:8000   (defaults to localhost if unset)
npm run dev
```

## Reproduce the model pipeline
Scripts live in `backend/site_scraping/` and `backend/fine_tuning/`:
1. `save_recipes.py` — scrape recipes → `recipes.json`
2. `filter_recipes.py` — drop empty/invalid ones → `recipes_clean.json`
3. `generate_dataset.py` — Bielik-11B (teacher) generates targets → `recipes_bielik.jsonl`
4. `finetune.py` — LoRA fine-tune Bielik-1.5B on the dataset
5. `merge_polka.py` — merge the LoRA adapter into a standalone model → push to the HF Hub

## Known limitations & future work
- **Cold start:** free CPU hosting makes the first request after idle slow (container wake-up + generation).
- **Tips:** occasionally generic — a small model has its limits. Planned: better distillation targets for the tip.
- **Planned feature:** a copyable shopping list ("what am I missing for this recipe?").

## Acknowledgements
- **[Bielik](https://huggingface.co/speakleash) / SpeakLeash** — the base Polish models (teacher & student).

## Contact

Maja Bednarek

- GitHub: [majkab8](https://github.com/majkab8)
- Email: [bednarekmaja02@gmail.com]
- LinkedIn: [https://www.linkedin.com/in/maja-bednarek-599119324/]
