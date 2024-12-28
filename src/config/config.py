# src/config/config.py

import os

# 获取当前文件(config.py)所在的目录
_current_dir = os.path.dirname(os.path.abspath(__file__))

# 假设项目的结构类似：
# my_text_ocr_project/
# ├── docs/
# ├── output/
# ├── data/
# ├── src/
# │   └── config/
# │       └── config.py   <-- 这里
#
# 那么项目根目录即再向上两级
PROJECT_DIR = os.path.abspath(os.path.join(_current_dir, '../../'))

# 你也可以定义更多的路径配置（可选），例如：
# PDF 文档目录
DOCS_DIR = os.path.join(PROJECT_DIR, 'docs')
# 输出目录
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'output')
# 数据目录（语料库、统计结果等）
DATA_DIR = os.path.join(PROJECT_DIR, 'data')

# 如果还有其他全局配置，如日志级别、数据库连接等，都可在这里添加
LOG_LEVEL = "INFO"
# DB_CONNECTION_STRING = "mysql://user:password@host:port/db_name"

if __name__ == "__main__":
    # 测试：打印这些路径，检查是否符合预期
    print("PROJECT_DIR:", PROJECT_DIR)
    print("DOCS_DIR:", DOCS_DIR)
    print("OUTPUT_DIR:", OUTPUT_DIR)
    print("DATA_DIR:", DATA_DIR)
