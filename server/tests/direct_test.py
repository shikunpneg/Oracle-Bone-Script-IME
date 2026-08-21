"""直接测试 render 函数，绕过 HTTP"""
import sys
sys.path.insert(0, '.')
from app.render_service import RenderService
from pathlib import Path

font_path = Path('../assets/fonts/FZJIAGW.ttf')
service = RenderService(font_path=font_path)
print(f"Font loaded: {service.font is not None}")

# 渲染单字"中"
png, _ = service.render("中", font_size=220, canvas=256, return_svg=False)
print(f"Single char '中' PNG: {len(png)} bytes")
with open("direct_test_single.png", "wb") as f:
    f.write(png)

# 渲染多字"我爱甲骨文"
png, _ = service.render("我爱甲骨文", font_size=120, canvas=180, return_svg=False)
print(f"Multi char '我爱甲骨文' PNG: {len(png)} bytes")
with open("direct_test_multi.png", "wb") as f:
    f.write(png)

print("OK")