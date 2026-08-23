# 甲骨文输入法 · 用户语法手册

> 让任何人在 QQ / 微信 / 任意输入框打汉字，直接输出甲骨文形态。

---

## 目录

- [简介](#简介)
- [快速上手](#快速上手)
- [输入方式](#输入方式)
  - [图片输出模式（推荐）](#图片输出模式推荐)
  - [文字输出模式](#文字输出模式)
  - [OCR 反向识别](#ocr-反向识别)
- [平台部署](#平台部署)
  - [Windows / macOS / Linux 桌面端](#windows--macos--linux-桌面端)
  - [Android](#android)
  - [iOS](#ios)
  - [Chrome / Edge 浏览器](#chrome--edge-浏览器)
- [快捷键一览](#快捷键一览)
- [故障排查](#故障排查)
- [进阶：自定义字体与字符集](#进阶自定义字体与字符集)

---

## 简介

**甲骨文输入法** 是基于 RIME（中州韵）引擎的开源输入法扩展方案。核心目标：

> **像搜狗输入法一样打汉字，但输出的是甲骨文形态。**

支持两大模式：

| 模式 | 触发 | 上屏内容 | 对方是否需装字体 |
|------|------|----------|------------------|
| **图片输出**（推荐） | `Ctrl+Shift+I` | 甲骨文 PNG 图片 | ❌ 不需要 |
| **文字输出** | `Ctrl+Shift+O` | 甲骨文字符（需装字体） | ⚠️ 需要 |

---

## 快速上手

### 5 分钟体验（最简方案）

无需安装任何输入法，**5 分钟**就能体验甲骨文：

1. 打开 Web Demo：https://shikunpneg.github.io/Oracle-Bone-Script-IME/
2. 输入"我爱甲骨文"
3. 点击「生成甲骨文图片」
4. 点击「复制图片到剪贴板」
5. 粘贴到任意微信/QQ 聊天窗口

> 对方不需要装任何字体，直接看到图片。

### 完整部署（30 分钟）

1. **下载字体**
   ```bash
   bash scripts/download_fonts.sh
   # 或 Windows:
   powershell -ExecutionPolicy Bypass -File scripts\download_fonts.ps1
   ```
2. **启动渲染服务**
   ```bash
   cd server
   pip install -r requirements.txt
   python -m app.main
   # 监听 http://127.0.0.1:19840
   ```
3. **安装 RIME 输入法**
   - Windows：[小狼毫](https://rime.im/download/)
   - macOS：[鼠须管](https://rime.im/download/)
   - Linux：`sudo apt install ibus-rime` 或 `fcitx5-rime`
4. **导入甲骨文方案**
   ```bash
   cp -r rime/* ~/.config/rime/   # Linux/macOS
   # Windows: 复制到 %APPDATA%\Rime\
   ```
5. **在 `default.custom.yaml` 注册**
   ```yaml
   patch:
     schema_list:
       - schema: jiaguwen
   ```
6. **重启 RIME**
   - 小狼毫：托盘菜单 → 重新部署
   - 鼠须管：菜单栏 → 部署

---

## 输入方式

### 图片输出模式（推荐）

#### 工作原理

```
你输入"我爱甲骨文"
   ↓
RIME 引擎处理（拼音 → 候选）
   ↓
候选词带"🐘甲骨文"标签
   ↓
你按空格上屏
   ↓
oracle_image_trigger.lua 调用本地渲染服务 (127.0.0.1:19840)
   ↓
渲染服务把"我爱甲骨文"渲染成 PNG
   ↓
PNG 写入剪贴板 + 自动模拟 Ctrl+V
   ↓
聊天框出现一张甲骨文图片 ✅
```

#### 启用方法

1. 启动本地渲染服务（见上文）
2. 在 RIME 输入状态下按 `Ctrl+Shift+I`（切换"图片模式"）
3. 状态栏出现"图片模式"提示
4. 正常打字，候选词上屏时自动变成图片

#### 关闭方法

再次按 `Ctrl+Shift+I` 切回"文字模式"。

### 文字输出模式

#### 工作原理

```
你输入"我爱甲骨文"
   ↓
候选词用 FZJIAGW.ttf 字体渲染
   ↓
候选面板显示为甲骨文形态
   ↓
你按数字键选词 / 空格上屏
   ↓
聊天框里直接出现"我爱甲骨文"汉字
   （对方必须也装 FZJIAGW.ttf 才能看到字形，否则是豆腐块）
```

#### 启用方法

1. 安装方正甲骨文字体：https://www.foundertype.com/
2. RIME 输入状态下按 `Ctrl+Shift+O`（或确保 `oracle_image_mode` 关闭）
3. 候选面板自动使用甲骨文字体

#### 适用场景

- 自己学习/打印：Word/PPT 切换字体
- 与同样装了字体的朋友交流
- 论坛签名、博客装饰

### OCR 反向识别

#### 工作原理

```
你看到一张甲骨文图片（截图 / 剪贴板）
   ↓
按 Ctrl+Shift+G 触发 OCR
   ↓
ONNX 模型识别（基于 HUST-OBC ResNet50，Top-1 准确率 94.6%）
   ↓
返回 Top-5 现代汉字候选
   ↓
置信度最高的字写入剪贴板
```

#### 启用方法

1. 下载 OCR 模型（首次需 ~100MB）
   ```bash
   bash scripts/download_weights.sh
   ```
2. 按 `Ctrl+Shift+G`
3. 剪贴板中的甲骨文图片自动识别为汉字

#### 适用场景

- 学习时遇到不认识的甲骨文
- 古籍数字化录入

---

## 平台部署

### Windows / macOS / Linux 桌面端

| 步骤 | Windows | macOS | Linux |
|------|---------|-------|-------|
| 1. 装 RIME | 小狼毫 Weasel | 鼠须管 Squirrel | ibus-rime / fcitx5-rime |
| 2. 用户目录 | `%APPDATA%\Rime\` | `~/Library/Rime/` | `~/.config/rime/` |
| 3. 复制方案 | `cp rime/* %APPDATA%\Rime\` | `cp rime/* ~/Library/Rime/` | `cp rime/* ~/.config/rime/` |
| 4. 注册 | 编辑 `default.custom.yaml` 加入 `- schema: jiaguwen` | 同左 | 同左 |
| 5. 部署 | 托盘菜单 → 重新部署 | 菜单栏 → 部署 | `ibus restart` |

### Android

1. 安装 [同文输入法（Trime）](https://github.com/osfans/trime)
2. 把 `rime/` 目录推送到手机：
   ```bash
   adb push rime/ /sdcard/rime/
   ```
3. 在同文输入法设置中导入该目录
4. 设置 → 键盘 → 启用「同文输入法」
5. 启动渲染服务（推荐在 Android 上用 [Termux](https://termux.com/) 运行 Python 脚本）

### iOS

1. 安装 [仓输入法 Hamster](https://github.com/imfuxiao/Hamster)
2. 通过 iCloud / WebDAV 把 `rime/` 配置同步到 Hamster 的 `Rime/` 目录
3. 设置 → 通用 → 键盘 → 键盘 → 添加新键盘 → 仓输入法
4. **重要**：iOS 需要企业签名或开发者证书才能完整运行 RIME

### Chrome / Edge 浏览器

1. 打开 `chrome://extensions/`
2. 开启"开发者模式"
3. 点击"加载已解压的扩展程序"，选择 `extension/` 目录
4. 启动本地渲染服务
5. 任意网页输入框按 `Ctrl+Shift+I` 触发图片输出

---

## 快捷键一览

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+`` | 切换 RIME 方案 |
| `Ctrl+Shift+I` | 切换"图片输出模式"（桌面/扩展） |
| `Ctrl+Shift+G` | 触发 OCR 反向识别（桌面/扩展） |
| `Ctrl+Shift+R` | 切换"OCR 反向模式"（RIME 内部） |
| `Ctrl+V` | 粘贴图片（自动触发） |

---

## 故障排查

### Q1：打字后没反应

**症状**：按 `Ctrl+Shift+I` 后，输入汉字无变化。

**排查**：
1. 确认本地渲染服务已启动：访问 `http://127.0.0.1:19840/health`
2. 确认服务返回 `font_loaded: true`，否则说明 FZJIAGW.ttf 没放对位置
3. 查看服务日志（PowerShell/终端输出）

### Q2：图片发出去了但对方看到豆腐块

**症状**：自己看到图片正常，但朋友说显示"口口口"。

**排查**：
1. 确认你发出的是**图片**而非文字（图片会显示成图片预览）
2. 如果发出的是文字流，说明图片模式没启用 → 按 `Ctrl+Shift+I` 切换
3. 让对方切换到支持自定义字体的输入法或浏览器查看

### Q3：候选面板不显示甲骨文

**症状**：候选词仍是普通宋体。

**排查**：
1. 确认 FZJIAGW.ttf 已安装到系统字体目录
2. 确认 RIME 方案已切换到「甲骨文输入」
3. 重启 RIME 引擎
4. 在 `jiaguwen.schema.yaml` 中检查 `style.font_face: FZJIAGW`

### Q4：OCR 识别率低

**症状**：复制甲骨文图片后识别为错误汉字。

**排查**：
1. 确保图片清晰（避免模糊、噪点）
2. 单字识别效果 > 多字连写
3. 调整图片大小至 64×64 附近
4. 若识别整张拓片，需先用检测算法分割单字

---

## 进阶：自定义字体与字符集

### 替换为其他字体

如需使用白舟甲骨、汉仪陈体甲骨等其他字体：

1. 下载字体到 `assets/fonts/`
2. 修改 `rime/jiaguwen.schema.yaml`：
   ```yaml
   style:
     font_face: HakusyuKoukotsu   # 或 HYChenTiJiaGuWen
   ```
3. 修改 `server/app/main.py`：
   ```python
   FONT_PATH = ROOT / "assets" / "fonts" / "HakusyuKoukotsu.ttf"
   ```
4. 重启服务

### 扩展字符集

目前覆盖方正甲骨文的 1431 个字。如需扩展到 1588+ 已释字：

1. 下载 [HUST-OBC 数据集](https://github.com/Pengjie-W/HUST-OBC)
2. 用 PD-OBS 模型预测其他字的现代汉字映射
3. 把新字符加入到 `data/id_to_chinese.json`
4. 重新跑 `python scripts/build_glyph_assets.py`

---

## 反馈与贡献

- 🐛 Bug 报告：https://github.com/shikunpneg/Oracle-Bone-Script-IME/issues
- 💡 功能建议：https://github.com/shikunpneg/Oracle-Bone-Script-IME/discussions
- 📖 贡献指南：https://github.com/shikunpneg/Oracle-Bone-Script-IME/blob/main/CONTRIBUTING.md