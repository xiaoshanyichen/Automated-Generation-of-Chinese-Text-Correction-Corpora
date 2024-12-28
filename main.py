# main.py
# This script processes all PDF files in the 'docs/' directory step by step:
# 1) PDF preprocessing
# 2) OCR
# 3) Generate correction corpus

import os
import time
import json

# Import functions from your existing modules
from src.preprocess import convert_pdf_2_img, get_pdf_file_text
from src.image_ocr import get_pdf_file_ocr_result
from src.corpus_generator import text_preprocess, get_sentences, find_differences
from src.config.config import PROJECT_DIR

def process_single_pdf(pdf_file_name: str):
    """
    Process a single PDF file end-to-end:
    1) Convert each page to image and extract the correct text from the PDF
    2) Perform OCR on the images
    3) Compare OCR text and correct text to generate a correction corpus
    """
    pdf_path = os.path.join(PROJECT_DIR, "docs", pdf_file_name)
    pdf_name_no_ext = os.path.splitext(pdf_file_name)[0]

    print(f"[INFO] Processing PDF: {pdf_path}")
    start_time = time.time()

    # Step 1) PDF Preprocessing
    convert_pdf_2_img(pdf_path)
    get_pdf_file_text(pdf_path)
    print(f"[INFO] PDF Preprocessing completed in {time.time() - start_time:.2f}s")

    # Step 2) OCR
    pdf_output_dir = os.path.join(PROJECT_DIR, "output", pdf_name_no_ext)
    print(f"[INFO] Performing OCR on images in {pdf_output_dir}")
    t1 = time.time()
    get_pdf_file_ocr_result(pdf_output_dir)
    print(f"[INFO] OCR completed in {time.time() - t1:.2f}s")

    # Step 3) Corpus Generation
    original_text_path = os.path.join(pdf_output_dir, "original_text.json")
    ocr_result_path = os.path.join(pdf_output_dir, "ocr_result.json")

    # Load JSON data for original text and OCR text
    with open(original_text_path, "r", encoding="utf-8") as f:
        original_text_dict = json.load(f)
    with open(ocr_result_path, "r", encoding="utf-8") as f:
        ocr_text_dict = json.load(f)

    t2 = time.time()
    final_corpus_list = []
    # Iterate over pages
    for page_str, ocr_page_text in ocr_text_dict.items():
        if page_str in original_text_dict:
            correct_text = original_text_dict[page_str]
            # Generate correction pairs for each page
            page_corpus = generate_page_corpus(correct_text, ocr_page_text)
            final_corpus_list.extend(page_corpus)

    # Save the final correction corpus for this PDF
    corpus_output_path = os.path.join(PROJECT_DIR, "data", f"{pdf_name_no_ext}_corpus.json")
    with open(corpus_output_path, "w", encoding="utf-8") as f:
        json.dump(final_corpus_list, f, ensure_ascii=False, indent=4)

    print(f"[INFO] Generated {len(final_corpus_list)} corpus items for {pdf_file_name}, "
          f"saved to {corpus_output_path}. Elapsed: {time.time() - t2:.2f}s")
    print("========================================================")


def generate_page_corpus(correct_text: str, ocr_text: str) -> list:
    """
    Generate correction pairs for one PDF page using simple Jaccard-based matching.
    It compares each OCR sentence with all correct sentences of the same page,
    identifies the best match, and collects differences.
    """
    corpus_list = []

    original_sents = get_sentences(text_preprocess(correct_text))
    ocr_sents = get_sentences(text_preprocess(ocr_text))

    for ocr_sent in ocr_sents:
        if len(ocr_sent) < 4:
            continue
        best_candidate = ""
        best_sim = 0.0

        # Find the most similar correct sentence based on Jaccard similarity
        for candidate in original_sents:
            if len(candidate) == len(ocr_sent):
                set_ocr = set(ocr_sent)
                set_candidate = set(candidate)
                jaccard_sim = len(set_ocr & set_candidate) / len(set_ocr | set_candidate)
                if jaccard_sim > best_sim:
                    best_sim = jaccard_sim
                    best_candidate = candidate

        # If the best match meets the threshold, record differences
        if best_sim >= 0.8:
            diffs = find_differences(best_candidate, ocr_sent)
            if 0 < len(diffs) < 6:
                corpus_list.append({
                    "ori_sent": best_candidate,
                    "ocr_sent": ocr_sent,
                    "diffs": diffs
                })

    return corpus_list


if __name__ == "__main__":
    overall_start_time = time.time()

    # Step 0) Scan all PDF files in docs/ directory
    doc_dir = os.path.join(PROJECT_DIR, "docs")
    pdf_files = [f for f in os.listdir(doc_dir) if f.lower().endswith(".pdf")]

    print(f"[INFO] Found {len(pdf_files)} PDF files in {doc_dir}")

    # Process each PDF file
    for pdf_file in pdf_files:
        process_single_pdf(pdf_file)

    print(f"[INFO] All tasks completed! Total time: {time.time() - overall_start_time:.2f}s")
