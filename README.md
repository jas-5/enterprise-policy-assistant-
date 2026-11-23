# enterprise-policy-assistant

企业制度问答助手（学习项目）。目标：把公司制度 Markdown 切成条款 → 建索引 → 用检索回答"报销几天内要提交"这类问题。

## 进度

- [x] Day 2：读 `data/` 下制度文件，按 `##` 小标题切条款并打印
- [ ] Day 3：条款向量化 + 检索

## 运行

```bash
python ingest.py
```

输出示例：

```text
[travel-policy-01] 报销时限 | 出差结束后 7 天内提交报销申请。 | 来源：travel-policy.md
```

## 目录

```text
data/           制度 Markdown，一个 `##` 一条规定
ingest.py       加载 + 按标题切分 + 打印
```
