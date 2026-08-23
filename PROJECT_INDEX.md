# Oracle-Bone-Script-IME · 项目索引

> 项目所在地：`e:\甲骨文输入法\oracle-bone-script-ime`
> 创建时间：2026-08-20
> 当前版本：v0.1.0
> **状态：✅ MVP 已完成，smoke 测试全部通过**

---

## 🎯 已完成功能

| 功能 | 状态 | 验证 |
|------|------|------|
| ✅ 字体下载 | 完成 | FZJIAGW.ttf 2.5 MB 1430 字 |
| ✅ 字体子集化 | 完成 | WOFF2 2.5 MB（字符 1430） |
| ✅ PNG 预渲染 | 完成 | 1430 张透明 PNG，总 6.4 MB |
| ✅ SVG sprite 拼装 | 完成 | 217 KB |
| ✅ 字符索引生成 | 完成 | char-index.json 232 KB |
| ✅ FastAPI 渲染服务 | 完成 | `/health`、`/oracle/render` 端到端通过 |
| ✅ RIME 方案 + Lua 钩子 | 完成 | 3 个 lua 文件 + schema.yaml + dict.yaml |
| ✅ Chrome MV3 扩展 | 完成 | 6 个文件 + 上架材料 |
| ✅ Electron 桌面端 | 完成 | 5 个文件（main/preload/renderer） |
| ✅ Web Demo (Vue 3) | 完成 | 7 个文件 |
| ✅ 完整文档 | 完成 | MANUAL/ARCHITECTURE/DEVELOPMENT/IMAGE_MODE/DATA |
| ✅ README/LICENSE/CI/.gitignore | 完成 | 标准开源项目元数据 |
| ✅ OCR 接口占位 | 完成 | 模型未下载时返回 503，符合预期 |

## 📊 smoke test 结果（2026-08-20）

```
=== 1. GET / ===                                          status=200 ✓
=== 2. GET /health ===   font_loaded=true, ocr_loaded=false ✓
=== 3. POST /oracle/render (auto_paste=False) ===
       content-type=image/png
       x-oracle-text-b64=55Sy6aqo5paH => 甲骨文
       png bytes=3769 (生成成功) ✓
=== 4. POST /oracle/render (empty text → 400) ===        ✓
=== 5. POST /oracle/ocr (无权重 → 503) ===               ✓
=== ✅ 所有 smoke 测试通过 ===
```

## 🐛 已修复的关键 Bug

1. **uvicorn 中文 header 编码失败** → 改用 `X-Oracle-Text-B64` Base64 编码
2. **PowerShell 中文路径 + 字符编码错误** → 改用 Base64 + 临时 .ps1 文件
3. **urllib header 大小写敏感** → 客户端统一转小写

## 📂 项目结构

