# train_correction_model.py
# This script trains a text-correction Seq2Seq model using a T5-style architecture
# and the train.jsonl/dev.jsonl data produced by 'generate_train_val.py'.

import os
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments
)


def main():
    # Specify your model name
    # You can switch to other T5-based models that support Chinese
    model_name = "uer/t5-base-chinese-cluecorpussmall"

    # Paths to your train/dev JSON lines
    data_dir = "./data"
    train_file = os.path.join(data_dir, "train.jsonl")
    dev_file = os.path.join(data_dir, "dev.jsonl")

    # Load datasets
    raw_datasets = load_dataset(
        "json",
        data_files={
            "train": train_file,
            "validation": dev_file
        }
    )

    # Initialize tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Preprocessing function
    def preprocess_function(examples):
        inputs = examples["input_text"]
        targets = examples["target_text"]

        # Encode inputs
        model_inputs = tokenizer(inputs, max_length=128, truncation=True)

        # Encode targets
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(targets, max_length=128, truncation=True)

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    # Map function to each split
    tokenized_datasets = raw_datasets.map(preprocess_function, batched=True)

    # Data collator for Seq2Seq
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    # Training arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir="./checkpoints/",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        num_train_epochs=3,  # Adjust as needed
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        logging_steps=50,
        learning_rate=1e-4,
        predict_with_generate=True
    )

    # Build the trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        tokenizer=tokenizer,
        data_collator=data_collator
    )

    # Train
    trainer.train()

    # You could add trainer.save_model() here if needed
    # Or rely on the epoch-based saves in output_dir


if __name__ == "__main__":
    main()

