#!/bin/bash
# list-skills.sh - 检查本地技能的安装状态

LOCAL_SKILLS="$(dirname "$0")"

# 动态获取 OpenClaw 技能目录
OPENCLAW_SKILLS=""

# 1. 优先检查环境变量
if [ -n "$OPENCLAW_SKILLS_DIR" ]; then
    OPENCLAW_SKILLS="$OPENCLAW_SKILLS_DIR"
fi

# 2. 尝试通过 openclaw 命令获取
if [ -z "$OPENCLAW_SKILLS" ] && command -v openclaw &> /dev/null; then
    # 尝试从 openclaw status 或 config 输出中提取
    OPENCLAW_ROOT=$(openclaw status 2>/dev/null | grep -oP '(?<=root: )\S+' | head -1)
    if [ -n "$OPENCLAW_ROOT" ] && [ -d "$OPENCLAW_ROOT/skills" ]; then
        OPENCLAW_SKILLS="$OPENCLAW_ROOT/skills"
    fi
fi

# 3. 尝试 npm 全局路径
if [ -z "$OPENCLAW_SKILLS" ] && command -v npm &> /dev/null; then
    NPM_PREFIX=$(npm prefix -g 2>/dev/null)
    if [ -n "$NPM_PREFIX" ] && [ -d "$NPM_PREFIX/lib/node_modules/openclaw/skills" ]; then
        OPENCLAW_SKILLS="$NPM_PREFIX/lib/node_modules/openclaw/skills"
    fi
fi

# 4. 备用路径 (Docker 常见路径)
if [ -z "$OPENCLAW_SKILLS" ]; then
    for path in \
        "/app/openclaw/skills" \
        "/opt/openclaw/skills" \
        "/usr/local/openclaw/skills" \
        "/opt/homebrew/lib/node_modules/openclaw/skills" \
        "/usr/local/lib/node_modules/openclaw/skills" \
        "$HOME/.npm-global/lib/node_modules/openclaw/skills"
    do
        if [ -d "$path" ]; then
            OPENCLAW_SKILLS="$path"
            break
        fi
    done
fi

# 获取 OpenClaw 已安装的技能列表
installed=()
if [ -n "$OPENCLAW_SKILLS" ] && [ -d "$OPENCLAW_SKILLS" ]; then
    for skill_dir in "$OPENCLAW_SKILLS"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            if [[ "$skill_name" != "." ]] && [[ "$skill_name" != ".." ]]; then
                installed+=("$skill_name")
            fi
        fi
    done
fi

echo ""
echo "📦 技能安装状态"
[ -n "$OPENCLAW_SKILLS" ] && echo "   技能目录：$OPENCLAW_SKILLS"
echo ""

# 检查本地技能目录
for skill_dir in "$LOCAL_SKILLS"/*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        
        # 跳过系统目录
        if [[ "$skill_name" == "venv" ]] || [[ "$skill_name" == "scripts" ]] || [[ "$skill_name" == "__pycache__" ]]; then
            continue
        fi
        
        if [ -f "$skill_dir/SKILL.md" ]; then
            # 检查是否已安装到 OpenClaw
            is_installed=false
            for installed_skill in "${installed[@]}"; do
                if [ "$installed_skill" == "$skill_name" ]; then
                    is_installed=true
                    break
                fi
            done
            
            if [ "$is_installed" = true ]; then
                echo "  ✅  $skill_name"
            else
                echo "  ❌  $skill_name"
            fi
        fi
    fi
done

echo ""
