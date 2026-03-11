# 追加规则

## 核心原则

- **内存拼接** - 设定模块在运行时拼接，不修改原本文件
- **文件独立** - 追加文件保持独立，不修改原始文件
- **优先级** - 设定冲突时以核心文件（SOUL.md / AGENTS.md）为准
- **连接模式** - 追加 skill 使用文件连接，不复制文件内容
- **自动启用** - 文件存在即启用，删除即失效

## 追加配置

| 追加文件 | 合并目标 | 说明 |
|----------|----------|------|
| `smart-openclaw/ADDITION_SOUL.md` | `SOUL.md` | 追加人格 |
| `smart-openclaw/ADDITION_AGENTS.md` | `AGENTS.md` | 追加工作风格 |
| `smart-openclaw/skills/` | 运行时加载 | 追加技能 |

## 追加 SKILL

- 需要追加的 skill 都在 `smart-openclaw/skills/` 目录下
- **状态检查** - 运行 `./skills/list-skills.sh` 检查本地技能的安装状态
- 输出说明：✅ 已安装到 OpenClaw | ❌ 未安装
