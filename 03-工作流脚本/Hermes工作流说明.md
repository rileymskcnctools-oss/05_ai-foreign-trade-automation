# Hermes 工作流设计

> 用"小白也能懂"的方式讲解
> 你不需要写代码，只需要理解逻辑

---

## 一、Hermes 是什么？

Hermes 是一个 AI Agent（智能助手）。
它可以：

- 读取文件
- 调用 AI（Qwen3.6-plus）
- 处理数据
- 保存结果

**简单说**：Hermes 就是一个帮你干活的"数字员工"。

---

## 二、单产品处理流程

### 步骤 1：告诉 Hermes 读取产品数据

你对 Hermes 说：

```
请读取桌面上的产品参数表，找到 GF-001 这个产品的所有信息。
```

Hermes 会：

- 打开 Excel 文件
- 找到 product_id = GF-001 的那一行
- 读取所有字段的信息

### 步骤 2：告诉 Hermes 组装 Prompt

你对 Hermes 说：

```
用 GF-001 的产品信息，填充 SEO 标题的 Prompt 模板。
模板在：02-Prompt模板库/01-SEO标题Prompt.md
```

Hermes 会：

- 打开 Prompt 模板
- 把 `{product_name_en}` 替换成 "Garden Fork"
- 把 `{material}` 替换成 "Carbon Steel + Ash Wood"
- 把所有 `{大括号}` 都替换成实际数据
- 生成一个完整的 Prompt

### 步骤 3：告诉 Hermes 调用 AI

你对 Hermes 说：

```
把组装好的 Prompt 发给 Qwen，让它生成 SEO 标题。
```

Hermes 会：

- 把完整的 Prompt 发给 Qwen3.6-plus
- 等待 Qwen 返回结果
- 拿到 AI 生成的 5 个 SEO 标题

### 步骤 4：告诉 Hermes 保存结果

你对 Hermes 说：

```
把生成的 SEO 标题保存到 05-输出结果/GF-001_seo_titles.csv
```

Hermes 会：

- 创建一个 CSV 文件
- 把 5 个标题写入文件
- 保存完成

---

## 三、实际操作示例

### 第一次：手动跑通一个产品

这是你第一天要做的事——不用代码，纯手动：

**Step 1：准备产品数据**
你已经有了 Excel，里面有 GF-001 的信息。

**Step 2：手动填充 Prompt**
打开 `02-Prompt模板库/01-SEO标题Prompt.md`
把 `{大括号}` 替换成 GF-001 的实际数据。

**Step 3：发送给 Qwen**
把填充好的完整 Prompt 发给 Qwen3.6-plus。

**Step 4：复制结果**
把 AI 返回的 5 个标题复制到 `05-输出结果/` 文件夹中。

**Step 5：重复**
对卖点、WhatsApp、RFQ 等每个 Prompt 都做一次。

---

## 四、批量处理逻辑（第 2 周学习）

### 批量处理是什么？

"批量"就是：对每个产品，做同样的事。

```
产品 A → 生成 SEO 标题 → 保存
产品 B → 生成 SEO 标题 → 保存
产品 C → 生成 SEO 标题 → 保存
...
```

### 用外卖店比喻批量处理

想象你经营一家外卖店：

- 今天接到 10 个订单
- 每个订单都要：接单 → 做菜 → 打包 → 配送
- 流程一样，只是每个订单的菜不同

批量处理也是一样：

- 有 10 个产品
- 每个产品都要：读数据 → 组装 Prompt → 调用 AI → 保存结果
- 流程一样，只是每个产品的数据不同

### 批量处理的步骤

```
Step 1：读取所有产品
  Hermes 打开 Excel，读取所有行
  结果：产品列表 [A, B, C, D, ...]

Step 2：对每个产品循环
  对于 产品A：
    → 组装 Prompt
    → 调用 AI
    → 保存结果
  对于 产品B：
    → 组装 Prompt
    → 调用 AI
    → 保存结果
  对于 产品C：
    → ...

Step 3：全部完成
  生成汇总报告
```

---

## 五、Hermes 读取 Excel 的方法

### 方法 1：用 Python 读取（推荐）

Hermes 可以用 Python 读取 Excel 文件：

```python
# 这是 Python 代码，你不需要写，Hermes 会帮你执行
import pandas as pd

# 读取 Excel
df = pd.read_excel("产品参数表.xlsx")

# 查看所有产品
print(df[['product_id', 'product_name_en']].to_string())

# 查看某一个产品
product = df[df['product_id'] == 'GF-001'].iloc[0]
print(f"产品名: {product['product_name_en']}")
print(f"材质: {product['material']}")
```

