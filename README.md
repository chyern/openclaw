# smart-openclaw · OpenClaw 可插拔扩展系统

为 全新OpenClaw 提供轻量级、可插拔的设定追加和技能扩展能力，让你可以：
- 🧠 **动态扩展 AI 人格**（./ADDITION_SOUL.md）
- ⚙️ **定制化行为流程**（./ADDITION_AGENTS.md）
- 🔧 **灵活加载技能**（./skills/）

---

## 📁 项目结构

```
smart-openclaw/
├── DESIGN.md                    # 追加规则说明
├── ADDITION_SOUL.md             # AI 人格补充设定
├── ADDITION_AGENTS.md           # 行为流程补充设定
├── skills/                      # 自定义技能库
```

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/chyern/smart-openclaw.git
cd smart-openclaw
```

### 2. 配置 OpenClaw
在你的 OpenClaw 工作区 `AGENTS.md` 中添加一行：

```markdown
读 {path}/smart-openclaw/DESIGN.md，根据其内容执行额外的动作
```

### 3. 自定义设定
编辑追加文件来扩展 AI 的行为：
- `ADDITION_SOUL.md` – 人格与底线
- `ADDITION_AGENTS.md` – 工作方式

### 4. 管理技能
- **添加技能**：`./skills/` 为自定义技能目录，按需加载

---