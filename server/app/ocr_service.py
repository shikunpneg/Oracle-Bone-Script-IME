"""
ocr_service.py — OCR 反向识别服务（图片 → 汉字）

加载 ONNX 模型（HUST-OBS 训练好的 ResNet50 / OBC-ViT）
对单字图片进行分类，返回 Top-K 候选汉字
"""

import io
import json
import logging
from pathlib import Path

import numpy as np
from PIL import Image

log = logging.getLogger(__name__)


class OCRService:
    """甲骨文 OCR 服务"""

    def __init__(self, weight_path: Path, id_to_chinese_path: Path | None = None):
        self.weight_path = Path(weight_path)
        self.id_to_chinese_path = (
            Path(id_to_chinese_path) if id_to_chinese_path else None
        )
        self.session = None
        self.id_to_chinese = {}
        self._load_model()
        self._load_mapping()

    def _load_model(self):
        """加载 ONNX Runtime 模型"""
        if not self.weight_path.exists():
            log.warning(
                f"OCR 模型未找到: {self.weight_path}\n"
                "OCR 反向功能将不可用。详见 weights/README.md"
            )
            return

        try:
            import onnxruntime as ort
            self.session = ort.InferenceSession(str(self.weight_path))
            log.info(f"✓ ONNX 模型已加载: {self.weight_path}")
            log.info(f"  输入: {[i.name for i in self.session.get_inputs()]}")
            log.info(f"  输出: {[o.name for o in self.session.get_outputs()]}")
        except Exception as e:
            log.error(f"模型加载失败: {e}")

    def _load_mapping(self):
        """加载 ID → 现代汉字映射"""
        if self.id_to_chinese_path and self.id_to_chinese_path.exists():
            try:
                with self.id_to_chinese_path.open(encoding="utf-8") as f:
                    data = json.load(f)
                # 转为 {int_id: chinese_char}
                if isinstance(data, dict):
                    if "id_to_chinese" in data:
                        self.id_to_chinese = {
                            int(k): v for k, v in data["id_to_chinese"].items()
                        }
                    else:
                        self.id_to_chinese = {int(k): v for k, v in data.items()}
                log.info(f"✓ 已加载 {len(self.id_to_chinese)} 个 ID→汉字映射")
            except Exception as e:
                log.warning(f"映射加载失败: {e}")

    def recognize(self, image_bytes: bytes, top_k: int = 5) -> list[dict]:
        """
        识别单字甲骨文图片

        Args:
            image_bytes: 图片字节流
            top_k: 返回 Top-K 候选

        Returns:
            [{"obs_id": int, "chinese": "中", "conf": 0.95}, ...]
        """
        if self.session is None:
            raise RuntimeError("OCR 模型未加载")

        # 预处理：灰度化 → 64×64 → 归一化
        img = Image.open(io.BytesIO(image_bytes)).convert("L").resize((64, 64))
        arr = np.array(img, dtype=np.float32) / 255.0
        # 添加 batch 和 channel 维度: (1, 1, 64, 64)
        arr = arr.reshape(1, 1, 64, 64)

        # 推理
        input_name = self.session.get_inputs()[0].name
        outputs = self.session.run(None, {input_name: arr})
        logits = outputs[0][0]

        # softmax
        exp = np.exp(logits - np.max(logits))
        probs = exp / exp.sum()

        # Top-K
        top_indices = np.argsort(probs)[::-1][:top_k]
        candidates = []
        for idx in top_indices:
            idx_int = int(idx)
            candidates.append({
                "obs_id": idx_int,
                "chinese": self.id_to_chinese.get(idx_int, f"<U+{idx_int:04X}>"),
                "conf": float(probs[idx]),
            })
        return candidates