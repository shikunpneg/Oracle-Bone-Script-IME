# Oracle-Bone-Script-IME Server

甲骨文输入法后端服务 · Python FastAPI

## 功能

| 端点 | 方法 | 作用 |
|------|------|------|
| `/oracle/render` | POST | 文字 → PNG（自动粘贴） |
| `/oracle/ocr` | POST | PNG → 汉字 Top-K |
| `/health` | GET | 健康检查 |

## 安装

```bash
cd server
pip install -r requirements.txt
```

## 启动

```bash
python -m app.main
# 或
python app/main.py
# 监听 http://127.0.0.1:19840
```

## API 调用示例

### 字 → 图

```bash
curl -X POST http://127.0.0.1:19840/oracle/render \
  -H "Content-Type: application/json" \
  -d '{"text": "中", "auto_paste": false}' \
  --output oracle.png
```

返回 PNG 文件。同时设置 `auto_paste: true` 时，会自动写入剪贴板并模拟 Ctrl+V。

### 图 → 字

```bash
curl -X POST http://127.0.0.1:19840/oracle/ocr \
  -F "image=@oracle_glyph.png"
```

返回 JSON：

```json
{
  "candidates": [
    { "obs_id": 234, "chinese": "中", "conf": 0.95 },
    { "obs_id": 102, "chinese": "仲", "conf": 0.03 },
    ...
  ]
}
```

## 跨平台依赖

| 平台 | 额外依赖 |
|------|----------|
| Windows | PowerShell（系统自带） |
| macOS | osascript（系统自带） |
| Linux | `sudo apt install xclip xdotool` |

## 模型权重

OCR 反向需要 ONNX 权重，详见 [`../weights/README.md`](../weights/README.md)。
未下载权重时 `/oracle/ocr` 端点返回 503。