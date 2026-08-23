# 数据与资源说明

> 本项目使用的所有数据/模型/字体的来源与 License

## 字体资源

| 字体 | 来源 | License | 用途 |
|------|------|---------|------|
| **方正甲骨文 FZJIAGW.ttf** | [方正字库](https://www.foundertype.com/) | 发布使用免费 | 主字体（1431 字） |
| 白舟甲骨 HakusyuKoukotsu | [白舟書体](https://www.hakusyu.com/) | 教育免费（每年 9-11 月） | 备选字体 |
| 汉仪陈体甲骨文 | [汉仪字库](https://www.hanyi.com.cn/) | 个人 ¥10 / 商业授权 | 备选字体 |

**方正甲骨文字体使用注意**：
- 免费范围：发布使用（如文档、网页、印刷品）
- 程序嵌入、API 输出需另询商用授权
- 本项目作为输入法引擎使用，建议联系方正字库确认 License

## 数据集

| 数据集 | 来源 | License | 用途 |
|--------|------|---------|------|
| **HUST-OBC** | [HUST 白翔组](https://github.com/Pengjie-W/HUST-OBC) | **CC BY-NC-ND 4.0**（学术研究） | OCR 训练数据（1588 已释字 + 9411 未释字） |
| **EVOBC** | [HUST + 安阳师范 + 华南理工](https://github.com/RomanticGodVAN/character-Evolution-Dataset) | **CC BY-NC-SA 4.0** | 跨时期字形演化数据 |
| **PD-OBS** | [复旦 PKXX1943](https://github.com/PKXX1943/PD-OBS) | 论文申请 | 释读训练数据 |
| **Oracle-MNIST** | [北邮](https://github.com/wm-bupt/oracle-mnist) | Apache-2.0 | 教学基准 |
| **OBIMD** | HuggingFace KLOBIP | CC BY-NC-ND | 多模态数据集 |
| **Wikimedia 古汉字** | [Wikimedia Commons](https://commons.wikimedia.org/wiki/Commons:Ancient_Chinese_characters_project) | CC0 公共领域 | 单字 SVG 数据源 |
| **殷契文渊** | [安阳师范](http://jgw.aynu.edu.cn/) | 学术免费 | 数据检索与字形来源 |

**重要提示**：

- ⚠️ HUST-OBC 和 EVOBC 均为 **CC BY-NC-*** 协议，**禁止商业使用**
- ⚠️ 如需商用，请联系对应团队获取书面授权
- ✅ Wikimedia 古汉字 SVG 为 **CC0**，可自由商用
- ✅ Oracle-MNIST 为 **Apache-2.0**，可自由商用

## 模型权重

| 模型 | 来源 | License | 备注 |
|------|------|---------|------|
| OBC-ViT | [GitHub](https://github.com/zhz5687/Transformer-OBS-Recognition) | MIT | 封闭集 Top-1 97.2% |
| HUST-OBC ResNet50 | [GitHub](https://github.com/Pengjie-W/HUST-OBC) | CC BY-NC-ND 4.0 | 学术研究使用 |
| PD-OBS (Qwen2.5-VL) | [GitHub](https://github.com/PKXX1943/PD-OBS) | 论文申请 | 开放集 Top-10 88.3% |
| AlphaOracle | [GitHub](https://github.com/Yuliang-Liu/AlphaOracle) | Apache-2.0 | 专家工作流启发 |
| OBSD | [GitHub](https://github.com/guanhaisu/OBSD) | MIT（推测） | 扩散模型释读 |
| OracleFusion | [GitHub](https://github.com/lcs0215/OracleFusion) | 学术 | 结构性破译 ICCV 2025 |

## 上游项目致谢

### RIME 输入法引擎

- **项目**：[rime/home](https://github.com/rime/home)
- **License**：GPLv3
- **作用**：本项目的输入法核心引擎
- **前端**：
  - 小狼毫 Weasel：https://github.com/rime/weasel
  - 鼠须管 Squirrel：https://github.com/rime/squirrel
  - 同文输入法 Trime：https://github.com/osfans/trime
  - 仓输入法 Hamster：https://github.com/imfuxiao/Hamster

### 第三方 Python 库

- **FastAPI**：MIT
- **Pillow**：HPND
- **fontTools**：MIT
- **brotli**：MIT
- **onnxruntime**：MIT

### 第三方 Node 库

- **Electron**：MIT
- **Vue 3**：MIT
- **Vite**：MIT
- **vite-plugin-svg-icons**：MIT
- **robotjs**：MIT

## 字源映射表

本项目维护 `data/id_to_chinese.json`（HUST-OBC 风格的 ID↔汉字映射）。

**生成方式**：

```bash
# 从 HUST-OBC 仓库获取
wget https://raw.githubusercontent.com/Pengjie-W/HUST-OBC/main/id_to_chinese.json
# 放置到 data/id_to_chinese.json
```

**许可**：依 HUST-OBC 协议（CC BY-NC-ND）。

## 数据使用建议

### 学术研究

可直接使用全部数据集（包括 NC 协议）。

### 商业产品

- ✅ 使用 Wikimedia 古汉字 SVG（CC0）
- ✅ 使用 Oracle-MNIST（Apache-2.0）
- ✅ 使用 AlphaOracle（Apache-2.0）
- ⚠️ HUST-OBC / EVOBC / PD-OBS 需联系作者获取商用授权
- ⚠️ 方正甲骨文程序嵌入需联系方正字库确认 License

### 商标与品牌

- "Oracle-Bone-Script-IME" 仅为本仓库名
- 不与甲骨文相关商业品牌存在隶属关系

## 联系作者

如需对数据进行商业授权，请直接联系：

- HUST 白翔组（hustvision@163.com 推测）
- 安阳师范学院甲骨文信息处理教育部重点实验室
- 复旦出土文献与古文字研究中心

## 更新日志

- 2026-08-20：v0.1.0 首次发布（Fangzheng FZJIAGW + HUST-OBC 子集）