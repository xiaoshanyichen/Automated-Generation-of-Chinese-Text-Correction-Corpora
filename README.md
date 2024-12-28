# Automated-Generation-of-Chinese-Text-Correction-Corpora

[English](javascript:showEnglish()) | [中文](javascript:showChinese())

<div id="english-content" style="display: block; margin-top: 20px;">
  
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

</div>


<div id="chinese-content" style="display: none; margin-top: 20px;">

## 自动化生成中文文本纠错语料

**项目简介**  
该项目致力于从文字版 PDF 文档以及 OCR 识别结果中，**自动化构建中文文本纠错语料**。主要流程如下：

1. **PDF 预处理**  
   - 使用 PyMuPDF（fitz）从文本型 PDF 提取相对准确的“正确文本”。
   - 将每页 PDF 转成 PNG 图片，以便后续 OCR 使用。

2. **OCR**  
   - 利用 PaddleOCR 对图片进行文字识别，从而得到带有 OCR 错误的文本。

3. **语料构建**  
   - 通过相似度、字符差异度等规则比对“正确文本”与“错误文本”。
   - 自动形成高质量文本纠错对（错误 → 正确）。

**项目功能**  
- **PDF 文本提取**：从 PDF 中获取基础的正确文本。  
- **OCR 转写**：生成带错误的文本。  
- **自动匹配**：对比正确与错误文本，产出纠错对。  
- **形近字分析**：统计并输出常见易混淆字映射，助力后续研究。

- **模型训练与测试**  
- 你可以使用 `(ocr_sent, ori_sent)` 训练一个序列到序列的中文纠错模型（如 T5）。
- 通过预先准备的测试集来验证模型对于 OCR 错别字的纠正效果。

</div>

<script>
function showEnglish() {
  document.getElementById('english-content').style.display = 'block';
  document.getElementById('chinese-content').style.display = 'none';
}

function showChinese() {
  document.getElementById('english-content').style.display = 'none';
  document.getElementById('chinese-content').style.display = 'block';
}
</script>
