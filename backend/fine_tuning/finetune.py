import json
from pathlib import Path
import torch
from datasets import Dataset
from peft import LoraConfig, TaskType
from transformers import AutoTokenizer, AutoModelForCausalLM
from trl import SFTConfig, SFTTrainer

path = Path(__file__).parent / "recipes_bielik.jsonl"
records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

model_name = "speakleash/Bielik-1.5B-v3.0-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map={"": 0}, dtype=torch.bfloat16)

lora_config = LoraConfig(
    r=32,
    lora_alpha=64,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

training_args = SFTConfig(
    output_dir=str(Path(__file__).parent / "polka-lora"),
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    learning_rate=1e-4,
    logging_steps=10,
    save_strategy="epoch",
    bf16=True,
    max_length=2048
)

SYSTEM = "Jesteś pomocnym polskim kucharzem. Odpowiadasz wyłącznie po polsku."
def to_example(record):
    target = json.dumps({"steps": record["steps"], "tip": record["tip"]}, ensure_ascii=False)
    return {"messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": record["prompt"]},
        {"role": "assistant", "content": target},
    ]}

examples = [to_example(record) for record in records]
dataset = Dataset.from_list(examples)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    processing_class=tokenizer,
    peft_config=lora_config
)

trainer.train()

