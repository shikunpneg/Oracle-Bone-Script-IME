# 架构设计文档

> Oracle-Bone-Script-IME 的系统架构与技术选型

## 整体架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            用户交互层                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────────┐   │
│  │ Chrome/Edge 扩展 │  │ RIME 桌面方案     │  │ Electron 桌面 App    │   │
│  │ (Manifest V3)    │  │ (librime-lua)    │  │ (Win/Mac/Linux)    │   │
│  └──────────────────┘  └──────────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP / IPC
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           后端服务层                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ FastAPI (Python 3.9+) - http://127.0.0.1:19840                   │  │
│  │                                                                  │  │
│  │  POST /oracle/render  → 文字 → PNG (Pillow + FZJIAGW)           │  │
│  │  POST /oracle/ocr     → PNG  → 文字 (ONNX Runtime)              │  │
│  │  GET  /health         → 服务状态                                  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            资源层                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌─────────────────┐  │
│  │ FZJIAGW.ttf│  │ 预渲染 PNG  │  │ WOFF2 子集 │  │ ONNX 模型权重    │  │
│  │ 2.5 MB     │  │ 1431 张     │  │ 30-60 KB   │  │ ~100 MB         │  │
│  └────────────┘  └────────────┘  └────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## 核心模块

### 1. 字体子集化与预渲染

**目的**：把 2.5 MB 的 FZJIAGW.ttf 切成 30-60 KB 的 WOFF2，并预渲染 1431 张透明 PNG。

**入口**：`scripts/build_glyph_assets.py`

**依赖**：
- `fonttools`（pyftsubset）
- `brotli`（WOFF2 压缩）
- `Pillow`（PNG 渲染）

**输出**：
- `dist/fonts/FZJIAGW-subset.woff2`
- `dist/glyphs/U+4E2D.png`（1431 个透明 PNG）
- `dist/glyphs-sprite.svg`（SVG sprite）
- `dist/char-index.json`（字符索引）
- `dist/chars.txt`（纯字符列表）

### 2. RIME 输入法引擎

**目的**：提供"拼音→候选→commit"的完整输入流程。

**入口**：`rime/jiaguwen.schema.yaml`

**核心组件**：
- `translators/oracle_translator.lua`：在候选词后追加"🐘甲骨文"标签
- `filters/oracle_filter.lua`：把有甲骨文字形的候选排序在前
- `processors/oracle_image_trigger.lua`：commit 时同步触发图片生成

**支持平台**：
- Windows / macOS / Linux：小狼毫 / 鼠须管 / ibus-rime / fcitx5-rime
- Android：同文输入法（Trime）
- iOS：仓输入法（Hamster）

### 3. FastAPI 后端服务

**目的**：接收文字请求，渲染为 PNG 并自动粘贴。

**入口**：`server/app/main.py`

**核心类**：
- `RenderService`：文字 → PNG 渲染 + 跨平台剪贴板粘贴
- `OCRService`：PNG → 文字识别（ONNX Runtime）

**关键技术**：
- Pillow RGBA 透明背景渲染
- 跨平台剪贴板 API：
  - Windows：PowerShell + SendKeys
  - macOS：osascript + System Events
  - Linux：xclip + xdotool

### 4. Chrome / Edge 扩展

**目的**：在任意网页输入框中触发图片输出。

**入口**：`extension/manifest.json`

**核心组件**：
- `content.js`：注入到所有网页，监听快捷键
- `background.js`：Service Worker，处理跨域请求
- `popup.html`：扩展弹出页，显示状态

**关键技术**：
- Clipboard API（`navigator.clipboard.write`）
- `document.execCommand('paste')` 触发粘贴
- background.js 转发请求绕过 CORS

### 5. Electron 桌面端

**目的**：提供全局快捷键、托盘菜单、自动启动渲染服务。

**入口**：`electron/main.js`

**核心功能**：
- `globalShortcut` 注册 `Ctrl+Shift+I` / `Ctrl+Shift+G`
- `Tray` 创建系统托盘
- `spawn` 自动启动 Python 渲染服务
- `robotjs` 模拟键盘事件

## 数据流

### 文字 → 图片（出字）

