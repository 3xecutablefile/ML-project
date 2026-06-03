# Local conversational ai 

Retrained GPT-2 for simple English conversations.

## Quick Start

```bash
pip install -r requirements.txt
python3 dataset/build_data.py     # generate training data
python3 main.py train --epochs 3  # fine-tune GPT-2
python3 main.py generate "You: Hello"  # chat with it
```

## Commands

| Command | Description |
|---------|-------------|
| `train` | Fine-tune GPT-2 on conversation data |
| `generate` | Generate a response from a prompt |

### Train options

`--epochs`, `--batch`, `--lr`, `--data` (folder with .txt files)

### Generate options

`--max-new`, `--temperature`, `--top-p`, `--model` (path to fine-tuned model)

## Structure

```
├── dataset/         # .txt files (one conversation per paragraph)
├── models/          # saved fine-tuned models
├── outputs/         # training checkpoints
├── train.py         # fine-tuning logic
├── generate.py      # text generation
├── main.py          # CLI entry point
└── config.py        # configuration
```