```
oracle-bone-script-ime/
├── README.md                  # 项目主页（中文）
├── LICENSE                    # Apache-2.0
├── CHANGELOG.md               # 版本历史
├── CONTRIBUTING.md            # 贡献指南
├── .gitignore                 # Git 忽略配置
│
├── assets/
│   └── fonts/
│       └── FZJIAGW.ttf        # 方正甲骨文 2.5 MB
│
├── data/                      # （预留）ID→汉字映射
├── weights/                   # （预留）ONNX 模型权重
│   └── README.md
│
├── scripts/
│   ├── build_glyph_assets.py  # 字体子集化 + 渲染脚本
│   ├── download_fonts.sh      # Linux/macOS 字体下载
│   ├── download_fonts.ps1     # Windows 字体下载
│   └── download_weights.sh    # 模型权重下载
│
├── dist/                      # 构建产物（应纳入 git lfs 或 .gitignore）
│   ├── chars.txt              # 1430 个汉字
│   ├── char-index.json        # 字符索引
│   ├── glyphs-sprite.svg      # SVG sprite
│   ├── fonts/
│   │   └── FZJIAGW-subset.woff2
│   └── glyphs/                # 1430 张 PNG（6.4 MB）
│       ├── U+4E00.png
│       ├── U+4E01.png
│       └── ... (1430 个)
│
├── rime/                      # RIME 输入法方案
│   ├── jiaguwen.schema.yaml
│   ├── jiaguwen.dict.yaml
│   ├── lua/
│   │   ├── oracle_translator.lua
│   │   ├── oracle_filter.lua
│   │   └── oracle_image_trigger.lua
│   └── README.md
│
├── server/                    # FastAPI 后端
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── README.md
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI 入口
│   │   ├── render_service.py  # 字 → 图渲染 + 剪贴板
│   │   ├── ocr_service.py     # 图 → 字 OCR
│   │   └── run.py
│   └── tests/
│       ├── __init__.py
│       ├── test_render.py
│       ├── test_api.py
│       ├── smoke_test.py      # 端到端测试
│       ├── direct_test.py
│       ├── auto_paste_test.py
│       └── debug_render.py
│
├── extension/                 # Chrome/Edge MV3 扩展
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   ├── content.css
│   ├── popup.html
│   ├── popup.js
│   └── store/
│       └── STORE_LISTING.md   # Chrome Web Store 上架材料
│
├── electron/                  # Electron 桌面端
│   ├── package.json
│   ├── main.js                # 主进程
│   ├── preload.js
│   └── renderer/
│       ├── index.html
│       └── renderer.js
│
├── web/                       # Web Demo (Vue 3 + Vite)
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── style.css
│   │   ├── components/
│   │   └── assets/
│   └── README.md
│
├── docs/                      # 完整用户文档
│   ├── MANUAL.md              # 用户语法手册
│   ├── ARCHITECTURE.md        # 架构设计文档
│   ├── DEVELOPMENT.md         # 开发指南
│   ├── IMAGE_MODE.md          # 图片模式详细指南
│   └── DATA.md                # 数据与 License
│
└── .github/
    └── workflows/
        └── ci.yml             # GitHub Actions CI
```

## 🚀 下一步

### 用户侧（本地操作）

1. **安装 Git**（推荐 2.40+）：https://git-scm.com/download/win
2. **克隆或拉取本仓库**：
   ```bash
   cd e:\甲骨文输入法\oracle-bone-script-ime
   git init
   git remote add origin https://github.com/shikunpneg/Oracle-Bone-Script-IME.git
   git add .
   git commit -m "feat: initial release v0.1.0 - complete MVP"
   git push -u origin main --force
   ```
3. **（可选）下载 OCR 模型权重**：见 `weights/README.md`
4. **（可选）安装 RIME 输入法**：见 `docs/MANUAL.md`

### 项目侧（下一步开发）

- W2：FastAPI 服务已上线 → 在自己电脑用浏览器扩展测试微信/QQ 聊天框
- W3：RIME 桌面端实测（小狼毫/鼠须管）
- W4：同文输入法 Android 移植
- W5：OCR 模型 ONNX 转换 + 推理
- W6：Chrome Web Store 提交上架
- W7：Electron 桌面端打包（electron-builder）
- W8：v1.0.0 正式版发布

## 📝 关键命令速查

```bash
# 1. 安装 Python 依赖（清华源）
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fastapi uvicorn pillow fonttools brotli pydantic numpy httpx pytest pytest-asyncio python-multipart

# 2. 构建字体资产（PNG + WOFF2 + SVG sprite）
python scripts/build_glyph_assets.py

# 3. 启动后端服务
cd server && python -m uvicorn app.main:app --host 127.0.0.1 --port 19840

# 4. smoke test
cd server && python tests/smoke_test.py

# 5. 直接渲染测试
cd server && python tests/direct_test.py

# 6. 启动 Web Demo
cd web && npm install && npm run dev

# 7. 启动 Electron 桌面端
cd electron && npm install && npm start
```