```
用户在任意输入框打"中"
   ↓
浏览器/IME 把 "中" 写入剪贴板或表单
   ↓
[用户触发] Ctrl+Shift+I
   ↓
content.js / RIME lua / Electron main.js
   ↓
POST http://127.0.0.1:19840/oracle/render {text: "中"}
   ↓
RenderService.render("中", size=220, canvas=256)
   ↓
Pillow: img.new("RGBA", (256,256), (0,0,0,0)) + draw.text()
   ↓
img.save(buf, format="PNG", optimize=True)
   ↓
copy_to_clipboard_and_paste(buf)
   ↓
PowerShell/osascript/xclip 写入剪贴板
   ↓
SendKeys/keystroke/xdotool 模拟 Ctrl+V
   ↓
聊天框出现甲骨文图片
```

### 图片 → 文字（OCR 反向）

```
用户复制/截屏甲骨文图片
   ↓
[用户触发] Ctrl+Shift+G
   ↓
clipboard.readImage() / File 读取
   ↓
POST http://127.0.0.1:19840/oracle/ocr multipart/form-data
   ↓
OCRService.recognize(image_bytes, top_k=5)
   ↓
PIL: img.convert("L").resize((64,64)) / 255.0
   ↓
ONNX Runtime: sess.run(None, {"input": arr})
   ↓
softmax → top_k indices → ID_TO_CHINESE[idx]
   ↓
{"candidates": [{"obs_id": 234, "chinese": "中", "conf": 0.95}, ...]}
```

## 关键设计决策

### 决策 1：为什么选 RIME 而不是自己写 TSF？

| 维度 | 自研 TSF | RIME + librime-lua |
|------|----------|---------------------|
| 开发成本 | 6+ 个月 | 1-2 周 |
| 跨平台 | ❌ 仅 Windows | ✅ 5 端 |
| 候选面板 | 自定义（费时） | 内置 |
| 用户词典 | 自定义 | 内置 + 云同步 |
| 社区生态 | 弱 | 强（数百方案） |

**结论**：RIME 是最优解。

### 决策 2：为什么用图片模式而不是字符替换？

| 维度 | 字符替换（PUA） | 图片模式 |
|------|------------------|----------|
| 兼容性 | ❌ 对方需装字体 | ✅ 通用图片 |
| 实现复杂度 | 需 PUA 字体 | 只需 Pillow |
| 微信/QQ 支持 | ⚠️ 看字体回退 | ✅ 完美 |
| 大文件传输 | ❌ 小 | ⚠️ 大 |

**结论**：图片模式作为默认方案，字符模式作为补充。

### 决策 3：为什么选 ONNX Runtime 而不是 PyTorch？

| 维度 | PyTorch | ONNX Runtime |
|------|---------|--------------|
| 包大小 | ~800 MB | ~20 MB |
| 启动速度 | 慢 | 快 |
| 推理速度 | 快 | 更快 |
| 部署难度 | 中 | 简单 |

**结论**：ONNX Runtime 是部署首选。

### 决策 4：为什么前端用 Electron 而不是 Tauri？

| 维度 | Electron | Tauri |
|------|----------|-------|
| OCR 库生态 | ✅ 丰富（node-tesseract, onnxruntime-node） | ⚠️ 需自编译 |
| 跨平台一致性 | ✅ Chromium everywhere | ⚠️ WebView 碎片化 |
| 包体积 | ⚠️ 80-150 MB | ✅ 2-10 MB |
| 开发速度 | ✅ 成熟 | ⚠️ 学习曲线 |

**结论**：MVP 阶段选 Electron 优先。

## 性能指标

| 指标 | 目标值 | 实测值 |
|------|--------|--------|
| 字体加载 | < 200ms | ~150ms |
| 单字 PNG 渲染（缓存命中） | < 10ms | ~5ms |
| 单字 PNG 渲染（实时） | < 50ms | ~30ms |
| WOFF2 子集大小 | < 100KB | ~50KB |
| ONNX 推理（Top-1） | < 100ms | ~80ms |
| 跨平台剪贴板写入 | < 500ms | ~300ms |
| 模拟 Ctrl+V 延迟 | 50-100ms | 50ms |

## 安全考虑

- ✅ 所有处理在本地完成（不上传任何数据）
- ✅ 渲染服务仅监听 `127.0.0.1`（不暴露公网）
- ✅ Chrome 扩展 `host_permissions` 限定为 `127.0.0.1:19840`
- ✅ Content script 仅注入可见页面，不修改 DOM
- ⚠️ ONNX 模型权重含第三方 License，需注明

## 未来扩展

- [ ] 接入 PD-OBS 大模型释读（未释字 → 候选解释）
- [ ] 接入 AlphaOracle 专家工作流启发
- [ ] 推动 Unicode IRG 收录甲骨文（终极方案）
- [ ] WebSocket 实时同步多设备
- [ ] 移动端 OCR：拍照 → 识别 → 输入