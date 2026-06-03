from transformers import AutoTokenizer, AutoModelForCausalLM
from config import BASE_MODEL, MAX_LENGTH, DEVICE, MODELS_DIR

def generate(prompt, model_name=None, max_new=80, temperature=0.7,
             top_p=0.9, num_return=1):
    model_path = MODELS_DIR / "convo-model"
    if model_path.exists() and model_name is None:
        model_name = str(model_path)

    model_name = model_name or BASE_MODEL

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_name)

    device = DEVICE if DEVICE != "mps" or (DEVICE == "mps" and AutoModelForCausalLM is not None) else "cpu"
    if DEVICE == "mps":
        import torch
        if torch.backends.mps.is_available():
            model = model.to("mps")
            device = "mps"
        else:
            device = "cpu"

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new,
        temperature=temperature,
        top_p=top_p,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        num_return_sequences=num_return,
    )

    results = []
    for out in outputs:
        text = tokenizer.decode(out, skip_special_tokens=True)
        results.append(text)
        print(f"\n--- Response ---")
        print(text)

    return results

if __name__ == "__main__":
    import sys
    prompt = sys.argv[1] if len(sys.argv) > 1 else "You: Hello\nAI:"
    generate(prompt)
