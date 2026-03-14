# smart-openclaw · OpenClaw 可插拔扩展系统

为 OpenClaw 提供轻量级、可插拔的设定追加和技能扩展能力，让你可以：
- 🧠 **动态扩展 AI 人格**（./ADDITION_SOUL.md）
- ⚙️ **定制化行为流程**（./ADDITION_AGENTS.md）
- 🔧 **灵活加载技能**（./skills/）

---

## 📁 项目结构

```
smart-openclaw/
├── README.md                    # 项目说明
├── LICENSE                      # MIT 许可证
├── DESIGN.md                    # 追加规则说明
├── ADDITION_SOUL.md             # AI人格补充设定
├── ADDITION_AGENTS.md           # 行为流程补充设定
└── skills/                      # 自定义技能目录
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
读 /path/to/smart-openclaw/DESIGN.md，根据其内容执行额外的动作
```

### 3. 自定义设定
编辑追加文件来扩展 AI 的行为：
- `ADDITION_SOUL.md` – 人格与底线
- `ADDITION_AGENTS.md` – 工作方式

### 4. 管理技能
- **添加技能**：`./skills/` 为自定义技能目录，按需加载

---

## 🧩 工作原理

smart-openclaw 遵循 DESIGN.md 中定义的 **追加规则**：

1. **内存拼接** – OpenClaw 在启动时将原文件（`SOUL.md`/`AGENTS.md`）与追加文件在内存中合并
2. **文件独立** – 不修改 OpenClaw 原文件，追加文件保持独立
3. **技能连接** – `./skills/` 中的技能通过文件连接方式加载

> 这意味着你可以安全地测试新设定，随时启用或禁用，无需担心破坏原有配置。

## 🔗 参考链接

- [OpenClaw 官方文档](https://docs.openclaw.ai) – 完整功能和配置说明
- [OpenClaw 技能中心 (ClawHub)](https://clawhub.com) – 更多社区技能
- [GitHub 仓库](https://github.com/chyern/smart-openclaw) – 查看源码和提交问题

---