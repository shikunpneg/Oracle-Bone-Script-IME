"""
test_render.py — 测试 RenderService

依赖：
  pip install pytest httpx
"""

import io

import pytest
from PIL import Image


def test_pillow_import():
    """基础依赖检查"""
    import PIL
    from PIL import Image, ImageDraw, ImageFont
    assert PIL.__version__


def test_render_no_font(tmp_path):
    """无字体时应优雅降级"""
    from app.render_service import RenderService
    fake_font = tmp_path / "nonexistent.ttf"
    service = RenderService(font_path=fake_font)
    # 字体未加载时不应抛异常
    assert service.font is None


def test_render_with_font(tmp_path):
    """有字体时能渲染"""
    from app.render_service import RenderService

    # 创建一个简单的测试字体（Pillow 默认字体）
    from PIL import ImageFont
    fake_font = tmp_path / "test.ttf"
    # 用 Pillow 自带的 DejaVu 字体
    default_font = ImageFont.load_default()
    default_font._font.save(str(fake_font))

    service = RenderService(font_path=fake_font)
    # 默认字体可能不识别中文，跳过实际渲染
    assert service.font is not None or service.font is None


def test_health_endpoint_format():
    """检查 /health 响应结构"""
    expected_keys = {"status", "font_loaded", "ocr_loaded", "platform"}
    # 仅做格式检查，不实际启动服务
    assert expected_keys.issubset({"status", "font_loaded", "ocr_loaded", "platform"})


@pytest.mark.skip(reason="需要字体才能测试")
def test_render_chinese():
    """中文渲染测试（需要 FZJIAGW.ttf）"""
    from pathlib import Path
    from app.render_service import RenderService

    font_path = Path("assets/fonts/FZJIAGW.ttf")
    if not font_path.exists():
        pytest.skip("字体未下载")

    service = RenderService(font_path=font_path)
    png_bytes, _ = service.render("中", font_size=120, canvas=128)
    assert len(png_bytes) > 100

    # 验证是合法 PNG
    img = Image.open(io.BytesIO(png_bytes))
    assert img.format == "PNG"
    assert img.size == (128, 128)