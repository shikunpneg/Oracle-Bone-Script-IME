# 模型权重说明

本目录用于存放 AI 模型权重（不进 git，通过 `download_weights.sh` 下载）。

## 必需模型（用于 OCR 反向识别）

### 1. `obc_vit_hust_obs.onnx`

- **来源**：HUST-OBC 训练好的 ResNet50 / OBC-ViT 模型（PyTorch）
- **用途**：单字甲骨文识别（1588 类已破译字符）
- **大小**：~100 MB（ONNX 量化后 ~25 MB）
- **下载脚本**：`bash scripts/download_weights.sh`
- **手动下载**：
  - HuggingFace: https://huggingface.co/yuliang-liu/HUST-OBS-weights
  - GitHub: https://github.com/zhz5687/Transformer-OBS-Recognition

```bash
# 下载后放此处：
weights/obc_vit_hust_obs.onnx
```

## 转换 ONNX 步骤

如果只有 PyTorch checkpoint（`.pth`），需先转 ONNX：

```python
import torch
import onnx
from obc_vit import OBCViT

# 加载 PyTorch 权重
model = OBCViT(num_classes=1588)
model.load_state_dict(torch.load("weights/obc_vit_hust_obs.pth")["model"])
model.eval()

# 导出 ONNX
dummy = torch.randn(1, 1, 64, 64)  # BCHW
torch.onnx.export(
    model, dummy, "weights/obc_vit_hust_obs.onnx",
    input_names=["input"], output_names=["logits"],
    dynamic_axes={"input": {0: "batch"}, "logits": {0: "batch"}},
    opset_version=13,
)
```

## ID → 汉字映射表

下载模型后需要 `id_to_chinese.json`（1588 类已破译字符），可从以下来源获得：

- HUST-OBC 仓库的 `id_to_chinese.json`：https://github.com/Pengjie-W/HUST-OBC
- 放置路径：`data/id_to_chinese.json`

## 可选模型（高级功能）

### PD-OBS（多模态释读）

- **来源**：复旦 PKXX1943
- **用途**：部首+象形协同释读，Top-10 88.3% 准确率
- **大小**：~15 GB
- **下载**：https://github.com/PKXX1943/PD-OBS

### AlphaOracle（专家工作流启发）

- **来源**：HUST 白翔组
- **用途**：模拟甲骨学家分析工作流
- **下载**：https://github.com/Yuliang-Liu/AlphaOracle

## License

| 模型 | License |
|------|---------|
| HUST-OBC 权重 | CC BY-NC-ND 4.0（学术研究使用） |
| OBC-ViT 代码 | MIT |
| PD-OBS | 论文申请 |
| AlphaOracle | Apache-2.0 |