- [English](README.md)
- [中文](README.zh_CN.md)

## 自动化生成中文文本纠错语料以及训练纠错模型

**项目介绍**  
在本项目中，我通过比较从 PDF 文件中提取的文本与 OCR 工具识别得到的文本，来自动化构建高质量的中文文本纠错语料。最终的目标是生成一个大型数据集，其中一条句子是从基于文字的 PDF 中直接获取的“正确”版本，另一条句子则是从同一个 PDF 内容转换成图像后再使用 OCR 获得的“错误”版本。通过系统地挖掘这两个句子间的差异，我们能够识别出单个汉字级别的错误，这些错误可以为多种下游任务提供有价值的训练数据，包括自动文本纠错模型、用于 OCR 纠错的语言模型微调，以及汉字相似度分析等。

**动机**  
有时候，我想编辑一些自己写过的旧文档，做一些微调然后保存下来，可是我手头能找到的只有当时的 PDF 版本，这就多了将文档转换成文本的一步。在这个过程中，我发现使用现有工具时，中文文本常常出现一定程度的差异（很有可能是因为很多汉字非常像，有些笔画多的字比英文字母复杂得多），而英文文本通常较为完整一致。因此，我决定开发一个语料库，并在该语料库上训练一个纠错模型，让它在第一层文本提取方法之后充当第二层修正。（主要也是把它当作一次 NLP 练习，因为我此前除了用 LLM 生成语料外，还没实际自己动手构建过语料。）

中文版还在施工中。。->
1. **PDF Preprocessing**  
   The first step is the PDF preprocessing step, which involves taking a text-based PDF file and extracting the text from each page. I used PyMuPDF (imported as fitz in Python) to obtain the textual content. The results are stored in a JSON file, mapping page indices to text content.  
   For example, check out the cover page and contents page of ***deguo_tongshi***:![Alt Text](/../assets/deguo_tongshi_cover.png) ![Alt Text](/../assets/deguo_tongshi_contents.png)
   The resulted text is:
   ```json
   {
      "0": "",
      "1": "目录\n前言\n导言　德国在哪里？\n第一章　立国时代：日耳曼人与德意志人\n一、古代日耳曼人\n二、日耳曼部族民大迁徙\n三、法兰克王国的兴衰\n四、德意志人和德意志王国的出现\n作者评曰\n第二章　封建时代：民族国家的被延误\n一、迟缓的封建化\n二、皇权与教权：争霸欧洲\n三、皇权与城市：互促还是互制？\n四、皇权与诸侯：七选侯当家\n作者评曰\n第三章　宗教改革时代：民族运动的发端\n一、路德与宗教改革\n二、骑士宗教改革\n三、人民宗教改革：闵采尔和农民战争\n四、诸侯宗教改革和反宗教改革\n五、三十年战争：宗教改革时代的悲惨结局\n作者评曰\n第四章　普鲁士崛起时代：对德意志民族是祸是福？\n一、霍亨索伦家族的统治\n二、普鲁士王国的崛起\n三、“士兵王”的军事立国\n四、弗里德里希大王的开明君主专制\n五、普鲁士精神和普奥争霸\n作者评曰\n第五章　“启蒙”时代：从文化民族主义到政治民族主义\n一、德意志的启蒙运动\n二、“狂飙突进”运动\n三、法国大革命与德意志文化民族主义\n四、拿破仑战争与德意志政治民族主义\n作者评曰\n"
   }
   ```
   This extracted text is effectively our “ground-truth” or “correct” version because text-based PDFs. However, the first page is an image-based PDF, unlike the second page which contains a font-encoded text layer that should accurately represent the publication’s intended characters, we did not get any text for the cover page.   


2. **OCR**  
   However, to simulate the kind of errors that might arise from real-world scanning or image-based PDFs, we also convert each page of the PDF into an image (for instance, PNG format). Again I will use the same PyMuPDF library, which can render each page at a chosen resolution and produce an image. Once the images are generated for each page, we apply an OCR tool, in this case PaddleOCR, to extract text from the images. It is expected that this process will produce certain recognition errors when dealing with various fonts, complex layouts, or slight image distortions. These OCR outputs constitute our “incorrect” text, a version that should in principle match the original PDF text, but will naturally deviate due to misrecognitions.   
   
   Here is an example generated from ***deguo_tongshi***, **page 83**:
   ```json
   {
      "83": "四、诸侯宗教改革和反宗教改革路德的宗教改革，正处在德意志社会内部萌生新的早期资本主义经济关系之时，因此路德教教义除了代表一种民族国家的要求外，还贯穿一种德意志特有的新教资本主义精神。由于民族运动和社会力量不足以克服封建主义，路德教教义的社会内涵也就发生变化，新教资本主义精神也遭到扭曲和阻遇。这就是为什么路德本人竭力反对农民战争的暴力行为以及城市市民阶级不支持农民起义的深层原因。路德的宗教改革被德意志诸侯所利用，成为他们劫掠和坐收渔人之利的工具。在许多诸侯邦内，仿效萨克森选侯的榜样，组织起本邦新教教会，诸侯则成为本邦教会的首脑，集本邦的国家权力和教会权力于一身，巩固了自已的权力和独立性。教士们在新教邦内成为诸侯的官员和诸侯统治的重要支柱。不仅如此，新教邦诸侯还在教产还俗的浪潮中发了大财，加强了财政实力。这种诸侯宗教改革的传播，不仅扩大了正统天主教派同宗教改革运动之间的裂痕，也遭到德皇查理五世的反对。查理五世看出，德意志各邦诸侯权力的加强，是对皇帝中央集权计划的巨大威胁。不过当时的政治形势让皇帝抽不出手来，他为了获得意大利的支配权而卷入同法国国王弗朗索瓦一世长达20年的系列战争中。在天主教集团首领皇帝不在的情况下，1522年帝国议会在纽伦堡开会。在萨克森选侯弗里德里希影响下的新教福音派（Evangelium，即路德派）集团不仅公然蔑视教皇及其使臣，而且道使帝国议会宣布上年的沃尔姆斯救令不予施行。1525年普鲁士宗教骑士团国家宣布世俗化，把路德教作为领地宗教。1526年黑森伯爵排力浦与萨克森选侯约翰，加上吕纳堡、普鲁士、马格德堡诸诸侯，形成同情路德教的第一个诸侯组织托尔高联盟，在同年的斯派耶尔帝国议会上否定了奥地利大公提出的施行沃尔姆斯救令以及禁止宗教改革的意见，通过一些有利于路德派教义的法令：把有关信仰的决定交由各邦自行处理。在天主教阵营中，巴伐利亚公爵和几位来自南德的主教，则与查理五世的弟弟，奥地利亲王斐迪南联合起来。在1529年召开的斯派耶尔帝国议会上形势陡变。皇帝在同法朗索瓦一世的战争中打了几次胜仗，加强了斐迪南和天主教集团在帝国议会的地位。查理五世的代表宣布，废止1526年斯派耶尔帝国议会的决议，重申沃尔姆斯救令。会议通过决议：严格执行沃尔姆斯敕令，不得实行宗教改革，不宽容新教各派和再洗礼派，不得剥夺大主教会的"
   }
   ```

