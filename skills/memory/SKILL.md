# Memory Skill - 对话记忆与归纳

## 定义

### 记忆碎片（Memory Fragmentization）
**路径：** `memory/fragmentization/YYYY-MM-DD HH.md`

- 原始、完整、追加式的对话日志
- 每次用户交互时自动记录
- 保留所有细节，不做筛选
- 按小时分割文件（便于管理和定位）
- **时间戳精度：** 秒级（`HH:mm:ss`）

### 记忆宫殿（Memory Palace）
**路径：** `memory/palace/`

- 由记忆碎片整理生成的结构化知识库
- 按照不同的知识体系创建下级目录
- 根据具体内容创建不同的 `.md` 文件
- **文件命名：** 英文（如 `user-preferences.md`、`project-context.md`）
- **内容风格：** 中文
- **热度分类：**
  - 🔥 热点记忆 - 高频读取的内容
  - ❄️ 冷记忆 - 低频读取的内容

### 记忆目录（Memory Directory）
**路径：** `memory/directory.md`

- 维护记忆在记忆宫殿中的路径和说明
- **不记录具体内容**，只记录索引
- 通过路径定位到记忆宫殿中的具体内容
- 记录**上一次整理时间**，用于增量整理

### 记忆索引（RAG Vector Index）
**路径：** `memory/chroma/`

- ChromaDB 本地向量存储（自动生成）
- 支持语义检索，无需手动维护索引
- **检索成本：** 几乎 0 LLM tokens（本地向量计算）
- **Embedding 模型：** sentence-transformers（本地运行）

---

## 检索模式

### 模式 1：RAG 语义检索（默认）⭐

**适用场景：**
- 模糊查询（"用户喜欢什么"）
- 跨文件检索
- 大量记忆文件（>10 个）

**工作流程：**
```
1. 用户提问 → 检测需要记忆
2. RAG 搜索 → 语义匹配 → 返回相关片段
3. 消耗：~0 LLM tokens（本地向量计算）
```

**命令：**
```bash
python skills/memory/scripts/rag_search.py search "查询内容"
```

**依赖：**
```bash
pip install -r skills/memory/requirements.txt
```

---

### 模式 2：目录索引检索（备用）

**适用场景：**
- RAG 未初始化
- 简单关键词匹配
- 已知确切文件名

**工作流程：**
```
1. 读 memory/directory.md（~100 tokens）
2. 定位到具体文件
3. 按需读取（~200-500 tokens）
```

---

## 记忆读取时机

| 时机 | 说明 | 推荐模式 |
|------|------|----------|
| 会话启动 | 新会话开始时读取热点记忆 | RAG |
| 提及相关话题 | 检测到关键词/项目名时 | RAG |
| 做决策前 | 涉及用户偏好/历史决策时 | RAG |
| 心跳检查 | 定期读取记忆 | RAG |
| 长对话中 | 对话超过 10 轮后 | RAG |
| 简单问答 | "今天天气如何" | 不读取 |
| 用户明确说不用查 | 跳过检索 | 不读取 |
| 紧急操作 | "快停止那个进程" | 不读取 |

---

## 记忆整理流程

### 自动整理（推荐）

```
1. 对话进行中 → 实时记录到 fragmentization/
2. 会话结束 → 触发整理任务
3. 整理任务 → 读取碎片 → 更新 palace/ → 更新 RAG 索引
```

### 手动整理

```bash
# 初始化/更新 RAG 索引
python skills/memory/scripts/rag_search.py init

# 搜索记忆
python skills/memory/scripts/rag_search.py search "用户偏好"

# 添加单个记忆
python skills/memory/scripts/rag_search.py add "filename.md" "内容"
```

---

## 为什么用 RAG？

| 方案 | Token 消耗 | 检索准确度 | 维护成本 |
|------|-----------|-----------|----------|
| **RAG 语义检索** | ~0 tokens | ⭐⭐⭐⭐⭐ 语义匹配 | 低（自动） |
| 目录索引检索 | ~300-600 tokens | ⭐⭐⭐ 关键词匹配 | 中（手动维护） |
| 读取所有记忆 | ~5000+ tokens | ⭐⭐⭐⭐ 完整上下文 | 低（但浪费） |

**RAG 优势：**
- ✅ 检索几乎 0 LLM tokens
- ✅ 语义匹配（不是关键词）
- ✅ 自动维护索引
- ✅ 本地运行（无需外部 API）
- ✅ 可扩展到大量记忆

---

## 依赖安装

```bash
# 进入 skill 目录
cd skills/memory

# 安装依赖
pip install -r requirements.txt

# 初始化索引
python scripts/rag_search.py init
```

**依赖说明：**
- `chromadb` - 本地向量数据库
- `sentence-transformers` - 本地 Embedding 模型（支持中文）
- `faiss-cpu` - 可选，更快的向量检索

---

## 故障降级

| 问题 | 降级方案 |
|------|----------|
| RAG 未安装依赖 | 自动降级到目录索引模式 |
| 索引为空 | 提示用户运行 `init` |
| 检索无结果 | 返回空列表，不报错 |

---
