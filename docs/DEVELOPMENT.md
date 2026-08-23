# 开发指南

> 给贡献者的快速上手手册

## 开发环境

- Python 3.9+
- Node.js 18+
- （可选）Git
- （可选）PowerShell / Bash

## 仓库结构

```
oracle-bone-script-ime/
├── assets/fonts/           # 甲骨文字体（不进 git）
├── data/                   # 字源映射数据
├── dist/                   # 构建产物
│   ├── fonts/              # WOFF2 子集
│   ├── glyphs/             # 预渲染 PNG
│   └── glyphs-sprite.svg   # SVG sprite
├── docs/                   # 用户文档
├── electron/               # Electron 桌面端
├── extension/              # Chrome/Edge 扩展
├── rime/                   # RIME 输入法方案
├── scripts/                # 工具脚本
├── server/                 # FastAPI 后端
│   ├── app/                # 业务代码
│   └── tests/              # 测试
├── web/                    # Web Demo
└── weights/                # 模型权重（不进 git）
```

## 本地开发流程

### 1. 安装字体

```bash
bash scripts/download_fonts.sh
# 或 Windows: powershell -ExecutionPolicy Bypass -File scripts\download_fonts.ps1
```

### 2. 构建 WOFF2 + PNG + SVG sprite

```bash
pip install fonttools brotli Pillow
python scripts/build_glyph_assets.py
```

输出到 `dist/`。

### 3. 安装服务端依赖

```bash
cd server
pip install -r requirements.txt
```

### 4. 启动服务端

```bash
cd server
python -m app.main
# 或开发模式（自动重载）：
uvicorn app.main:app --reload --host 127.0.0.1 --port 19840
```

### 5. 启动 Web Demo

```bash
cd web
npm install
npm run dev
# 访问 http://localhost:5173
```

### 6. 加载 Chrome 扩展

1. 打开 `chrome://extensions/`
2. 开启开发者模式
3. 点击"加载已解压的扩展程序"，选择 `extension/` 目录

### 7. 启动 Electron 桌面端

```bash
cd electron
npm install
npm start
```

## 测试

### 单元测试

```bash
cd server
pytest tests/
```

### API 端到端测试

```bash
# 服务启动后
curl http://127.0.0.1:19840/health

curl -X POST http://127.0.0.1:19840/oracle/render \
  -H "Content-Type: application/json" \
  -d '{"text":"中","auto_paste":false}' \
  --output test.png
```

### RIME 测试

```bash
# 复制方案到 RIME 目录
cp -r rime/* ~/.config/rime/

# 部署（小狼毫托盘菜单）
# 或手动触发：
rime_deployer --build ~/.config/rime
```

## 添加新功能

### 案例：增加"候选词 OCR 反查"

1. 在 `server/app/ocr_service.py` 加新方法：
   ```python
   def recognize_candidates(self, image_bytes, top_k=10):
       # ... 实现
   ```

2. 在 `server/app/main.py` 暴露端点：
   ```python
   @app.post("/oracle/ocr-candidates")
   def ocr_candidates(image: UploadFile = File(...)):
       ...
   ```

3. 在 `extension/content.js` 调用：
   ```javascript
   const res = await chrome.runtime.sendMessage({
     action: "call-render-server",
     path: "/oracle/ocr-candidates",
     method: "POST",
     body: formData,
   });
   ```

4. 在 `docs/MANUAL.md` 文档化。

## 提交代码

```bash
# 1. fork 主仓库
# 2. 创建功能分支
git checkout -b feat/awesome-feature

# 3. 编写代码 + 测试

# 4. 提交
git add .
git commit -m "feat: add awesome feature"

# 5. 推送到你的 fork
git push origin feat/awesome-feature

# 6. 在 GitHub 上开 PR
```

### 提交信息规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型：`feat` / `fix` / `docs` / `style` / `refactor` / `test` / `chore`

示例：
```
feat(server): add /oracle/ocr endpoint
docs(manual): add image mode usage guide
fix(rime): fix image_trigger crash when server offline
```

## 发布新版本

1. 更新 `CHANGELOG.md`
2. 更新 `version` 字段：
   - `server/pyproject.toml`
   - `electron/package.json`
   - `web/package.json`
   - `extension/manifest.json`
3. GitHub Actions 自动构建：
   - Python：`python -m build` → 发布到 PyPI（手动）
   - Electron：`electron-builder` → GitHub Release
   - Chrome 扩展：手动上传到 Chrome Web Store

## 调试技巧

### RIME 日志

- Windows：`%TEMP%\rime.weasel.*.INFO`
- macOS：`/tmp/rime.squirrel.*.INFO`
- Linux：`~/.local/share/rime/rime.*.INFO`

启用 Lua 调试：在 schema.yaml 加入：
```yaml
__include:
  lua_debug: true
```

### 服务端日志

```bash
cd server
python -m app.main
# 默认 INFO 级别；详细日志加：
LOG_LEVEL=DEBUG python -m app.main
```

### Chrome 扩展调试

- 右键扩展图标 → 检查弹出页
- `chrome://extensions/` → "检查视图"链接 → DevTools
- `chrome://extensions/` → 错误日志

### Electron 调试

```bash
cd electron
npm start -- --dev  # 自动打开 DevTools
```