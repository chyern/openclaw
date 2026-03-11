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
2. **RAG 优先** → 检索成本几乎为 0，适合频繁查询
3. **目录索引降级** → RAG 不可用时自动 fallback
4. **本地运行** → 无需外部 API，数据隐私安全

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
- `memory/directory.md` - 记忆目录索引
- `memory/chroma/` - 向量数据库索引

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

### v0.1.0 (2026-03-11) - 初始版本
- ✅ 基础碎片记录功能
- ✅ RAG 语义检索（ChromaDB + sentence-transformers）
- ✅ 记忆宫殿结构定义
- ✅ 目录索引降级方案
- ✅ 自动整理任务

---

## 🔗 相关文档

- [SKILL.md](./SKILL.md) - 完整技能定义
- [OpenClaw 文档](https://docs.openclaw.ai) - 平台文档

---

*最后更新：2026-03-11*
