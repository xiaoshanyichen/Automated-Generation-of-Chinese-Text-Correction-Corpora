# evaluate_model.py
# This script can load a trained checkpoint and test multiple lines of OCR sentences.

import os
from transformers import pipeline

def main():
    model_path = "./checkpoints/checkpoint-1000"
    corrector = pipeline("text2text-generation", model=model_path, tokenizer=model_path)

    # Provide a file of OCR lines to test, one sentence per line
    input_file = "test_sentences.txt"
    output_file = "test_results.txt"

    with open(input_file, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
        for line in f_in:
            ocr_sentence = line.strip()
            if not ocr_sentence:
                continue

            # Perform inference
            result = corrector(ocr_sentence, max_length=128, num_beams=4)
            corrected_text = result[0]["generated_text"]

            # Write results
            f_out.write(f"OCR: {ocr_sentence}\n")
            f_out.write(f"Corrected: {corrected_text}\n")
            f_out.write("------\n")

    print("[INFO] Batch inference completed.")
    print(f"[INFO] See output in {output_file}")

if __name__ == "__main__":
    main()
