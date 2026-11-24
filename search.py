# 把标题和正文放进 page_content，让 embedding 模型根据这两段文字检索"
#编号和来源放进 metadata，搜到之后还能知道这段原文出自哪儿。"

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

from ingest import load_chunks

documents = []
for chunk in load_chunks():
    document = Document(
        page_content=chunk["title"] + "\n" + chunk["text"],
        metadata={
            "chunk_id": chunk["chunk_id"],
            "source": chunk["source"],
        },
    )
    documents.append(document)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs={"device": "cpu"},
)
store = InMemoryVectorStore(embeddings)
store.add_documents(documents)

if __name__ == "__main__":
    for question in ["出差后多久要报销？", "入职满一年有几天年假？"]:
        print(f"\n问题：{question}")
        for doc, score in store.similarity_search_with_score(question, k=3):
            print(f"{score:.3f} [{doc.metadata['chunk_id']}] {doc.metadata['source']}")
            print(doc.page_content)
