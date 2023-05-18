from transformers import AutoModelForCausalLM, Trainer, TrainingArguments, AutoTokenizer, DataCollatorWithPadding, TrainingArguments
from peft import get_peft_config, get_peft_model, LoraConfig, TaskType
from datasets import load_dataset

model_name_or_path = "togethercomputer/RedPajama-INCITE-Base-3B-v1"
tokenizer_name_or_path = "togethercomputer/RedPajama-INCITE-Base-3B-v1"

# CREATE TOKENIZER
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name_or_path)

# CREATE MODEL
model = AutoModelForCausalLM.from_pretrained(
    model_name_or_path,
)
peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM, inference_mode=False, r=16, lora_alpha=32, lora_dropout=0.1
)
model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

# CREATE DATASET
dataset = load_dataset("json", data_files={"train": "data_generation/train.json"})
def tokenize_function(examples):
    return tokenizer(examples["text"])
tokenized_datasets = dataset.map(tokenize_function, batched=True)
print(tokenized_datasets)

# CREATE TRAINER
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
training_args = TrainingArguments(
    output_dir="test_trainer", 
    label_names=["labels"]
)
trainer = Trainer(
    model=model, 
    args=training_args, 
    train_dataset=tokenized_datasets["train"],
    data_collator=data_collator,
    tokenizer=tokenizer,
)
trainer.train()