#!/usr/bin/env bash
#
# download_fonts.sh — 自动下载甲骨文相关字体
#
# 支持系统：Linux / macOS（Git Bash）/ WSL
# Windows 原生 PowerShell 用户请使用 scripts/download_fonts.ps1
#
# 用法：
#   bash scripts/download_fonts.sh            # 下载所有推荐字体
#   bash scripts/download_fonts.sh fzjiagw    # 仅下载方正甲骨文

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
FONT_DIR="$ROOT/assets/fonts"
mkdir -p "$FONT_DIR"

cd "$FONT_DIR"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info() { echo -e "${GREEN}[INFO]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
err()  { echo -e "${RED}[ERR ]${NC} $*"; }

# 方正甲骨文下载（多个镜像，按优先级尝试）
download_fzjiagw() {
  local URLS=(
    "https://www.foundertype.com/FZJiaGuWen.ttf"
    "https://cdn1.foundertype.com/Public/Uploads/FZJiaGuWen.ttf"
    "https://www.zishuai.com/fonts/FZJIAGW.ttf"
    "https://m.fontke.com/font/167501847/FZJIAGW.ttf"
    "https://www.souziti.com/font/FZJIAGW-47329/FZJIAGW.ttf"
  )

  if [[ -f "FZJIAGW.ttf" ]]; then
    info "FZJIAGW.ttf 已存在，跳过"
    return 0
  fi

  info "下载方正甲骨文 FZJIAGW.ttf..."
  for url in "${URLS[@]}"; do
    warn "尝试镜像: $url"
    if curl -L -f -o FZJIAGW.ttf "$url" 2>/dev/null; then
      info "✓ 下载成功: FZJIAGW.ttf ($(du -h FZJIAGW.ttf | cut -f1))"
      return 0
    fi
  done

  err "✗ 所有镜像均失败，请手动从方正字库官网下载并放置到 $FONT_DIR/FZJIAGW.ttf"
  err "  官方地址：https://www.foundertype.com/index.php/Register/index.html"
  return 1
}

# 白舟甲骨文（CC0，2025 年日本白舟书体免费下载季）
download_hakusyu() {
  if [[ -f "HakusyuKoukotsu.ttf" ]]; then
    info "HakusyuKoukotsu.ttf 已存在，跳过"
    return 0
  fi

  info "下载白舟甲骨文（每年 9-11 月限时免费下载）..."
  warn "白舟书体仅每年 9-11 月开放免费下载，如未到时间请访问 https://j-font.com/font/detail?font_id=48"
  warn "或从 mianfeiziti.com/thread-81674.htm 查找镜像"
}

# 汉仪陈体甲骨文（个人版 ¥10，商业版需联系）
download_hanyi_chen() {
  if [[ -f "HYChenTiJiaGuWen.ttf" ]]; then
    info "HYChenTiJiaGuWen.ttf 已存在，跳过"
    return 0
  fi

  info "汉仪陈体甲骨文..."
  warn "汉仪陈体甲骨文需购买个人版（¥10）或商业版"
  warn "购买地址：https://www.hanyi.com.cn/ 或第三方下载站"
}

# 主逻辑
case "${1:-all}" in
  fzjiagw)   download_fzjiagw ;;
  hakusyu)   download_hakusyu ;;
  hanyi)     download_hanyi_chen ;;
  all|*)
    download_fzjiagw || warn "方正甲骨文下载失败"
    download_hakusyu
    download_hanyi_chen
    ;;
esac

info "字体下载完成。已下载字体："
ls -lh "$FONT_DIR"/*.ttf 2>/dev/null || warn "目录中暂无字体文件"