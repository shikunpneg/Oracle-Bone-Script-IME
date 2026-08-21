# RIME 甲骨文输入方案

> RIME 中州韵跨平台开源输入法的甲骨文扩展方案

## 支持平台

| 平台 | RIME 前端 | 仓库 |
|------|-----------|------|
| Windows | 小狼毫 Weasel | https://github.com/rime/weasel |
| macOS | 鼠须管 Squirrel | https://github.com/rime/squirrel |
| Linux | ibus-rime / fcitx5-rime | https://github.com/rime/ibus-rime |
| Android | 同文输入法 Trime | https://github.com/osfans/trime |
| iOS | 仓输入法 Hamster | https://github.com/imfuxiao/Hamster |

## 安装步骤（以小狼毫为例）

1. **下载方案文件**
   ```bash
   # 克隆本仓库到本地
   git clone https://github.com/shikunpneg/Oracle-Bone-Script-IME.git
   ```

2. **复制到 RIME 用户目录**
   - Windows：`C:\Users\<你>\AppData\Roaming\Rime\`
   - macOS：`~/Library/Rime/`
   - Linux：`~/.config/rime/`

   ```bash
   # Linux/macOS
   cp -r Oracle-Bone-Script-IME/rime/* ~/.config/rime/
   ```

3. **注册方案**

   在 `default.custom.yaml` 中追加：
   ```yaml
   patch:
     schema_list:
       - schema: jiaguwen
   ```

4. **安装字体（文字模式）**

   下载 [方正甲骨文 FZJIAGW.ttf](https://www.foundertype.com/) 后安装到系统。

5. **启动渲染服务（图片模式）**

   ```bash
   cd Oracle-Bone-Script-IME/server
   pip install -r requirements.txt
   python app/main.py
   # 监听 127.0.0.1:19840
   ```

6. **部署完成**

   - 重启 RIME（小狼毫托盘菜单 → 重新部署）
   - 按 `Ctrl+`` 切换到「甲骨文输入」方案
   - `Ctrl+Shift+I` 切换"图片输出模式"

## 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+Shift+I` | 切换「文字 / 图片」输出模式 |
| `Ctrl+Shift+R` | 切换「OCR 反向模式」 |
| `Ctrl+Shift+G` | 触发 OCR 识别（截图/剪贴板） |
| `Ctrl+\`` | 切换 RIME 方案 |

## 目录结构

```
rime/
├── jiaguwen.schema.yaml      # 方案定义
├── jiaguwen.dict.yaml        # 码表（示例）
├── lua/
│   ├── oracle_translator.lua # 候选词追加"🐘甲骨文"标签
│   ├── oracle_filter.lua     # 候选排序/过滤
│   └── oracle_image_trigger.lua  # commit 时触发图片生成
└── README.md
```

## 工作流程

```
用户在任意输入框打字
   ↓
RIME 引擎处理（拼音 → 候选）
   ↓
oracle_filter 排序（有甲骨文字形的优先）
   ↓
oracle_translator 给候选加 🐘 标签
   ↓
用户选词 → commit 文字
   ↓
若开启"图片模式" → oracle_image_trigger 调用本地渲染服务
   ↓
渲染服务生成 PNG → 写剪贴板 → 模拟 Ctrl+V
   ↓
聊天框出现一张甲骨文图片
```

## 已知限制

- 仅覆盖方正甲骨文字体收录的 1431 个汉字（占常用字约 70%）
- 图片模式需要本地渲染服务常驻
- 部分生僻字可能在 FZJIAGW 中缺失（会显示豆腐块），可用「文字模式」降级
- iOS 仓输入法无法直接调用外部 Python 服务，需用 iOS Shortcuts 中转

## 调试

RIME 调试日志位于：
- Windows：`%TEMP%\rime.weasel.*.INFO`
- macOS：`/tmp/rime.squirrel.*.INFO`

启用 Lua 调试：在 `jiaguwen.schema.yaml` 中加入：
```yaml
__include: lua_debug: true
```