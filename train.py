base_model_hf = "togethercomputer/RedPajama-INCITE-Chat-3B-v1" #@param {type: "string"}
finetune_epochs = 5 #@param {type: "integer"}

ADAPTERS_NAME='RedPajama-LoRA' #@param {type: "string"}

import wandb
import torch 
import torch.nn as nn 
import time
import json
import transformers 
from datasets import Dataset, load_dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "togethercomputer/RedPajama-INCITE-Chat-3B-v1", 
    device_map='auto',
)

tokenizer = AutoTokenizer.from_pretrained("togethercomputer/RedPajama-INCITE-Chat-3B-v1")
tokenizer.pad_token = tokenizer.eos_token

for param in model.parameters():
  param.requires_grad = False  # freeze the model - train adapters later
  if param.ndim == 1:
    # cast the small parameters (e.g. layernorm) to fp32 for stability
    param.data = param.data.to(torch.float32)

model.gradient_checkpointing_enable()  # reduce number of stored activations
model.enable_input_require_grads()

def print_trainable_parameters(model):
    """
    Prints the number of trainable parameters in the model.
    """
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(
        f"trainable params: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param}"
    )

config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["query_key_value", "xxx"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, config)
print_trainable_parameters(model)


# impotr dataset from train.json, specifying that this only has training data
dataset = load_dataset("json", data_files={"train": "train.json"})
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=256)
dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])
dataset = dataset["train"]

wandb.init(project="lucygpt-redpajama-base-3b", 
           name=str(time.time()))

trainer = transformers.Trainer(
    model=model, 
    train_dataset=dataset,
    args=transformers.TrainingArguments(
        per_device_train_batch_size=16, 
        gradient_accumulation_steps=16,
        warmup_steps=20, 
        learning_rate=3e-4, 
        fp16=True,
        num_train_epochs=finetune_epochs,
        logging_steps=1, 
        output_dir='outputs',
        report_to="wandb"
    ),
    data_collator=transformers.DataCollatorForLanguageModeling(tokenizer, mlm=False)
)

model.config.use_cache = False

import os
trainer.train()

wandb.finish()

model.save_pretrained(f"{ADAPTERS_NAME}")
