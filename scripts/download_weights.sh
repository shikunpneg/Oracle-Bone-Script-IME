#!/usr/bin/env bash
#
# download_weights.sh — 下载甲骨文识别模型权重
#
# 用法：
#   bash scripts/download_weights.sh            # 下载所有
#   bash scripts/download_weights.sh hust       # 仅下载 HUST-OBC

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
WEIGHTS_DIR="$ROOT/weights"
mkdir -p "$WEIGHTS_DIR"

cd "$WEIGHTS_DIR"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info() { echo -e "${GREEN}[INFO]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }

download_hust_obs() {
  if [[ -f "obc_vit_hust_obs.onnx" ]]; then
    info "obc_vit_hust_obs.onnx 已存在，跳过"
    return 0
  fi

  info "下载 HUST-OBS 预训练模型..."
  warn "ONNX 权重文件不在 GitHub LFS 中，需手动获取："
  echo "  1. 访问 https://github.com/Pengjie-W/HUST-OBC"
  echo "  2. 下载 weights/obc_vit_hust_obs.pth"
  echo "  3. 转换为 ONNX（见 weights/README.md）"
  echo "  4. 放置到 $WEIGHTS_DIR/obc_vit_hust_obs.onnx"
}

download_hust_obs

info "当前 $WEIGHTS_DIR 内容:"
ls -lh "$WEIGHTS_DIR"/*.onnx "$WEIGHTS_DIR"/*.pth 2>/dev/null || warn "目录中暂无权重文件"