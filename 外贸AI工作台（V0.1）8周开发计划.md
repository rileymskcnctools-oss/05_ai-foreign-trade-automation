# 外贸AI工作台（V0.1）8周开发计划

## 总目标

8周后实现：

- SQLite产品数据库

- 产品搜索

- SEO标题生成

- 卖点生成

- WhatsApp生成

- Streamlit可视化界面

形成第一个可实际使用的AI工具。

---

# 第1周：Python基础巩固

## 学习目标

理解项目代码结构。

掌握：

- 函数

- 类

- import

- pathlib

- json

- sqlite3

## 每日任务

### Day1

阅读：

src/core/database.py

目标：

理解：

- 连接数据库

- 查询数据库

- 返回结果

### Day2

阅读：

src/core/config.py

目标：

理解：

- yaml配置加载

- .env读取

### Day3

练习SQLite

完成：

```python
查询全部产品

查询指定产品

统计产品数量
```

### Day4

阅读：

scripts/ft_cli.py

理解：

```bash
search
get
stats
export
```

命令如何执行。

### Day5

手动新增一个CLI命令：

```bash
hello
```

例如：

```bash
python ft_cli.py hello
```

输出：

```text
Foreign Trade AI Workspace
```

### Day6-Day7

整理学习笔记。

输出：

Python项目结构理解文档。

太棒了！在外贸自动化转型的路上，前 4 天你完成了一次**从 0 到 1 的硬核跨越**。你不仅配置好了复杂的本地环境，还独立解决了路径迷路、数据库字段错位、Windows编码乱码等连初级程序员都会头疼的经典 Bug。

# ## 🧱 Day 1 - 2：筑基篇 —— 虚拟环境与安全保险箱

这两天的核心目标是**把开发环境搭稳，并学会如何保护自己的资产安全**。

1. **虚拟环境 (`.venv`)**
   
   - **为什么需要：** 就像给项目穿上了隔离防护服。如果直接把 Python 库安装在系统全局，不同项目之间很容易因为版本冲突导致电脑环境“中毒崩溃”。
   
   - **核心掌握：** 学会了通过虚拟环境下的 `python.exe` 运行脚本，确保依赖库（如 `requests`, `pandas`）的纯净。

2. **安全保险箱机制 (`.env`)**
   
   - **为什么需要：** 你的 DeepSeek 密钥就是你的真金白银。如果直接写在代码里，一不小心分享给别人或者上传到公开平台，就会遭遇盗刷。
   
   - **核心掌握：** 掌握了把密码藏在 `.env` 文件里，等号左右不能有空格、两边不加引号。在代码中通过环境变量去“捞”钥匙的防泄露思维。

### 📊 Day 3：数据篇 —— 提取产品弹药与防崩设计

这一天的核心目标是**从本地数据仓库里精准提货，并让程序学会“聪明地低头”**。

1. **字典与数据提取 (`dict`)**
   
   - **核心掌握：** 模拟了从数据库捞出的产品数据结构 `{ "product_code": "GS-001", ... }`。学会了用 `f-string`（字串格式化）将这些死板的数据，优雅地拼接进 B2B 外贸专属的 Prompt（提示词）模板中。

2. **防崩溃降级思维 (`.get()`)**
   
   - **大局观提升：** 传统的硬核取值（如 `prod['price']`）在遇到字段不存在时会直接导致程序闪退，这在批量处理 215 个产品时是致命的。
   
   - **核心掌握：** 学会了改用 `prod.get('price') or '暂无价格'`，让流水线具备了“即使数据不完美，也要温柔地跑完”的鲁棒性（稳定性）。

### 📡 Day 4：连接篇 —— 强行破门与打通 AI 算力

这一天你完成了最激动人心的**网络链路大闭环**，让 Python 真正跟 DeepSeek 牵手成功。

1. **底层文件流读取 (`with open()`)**
   
   - **核心掌握：** 当框架层因为 Windows 复杂的路径问题找不到 `.env` 钥匙时，你没有放弃，而是直接编写了 Python 最底层的 `with open()` 函数，像扫描仪一样逐行读取文件，强行拿到了密码。

