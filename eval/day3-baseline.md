# Day 3 向量检索与问答基线

题集来自 `data/` 的两份模拟制度，共 6 条。使用 `BAAI/bge-small-zh-v1.5` 在 CPU 上编码，内存向量索引每题取前 3 条，交给 `deepseek-flash` 生成回答。记录来自两次终端运行，候选按检索顺序记录。

```powershell
.\.venv\Scripts\python.exe -X utf8 ask.py
```

| ID | 问题 | 预期证据 | 实际候选 | 实际回答与引用 |
| --- | --- | --- | --- | --- |
| D3-01 | 出差后多久要报销？ | `travel-policy-01` | `travel-policy-01`、`leave-policy-03`、`leave-policy-02` | 出差结束后 7 天内提交报销申请。引用 `travel-policy-01`。 |
| D3-02 | 公司餐补每天多少？ | 无对应条款 | `leave-policy-01`、`travel-policy-03`、`travel-policy-01` | 当前制度资料中找不到可引用的依据。无引用。 |
| D3-03 | 入职满一年有几天年假？ | `leave-policy-01` | `leave-policy-01`、`leave-policy-02`、`leave-policy-03` | 5 天带薪年假。引用 `leave-policy-01`。 |
| D3-04 | 一线城市出差住宿每晚最高多少元？ | `travel-policy-03` | `travel-policy-03`、`travel-policy-01`、`travel-policy-02` | 500 元。引用 `travel-policy-03`。 |
| D3-05 | 公司每月几号发工资？ | 无对应条款 | `leave-policy-01`、`travel-policy-01`、`leave-policy-03` | 当前制度资料中找不到可引用的依据。无引用。 |

3 道有答案题的预期证据均排第 1，2 道缺证据题均输出依据不足提示。报销题第 2、3 条候选来自请假制度，可用于比较后续检索方法是否减少无关候选。
