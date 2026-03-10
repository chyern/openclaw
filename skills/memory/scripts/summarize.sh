#!/bin/bash
# Memory Summarize Script
# 用于手动触发记忆总结的命令行工具

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory/fragmentization"
MEMORY_FILE="$WORKSPACE/memory/permanent.md"
TODAY=$(date +%Y-%m-%d)
TODAY_FILE="$MEMORY_DIR/$TODAY.md"

# 确保目录存在
mkdir -p "$MEMORY_DIR"

# 如果今日文件不存在，创建模板
if [ ! -f "$TODAY_FILE" ]; then
    cat > "$TODAY_FILE" << EOF
# $TODAY - 会话日志

## 会话记录
- 待填充

## 关键信息
- 待填充

## 待办
- 无

EOF
    echo "✅ 创建今日记忆文件：$TODAY_FILE"
else
    echo "📄 今日文件已存在：$TODAY_FILE"
fi

# 显示今日文件内容
echo ""
echo "=== 今日记忆内容 ==="
cat "$TODAY_FILE"
