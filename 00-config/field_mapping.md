# Excel 产品数据库设计

> 这是整个系统的基础。设计得好，后面的自动化就顺。

---

## 一、为什么要有设计规范？

想象你去超市：

- 所有商品都有标签：品名、价格、重量、产地
- 如果没有标签，你找不到想要的东西
- AI 也是一样——它需要结构化的数据才能工作

**原则**：一个字段只存一种信息。

- ❌ 错误：`规格` 字段存 "4齿, 30cm, 碳钢" （三种信息混在一起）
- ✅ 正确：分开存 → `齿数: 4` `长度: 30cm` `材质: 碳钢`

---

## 二、完整字段设计

### A 区：产品基本信息（AI 生成内容的基础）

| 列号  | 字段名（英文）         | 字段名（中文） | 示例值           | 为什么重要      | 填写规则         |
| --- | --------------- | ------- | ------------- | ---------- | ------------ |
| A   | product_id      | 产品编号    | GF-001        | 唯一标识，避免混淆  | 自编规则：类别缩写+序号 |
| B   | product_name_cn | 产品中文名   | 园林叉           | 你的内部参考     | 简洁           |
| C   | product_name_en | 产品英文名   | Garden Fork   | AI 生成内容的基础 | 标准英文名        |
| D   | category        | 产品类别    | Digging Tools | 分类管理       | 从预设列表选       |
| E   | sub_category    | 子类别     | Forks         | 更细分类       | 从预设列表选       |

### B 区：产品技术参数（AI 写卖点的依据）

| 列号  | 字段名（英文）           | 字段名（中文）  | 示例值                     | 为什么重要    | 填写规则            |
| --- | ----------------- | -------- | ----------------------- | -------- | --------------- |
| F   | material          | 材质       | Carbon Steel + Hardwood | 买家最关心的   | 写全，不要缩写         |
| G   | handle_material   | 手柄材质     | Ash Wood                | 影响手感和耐用性 | 如无单独手柄，填 "一体成型" |
| H   | length_cm         | 长度(cm)   | 30                      | 规格核心数据   | 只填数字            |
| I   | weight_kg         | 重量(kg)   | 0.8                     | 运费计算依据   | 只填数字，精确到小数点后1位  |
| J   | head_width_cm     | 头部宽度(cm) | 8                       | 工作面积参考   | 只填数字            |
| K   | tine_count        | 齿数/刃数    | 4                       | 规格核心数据   | 只填数字            |
| L   | hardness          | 硬度       | HRC 45-50               | 质量指标     | 如无则留空           |
| M   | surface_treatment | 表面处理     | Polished + Lacquered    | 防锈工艺     | 写具体工艺           |

### C 区：商业信息（AI 写报价和开发话术的依据）

| 列号  | 字段名（英文）          | 字段名（中文）  | 示例值       | 为什么重要   | 填写规则       |
| --- | ---------------- | -------- | --------- | ------- | ---------- |
| N   | moq              | 最小起订量    | 500       | 买家决策关键  | 只填数字（单位：件） |
| O   | packaging_type   | 包装方式     | Color Box | 影响成本和展示 | 选预设值       |
| P   | qty_per_carton   | 每箱数量     | 20        | 运费计算    | 只填数字       |
| Q   | carton_size_cm   | 外箱尺寸(cm) | 62x32x35  | 运费计算    | 长x宽x高      |
| R   | gw_per_carton_kg | 每箱毛重(kg) | 17.5      | 运费计算    | 只填数字       |
| S   | lead_time_days   | 交货期(天)   | 25        | 买家决策关键  | 只填数字       |
| T   | certification    | 认证       | CE, GS    | 欧洲市场必需  | 逗号分隔       |

### D 区：SEO & 市场信息（AI 生成 SEO 内容的依据）

| 列号  | 字段名（英文）         | 字段名（中文） | 示例值                                   | 为什么重要  | 填写规则       |
| --- | --------------- | ------- | ------------------------------------- | ------ | ---------- |
| U   | target_keywords | 目标关键词   | garden fork, digging fork, steel fork | SEO 基础 | 逗号分隔，3-5 个 |
| V   | use_scenario    | 使用场景    | Garden soil turning, compost mixing   | 写卖点用   | 逗号分隔       |
| W   | target_markets  | 目标市场    | Europe, Africa, South America         | 市场定制文案 | 逗号分隔       |
| X   | selling_angle   | 核心卖点    | Extra-strong tines, ergonomic handle  | AI 参考  | 1-2 句话     |
| Y   | competitor_ref  | 竞品参考    | Fiskars X3, Spear & Jackson           | 对标分析   | 品牌+型号      |

### E 区：AI 生成内容存放（输出区）

