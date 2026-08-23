#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_glyph_assets.py — 甲骨文输入法的核心构建脚本

功能：
  1. 从 FZJIAGW.ttf 提取 cmap（汉字 → glyph）映射
  2. 用 pyftsubset 切出 WOFF2 子集（30-60 KB）
  3. 用 Pillow 预渲染 1431 个透明背景 PNG
  4. 拼装 SVG sprite（含 viewBox 索引）
  5. 输出 dist/ 目录构建产物

依赖：
  pip install fonttools brotli pillow

用法：
  python scripts/build_glyph_assets.py
  python scripts/build_glyph_assets.py --font /path/to/FZJIAGW.ttf --size 220

作者：Oracle-Bone-Script-IME 团队
许可：Apache-2.0
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from fontTools.ttLib import TTFont
    from fontTools.subset import Subsetter, Options
except ImportError:
    sys.exit("缺少 fonttools，请运行: pip install fonttools brotli")

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("缺少 Pillow，请运行: pip install pillow")


def extract_charlist(font_path: Path) -> list[str]:
    """从字体 cmap 中提取所有已映射的 BMP/CJK 汉字字符"""
    font = TTFont(str(font_path))
    cmap = font.getBestCmap()
    chars = []
    for cp in sorted(cmap.keys()):
        ch = chr(cp)
        # 只保留 CJK 统一汉字 + CJK 扩展 A-F + PUA
        if (
            0x4E00 <= cp <= 0x9FFF           # CJK Unified
            or 0x3400 <= cp <= 0x4DBF        # CJK Ext A
            or 0x20000 <= cp <= 0x2A6DF      # CJK Ext B
            or 0x2A700 <= cp <= 0x2B73F      # CJK Ext C
            or 0x2B740 <= cp <= 0x2B81F      # CJK Ext D
            or 0x2B820 <= cp <= 0x2CEAF      # CJK Ext E
            or 0x2CEB0 <= cp <= 0x2EBEF      # CJK Ext F
            or 0x30000 <= cp <= 0x3134F      # CJK Ext G
            or 0xE000 <= cp <= 0xF8FF        # PUA
        ):
            chars.append(ch)
    print(f"[INFO] 从字体提取了 {len(chars)} 个字符")
    return chars


def subset_font(font_path: Path, chars: list[str], output: Path):
    """字体子集化（WOFF2 格式，保留全部布局特性）"""
    print(f"[INFO] 字体子集化: {font_path.name} → {output.name}")
    font = TTFont(str(font_path))
    opts = Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.hinting = False
    opts.legacy_cmap = False
    opts.name_IDs = ["*"]
    sub = Subsetter(options=opts)
    sub.populate(text="".join(chars))
    sub.subset(font)
    output.parent.mkdir(parents=True, exist_ok=True)
    font.save(str(output))
    size_kb = output.stat().st_size / 1024
    print(f"[INFO] ✓ 子集化完成: {output.name} ({size_kb:.1f} KB)")


def render_glyphs(font_path: Path, chars: list[str], out_dir: Path,
                  size: int = 220, canvas: int = 256):
    """预渲染每个字为 256×256 透明背景 PNG"""
    print(f"[INFO] 预渲染 {len(chars)} 张 PNG（size={size}, canvas={canvas}）...")
    out_dir.mkdir(parents=True, exist_ok=True)
    pil_font = ImageFont.truetype(str(font_path), size)
    for i, ch in enumerate(chars):
        img = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), ch, font=pil_font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (canvas - w) // 2 - bbox[0]
        y = (canvas - h) // 2 - bbox[1]
        draw.text((x, y), ch, font=pil_font, fill=(0, 0, 0, 255))
        png_path = out_dir / f"U+{ord(ch):04X}.png"
        img.save(png_path, optimize=True)
        if (i + 1) % 100 == 0:
            print(f"  [{i+1}/{len(chars)}] 已渲染 U+{ord(ch):04X}.png")
    print(f"[INFO] ✓ PNG 渲染完成，共 {len(chars)} 张")


