# -*- coding: utf-8 -*-
"""Day 2：读取 data/ 下的制度 Markdown，按 `##` 小标题切成条款并打印。

对应 All-in-RAG 第二章的两个知识点：
- 04_data_load.md     数据加载：把文件读成程序能处理的字符串
- 05_text_chunking.md 文本分块（3.4 基于文档结构的分块）：
  按标题聚合内容，并把「标题 + 来源文件名」当作元数据挂到每个块上。
"""

from pathlib import Path

for path in sorted(Path("data").glob("*.md")):
    text = path.read_text(encoding="utf-8")
    print(path.name)

    sections = []
    for line in text.splitlines():
        if line.startswith("## "):
            sections.append({"title": line[3:].strip(), "lines": []})
        elif sections:
            sections[-1]["lines"].append(line)

    for number, section in enumerate(sections, start=1):
        chunk_id = f"{path.stem}-{number:02d}"
        body = "\n".join(section["lines"]).strip()

        print(f"[{chunk_id}] {section['title']}")
        print(body)
        print(f"来源：{path.name}")
        print()