### 方法 2：导出为 CSV 再读取

CSV 是纯文本格式，更简单：

```python
import csv

# 读取 CSV
with open("products.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"处理产品: {row['product_id']}")
        # 对每个产品做处理...
```

### 方法 3：直接用 Hermes 的读取文件功能

你可以直接对 Hermes 说：

```
读取 01-产品数据库模板/产品参数表.xlsx 的内容
```

Hermes 会用 `read_file` 工具读取文件内容。

---

## 六、Hermes 调用 Qwen 的方法

Hermes 内部会调用 Qwen3.6-plus，你只需要：

### 手动方式

直接对 Hermes 说：

```
请用以下 Prompt 调用 Qwen：

你是一个 SEO 专家...（完整的 Prompt）
```

### 自动化方式（第 2 周）

Hermes 会自动：

1. 从 Excel 读取产品数据
2. 填充 Prompt 模板
3. 调用 Qwen
4. 保存结果

---

## 七、输出结果保存

### 保存格式选择

| 格式       | 适用场景        | 优点        | 缺点     |
| -------- | ----------- | --------- | ------ |
| CSV      | 表格数据（标题、参数） | Excel 可打开 | 不适合长文本 |
| TXT      | 长文本（话术、详情）  | 简单直接      | 不结构化   |
| JSON     | 结构化数据       | AI 友好     | 人看略复杂  |
| Markdown | 详情页文案       | 格式化       | 需要渲染   |

### 推荐的文件结构

```
05-输出结果/
├── 汇总/
│   ├── all_seo_titles.csv          # 所有产品的 SEO 标题
│   ├── all_selling_points.csv      # 所有产品的卖点
│   └── all_whatsapp_scripts.csv    # 所有产品的 WhatsApp 话术
├── GF-001/
│   ├── seo_titles.json
│   ├── selling_points.json
│   ├── whatsapp_scripts.json
│   ├── alibaba_detail.md
│   ├── rfq_reply.txt
│   └── market_versions/
│       ├── nigeria.json
│       └── germany.json
├── GF-002/
│   └── ...
└── GF-003/
    └── ...
```

---

## 八、完整工作流示例

### 你要对 Hermes 说的话（Day 12 的实操）

```
请帮我完成以下任务：

1. 读取桌面上的产品参数表，找到 GF-001 的所有信息

2. 用这些信息填充 SEO 标题 Prompt 模板
   （模板在 02-Prompt模板库/01-SEO标题Prompt.md）

3. 把填充好的 Prompt 发给 Qwen，让它生成 5 个 SEO 标题

4. 把结果保存到 05-输出结果/GF-001/seo_titles.json

5. 重复步骤 2-4，但用卖点描述 Prompt 模板
   保存到 05-输出结果/GF-001/selling_points.json

6. 完成后告诉我结果
```

这就是一个完整的产品处理流程！

---

## 九、关键概念对照表

| 技术术语   | 大白话           | 外卖比喻           |
| ------ | ------------- | -------------- |
| 读取文件   | 打开文件看内容       | 看订单上写了什么菜      |
| 解析数据   | 把文件内容拆开看      | 把订单拆成：菜名、数量、备注 |
| 填充模板   | 把数据填到模板里      | 按照菜谱准备食材       |
| 调用 API | 让 AI 干活       | 把食材交给厨师        |
| 解析响应   | 把 AI 返回的结果整理好 | 把做好的菜装盘        |
| 保存文件   | 把结果写到文件里      | 把菜打包好准备配送      |
| 循环     | 对每个产品重复做      | 一个订单一个订单处理     |

---

## 十、常见问题

### Q: 我不会写代码怎么办？

A: 你不需要写代码。Hermes 会帮你执行 Python 代码。你只需要告诉我"做什么"。

### Q: AI 返回的结果格式不对怎么办？

A: 在 Prompt 中强调输出格式（如 JSON），AI 就会按格式返回。如果还是不对，可以在 Prompt 中给一个输出示例。

### Q: 处理一个产品要多久？

A: 生成一次内容大约 10-30 秒。一个产品有 6 种内容，大约需要 2-3 分钟。10 个产品大约 20-30 分钟。

### Q: 可以一边处理一边做别的事吗？

A: 可以。批量处理时，Hermes 会在后台运行，你可以做别的事。完成后会通知你。
