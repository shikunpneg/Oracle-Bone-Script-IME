"""
run.py — 启动脚本入口
支持: python -m app.run
"""

import logging
import sys

import uvicorn

from .main import FONT_PATH, app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("oracle-ime")

if __name__ == "__main__":
    log.info(f"启动甲骨文输入法服务端，监听 http://127.0.0.1:19840")
    log.info(f"字体路径: {FONT_PATH} (存在: {FONT_PATH.exists()})")
    uvicorn.run(app, host="127.0.0.1", port=19840, log_level="info")