| 列号  | 字段名（英文）               | 字段名（中文）     | 示例值                            | 说明            |
| --- | --------------------- | ----------- | ------------------------------ | ------------- |
| Z   | seo_title_1           | SEO 标题1     | Heavy Duty Garden Fork...      | AI 生成         |
| AA  | seo_title_2           | SEO 标题2     | Professional Digging Fork...   | AI 生成         |
| AA  | seo_title_3           | SEO 标题3     | 4-Tine Steel Garden Fork...    | AI 生成         |
| AC  | selling_points        | 五点卖点        | 1.Ergonomic... 2.Heavy-duty... | AI 生成，JSON 格式 |
| AD  | whatsapp_script       | WhatsApp 话术 | Hi! We manufacture...          | AI 生成         |
| AE  | alibaba_detail_status | 阿里详情状态      | pending/generated              | 标记是否已生成       |

---

## 三、预设值列表（下拉菜单用）

### 产品类别（category）

```
Digging Tools      → 挖掘工具（铲、叉、耙）
Cutting Tools      → 切割工具（剪刀、锯）
Watering Tools     → 浇水工具
Pruning Tools      → 修剪工具
Weeding Tools      → 除草工具
Harvesting Tools   → 收获工具
Soil Preparation   → 土壤准备工具
```

### 包装方式（packaging_type）

```
Color Box          → 彩盒
Blister Card       → 吸塑卡
Poly Bag           → 塑料袋
Shrink Wrap        → 热缩膜
Hang Card          → 挂卡
Display Box        → 展示盒
Bulk Pack          → 散装
Custom Packaging   → 定制包装
```

### 表面处理（surface_treatment）

```
Polished           → 抛光
Painted            → 喷漆
Powder Coated      → 喷塑
Chrome Plated      → 镀铬
Galvanized         → 镀锌
Lacquered          → 烤漆
Electrophoresis    → 电泳
Heat Treated       → 热处理
```

---

## 四、命名规则

### 产品编号规则

```
格式：[类别缩写]-[序号]

类别缩写：
  GF = Garden Fork
  GS = Garden Spade
  GR = Garden Rake
  SH = Shovel
  HT = Hoe Tool
  PR = Pruner
  SC = Scissors
  WS = Watering System

示例：
  GF-001 = 园林叉 第1款
  GF-002 = 园林叉 第2款
  GS-001 = 园林铲 第1款
```

### 文件命名规则

```
输出文件命名：[产品编号]_[内容类型]_[日期]

示例：
  GF-001_seo_titles_20260603.csv
  GF-001_selling_points_20260603.txt
  GF-001_whatsapp_20260603.txt
  GF-001_market_africa_20260603.txt
```

---

## 五、示例数据（前 3 个产品）

| product_id | product_name_cn | product_name_en | category      | material                     | length_cm | weight_kg | tine_count | target_keywords                                   | moq | packaging_type |
| ---------- | --------------- | --------------- | ------------- | ---------------------------- | --------- | --------- | ---------- | ------------------------------------------------- | --- | -------------- |
| GF-001     | 园林叉             | Garden Fork     | Digging Tools | Carbon Steel + Ash Wood      | 30        | 0.8       | 4          | garden fork, digging fork, steel fork             | 500 | Color Box      |
| GS-001     | 园林铲             | Garden Spade    | Digging Tools | Carbon Steel + Hardwood      | 28        | 0.6       | N/A        | garden spade, digging spade, transplanting shovel | 500 | Color Box      |
| GR-001     | 园林耙             | Garden Rake     | Digging Tools | Carbon Steel + Wooden Handle | 35        | 0.9       | 14         | garden rake, leaf rake, steel rake                | 300 | Blister Card   |

---

## 六、为什么要这样设计？

### 从外贸业务角度

1. **分开存**：材质和手柄分开，因为买家关注点不同
   
   - 欧洲买家：关心材质（环保、认证）
   - 非洲买家：关心耐用性（材质硬度）

2. **数字化**：长度、重量只填数字
   
   - 方便 AI 计算（"重量只有 0.8kg，便于携带"）
   - 方便排序和筛选

3. **预设值**：包装方式用下拉菜单
   
   - 避免 "彩色盒""彩盒""彩盒包装" 三种写法
   - AI 能准确理解

### 从 AI 自动化角度

1. **字段英文名**：AI 理解英文字段名更准确
2. **一行一个产品**：AI 循环处理时，一次处理一行
3. **输出区预留列**：AI 生成的内容可以直接写回 Excel

---

## 七、实际操作步骤

### 创建 Excel 模板

1. 打开 Excel
2. 按上面的字段设计，创建列
3. 用数据验证功能创建下拉菜单（类别、包装方式等）
4. 填入 3 个真实产品作为测试数据
5. 保存为 `产品参数表模板.xlsx`

### 填写注意事项

- ✅ 必填字段：product_id, product_name_en, category, material, target_keywords
- ⚠️ 选填字段：硬度、认证、竞品参考（没有就留空）
- ❌ 不要合并单元格！AI 无法处理合并的单元格

---

现在，你的 Day 2 任务就是按照这个设计，创建你的第一个 Excel 产品参数表！