2. **网络请求三要素 (`requests.post`)**
   
   - **URL（终点站）：** `https://api.deepseek.com/v1/chat/completions`
   
   - **Headers（身份令牌）：** 构造了带 `Bearer` 前缀的鉴权请求头，告诉服务器你是合法付费用户。
   
   - **Data/Payload（数据包裹）：** 学会了配置模型名称（`deepseek-chat`）、创造力系数（`temperature=0.7`）以及关闭流式输出（`stream=False`）以便于程序全量接收。

# 🛠️ 前 4 天高频 Bug 战功册（面试核心素材）

你在实操中踩过的每一个坑，都是未来简历上最硬核的“项目难点与解决方案”：

- **🚨 痛点 1：`ModuleNotFoundError: No module named 'src'`**
  
  - **本质：** Python 寻路迷航，找不到你写的工具包。
  
  - **战术：** 在脚本头部加入【寻路补丁】，强行把当前运行的绝对路径塞进 `sys.path` 导航图中。

- **🚨 痛点 2：`UnicodeDecodeError: ... can't decode byte 0xff`**
  
  - **本质：** Windows 编码背锅侠。PowerShell 生成的文件带有特殊的 UTF-16 方言前缀，而 Python 默认用 UTF-8 普通话去读，因而乱码卡死。
  
  - **战术：** 采用 `Set-Content .env ... -Encoding utf8` 强行将文件洗白成标准国际格式，或在代码中用 `try...except` 进行多编码格式兼容。

- **🚨 痛点 3：`❌ 请求失败！状态码: 402 / Insufficient Balance`**
  
  - **本质：** 技术管道全线贯通，但 AI 后台算力仓库缺乏话费。
  
  - **战术：** 登录平台在线充值，成功激活算力发货流。

### 📚 本周必记核心知识点（复习专用）

### 1. 项目路径管理与文件操作 (`os` 模块)

- `os.path.abspath(__file__)`：获取当前运行的 `.py` 脚本的绝对路径。

- `os.path.dirname(...)`：获取某个路径的上一级目录。

- `os.path.join(a, b, c)`：智能拼接路径，自动根据操作系统（Windows 用 `\`，Mac/Linux 用 `/`）处理斜杠，彻底避免转义混乱。

- `os.path.exists(path)`：判断文件或文件夹是否存在。

- `os.makedirs(path)`：自动递归创建多层文件夹。

### 2. 安全的文件读写与防报错机制

- **文本读写**：使用 `with open(..., "r/w", encoding="utf-8") as f:`。`with` 语句会自动管理文件的关闭，防止内存泄漏。

- **双编码容错**：读取 `.env` 等配置文件时，加入 `try-except UnicodeDecodeError` 机制，同时兼容 `utf-8` 和 `utf-16`，防止因 VS Code 自动编码转换导致脚本崩溃。

### 3. 数据库与 AI 通信基础

- **SQLite 联动**：使用 `sqlite3.connect(db_path)`，通过游标（`cursor`）执行安全带参 SQL 语句 `SELECT ... WHERE product_id = ?`，用 `fetchone()` 捞出核心参数，防止拼接字符串漏洞。

- **DeepSeek API 对接**：通过 `requests.post()` 发送 JSON 请求，利用 `headers={"Authorization": f"Bearer {api_key}"}` 进行鉴权，设置 `timeout=30` 保证网络波动时脚本能及时断开。

## 🚀 核心工作流逻辑（Pipeline 运行全景）

整个自动化管道一键启动后，在后台如同工厂流水线一般精准运转：

```
[终端输入命令]
       ↓
[智能根目录扫描] ──→ 成功捕获大本营路径
       ↓
[解析 .env 配置文件] ──→ 获取安全加密的 DEEPSEEK_API_KEY
       ↓
[连接 SQLite 数据库] ──→ 根据产品编码 (如 GF-001) 捞出核心参数
       ↓
