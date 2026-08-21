"""
甲骨文输入法 · FastAPI 后端服务

提供两个核心端点：
  POST /oracle/render { text } → PNG 图片（字 → 图）
  POST /oracle/ocr    { image } → 汉字候选（图 → 字）

支持跨平台自动粘贴到剪贴板：
  - Windows: PowerShell + SendKeys
  - macOS: osascript
  - Linux: xclip + xdotool
"""

import logging
import sys
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

from .ocr_service import OCRService
from .render_service import RenderService

# === 日志配置 ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("oracle-ime")

# === 路径配置 ===
ROOT = Path(__file__).resolve().parent.parent.parent
FONT_PATH = ROOT / "assets" / "fonts" / "FZJIAGW.ttf"
WEIGHTS_DIR = ROOT / "weights"
ID_TO_CHINESE_PATH = ROOT / "data" / "id_to_chinese.json"


# === FastAPI 应用 ===
app = FastAPI(
    title="Oracle-Bone-Script-IME Server",
    description="甲骨文输入法后端 · 字转图渲染 + OCR 反向识别",
    version="0.1.0",
)

# 允许 Chrome 扩展跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === 服务实例 ===
render_service = RenderService(font_path=FONT_PATH)
ocr_service = None  # 延迟初始化（需 ONNX 权重）


# === 数据模型 ===
class RenderRequest(BaseModel):
    text: str
    mode: str = "image"  # image | svg
    auto_paste: bool = True
    font_size: int = 220
    canvas: int = 256


class RenderResponse(BaseModel):
    status: str
    text: str
    png_bytes: int
    pasted: bool


class OCRResponse(BaseModel):
    candidates: list[dict]


# === 健康检查 ===
@app.get("/")
def root():
    return {
        "name": "Oracle-Bone-Script-IME Server",
        "version": "0.1.0",
        "endpoints": [
            "POST /oracle/render  - 文字 → 图片",
            "POST /oracle/ocr     - 图片 → 文字",
            "GET  /health         - 健康检查",
        ],
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "font_loaded": render_service.font is not None,
        "ocr_loaded": ocr_service is not None,
        "platform": sys.platform,
    }


# === 字 → 图渲染 ===
@app.post("/oracle/render")
def render_text(req: RenderRequest):
    """接收文字，返回甲骨文 PNG 图片（透明背景）"""
    if not req.text.strip():
        raise HTTPException(400, "text 不能为空")

    try:
        png_bytes, svg_text = render_service.render(
            text=req.text,
            font_size=req.font_size,
            canvas=req.canvas,
            return_svg=(req.mode == "svg"),
        )

        # 自动复制到剪贴板 + 模拟粘贴
        pasted = False
        if req.auto_paste:
            pasted = render_service.copy_to_clipboard_and_paste(
                png_bytes=png_bytes, text=req.text
            )

        if req.mode == "svg":
            return Response(content=svg_text, media_type="image/svg+xml")

        # 中文字符不能直接放在 HTTP header（uvicorn 用 latin-1 编码）
        # 改用 Base64 编码到 X-Oracle-Text-B64 头
        import base64
        text_b64 = base64.b64encode(req.text.encode("utf-8")).decode("ascii")

        return Response(
            content=png_bytes,
            media_type="image/png",
            headers={
                "X-Oracle-Pasted": "true" if pasted else "false",
                "X-Oracle-Text-B64": text_b64,
                "Access-Control-Expose-Headers": "X-Oracle-Pasted, X-Oracle-Text-B64",
            },
        )
    except Exception as e:
        log.exception("渲染失败")
        raise HTTPException(500, f"渲染失败: {e}")


# === 图 → 字 OCR ===
@app.post("/oracle/ocr")
def ocr_image(image: UploadFile = File(...)):
    """接收甲骨文图片，返回 Top-5 汉字候选"""
    global ocr_service

    # 延迟加载 OCR 模型（避免服务启动慢）
    if ocr_service is None:
        weight_path = WEIGHTS_DIR / "obc_vit_hust_obs.onnx"
        if not weight_path.exists():
            raise HTTPException(
                503,
                f"OCR 模型未就绪，请先下载权重到 {weight_path}（见 weights/README.md）"
            )
        ocr_service = OCRService(
            weight_path=weight_path,
            id_to_chinese_path=ID_TO_CHINESE_PATH,
        )

    try:
        image_bytes = image.file.read()
        candidates = ocr_service.recognize(image_bytes, top_k=5)
        return {"candidates": candidates}
    except Exception as e:
        log.exception("OCR 失败")
        raise HTTPException(500, f"OCR 失败: {e}")


if __name__ == "__main__":
    import uvicorn
    log.info(f"启动甲骨文输入法服务端，监听 http://127.0.0.1:19840")
    log.info(f"字体路径: {FONT_PATH} (存在: {FONT_PATH.exists()})")
    uvicorn.run(app, host="127.0.0.1", port=19840, log_level="info")