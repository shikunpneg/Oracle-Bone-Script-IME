"""演示：渲染多字 PNG 并拼接到一张图"""
import sys, io
sys.path.insert(0, '.')
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from app.render_service import RenderService

font_path = Path('../assets/fonts/FZJIAGW.ttf')
service = RenderService(font_path=font_path)

# 渲染单字列表
text = "甲骨文"
imgs = []
for ch in text:
    png, _ = service.render(ch, font_size=120, canvas=140)
    imgs.append(Image.open(io.BytesIO(png)))

# 拼接
total_w = sum(img.width for img in imgs)
combined = Image.new("RGBA", (total_w, imgs[0].height), (255, 255, 255, 255))  # 白底便于查看
x = 0
for img in imgs:
    combined.paste(img, (x, 0), img)
    x += img.width

combined.save("demo_combined.png")
print(f"Saved demo_combined.png ({combined.size}, {combined.size[0]*combined.size[1]} px)")

# 同时生成单字大图"甲"
big = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
font = ImageFont.truetype(str(font_path), 380)
draw = ImageDraw.Draw(big)
bbox = draw.textbbox((0, 0), "甲", font=font)
w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
x = (512 - w) // 2 - bbox[0]
y = (512 - h) // 2 - bbox[1]
draw.text((x, y), "甲", font=font, fill=(0, 0, 0, 255))
big.save("demo_big_甲.png")
print(f"Saved demo_big_甲.png (512x512)")