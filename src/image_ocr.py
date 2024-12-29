# src/image_ocr.py
import json
import os
from paddleocr import PaddleOCR

from src.config.config import PROJECT_DIR


def get_pdf_file_ocr_result(pdf_file_dir_path: str) -> dict[int, str]:
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")
    page_ocr_result = {}
    files = [file for file in os.listdir(pdf_file_dir_path) if file.endswith(".png")]

    files.sort(key=lambda x: int(x.split(".")[0]))
    for file in files:
        text = ""
        page_no = int(file.split(".")[0])
        img_path = os.path.join(pdf_file_dir_path, file)
        result = ocr.ocr(img_path, cls=False)
        for idx in range(len(result)):
            res = result[idx]
            if res:
                for line in res:
                    text += line[1][0]
                    print(f"page: {page_no}, text: {line[1][0]}")
        page_ocr_result[page_no] = text

    # save ocr result in json
    json_output_path = os.path.join(pdf_file_dir_path, "ocr_result.json")
    with open(json_output_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(page_ocr_result, ensure_ascii=False, indent=4))
    return page_ocr_result


if __name__ == '__main__':
    pdf_file_name = "deguo_tongshi"
    pdf_dir_path = os.path.join(PROJECT_DIR, f"output/{pdf_file_name}")

    ocr_result = get_pdf_file_ocr_result(pdf_dir_path)
    print("OCR Done!")
