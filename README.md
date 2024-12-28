- [English](README.md)
- [中文](readme/README.zh_CN.md)

## Automated Generation of Chinese Text Correction Corpora

**Project Introduction**  
This project aims to automatically construct Chinese text correction corpora from text-based PDF documents and OCR outputs. The overall workflow is as follows:

1. **PDF Preprocessing**  
   - Extract “correct text” from text-based PDFs using PyMuPDF (fitz).
   - Convert each PDF page to a PNG image for OCR.

2. **OCR**  
   - Use PaddleOCR on the PNG images to obtain text that may contain OCR errors.

3. **Corpus Construction**  
   - Compare the “correct text” and “erroneous text” by applying similarity checks, character difference thresholds, etc.
   - Automatically generate high-quality text correction pairs (error → correct).

**Key Features**  
- **PDF Text Extraction**: Retrieve text from PDF blocks.  
- **OCR**: Obtain imperfect text for error modeling.  
- **Automated Alignment**: Match correct vs. OCR text to build correction pairs.  
- **Similar Characters**: Generate a dictionary of visually similar characters for deeper analysis.

**Model Training & Evaluation**  
- You can fine-tune a Seq2Seq model (e.g., T5) on this corpus, using `(ocr_sent, ori_sent)` pairs.
- Evaluate the model using a custom test set to assess correction performance.
