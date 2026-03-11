# Memory Skill - 记忆技能

## 📖 这是什么

为 OpenClaw 提供**长期记忆能力**的技能包，让 AI 助理能够：
- 📝 **记录** - 自动保存对话到记忆碎片
- 🧠 **整理** - 将碎片归纳为结构化知识（记忆宫殿）
- 🔍 **检索** - 通过 RAG 语义检索快速找到相关记忆

---

## 💡 设计思想

### 核心理念

**分层存储 + 按需读取**，在记忆完整性和 token 效率之间找到平衡：

```
┌─────────────────────────────────────────────────────────┐
│  对话进行中                                              │
│    ↓                                                    │
│  原始碎片 (fragmentization/) ← 完整、追加式、按小时分割    │
│    ↓ (定期整理)                                          │
│  记忆宫殿 (palace/) ← 结构化、去重、分类存储              │
│    ↓                                                    │
│  向量索引 (chroma/) ← 语义检索，0 token 成本              │
└─────────────────────────────────────────────────────────┘
```

### 为什么这样设计

| 问题 | 传统方案 | Memory Skill 方案 |
|------|----------|------------------|
| 记忆太多读不完 | 全部加载 → 浪费 token | RAG 检索 → 只读相关的 |
| 检索不准确 | 关键词匹配 | 语义匹配（理解意思） |
| 维护成本高 | 手动整理 | 自动整理 + 增量更新 |
| 碎片化严重 | 单一文件 | 碎片→宫殿分层存储 |

### 关键决策

1. **碎片按小时分割** → 避免单文件过大，便于定位
2. **纯 RAG 检索** → 无中间索引层，简化架构
3. **本地运行** → 无需外部 API，数据隐私安全

---

## 📁 文件结构

```
skills/memory/
├── SKILL.md                 # 技能定义（OpenClaw 加载）
├── README.md                # 本文档（人类可读）
├── requirements.txt         # Python 依赖
├── scripts/
│   ├── rag_search.py        # RAG 检索主脚本
│   ├── fragmentize.py       # 碎片记录脚本
│   └── consolidate.py       # 整理脚本
└── venv/                    # 虚拟环境（自动生成）
```

**运行时生成：**
- `memory/fragmentization/` - 记忆碎片（原始对话日志）
- `memory/palace/` - 记忆宫殿（结构化知识）
- `memory/chroma/` - 向量数据库索引

---

## 🧠 记忆读取时机

| 时机 | 说明 |
|------|------|
| 会话启动 | 新会话开始时读取热点记忆 |
| 提及相关话题 | 检测到关键词/项目名时 |
| 做决策前 | 涉及用户偏好/历史决策时 |
| 心跳检查 | 定期读取记忆 |
| 长对话中 | 对话超过 10 轮后 |
| 简单问答 | "今天天气如何" — 不读取 |
| 用户明确说不用查 | 跳过检索 |
| 紧急操作 | "快停止那个进程" — 不读取 |

---

## 🔄 记忆整理流程

### 自动整理（推荐）

```
1. 对话进行中 → 实时记录到 fragmentization/
2. 会话结束 → 触发整理任务
3. 整理任务 → 读取碎片 → 更新 palace/ → 更新 RAG 索引
```

### 手动整理

```bash
# 初始化/更新 RAG 索引
python scripts/rag_search.py init

# 搜索记忆
python scripts/rag_search.py search "用户偏好"

# 添加单个记忆
python scripts/rag_search.py add "filename.md" "内容"
```

---

## 📦 依赖安装

```bash
cd skills/memory
pip install -r requirements.txt
python scripts/rag_search.py init
```

**依赖说明：**
- `chromadb` - 本地向量数据库
- `sentence-transformers` - 本地 Embedding 模型（支持中文）
- `faiss-cpu` - 可选，更快的向量检索

---

## 🔧 故障处理

| 问题 | 处理方案 |
|------|----------|
| 索引为空 | 运行 `python scripts/rag_search.py init` |
| 检索无结果 | 正常，返回空列表 |
| 依赖未安装 | 运行 `pip install -r requirements.txt` |

---

## 🔍 RAG 检索详解

### 工作流程

```
用户提问
    ↓
检测需要记忆检索
    ↓
RAG 搜索（本地 ChromaDB + 向量匹配）
    ↓
返回最相关的 3-5 个记忆片段
    ↓
拼接上下文 → 发送给 LLM 生成回答
```

**关键点：**
- 检索阶段**不调用 LLM**，纯本地向量计算
- 只有最终生成回答时才消耗 LLM tokens
- Embedding 模型：`sentence-transformers`（本地运行，支持中文）

### 方案对比

| 方案 | Token 消耗 | 检索准确度 | 维护成本 |
|------|-----------|-----------|----------|
| **RAG 语义检索** | ~0 tokens | ⭐⭐⭐⭐⭐ 语义匹配 | 低（自动） |
| 读取所有记忆 | ~5000+ tokens | ⭐⭐⭐⭐ 完整上下文 | 低（但浪费） |
| 关键词匹配 | ~100-300 tokens | ⭐⭐ 字面匹配 | 中 |

### RAG 优势

- ✅ **检索几乎 0 LLM tokens** — 本地向量数据库
- ✅ **语义匹配** — 理解意思，不是关键词
- ✅ **自动维护索引** — 添加/更新记忆时自动同步
- ✅ **本地运行** — 无需外部 API，数据隐私安全
- ✅ **可扩展** — 支持数千个记忆文件

### 技术细节

| 组件 | 说明 |
|------|------|
| **向量数据库** | ChromaDB（本地持久化，DuckDB + Parquet） |
| **Embedding 模型** | `paraphrase-multilingual-MiniLM-L12-v2` |
| **相似度算法** | 余弦相似度（cosine） |
| **索引位置** | `memory/chroma/` |
| **索引文件** | `memory/index.json`（元数据缓存） |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd skills/memory
pip install -r requirements.txt
```

### 2. 初始化索引

```bash
python scripts/rag_search.py init
```

### 3. 使用

```bash
# 搜索记忆
python scripts/rag_search.py search "用户偏好"

# 添加记忆
python scripts/rag_search.py add "filename.md" "内容"
```

---

## 📝 版本历史

### v0.1.1 (2026-03-11) - 简化架构
- ✅ 移除 directory.md，纯 RAG 检索
- ✅ 简化故障处理流程

### v0.1.0 (2026-03-11) - 初始版本
- ✅ 基础碎片记录功能
- ✅ RAG 语义检索（ChromaDB + sentence-transformers）
- ✅ 记忆宫殿结构定义
- ✅ 自动整理任务

---

## 🔗 相关文档

- [SKILL.md](./SKILL.md) - 完整技能定义
- [OpenClaw 文档](https://docs.openclaw.ai) - 平台文档

---

*最后更新：2026-03-11*
