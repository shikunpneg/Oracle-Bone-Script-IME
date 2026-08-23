"""
test_api.py — FastAPI 端到端测试

用法：
  # 启动服务后
  pytest server/tests/test_api.py -v
"""

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_root():
    """测试根路径"""
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Oracle-Bone-Script-IME Server" in data["name"]


@pytest.mark.asyncio
async def test_health():
    """测试健康检查"""
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_render_empty_text():
    """测试空文本应返回 400"""
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/oracle/render", json={"text": ""})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_render_no_font(monkeypatch):
    """测试无字体时返回 500"""
    from pathlib import Path
    from app import main
    from app.main import app

    # 把字体路径改成不存在的文件
    main.FONT_PATH = Path("/tmp/nonexistent.ttf")
    main.render_service = main.RenderService(font_path=main.FONT_PATH)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/oracle/render", json={"text": "中", "auto_paste": False})
    # 应该返回 500（因为字体不存在）
    assert response.status_code in (500, 503)