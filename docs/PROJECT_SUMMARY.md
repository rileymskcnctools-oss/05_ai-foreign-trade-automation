# Foreign Trade AI Workspace V0.1 — 项目总结文档

## 一、项目全景

- 项目名称: Foreign Trade AI Workspace V0.1
- 行业背景: 手工农具外贸（锄头/铲子/耙子/叉子）
- 目标用户: 外贸业务员 / 跨境电商运营
- 核心价值: 用AI自动生成产品营销内容，从手动30分钟/产品 → 自动5秒/产品
- GitHub: https://github.com/rileymskcnctools-oss/05_ai-foreign-trade-automation

---

## 二、技术架构

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Streamlit   │────▶│  FTDatabase  │────▶│   SQLite    │
│  Web 界面    │     │  (Python)    │     │  215产品    │
└──────┬──────┘     └──────┬───────┘     └─────────────┘
       │                   │
       ▼                   ▼
┌─────────────┐     ┌──────────────┐
│  ft_cli.py  │────▶│  LLMClient   │
│  CLI 命令行  │     │  DeepSeek API│
└─────────────┘     └──────────────┘
```

- CLI（ft_cli.py）→ 适合批量操作、脚本自动化
- Web（app.py）→ 适合日常使用、可视化操作

---

## 三、8周开发历程

| 周次 | 做了什么 | 关键技术 |
|------|---------|---------|
| 1-2 | 项目骨架 + SQLite + CSV导入 | SQLite, CSV(gbk编码), 类封装 |
| 3-4 | 接入DeepSeek AI + Prompt模板 | OpenAI SDK, 模板引擎, API调用 |
| 5 | 批量处理 + 重试 + 日志 | retry装饰器, 日志系统, argparse |
| 6 | Streamlit搜索界面 | @st.cache_resource, pandas DataFrame |
| 7 | AI工作台：按钮生成 → 保存 | st.button, session_state, PRAGMA |
| 8 | 30产品测试 + README + 发布 | 数据验证, 项目文档 |

---

## 四、核心代码讲解（面试必会）

### 1. 数据库层 (src/core/database.py)

```python
# 关键设计：WAL模式 + 超时 + 跨线程
self.conn = sqlite3.connect(db_path, check_same_thread=False, timeout=10)
self.conn.execute("PRAGMA journal_mode=WAL")  # 读写并发
```

面试话术: "SQLite默认是回滚日志模式，读会阻塞写。我开启了WAL模式，读操作不被写阻塞，适合Web应用的并发场景。timeout=10秒避免database locked错误。"

### 2. AI调用层 (src/core/llm_client.py)

```python
def chat(self, messages, temperature=0.7):
    response = self.client.chat.completions.create(
        model=self.model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content
```

面试话术: "我封装了LLMClient类，基于OpenAI SDK兼容接口对接DeepSeek API。chat方法接收消息列表，返回生成文本。temperature控制创造性——SEO标题用0.7，卖点用0.8，话术用0.9。"

### 3. Prompt模板系统 (prompts/ + src/utils/prompts.py)

```
prompts/
├── seo/
│   └── title.txt      # "你是一个SEO专家，为以下产品生成3个标题..."
└── social/
    └── whatsapp.txt    # "你是一个有10年经验的外贸业务员..."
```

面试话术: "我把Prompt和代码分离。每个Prompt是独立的txt文件，代码通过模板引擎加载并注入产品变量。好处是Prompt可以独立修改，不需要改代码，也方便非技术人员调优。"

### 4. Streamlit状态管理 (app.py)

```python
@st.cache_resource  # 数据库连接只初始化一次
def get_db():
    return FTDatabase()

if st.button("生成SEO标题"):
    with st.spinner("正在生成..."):
        success, msg = generate_ai_content(code, "seo")
    if success:
        st.success(msg)  # 绿色提示
    else:
        st.error(msg)    # 红色提示
```

面试话术: "Streamlit每次交互都重新执行全部脚本。我用@st.cache_resource缓存数据库连接避免重复创建，用st.spinner给用户等待反馈，st.success/st.error区分结果展示。"

---

## 五、踩坑经验（面试加分项）

| 坑 | 原因 | 解决 |
|----|------|------|
| CSV乱码 | GBK编码不是UTF-8 | open(file, encoding='gbk') |
| database is locked | 多进程同时访问SQLite | timeout=10 + WAL模式 |
| PRAGMA c[0] vs c[1] | c[0]是序号，c[1]才是列名 | dict(zip([c[1] for c in ...], row)) |
| Streamlit按钮不响应 | button每帧重置 | 用session_state保存状态 |
| 旧进程占端口 | Ctrl+C没杀干净 | taskkill /F /IM streamlit.exe |

---

## 六、面试高频问答

### Q: 这个项目解决了什么问题？

A: 手工农具外贸业务员每次上新品要写SEO标题、卖点描述、客户话术，手动需要30分钟/产品。我用AI自动化了这个流程，215个产品批量生成只需几分钟。

### Q: 为什么选SQLite而不是MySQL？

A: 这是单用户本地工具，SQLite零配置、无需服务器，数据量215条完全够用。如果是团队协作或数据量过万，会切换到PostgreSQL。

### Q: AI生成的内容质量怎么保证？

A: 三层保障：
1. Prompt模板经过反复调优，包含角色设定+输出格式约束
2. 产品数据越完整，生成质量越高
3. 人工抽查验证（第8周抽查30个产品，100%通过）

### Q: 这个项目体现了你什么能力？

A: 全栈开发能力（CLI+Web+数据库+AI API），独立完成从需求分析到部署的完整流程。更重要的是用技术解决实际业务问题的思维——我不是为了学技术而做项目，而是因为工作中真的需要这个工具。

### Q: 如果给你更多时间，你会怎么改进？

A: 三个方向：
1. 多语言——当前只有英文，非洲市场需要法语/阿拉伯语版本
2. 图片管理——产品没有图片展示
3. 客户CRM——跟客户沟通记录和报价单自动化

---

## 七、项目成果

| 交付物 | 状态 |
|--------|------|
| 215个产品完整数据库（43个字段/产品） | ✅ |
| AI生成SEO标题 × 215 | ✅ |
| AI生成卖点描述 × 215 | ✅ |
| AI生成WhatsApp话术 × 215 | ✅ |
| Streamlit Web界面（搜索+详情+AI生成） | ✅ |
| CLI命令行工具（6个命令） | ✅ |
| GitHub项目完整提交记录 | ✅ |
| README文档 + 安装教程 | ✅ |
| 30产品抽查测试 100%通过 | ✅ |

---

## 八、CLI命令速查

```bash
# 搜索产品
python scripts/ft_cli.py search "hoe"

# 查看统计
python scripts/ft_cli.py stats

# 生成单个产品SEO
python scripts/ft_cli.py generate GF-001 --type seo

# 生成全部内容类型
python scripts/ft_cli.py generate GF-001 --type all

# 批量生成（全部产品）
python scripts/ft_cli.py generate all --type all

# 批量生成（限制数量）
python scripts/ft_cli.py generate all --type seo --limit 10

# 检查缺失字段
python scripts/ft_cli.py missing
```

---

## 九、启动方式

```bash
# Web界面
streamlit run app.py

# CLI
python scripts/ft_cli.py <command>
```
