#docs 是刚搜到的三份原文，`context` 是加上条款编号后实际发给模型的文字。"
#最后的 allowed_ids 检查由 Python 执行，模型报出一个本次没搜到的编号，程序就不会展示那条答案。"

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from search import store

load_dotenv(Path(__file__).with_name(".env"))
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise SystemExit("请在项目根目录的 .env 中填写 DEEPSEEK_API_KEY。")

llm = ChatOpenAI(
    model="deepseek-flash",
    base_url="https://api.deepseek.com",
    api_key=api_key,
    extra_body={"thinking": {"type": "disabled"}},
    max_tokens=512,
).bind(response_format={"type": "json_object"})

for question in [
    "出差后多久要报销？",
    "公司餐补每天多少？",
    "入职满一年有几天年假？",
    "一线城市出差住宿每晚最高多少元？",
    "公司每月几号发工资？",
]:
    docs = store.similarity_search(question, k=3)
    allowed_ids = {doc.metadata["chunk_id"] for doc in docs}
    context = "\n\n".join(
        f"[{doc.metadata['chunk_id']}]\n{doc.page_content}" for doc in docs
    )

    print(f"\n问题：{question}")
    print(f"发给模型的资料：\n{context}")

    prompt = f"""只根据给定资料回答问题。返回 JSON，例如：
{{"answer": "答案正文", "citations": ["对应的条款编号"]}}
只引用直接支持答案的条款。资料不足时返回：
{{"answer": "当前制度资料中找不到依据。", "citations": []}}

资料：
{context}

问题：{question}
"""
    response = llm.invoke(prompt)
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        print("模型没有返回可读取的 JSON。")
        continue

    citations = result["citations"]
    if not citations or any(ref not in allowed_ids for ref in citations):
        print("回答：当前制度资料中找不到可引用的依据。")
        continue

    print(f"回答：{result['answer']}")
    print(f"引用：{', '.join(citations)}")
