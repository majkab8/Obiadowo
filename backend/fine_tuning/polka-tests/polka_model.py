from pathlib import Path
import torch
from peft import PeftModel
from transformers import AutoTokenizer, AutoModelForCausalLM

device = "cuda"
model_name = "speakleash/Bielik-1.5B-v3.0-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map={"": 0}, dtype=torch.bfloat16)
model = PeftModel.from_pretrained(model, str(Path(__file__).parent / "polka-lora" / "checkpoint-81"))

merged_model = model.merge_and_unload()
merged_model.save_pretrained(str(Path(__file__).parent / "polka"))
tokenizer.save_pretrained(str(Path(__file__).parent / "polka"))