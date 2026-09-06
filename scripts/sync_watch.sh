#!/bin/bash
# ============================================================
# P5 定时增量同步 watch 脚本
# ------------------------------------------------
# 每天跑一次增量同步：取最近 1 天的 Vibe-Research git
# 变更，增量更新 Obsidian vault 实体。
#
# 用法（crontab）：
#   0 8 * * * /Users/lizhiwei/Documents/Obsidian\ Vault/scripts/sync_watch.sh
#
# 或手动：
#   bash scripts/sync_watch.sh
# ============================================================
set -euo pipefail

VAULT_ROOT="/Users/lizhiwei/Documents/Obsidian Vault"
VIBE_RESEARCH="/Users/lizhiwei/project/code/stock/Vibe-Research"

cd "$VAULT_ROOT"

# 取最近 1 天的变更
python3 scripts/incremental_sync.py \
    --vault "$VAULT_ROOT" \
    --vibe-research "$VIBE_RESEARCH" \
    --since "1 day ago" \
    --quiet

# 退出码透传
exit $?
