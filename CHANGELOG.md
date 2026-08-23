# 更新日志

> Oracle-Bone-Script-IME 的版本演进记录

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 计划中
- 接入 PD-OBS 多模态释读
- 接入 AlphaOracle 专家工作流
- 移动端 OCR：拍照 → 识别 → 输入
- WebSocket 实时同步多设备

## [0.1.0] - 2026-08-20

### 新增
- ✨ **基础架构**：RIME 输入法方案 + FastAPI 后端服务
- 🐘 **图片输出模式**：打汉字 → 直接发甲骨文图片（解决"豆腐块"问题）
- 🔤 **文字输出模式**：候选面板用方正甲骨文字体渲染
- 📷 **OCR 反向识别**：基于 HUST-OBC ResNet50 ONNX 模型（Top-1 94.6%）
- 🖥️ **多端支持**：
  - Windows / macOS / Linux 桌面端（RIME）
  - Android（同文输入法）
  - iOS（仓输入法）
  - Chrome / Edge 扩展（Manifest V3）
  - Electron 桌面 App
- 🌐 **Web Demo**：Vue 3 + Vite 在线体验
- 🔧 **构建工具**：字体子集化（pyftsubset）+ 预渲染 1431 张 PNG + SVG sprite
- 📖 **完整文档**：用户手册、架构文档、开发指南、图片模式指南、数据说明

### 技术细节
- 字体：方正甲骨文 FZJIAGW.ttf（1431 字，免费商用）
- 数据：HUST-OBC + EVOBC + Wikimedia 古汉字 SVG（双轨数据源）
- 后端：Python 3.9+ / FastAPI / Pillow / onnxruntime
- 输入法：RIME / librime-lua
- 客户端：Chrome MV3 / Electron / Vue 3

### 已知限制
- 仅覆盖方正甲骨文 1431 字（约 70% 常用字）
- iOS 仓输入法无法直接调用外部 Python 服务
- 模拟 Ctrl+V 在某些 IME 焦点切换时可能失败

## [未来版本]

### v0.2.0（计划）
- 接入白舟甲骨文（CC0）作为备选字体
- 添加常用词组预渲染缓存
- 支持横排/竖排切换

### v0.3.0（计划）
- 接入多模态释读（PD-OBS）
- 跨设备用户词典同步
- iOS Shortcuts 中转方案

### v1.0.0（计划）
- 接入 AlphaOracle 完整工作流
- 完整覆盖 1588+ 已释字
- 移动端原生 App（Android + iOS）