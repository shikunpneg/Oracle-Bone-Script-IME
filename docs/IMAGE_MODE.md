# 图片输出模式 · 详细使用指南

> 解决"对方没装字体=豆腐块"的根本问题

## 工作流程图

```
[用户在任意输入框打字"我爱甲骨文"]
   ↓
[按 Ctrl+Shift+I 启用图片模式]
   ↓
RIME commit text "我爱甲骨文"
   ↓
oracle_image_trigger.lua 触发
   ↓
POST http://127.0.0.1:19840/oracle/render
{
  "text": "我爱甲骨文",
  "mode": "image",
  "auto_paste": true
}
   ↓
RenderService:
  1. Pillow 渲染"我爱甲骨文"为 PNG
  2. 写入系统剪贴板
  3. 模拟 Ctrl+V
   ↓
[聊天框出现甲骨文图片] ✅
   ↓
[发送给对方] 对方无需装任何字体
```

## 为什么需要图片模式？

### 问题：甲骨文字符不在 Unicode 中

- 目前 Unicode 没有为甲骨文分配独立码位
- 方正甲骨文字体使用 BMP 汉字码位承载字形
- 但这导致"对方设备若无对应字体，显示豆腐块"
- PUA 私有区字符在微信/QQ 中也无法可靠显示

### 解决方案：图片作为通用媒介

- 图片是**通用媒介**，不依赖字体
- 微信/QQ/Telegram/邮件/Slack 都能完美显示
- 接收方**零门槛**

## 启用步骤

### 桌面端

1. 启动渲染服务：
   ```bash
   cd server
   python -m app.main
   # 默认监听 127.0.0.1:19840
   ```

2. 在 RIME 输入状态下，按 `Ctrl+Shift+I` 切换到图片模式
   - 状态栏显示当前模式
   - 候选词后会显示"🐘"图标

3. 在任意输入框（微信/QQ/Word/网页）正常打字
   - 上屏时**不会**出现文字
   - 自动粘贴一张甲骨文图片

### Chrome/Edge 扩展

1. 启动本地渲染服务（同上）
2. 加载 `extension/` 目录到 Chrome
3. 在任意网页输入框点击聚焦
4. 按 `Ctrl+Shift+I`（也可点扩展图标）
5. 输入框中的文字自动变图片粘贴

### Electron 桌面端

1. 启动 Electron 应用（自动管理 Python 服务）
2. 全局按 `Ctrl+Shift+I`
3. 剪贴板中的文字自动渲染为图片并粘贴

## 跨平台差异

### Windows

```python
# PowerShell 写剪贴板 + SendKeys
Add-Type -AssemblyName System.Windows.Forms
$img = [System.Drawing.Image]::FromFile($tmp)
[System.Windows.Forms.Clipboard]::SetDataObject(...)
(New-Object -ComObject WScript.Shell).SendKeys("^v")
```

依赖：PowerShell（系统自带）

### macOS

```bash
# osascript 写剪贴板 + 模拟键盘
osascript -e 'set the clipboard to (read file ... as PNG picture)'
osascript -e 'tell application "System Events" to keystroke "v" using command down'
```

依赖：osascript（系统自带），**可能需要在"系统设置 → 隐私 → 辅助功能"中允许**

### Linux

```bash
# xclip 写剪贴板 + xdotool 模拟
xclip -selection clipboard -t image/png -i $tmp
xdotool key ctrl+v
```

依赖：
```bash
sudo apt install xclip xdotool
# 或 Fedora:
sudo dnf install xclip xdotool
```

## 高级配置

### 自定义字号

默认字号 220，适合微信聊天。如需更大或更小：

修改 `rime/jiaguwen.schema.yaml`：
```yaml
switches:
  - name: oracle_image_size
    states: [小, 中, 大]
    reset: 1   # 默认中
```

修改 `rime/lua/oracle_image_trigger.lua`：
```lua
local sizes = {120, 220, 320}
local size_idx = env.engine.context:get_option("oracle_image_size")
local req_body = string.format(
    '{"text": "%s", "mode": "image", "font_size": %d}',
    commit_text, sizes[size_idx] or 220
)
```

### 自定义画布大小

修改 `server/app/render_service.py`：
```python
@app.post("/oracle/render")
def render_text(req: RenderRequest):
    png_bytes, _ = render_service.render(
        text=req.text,
        font_size=req.font_size,
        canvas=req.canvas,  # 默认 256
    )
```

### 多字渲染

如需一次渲染多个字符（如"我爱甲骨文"），服务端会自动计算布局：

```python
# 当前实现：每个字符独立 256×256 PNG，水平拼接
def render_multi(self, text, font_size=220, canvas=256):
    imgs = []
    for ch in text:
        img = self._render_single(ch, font_size, canvas)
        imgs.append(img)
    # 拼接
    total_width = canvas * len(imgs)
    combined = Image.new("RGBA", (total_width, canvas), (0,0,0,0))
    for i, img in enumerate(imgs):
        combined.paste(img, (i*canvas, 0), img)
    return combined
```

## 故障排查

### Q1：图片模式按了但没反应

**症状**：`Ctrl+Shift+I` 后，输入框无变化。

**排查**：
```bash
# 1. 确认服务在线
curl http://127.0.0.1:19840/health

# 2. 直接测试渲染
curl -X POST http://127.0.0.1:19840/oracle/render \
  -H "Content-Type: application/json" \
  -d '{"text":"中","auto_paste":false}' \
  --output test.png
# 检查 test.png 是否是合法 PNG
file test.png
```

### Q2：模拟 Ctrl+V 失败

**症状**：剪贴板有图，但聊天框没出现图片。

**原因**：
- Windows：被杀毒软件拦截
- macOS：未授予"辅助功能"权限
- Linux：缺少 xclip/xdotool

**解决**：
- Windows：在 PowerShell 中手动测试 `(New-Object -ComObject WScript.Shell).SendKeys("^v")`
- macOS：系统设置 → 隐私 → 辅助功能 → 添加 Terminal/iTerm
- Linux：`which xclip xdotool`

### Q3：图片发出去对方看不到

**症状**：自己看到图片正常，对方说"图片加载失败"。

**可能原因**：
1. 图片太大（> 5MB，微信限制）→ 调小字号
2. 网络问题 → 让对方重新接收
3. 平台不支持（如某些企业 IM）→ 用文本模式 + 引导装字体

### Q4：图片中的字是"？"或乱码

**症状**：生成的图片里是"？"或方块。

**原因**：FZJIAGW.ttf 中没有该字符。

**排查**：
```python
from fontTools.ttLib import TTFont
font = TTFont("assets/fonts/FZJIAGW.ttf")
cmap = font.getBestCmap()
print(f"中" in cmap)  # True
print(f"𠂉" in cmap)  # False
```

**解决**：
- 用图片模式时，遇到未收录字会自动 fallback
- 或下载白舟甲骨（更广覆盖）替换字体

## 安全提示

- ⚠️ 本服务仅监听 `127.0.0.1`，不暴露公网
- ⚠️ 但同局域网内其他设备可访问（如开放防火墙）
- 如需严格隔离，设置防火墙：
  ```bash
  # Linux
  sudo iptables -A INPUT -p tcp --dport 19840 -s 127.0.0.1 -j ACCEPT
  sudo iptables -A INPUT -p tcp --dport 19840 -j DROP
  ```