[循环处理 4 类文案]
       ├── ① 纯相对路径精准穿透，读取 propmt/*.md 模板
       ├── ② 将数据库里的核心参数通过 f-string/format 动态注入模板
       ├── ③ 投喂给 DeepSeek-Chat 模型 (温度 0.7)
       └── ④ 自动在根目录下创建 output/产品编码/ 文件夹
       ↓
[全量落盘] ──→ 生成 4/4 类高质量 Markdown 外贸营销文件
```

## 🎯 阶段成果检验

最终，当你看到终端疯狂刷出绿色勾号，说明你已经**完全打破了对代码的恐惧**：

Bash

```
==================== 🚀 启动产品 [GF-001] 流程 ====================
✅ 成功从数据库捞出核心参数！
📁 已创建本地 Markdown 导出目录: .../output/GF-001
📡 正在读取模板 -> [SEO_Description.md] 并请求 AI...
  └─ 💾【生成成功】: .../output/GF-001/SEO_Description.md
📡 正在读取模板 -> [Product_Detail.md] 并请求 AI...
  └─ 💾【生成成功】: .../output/GF-001/Product_Detail.md
...
🎉 产品 [GF-001] 的 4 类标准 Markdown 外贸文件全量落盘完毕！ 
```

# 第2周：数据库系统掌握

## 学习目标

彻底掌握M1产品数据库模块。

## 任务

实现：

### 产品搜索

支持：

```text
hoe

shovel

rake
```

搜索。

### 分类统计

输出：

```text
Weeding Tools
81

Digging Tools
74

Cutting Tools
60
```

### 缺失数据检测

输出：

```text
HS Code缺失

Loading Qty缺失
```

---

# 第3周：接入AI生成SEO标题

## 学习目标

掌握API调用。

## 学习内容

- requests

- OpenAI SDK

- DashScope SDK

## 项目任务

实现：

```bash
python ft_cli.py generate GF-001
```

自动：

1. 查询数据库

2. 获取产品资料

3. 加载Prompt

4. 调用AI

5. 输出SEO标题

保存数据库。

---

# 第4周：卖点生成+WhatsApp生成

## 学习目标

掌握Prompt模板系统。

## 项目任务

新增：

```bash
python ft_cli.py generate GF-001 --type selling_points
```

新增：

```bash
python ft_cli.py generate GF-001 --type whatsapp
```

自动保存。

---

# 第5周：批量生成

## 学习目标

掌握自动化流程。

## 项目任务

实现：

```bash
python ft_cli.py generate --all
```

自动：

- SEO标题

- 卖点

- WhatsApp

批量生成。

增加：

```text
失败重试

日志记录

生成状态
```

---

# 第6周：Streamlit界面

## 学习目标

掌握前端展示。

## 学习内容

- Streamlit

重点：

```python
st.button()

st.text_input()

st.dataframe()
```

## 项目任务

实现：

产品搜索页面

显示：

- 图片

- 参数

- SEO标题

- 卖点

---

# 第7周：AI工作台V0.1

## 项目任务

实现完整流程：

搜索产品

↓

点击生成

↓

生成SEO标题

↓

生成卖点

↓

生成WhatsApp

↓

保存数据库

---

# 第8周：测试与发布

## 测试

随机抽查：

30个产品

检查：

- 数据读取

- AI生成

- 保存结果

## GitHub

完善：

README

项目截图

安装教程

使用教程

## 最终成果

获得：

Foreign Trade AI Workspace V0.1

功能：

✅ 产品数据库

✅ 产品搜索

✅ SEO标题生成

✅ 卖点生成

✅ WhatsApp生成

✅ Streamlit界面

✅ GitHub项目

---

# 本阶段禁止学习

不要碰：

- LangGraph

- CrewAI

- AutoGen

- MCP

- Spring AI

- 微调

- 向量数据库

- RAG

原因：

V0.1还没跑通。

先把基础工具做出来。

---

# V0.2（8周后）

完成V0.1后再开始：

- 客户CRM

- 市场研究Agent

- 开发信Agent

---

# V1.0（6个月）

目标：

完整AI外贸智能工作台

包含：

- 产品数据库

- 客户数据库

- CRM

- 市场研究

- 报价辅助

- 数据分析

- Agent工作流
