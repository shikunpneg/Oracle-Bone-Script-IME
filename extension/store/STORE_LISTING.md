# Chrome Web Store 上架材料

## 必填字段

### 名称
甲骨文输入法 - Oracle Bone IME

### 简短描述（132 字符以内）
在任意网页输入框打汉字，自动转换为甲骨文图片。支持图片输出模式和 OCR 反向识别。

### 详细描述（最多 16,000 字符）
```
🐘 甲骨文输入法 - 让古文字走进现代聊天

【核心功能】
• 图片输出模式：打汉字 → 直接发甲骨文图片，零字体门槛
• OCR 反向识别：复制甲骨文图片 → 自动识别为现代汉字
• 跨平台：Win/macOS/Linux/Android/iOS 共享 RIME 配置

【使用场景】
• 微信/QQ 网页版聊天时发送甲骨文图片
• 公众号编辑器/知乎评论/Notion 等任何 contenteditable 区域
• 学习甲骨文：复制图片自动识别对应汉字

【快捷键】
• Ctrl+Shift+I：触发图片输出
• Ctrl+Shift+G：触发 OCR 反向识别

【工作原理】
本扩展调用本地运行的渲染服务（http://127.0.0.1:19840）。
首次使用需启动本地服务（详见 GitHub README）。

【开源】
代码：Apache-2.0
GitHub: https://github.com/shikunpneg/Oracle-Bone-Script-IME

【致谢】
HUST 白翔组、复旦 PD-OBS、安阳师范学院殷契文渊
```

## 单用途说明（Single Purpose）

本扩展的唯一目的是：将用户在网页输入框中输入的汉字，转换为对应的甲骨文图片（PNG），并写入剪贴板供用户粘贴；或将剪贴板中的甲骨文图片反向识别为现代汉字。它**不修改网页内容、不收集用户数据、不访问任何网络资源**（除本地 127.0.0.1 渲染服务外）。

## 权限正当理由

| 权限 | 理由 |
|------|------|
| `activeTab` | 仅在用户点击扩展图标或触发快捷键时访问当前标签页 |
| `clipboardWrite` | 将渲染好的甲骨文 PNG 写入系统剪贴板，供用户粘贴 |
| `storage` | 保存用户的模式偏好（文字模式 vs 图片模式） |
| `scripting` | 通过 content script 在网页中触发粘贴事件 |
| `host_permissions: 127.0.0.1:19840` | 调用本地渲染服务（用户自主启动的服务） |

**不需要的权限**（已主动移除）：
- ~~`clipboardRead`~~：仅在 OCR 反向时使用，且通过用户手势触发
- ~~`<all_urls>`~~：仅在 content script 注入时使用，host_permissions 已限定

## 隐私政策（Privacy Policy）

详见 `https://shikunpneg.github.io/Oracle-Bone-Script-IME/privacy`

### 核心要点
- 本扩展**不上传任何用户数据**
- 所有数据处理在用户本地完成
- 不访问除 `127.0.0.1:19840` 之外的任何网络地址
- 不收集、不存储、不分析用户输入内容

## 图标与截图

### 图标
- `icons/icon-128.png`（128×128 PNG，含 16 像素透明 padding）

### 小型宣传图
- `store/promo-small-440x280.png`

### 截图（1-5 张，1280×800）
- `store/screenshot-1-home.png`：主界面
- `store/screenshot-2-input.png`：输入框使用演示
- `store/screenshot-3-output.png`：聊天框效果

### Marquee 宣传图（可选）
- `store/marquee-1400x560.png`