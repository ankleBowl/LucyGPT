import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model

def load_base_model(model_name, tokenizer_name):
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    return model, tokenizer

def load_peft_model(model, peft_model_name):
    model.load_state_dict(torch.load(f'{peft_model_name}/pytorch_model.bin'))
    return model

def get_peft_model_with_config(model):
    config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["query_key_value", "xxx"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, config)
    return model

def generate_text(prompt, model, tokenizer):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=500, do_sample=True, temperature=0.7)
    return tokenizer.decode(outputs[0])

if __name__ == "__main__":
    base_model_hf = "mosaicml/mpt-7b-chat"
    tokenizer_model_hf = "EleutherAI/gpt-neox-20b"
    peft_model_name = "RedPajama-LoRA"
    
    model, tokenizer = load_base_model(base_model_hf, tokenizer_model_hf)
    model = get_peft_model_with_config(model)
    model = load_peft_model(model, peft_model_name)

    # test the model
    prompt = "You are"
    generated_text = generate_text(prompt, model, tokenizer)
    print(generated_text)