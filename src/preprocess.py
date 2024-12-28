# src/preprocess.py
import os
import json
import time
import fitz  # PyMuPDF
from PIL import Image
from src.config.config import PROJECT_DIR


def get_pdf_file_text(pdf_file_path: str) -> dict[int, str]:
    doc = fitz.open(pdf_file_path)
    page_result = {}
    for i in range(doc.page_count):
        page = doc[i]
        text = ""
        # obtain blocks of the page
        page_content = page.get_text("blocks")
        for record in page_content:
            # record[4] is text，record[-1] is a boolean indicating if this is an image
            if not record[-1]:
                text += record[4]
        page_result[i] = text
    doc.close()

    # save as a JSON file
    pdf_file_name = os.path.basename(pdf_file_path).split(".")[0]
    output_dir = os.path.join(PROJECT_DIR, f"output/{pdf_file_name}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    json_output_path = os.path.join(output_dir, "original_text.json")
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(page_result, f, ensure_ascii=False, indent=4)
    return page_result


def convert_pdf_2_img(pdf_file: str) -> list[str]:
    pdf_document = fitz.open(pdf_file)
    output_image_file_path_list = []
    pdf_file_name = os.path.basename(pdf_file).split(".")[0]
    output_dir = os.path.join(PROJECT_DIR, f"output/{pdf_file_name}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        save_image_path = os.path.join(output_dir, f"{page_number}.png")
        image.save(save_image_path)
        output_image_file_path_list.append(save_image_path)

    pdf_document.close()
    return output_image_file_path_list


if __name__ == '__main__':
    s_time = time.time()
    file_name = "weite.pdf"
    file_path = os.path.join(PROJECT_DIR, f"docs/{file_name}")

    # PDF -> PNG
    output_image_path_list = convert_pdf_2_img(file_path)

    # get PDF original text
    original_text = get_pdf_file_text(file_path)

    print(f"Done! Elapsed: {time.time() - s_time:.2f} s")
