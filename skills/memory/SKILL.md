# Memory Skill - 对话记忆与归纳

## 核心定义

### 存储结构

| 层级 | 路径 | 用途 |
|------|------|------|
| **碎片** | `memory/fragmentization/YYYY-MM-DD HH.md` | 原始对话日志（追加式，按小时分割） |
| **宫殿** | `memory/palace/` | 结构化知识库（按主题分类的 `.md` 文件） |
| **索引** | `memory/chroma/` | ChromaDB 向量索引（语义检索） |

---

## AI 使用指南

### 1. 初始化检查

**每次会话启动时执行：**
```bash
# 检查索引是否存在
if [ ! -d "$WORKSPACE_ROOT/memory/chroma" ]; then
    python skills/memory/scripts/rag_search.py init
fi
```

---

### 2. 记忆检索

**触发条件（满足任一即检索）：**
- 用户提到具体人名、项目名、地点
- 用户提问涉及偏好/历史/决策（"我之前说过..."）
- 对话超过 10 轮，需要上下文
- 心跳检查时（定期回顾）

**不检索的情况：**
- 简单事实问答（"今天几号"）
- 紧急操作（"快停止进程"）
- 用户明确说"不用查"

**检索命令：**
```bash
python skills/memory/scripts/rag_search.py search "<查询内容>"
```

**Query 提取策略：**
| 用户输入 | 提取的 Query |
|----------|-------------|
| "我上次说的那个项目" | "项目" |
| "鱼蛋喜欢吃什么" | "鱼蛋 偏好 食物" |
| "云鲸的加班文化" | "云鲸 加班 文化" |
| "记得帮我记下来" | （不检索，触发添加） |

**返回格式：**
```json
[{"content": "...", "filename": "...", "filepath": "...", "distance": 0.xx}]
```

**处理逻辑：**
- `distance < 0.3` → 高相关，直接使用
- `distance 0.3-0.6` → 中等相关，谨慎引用
- `distance > 0.6` 或空列表 → 无结果，告知用户"没找到相关记忆"

---

### 3. 记忆添加

**触发时机：**
- 心跳时整理（碎片 → 宫殿 → 索引）
- 用户明确说"记住这个"（立即添加）
- 发现重要信息（决策、偏好、待办）

**添加命令：**
```bash
python skills/memory/scripts/rag_search.py add "<文件名>" "<内容>"
```

**文件名规范：**
- 偏好类：`user-preferences.md`
- 项目类：`project-<项目名>.md`
- 待办类：`todos.md`
- 上下文类：`context-<主题>.md`

---

### 4. 心跳整理流程

**系统后台自动执行**（AI 不主动调用，只负责读取）：

```
阶段 1: 碎片 → 宫殿
1. 读取未整理的碎片文件
   → memory/fragmentization/YYYY-MM-DD HH.md

2. 提取关键信息（决策、偏好、待办、项目进展）
   → 分类整理

3. 更新记忆宫殿
   → memory/palace/<主题>.md

阶段 2: 宫殿 → 索引
4. 更新 RAG 索引
   → 系统自动调用脚本完成索引同步
```

**AI 角色：** 心跳时直接读取已更新的记忆宫殿和索引，无需执行整理命令。

---

## 依赖与环境

**安装依赖：**
```bash
pip install -r skills/memory/requirements.txt
```

**依赖包：**
- `chromadb` - 向量数据库
- `sentence-transformers` - Embedding 模型（支持中文）

**环境变量：**
- `WORKSPACE_ROOT` - 工作区根目录（默认：`/Users/narwal/.openclaw/workspace`）

---

## 故障处理

| 问题 | 处理方案 |
|------|----------|
| 索引目录不存在 | 运行 `init` 初始化 |
| 检索返回空列表 | 告知用户"没找到相关记忆"，不报错 |
| 依赖未安装 | 提示运行 `pip install -r requirements.txt` |
| 脚本执行失败 | 降级到不检索，继续对话 |

---

## 脚本位置

- **主脚本：** `skills/memory/scripts/rag_search.py`
- **依赖文件：** `skills/memory/requirements.txt`
- **辅助脚本：** `skills/memory/scripts/summarize.sh`（创建今日模板）

---