def build_svg_sprite(chars: list[str], out_path: Path, canvas: int = 256):
    """拼装 SVG sprite（每个字符一个 <symbol>，可用 <use> 引用）"""
    print(f"[INFO] 构建 SVG sprite: {out_path.name}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'style="display:none" width="0" height="0">'
    ]
    for ch in chars:
        cp = ord(ch)
        symbol_id = f"oracle-{cp:04X}"
        parts.append(
            f'<symbol id="{symbol_id}" viewBox="0 0 {canvas} {canvas}">'
            f'<text x="{canvas//2}" y="{canvas//2}" '
            f'text-anchor="middle" dominant-baseline="central" '
            f'font-size="{int(canvas*0.86)}">{ch}</text>'
            f'</symbol>'
        )
    parts.append('</svg>')
    out_path.write_text("\n".join(parts), encoding="utf-8")
    size_kb = out_path.stat().st_size / 1024
    print(f"[INFO] ✓ SVG sprite 完成: {out_path.name} ({size_kb:.1f} KB)")


def build_char_index(chars: list[str], out_path: Path):
    """导出字符索引 JSON（含 Unicode 码位、UTF-8 编码、SVG id）"""
    print(f"[INFO] 构建字符索引: {out_path.name}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    index = {
        "version": "0.1.0",
        "generator": "build_glyph_assets.py",
        "font": "FZJIAGW",
        "count": len(chars),
        "chars": [
            {
                "char": ch,
                "codepoint": f"U+{ord(ch):04X}",
                "utf8_hex": ch.encode("utf-8").hex(),
                "svg_id": f"oracle-{ord(ch):04X}",
                "png": f"glyphs/U+{ord(ch):04X}.png",
            }
            for ch in chars
        ],
    }
    out_path.write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"[INFO] ✓ 字符索引完成: {out_path.name} ({len(chars)} 条)")


def main():
    parser = argparse.ArgumentParser(
        description="甲骨文输入法 · 字体子集化与预渲染工具"
    )
    parser.add_argument(
        "--font",
        default="assets/fonts/FZJIAGW.ttf",
        help="输入字体文件路径（默认: assets/fonts/FZJIAGW.ttf）"
    )
    parser.add_argument(
        "--out-dir",
        default="dist",
        help="输出目录（默认: dist）"
    )
    parser.add_argument(
        "--size",
        type=int,
        default=220,
        help="渲染字号（默认: 220）"
    )
    parser.add_argument(
        "--canvas",
        type=int,
        default=256,
        help="画布尺寸（默认: 256×256）"
    )
    parser.add_argument(
        "--skip-png",
        action="store_true",
        help="跳过 PNG 预渲染（仅生成 WOFF2 和 SVG sprite）"
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    font_path = Path(args.font)
    if not font_path.is_absolute():
        font_path = root / font_path

    if not font_path.exists():
        sys.exit(f"字体文件不存在: {font_path}\n请先运行: bash scripts/download_fonts.sh")

    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = root / out_dir

    print(f"[INFO] 输入字体: {font_path}")
    print(f"[INFO] 输出目录: {out_dir}")
    print(f"[INFO] 渲染参数: size={args.size}, canvas={args.canvas}×{args.canvas}")

    # 1. 提取字符列表
    chars = extract_charlist(font_path)

    # 2. 写出字符列表（供其他脚本使用）
    chars_txt = out_dir / "chars.txt"
    chars_txt.parent.mkdir(parents=True, exist_ok=True)
    chars_txt.write_text("".join(chars), encoding="utf-8")
    print(f"[INFO] 字符列表: {chars_txt}")

    # 3. 字体子集化（WOFF2）
    subset_font(font_path, chars, out_dir / "fonts" / "FZJIAGW-subset.woff2")

    # 4. 预渲染 PNG
    if not args.skip_png:
        render_glyphs(font_path, chars, out_dir / "glyphs",
                      size=args.size, canvas=args.canvas)

    # 5. SVG sprite
    build_svg_sprite(chars, out_dir / "glyphs-sprite.svg", canvas=args.canvas)

    # 6. 字符索引 JSON
    build_char_index(chars, out_dir / "char-index.json")

    print("\n[INFO] 🎉 全部构建完成！")
    print(f"[INFO] 产物:")
    print(f"  • {out_dir}/chars.txt               - 字符列表")
    print(f"  • {out_dir}/fonts/FZJIAGW-subset.woff2  - 子集化字体")
    print(f"  • {out_dir}/glyphs/U+XXXX.png        - 1431 张透明 PNG")
    print(f"  • {out_dir}/glyphs-sprite.svg        - SVG sprite")
    print(f"  • {out_dir}/char-index.json          - 字符索引")


if __name__ == "__main__":
    main()