#!/usr/bin/env python3
import argparse
from train import train
from generate import generate

def main():
    parser = argparse.ArgumentParser(description="GPT-2 text generation — fine-tune on custom data")
    sub = parser.add_subparsers(dest="command", required=True)

    train_p = sub.add_parser("train", help="Fine-tune GPT-2 on text files in dataset/")
    train_p.add_argument("--data", help="Path to folder with .txt files (default: dataset/)")
    train_p.add_argument("--model", default="gpt2", help="Base model name")
    train_p.add_argument("--epochs", type=int, default=3)
    train_p.add_argument("--batch", type=int, default=4)
    train_p.add_argument("--lr", type=float, default=5e-5)
    train_p.add_argument("--device", default="cpu", help="Device to use (cpu or cuda)")

    gen_p = sub.add_parser("generate", help="Generate text from trained model")
    gen_p.add_argument("prompt", help="Text prompt")
    gen_p.add_argument("--model", help="Model path (default: models/fine-tuned-gpt2)")
    gen_p.add_argument("--max-new", type=int, default=100)
    gen_p.add_argument("--temperature", type=float, default=0.8)
    gen_p.add_argument("--top-p", type=float, default=0.9)
    gen_p.add_argument("--num-return", type=int, default=1)

    args = parser.parse_args()

    if args.command == "train":
        train(
            data_dir=args.data,
            model_name=args.model,
            epochs=args.epochs,
            batch_size=args.batch,
            lr=args.lr,
            device=args.device,
        )
    elif args.command == "generate":
        generate(
            prompt=args.prompt,
            model_name=args.model,
            max_new=args.max_new,
            temperature=args.temperature,
            top_p=args.top_p,
            num_return=args.num_return,
        )

if __name__ == "__main__":
    main()
