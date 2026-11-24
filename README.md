# enterprise-policy-assistant

企业制度问答助手（学习项目）。目标：把公司制度 Markdown 切成条款 → 建索引 → 用检索回答"报销几天内要提交"这类问题。

## 进度

- [x] Day 2：读 `data/` 下制度文件，按 `##` 小标题切条款并打印
- [x] Day 3：内存向量检索、带引用问答和证据不足提示

## 运行

在项目根目录用 PowerShell 创建环境并安装依赖，已有 `.venv` 可以继续使用。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install langchain-core langchain-huggingface sentence-transformers langchain-openai python-dotenv
```

仅运行向量检索，查看报销和年假两题的前三条候选及分数。首次运行会下载 `BAAI/bge-small-zh-v1.5`。

```powershell
.\.venv\Scripts\python.exe -X utf8 search.py
```

运行问答前，在项目根目录的 `.env` 中填入 `DEEPSEEK_API_KEY=你的密钥`。脚本依次运行五道题，并打印送给模型的资料、回答和引用。[Day 3 五题实测记录](eval/day3-baseline.md)

```powershell
.\.venv\Scripts\python.exe -X utf8 ask.py
```

## 目录

```text
data/           制度 Markdown，一个 `##` 一条规定
ingest.py       加载、按标题切分并返回条款
search.py       建立内存向量索引，打印检索候选
ask.py          用检索结果生成问答并检查引用编号
eval/           保留固定题目和实测结果
```
