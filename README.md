<div align="center">

# 甲骨文输入法 · Oracle-Bone-Script-IME

**「打汉字出甲骨文」开源输入法 · 像搜狗一样自然**

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/shikunpneg/Oracle-Bone-Script-IME)](https://github.com/shikunpneg/Oracle-Bone-Script-IME/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/shikunpneg/Oracle-Bone-Script-IME)](https://github.com/shikunpneg/Oracle-Bone-Script-IME/issues)

[English](README.en.md) · **简体中文** · [Demo](https://shikunpneg.github.io/Oracle-Bone-Script-IME/)

</div>

---

## 简介

**甲骨文输入法** 是基于 RIME（中州韵）引擎的开源输入法方案，**让用户像用搜狗输入法一样在 QQ / 微信 / 任意输入框打汉字，直接输出甲骨文形态**。

两大核心模式：

| 模式 | 触发 | 效果 |
|------|------|------|
| **文字模式**（默认） | `Ctrl+Shift+O` 切换 | 候选面板用甲骨文字体渲染，对方需装字体 |
| **图片模式**（推荐） | `Ctrl+Shift+I` 切换 | 上屏后**直接变甲骨文图片**，**对方零门槛看到** |

支持 Win / macOS / Linux / Android / iOS 五端共享同一套 RIME 配置。

## ✨ 核心特性

- 🐘 **1431 个已释甲骨文字**（方正甲骨文 FZJIAGW.ttf + Wikimedia 古汉字 SVG 双轨数据源）
- 🖼️ **图片输出模式**——彻底解决"对方没装字体 = 豆腐块"的难题
- 📱 **跨 5 端覆盖**——基于 librime，同一套 YAML 推到桌面 / Android / iOS
- 🔤 **OCR 反向**——看到甲骨文图片自动识别为现代汉字
- 🚀 **完全开源**——Apache-2.0 License，可商用
- 🎨 **可视化 Demo**——内置 Web Demo，无需安装即可在线预览

## 🎬 演示

### 实时渲染效果

| 单字演示 | 单字演示 | 单字演示 | 单字演示 | 单字演示 |
|----------|----------|----------|----------|----------|
| ![甲](demo_images/甲.png) | ![乙](demo_images/乙.png) | ![丙](demo_images/丙.png) | ![丁](demo_images/丁.png) | ![我](demo_images/我.png) |
| 甲 | 乙 | 丙 | 丁 | 我 |
| ![爱](demo_images/爱.png) | ![中](demo_images/中.png) | ![华](demo_images/华.png) | ![骨](demo_images/骨.png) | ![文](demo_images/文.png) |
| 爱 | 中 | 华 | 骨 | 文 |

### 句子级演示

![我爱中华甲骨文](demo_images/sentence.png)

> **在线体验**：https://shikunpneg.github.io/Oracle-Bone-Script-IME/

---

### 图片输出模式演示（推荐）

> 💡 **核心优势**：对方**完全不需要安装字体**，直接看到甲骨文图片

```text
输入：我爱甲骨文
      ↓
输出：[一张透明背景的甲骨文 PNG 图片自动上屏]
```

支持场景：
- ✅ QQ / 微信 / 钉钉 / 飞书 等所有输入框
- ✅ 网页表单、Markdown 编辑器、IDE
- ✅ 移动端同文 / 仓输入法

---

## 📦 安装

### 桌面端（Windows / macOS / Linux）

1. 安装 [RIME 输入法引擎](https://rime.im/)（小狼毫 / 鼠须管 / fcitx5-rime）
2. 下载本仓库的 `rime/` 目录到 RIME 用户配置目录
3. 在 `default.custom.yaml` 中注册甲骨文方案
4. 重启 RIME，按 `Ctrl+`` 切换到「甲骨文输入」

### 手机端（Android / iOS）

- **Android**：安装 [同文输入法](https://github.com/osfans/trime) + 导入 `rime/` 配置
- **iOS**：安装 [仓输入法 Hamster](https://github.com/imfuxiao/Hamster) + 导入 `rime/` 配置

### 浏览器扩展（Chrome / Edge）

1. 下载 `extension/` 目录
2. 打开 `chrome://extensions/`，开启开发者模式
3. 点击"加载已解压的扩展程序"，选择 `extension/` 目录
4. 任意网页按 `Ctrl+G` 触发图片输出

### 桌面 App（Electron）

```bash
cd electron
npm install
npm start
```

## 🚀 使用

### 图片输出模式（推荐）

1. 启动渲染服务：`python server/app/main.py`（默认监听 `127.0.0.1:19840`）
2. 在任意输入框切换到「甲骨文图片模式」：`Ctrl+Shift+I`
3. 打汉字："我爱甲骨文"
4. 上屏后**自动变成一张甲骨文图片**，对方无需装任何字体

### 文字模式

1. 安装 [方正甲骨文字体](https://www.foundertype.com/)（免费商用）
2. 切换到「甲骨文文字模式」：`Ctrl+Shift+O`
3. 打汉字 → 候选面板用甲骨文字体显示 → 直接上屏

### OCR 反向

```bash
curl -X POST http://127.0.0.1:19840/oracle/ocr \
  -F "image=@path/to/oracle_bone.png"
# 返回 Top-5 现代汉字候选
```

## 🧠 模型与数据

| 资源 | 来源 | License |
|------|------|---------|
| 甲骨文字体 FZJIAGW.ttf | [方正字库](https://www.foundertype.com/) | 免费商用（方正发布授权） |
| 古汉字 SVG | [Wikimedia Commons](https://commons.wikimedia.org/wiki/Commons:Ancient_Chinese_characters_project) | CC0 公共领域 |
| HUST-OBC 数据集 | [HUST 白翔组](https://github.com/Pengjie-W/HUST-OBC) | CC BY-NC-ND 4.0 |
| OBC-ViT 模型 | [Transformer-OBS-Recognition](https://github.com/zhz5687/Transformer-OBS-Recognition) | 学术研究 |
| PD-OBS 释读 | [复旦 PKXX1943](https://github.com/PKXX1943/PD-OBS) | 论文申请 |

详见 [docs/DATA.md](docs/DATA.md)。

## 🤝 贡献

欢迎贡献代码、数据集、字体改进！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📜 许可

- 代码：[Apache-2.0](LICENSE)
- 文档：[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)
- 字体：方正甲骨文依方正字库发布授权；Wikimedia 古汉字为 CC0
- 模型权重：依上游项目 License（HUST-OBC 等为 CC BY-NC-ND，仅学术研究使用）

## 🙏 致谢

- 华中科技大学白翔、刘禹良团队（HUST-OBC、EVOBC、OBSD、AlphaOracle）
- 复旦大学出土文献与古文字研究中心（PD-OBS）
- 安阳师范学院甲骨文信息处理教育部重点实验室（殷契文渊）
- 同文输入法（[osfans/trime](https://github.com/osfans/trime)）、仓输入法（[imfuxiao/Hamster](https://github.com/imfuxiao/Hamster)）
- RIME 项目组（[rime.im](https://rime.im/)）

## 引用

如果本项目对你的研究或产品有帮助，请引用：

```bibtex
@misc{oracle-bone-script-ime,
  title = {Oracle-Bone-Script-IME: An open-source input method for typing modern Chinese and outputting oracle bone script},
  year = {2026},
  url = {https://github.com/shikunpneg/Oracle-Bone-Script-IME}
}
```