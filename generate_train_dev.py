# generate_train_val.py
# This script merges all *_corpus.json files in the 'data/' directory,
# extracts (ocr_sent, ori_sent) from each sample, shuffles the data,
# and splits into train.jsonl (80%) and dev.jsonl (20%).

import os
import json
import random


def main():
    # Define paths
    data_dir = "./data"
    output_train = os.path.join(data_dir, "train.jsonl")
    output_dev = os.path.join(data_dir, "dev.jsonl")

    # Collect all corpus JSON files
    corpus_files = [
        f for f in os.listdir(data_dir)
        if f.endswith("_corpus.json")
    ]

    all_pairs = []

    # Read each corpus file
    for corpus_file in corpus_files:
        corpus_path = os.path.join(data_dir, corpus_file)
        with open(corpus_path, "r", encoding="utf-8") as f:
            samples = json.load(f)
        # Each sample has: {"ori_sent": "...", "ocr_sent": "...", "diffs": [...]}
        for s in samples:
            ocr_text = s.get("ocr_sent", "").strip()
            ori_text = s.get("ori_sent", "").strip()
            # Only keep samples with non-empty texts
            if ocr_text and ori_text:
                all_pairs.append((ocr_text, ori_text))

    # Shuffle the combined list
    random.shuffle(all_pairs)

    # Split 80/20 into train/dev
    split_idx = int(len(all_pairs) * 0.8)
    train_data = all_pairs[:split_idx]
    dev_data = all_pairs[split_idx:]

    # Write out to train.jsonl
    with open(output_train, "w", encoding="utf-8") as f_out:
        for (ocr_text, ori_text) in train_data:
            record = {
                "input_text": ocr_text,
                "target_text": ori_text
            }
            f_out.write(json.dumps(record, ensure_ascii=False) + "\n")

    # Write out to dev.jsonl
    with open(output_dev, "w", encoding="utf-8") as f_out:
        for (ocr_text, ori_text) in dev_data:
            record = {
                "input_text": ocr_text,
                "target_text": ori_text
            }
            f_out.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"[INFO] Merged {len(all_pairs)} pairs.")
    print(f"[INFO] Train set: {len(train_data)} -> {output_train}")
    print(f"[INFO] Dev set: {len(dev_data)} -> {output_dev}")


if __name__ == "__main__":
    main()
