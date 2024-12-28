# src/visually_similar_characters.py
import os
import json
from pprint import pprint
from collections import defaultdict
from src.config.config import PROJECT_DIR

def build_similar_char_dict():
    visually_similar_characters = defaultdict(set)
    data_dir = os.path.join(PROJECT_DIR, 'data')
    for filename in os.listdir(data_dir):
        if filename.endswith("_corpus.json"):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                samples = json.load(f)
            for sample in samples:
                for diff_item in sample["diffs"]:
                    correct_char = diff_item[1]
                    ocr_char = sample["ocr_sent"][diff_item[0]]

                    if '\u4e00' <= correct_char <= '\u9fff':  # check if it's a chinese character
                        visually_similar_characters[correct_char].add(ocr_char)

    return visually_similar_characters


if __name__ == '__main__':
    similar_char_dict = build_similar_char_dict()
    # show 10
    for idx, (char, confusions) in enumerate(similar_char_dict.items()):
        print(f"{char}: {confusions}")
        if idx > 8:
            break