3. **Corpus Construction**  
   We now have, for every page in the PDF, two versions of the text: one obtained via direct PDF text extraction (the presumed “correct” reference), and another obtained from the OCR-processed images (the “incorrect” text that usually contains a range of substitution, insertion, or deletion errors). The central step is to align and compare these two versions in order to identify pairs of sentences that differ minimally overall but show localized discrepancies—precisely the type of data that can form a text correction corpus.   
   The approach is to segment both the correct text and the OCR text into sentences. We can use a Chinese sentence segmentation tool, “sentencex”, to divide the raw text into manageable chunks. Then, for each OCR sentence, we look for the most similar “correct” sentence among the set of extracted reference sentences on the same page. My approach to determine whether two sentences are the "same" uses a Jaccard similarity based on the sets of characters in each sentence. If two sentences hit a Jaccard similarity above a certain threshold (I used **0.8** for ***deguo_tongshi***, but this hyperparameter can be fine-tuned per texts, consider **magazines** vs. **history books**), we assume that these two sentences are intended to be identical, aside from potential OCR mistakes.   
   For example, one discrepancy in ***deguo_tongshi*** on **page 83**:
   ```json
   {
      "ori_sent": "查理五世的代表宣布，废止1526年斯派耶尔帝国议会的决议，重申沃尔姆斯敕令。",
      "ocr_sent": "查理五世的代表宣布，废止1526年斯派耶尔帝国议会的决议，重申沃尔姆斯救令。",
        "diffs": [
            [
                35,
                "敕"
            ]
        ]
    }
   ```
   where "敕" is the original character while "救" is the ocr-sent character. One can easily spot the similarity in terms of looking alike between these characters.  

**Utilities**  
Not only is this corpus useful for training an OCR correction model (for instance, a seq2seq model such as T5 that translates erroneous text to correct text), but it also allows us to discover systematic confusions between visually similar Chinese characters. As an interesting byproduct, we can collect all pairs of distinct characters that were encountered in the “diffs” field across the entire corpus. Often, certain frequent confusions surface repeatedly, indicating that some characters, from a typography or stroke-based perspective, are more likely to get confused in OCR outputs. Examples might be “冉” vs “再,” “毽” vs “键,” or “颐” vs “顾.” These confusions can be further leveraged to build a dictionary of visually similar character mappings and eventually used to enhance our correction engine or to guide data augmentation strategies.  
The script for collecting such dictionary is provided in [visually_similar_characters.py](./../src/visually_similar_characters.py)

**Model Training**  
1. **Data Preparation**  
We started with a corpus of approximately 10,000 sentence pairs, each containing one OCR-erroneous sentence (ocr_sent) and the corresponding correct sentence (ori_sent). These pairs were randomly shuffled and split into training (80%), validation (10%), and testing (10%) sets. The data was stored in JSON Lines format, with each line including both the input text (ocr_sent) and the target text (ori_sent).


2. **Model Architecture and Hyperparameters**  
We used a T5-style model designed for Chinese: uer/t5-base-chinese-cluecorpussmall. The maximum input and output sequence lengths were each set to 128. We employed a batch size of 4 for both training and validation, a learning rate of 1e-4, and ran training for 3 epochs. These values were chosen to strike a balance between GPU memory constraints and model performance.


3. **Training Procedure**  
The training script followed the Hugging Face Seq2SeqTrainer framework. The DataCollatorForSeq2Seq handled dynamic padding and label alignment for the encoder-decoder architecture. A validation step occurred at the end of each epoch, storing checkpoints that included both model weights and optimizer states. Across epochs, the training loss should steadily decrease, indicating that the model was learning to map incorrect characters to their correct counterparts.


4. **Validation and Results**  
Working on it...