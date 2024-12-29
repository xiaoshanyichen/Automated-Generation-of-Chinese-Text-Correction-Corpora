# src/corpus_generator.py
import os
import json
import difflib
from sentencex import segment
from src.config.config import PROJECT_DIR


def text_preprocess(text: str) -> str:
    return text.replace("\n", "").strip()


def get_sentences(text: str) -> list[str]:
    return segment("zh", text)


def find_similar_sentence(ocr_sent: str, candidate_sentences: list[str]) -> str:
    """
    If length of sentences are the same and they have jaccard similarity > 0.8, consider the same
    """
    for candidate_sent in candidate_sentences:
        if ocr_sent == candidate_sent:
            # if they are 100% similar, return
            return candidate_sent
        if len(ocr_sent) == len(candidate_sent):
            set_ocr = set(ocr_sent)
            set_candidate = set(candidate_sent)
            jaccard_sim = len(set_ocr & set_candidate) / len(set_ocr | set_candidate)
            if jaccard_sim > 0.8:
                return candidate_sent
    return ""


def find_differences(s1: str, s2: str):
    """
    return the index and character that are not identical in s1 and s2
    """
    matcher = difflib.SequenceMatcher(None, s1, s2)
    differences = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != 'equal':
            # unmatched
            for i in range(i1, i2):
                differences.append((i, s1[i]))
    return differences


def get_corpus(original_text: str, ocr_text: str) -> list[dict]:
    """
    get diff pairs in two text files
    """
    corpus_list = []
    original_sents = get_sentences(text_preprocess(original_text))
    ocr_sents = get_sentences(text_preprocess(ocr_text))

    for ocr_sent in ocr_sents:
        if len(ocr_sent) <= 4:
            continue
        similar_sent = find_similar_sentence(ocr_sent, original_sents)
        if similar_sent:
            diffs = find_differences(similar_sent, ocr_sent)
            if 0 < len(diffs) < 6:  # diff character threshold
                corpus_list.append({
                    "ori_sent": similar_sent,
                    "ocr_sent": ocr_sent,
                    "diffs": diffs
                })

    return corpus_list


if __name__ == '__main__':
    pdf_file_name = "deguo_tongshi"
    pdf_dir_path = os.path.join(PROJECT_DIR, f"output/{pdf_file_name}")
    ocr_result_file_path = os.path.join(pdf_dir_path, "ocr_result.json")
    original_text_file_path = os.path.join(pdf_dir_path, "original_text.json")

    with open(ocr_result_file_path, "r", encoding="utf-8") as f:
        ocr_result_dict = json.load(f)

    with open(original_text_file_path, "r", encoding="utf-8") as f:
        original_text_dict = json.load(f)

    final_corpus_list = []
    for page_idx, ocr_page_text in ocr_result_dict.items():
        page_idx = str(page_idx)
        if page_idx in original_text_dict:
            correct_text = original_text_dict[page_idx]
            page_corpus_list = get_corpus(correct_text, ocr_page_text)
            final_corpus_list.extend(page_corpus_list)

    # save json in file
    json_output_path = os.path.join(PROJECT_DIR, f"data/{pdf_file_name}_corpus.json")
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(final_corpus_list, f, ensure_ascii=False, indent=4)

    print(f"found {len(final_corpus_list)} diff characters，saving to {json_output_path}")
