# -*- coding: utf-8 -*-

from pathlib import Path
def load_chunks():
    chunks = []
    for path in sorted(Path("data").glob("*.md")):
        text = path.read_text(encoding="utf-8")

        sections = []
        for line in text.splitlines():
            if line.startswith("## "):
                sections.append({"title": line[3:].strip(), "lines": []})
            elif sections:
                sections[-1]["lines"].append(line)

        for number, section in enumerate(sections, start=1):
            chunk_id = f"{path.stem}-{number:02d}"
            body = "\n".join(section["lines"]).strip()

            chunks.append({
                "chunk_id": chunk_id,
                "title": section["title"],
                "text": body,
                "source": path.name,
            })
    return chunks