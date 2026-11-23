# -*- coding: utf-8 -*-
"""Day 2：读取 data/ 下的制度 Markdown，按 `##` 小标题切成条款并打印。

对应 All-in-RAG 第二章的两个知识点：
- 04_data_load.md     数据加载：把文件读成程序能处理的字符串
- 05_text_chunking.md 文本分块（3.4 基于文档结构的分块）：
  按标题聚合内容，并把「标题 + 来源文件名」当作元数据挂到每个块上。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
HEADING_PREFIX = "## "


@dataclass
class Clause:
    """一条制度规定，字段顺序对应打印格式。"""

    clause_id: str  # travel-policy-01
    title: str      # 报销时限
    text: str       # 出差结束后 7 天内提交报销申请。
    source: str     # travel-policy.md


def load_markdown(path: Path) -> str:
    """读一个 Markdown 文件，统一成 \\n 换行。

    用 utf-8-sig 而不是 utf-8：Windows 记事本存出来的文件可能带 BOM，
    带着 BOM 读会让第一行的小标题前面多一个不可见字符，匹配不上。
    这里必须显式指定编码，否则 Windows 默认按 GBK 读，中文直接报错或乱码。
    """
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def split_clauses(raw: str, source: str) -> list[Clause]:
    """按二级标题切分：每遇到一个 `##` 就开一条新条款，直到下一个 `##`。"""
    stem = Path(source).stem
    groups: list[tuple[str, list[str]]] = []
    title: str | None = None
    body: list[str] = []

    for line in raw.split("\n"):
        if line.startswith(HEADING_PREFIX):
            if title is not None:                 # 收掉上一条
                groups.append((title, body))
            title = line[len(HEADING_PREFIX):].strip()
            body = []
            continue
        if title is not None:                     # 第一个 `##` 之前的内容不归属任何条款
            body.append(line)

    if title is not None:                         # 文件末尾收尾
        groups.append((title, body))

    clauses: list[Clause] = []
    for index, (clause_title, lines) in enumerate(groups, start=1):
        # 多行内容压成一行，保证打印时一条规定只占一行
        text = " ".join(part.strip() for part in lines if part.strip())
        clauses.append(
            Clause(
                clause_id=f"{stem}-{index:02d}",  # 按文件内顺序编号，跑多少次都一样
                title=clause_title,
                text=text,
                source=source,
            )
        )
    return clauses


def main() -> None:
    files = sorted(DATA_DIR.glob("*.md"))         # sorted 保证每次顺序一致
    if not files:
        print(f"没在 {DATA_DIR} 找到 Markdown 文件。")
        return

    total = 0
    for path in files:
        clauses = split_clauses(load_markdown(path), path.name)
        if not clauses:
            print(f"[跳过] {path.name} 里没有 `## ` 小标题")
            continue
        for clause in clauses:
            print(f"[{clause.clause_id}] {clause.title} | {clause.text} | 来源：{clause.source}")
        total += len(clauses)

    print(f"\n共 {len(files)} 个文件、{total} 条条款。")


if __name__ == "__main__":
    main()
