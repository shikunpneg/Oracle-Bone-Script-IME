"""
render_service.py — 文字 → 图片渲染服务

核心功能：
  1. 加载 FZJIAGW.ttf
  2. 用 Pillow 把文字渲染成透明背景 PNG
  3. 跨平台把 PNG 写入系统剪贴板 + 模拟 Ctrl+V

作者：Oracle-Bone-Script-IME 团队
许可：Apache-2.0
"""

import logging
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

log = logging.getLogger(__name__)


class RenderService:
    """甲骨文渲染服务"""

    def __init__(self, font_path: Path):
        self.font_path = Path(font_path)
        self.font = None
        self._load_font()

    def _load_font(self):
        """加载字体"""
        if not self.font_path.exists():
            log.warning(
                f"字体文件不存在: {self.font_path}\n"
                "请先运行: bash scripts/download_fonts.sh\n"
                "或从方正字库下载 FZJIAGW.ttf 放置到 assets/fonts/"
            )
            return
        try:
            self.font = ImageFont.truetype(str(self.font_path), 220)
            log.info(f"✓ 字体已加载: {self.font_path}")
        except Exception as e:
            log.error(f"字体加载失败: {e}")

    def render(
        self,
        text: str,
        font_size: int = 220,
        canvas: int = 256,
        return_svg: bool = False,
    ) -> tuple[bytes, str | None]:
        """
        渲染文字为 PNG bytes（透明背景）

        Returns:
            (png_bytes, svg_text or None)
        """
        if self.font is None:
            raise RuntimeError("字体未加载")

        # 重新设置字号
        font = ImageFont.truetype(str(self.font_path), font_size)

        # 创建透明画布
        img = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 居中绘制
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (canvas - w) // 2 - bbox[0]
        y = (canvas - h) // 2 - bbox[1]
        draw.text((x, y), text, font=font, fill=(0, 0, 0, 255))

        # 导出 PNG bytes
        import io
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        png_bytes = buf.getvalue()

        # 可选 SVG 输出（用 <text> + 字体名）
        svg_text = None
        if return_svg:
            svg_text = (
                f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'viewBox="0 0 {canvas} {canvas}">'
                f'<text x="{canvas//2}" y="{canvas//2}" '
                f'text-anchor="middle" dominant-baseline="central" '
                f'font-family="FZJIAGW" font-size="{int(font_size*0.86)}" '
                f'fill="black">{text}</text></svg>'
            )

        return png_bytes, svg_text

    def copy_to_clipboard_and_paste(self, png_bytes: bytes, text: str = "") -> bool:
        """
        跨平台写入剪贴板 + 模拟 Ctrl+V

        Returns:
            是否成功粘贴
        """
        # 保存临时文件
        with tempfile.NamedTemporaryFile(
            suffix=".png", delete=False, dir=tempfile.gettempdir()
        ) as f:
            f.write(png_bytes)
            tmp_path = f.name

        try:
            sysname = platform.system()

            if sysname == "Windows":
                return self._paste_windows(tmp_path)
            elif sysname == "Darwin":
                return self._paste_macos(tmp_path)
            elif sysname == "Linux":
                return self._paste_linux(tmp_path)
            else:
                log.warning(f"未知平台: {sysname}")
                return False
        finally:
            # 延迟删除（剪贴板读取需要文件存在）
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

    def _paste_windows(self, png_path: str) -> bool:
        """Windows：PowerShell 写剪贴板 + SendKeys（用 Base64 + 临时文件避免编码问题）"""
        try:
            # 1. 把图片读为 Base64
            import base64
            with open(png_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")

            # 2. 写入 PowerShell 脚本到临时文件
            import tempfile
            ps_script = (
                "Add-Type -AssemblyName System.Windows.Forms\n"
                "Add-Type -AssemblyName System.Drawing\n"
                "$bytes = [Convert]::FromBase64String('" + b64 + "')\n"
                "$ms = New-Object System.IO.MemoryStream($bytes, 0, $bytes.Length)\n"
                "$img = [System.Drawing.Image]::FromStream($ms, $true)\n"
                "[System.Windows.Forms.Clipboard]::SetImage($img)\n"
            )
            ps_file = tempfile.NamedTemporaryFile(
                suffix=".ps1", delete=False, mode="w", encoding="utf-8"
            )
            ps_file.write(ps_script)
            ps_file.close()

            subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file.name],
                check=True,
                capture_output=True,
                timeout=10,
            )

            # 3. 模拟 Ctrl+V
            subprocess.run(
                ["powershell", "-Command",
                 "(New-Object -ComObject WScript.Shell).SendKeys('^v')"],
                check=True,
                capture_output=True,
                timeout=5,
            )
            log.info("✓ Windows: 已粘贴甲骨文图片到剪贴板 + Ctrl+V")
            return True
        except subprocess.CalledProcessError as e:
            err = e.stderr.decode("utf-8", errors="ignore") if e.stderr else ""
            log.error(f"Windows 粘贴失败: {err}")
            return False
        except Exception as e:
            log.error(f"Windows 粘贴异常: {e}")
            return False

    def _paste_macos(self, png_path: str) -> bool:
        """macOS：osascript 写剪贴板 + 模拟 Cmd+V"""
        try:
            # 1. 写入剪贴板
            subprocess.run(
                ["osascript", "-e",
                 f'set the clipboard to (read file POSIX file "{png_path}" as PNG picture)'],
                check=True, timeout=5
            )

            # 2. 模拟 Cmd+V
            subprocess.run(
                ["osascript", "-e",
                 'tell application "System Events" to keystroke "v" using command down'],
                check=True, timeout=5
            )
            log.info("✓ macOS: 已粘贴甲骨文图片到剪贴板 + Cmd+V")
            return True
        except Exception as e:
            log.error(f"macOS 粘贴失败: {e}")
            return False

    def _paste_linux(self, png_path: str) -> bool:
        """Linux：xclip 写剪贴板 + xdotool 模拟 Ctrl+V"""
        try:
            # 1. 写入剪贴板
            subprocess.run(
                ["xclip", "-selection", "clipboard", "-t", "image/png", "-i", png_path],
                check=True, timeout=5,
            )

            # 2. 模拟 Ctrl+V
            subprocess.run(
                ["xdotool", "key", "ctrl+v"],
                check=True, timeout=5,
            )
            log.info("✓ Linux: 已粘贴甲骨文图片到剪贴板 + Ctrl+V")
            return True
        except FileNotFoundError as e:
            log.error(
                f"Linux 粘贴失败: 缺少依赖 {e.filename}\n"
                "请安装: sudo apt install xclip xdotool"
            )
            return False
        except Exception as e:
            log.error(f"Linux 粘贴异常: {e}")
            return False