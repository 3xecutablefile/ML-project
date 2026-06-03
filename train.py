import torch
from pathlib import Path
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
from config import BASE_MODEL, EPOCHS, BATCH_SIZE, LEARNING_RATE, MAX_LENGTH, DEVICE, DATASET_DIR, MODELS_DIR, OUTPUTS_DIR

def load_texts(data_dir):
    texts = []
    for f in sorted(Path(data_dir).glob("*.txt")):
        if f.name == "build_data.py":
            continue
        content = f.read_text(encoding="utf-8", errors="ignore").strip()
        blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
        texts.extend(blocks)
    if not texts:
        texts = [""]
    return texts

def train(data_dir=None, model_name=BASE_MODEL, epochs=EPOCHS,
          batch_size=BATCH_SIZE, lr=LEARNING_RATE, max_length=MAX_LENGTH):
    data_dir = data_dir or str(DATASET_DIR)

    raw_texts = load_texts(data_dir)
    if not raw_texts:
        print(f"No .txt files found in {data_dir}")
        print("Put .txt files in dataset/ and run again.")
        return

    print(f"Loaded {len(raw_texts)} text blocks from {data_dir}")

    dataset = Dataset.from_dict({"text": raw_texts})
    split = dataset.train_test_split(test_size=0.1, seed=42)
    train_ds, eval_ds = split["train"], split["test"]

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(model_name)

    def tok(examples):
        return tokenizer(examples["text"], truncation=True, max_length=max_length)

    train_tok = train_ds.map(tok, batched=True, remove_columns=["text"])
    eval_tok = eval_ds.map(tok, batched=True, remove_columns=["text"])

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    device_map = DEVICE if DEVICE != "mps" or (DEVICE == "mps" and torch.backends.mps.is_available()) else "cpu"
    if device_map == "mps":
        model = model.to("mps")

    args = TrainingArguments(
        output_dir=str(OUTPUTS_DIR),
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=lr,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=10,
        load_best_model_at_end=True,
        save_total_limit=2,
        fp16=False,
        use_cpu=DEVICE == "cpu",
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_tok,
        eval_dataset=eval_tok,
        data_collator=data_collator,
    )

    trainer.train()

    out_path = MODELS_DIR / "convo-model"
    out_path.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(out_path))
    tokenizer.save_pretrained(str(out_path))
    print(f"\nModel saved to {out_path}")

    return trainer

if __name__ == "__main__":
    train()
