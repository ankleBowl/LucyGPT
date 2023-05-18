from datasets import load_dataset

dataset = load_dataset("json", data_files={"train": "data_generation/train.json"})

from transformers import AutoModelForCausalLM, Trainer, TrainingArguments, AutoTokenizer, DataCollatorWithPadding
from peft import get_peft_config, get_peft_model, LoraConfig, TaskType
model_name_or_path = "togethercomputer/RedPajama-INCITE-Base-3B-v1"
tokenizer_name_or_path = "togethercomputer/RedPajama-INCITE-Base-3B-v1"

tokenizer = AutoTokenizer.from_pretrained(tokenizer_name_or_path)

model = AutoModelForCausalLM.from_pretrained(
    model_name_or_path,
    load_in_8bit=True,
)

peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM, inference_mode=False, r=8, lora_alpha=32, lora_dropout=0.1
)

model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

from transformers import TrainingArguments
training_args = TrainingArguments("test_trainer")

trainer = Trainer(
    model=model, 
    args=training_args, 
    train_dataset=dataset["train"],
    data_collator=data_collator,
    tokenizer=tokenizer,
)

trainer.train()