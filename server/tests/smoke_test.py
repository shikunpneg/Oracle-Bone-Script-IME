"""端到端 smoke 测试：curl-like Python 调用"""
import urllib.request
import json
import sys

BASE = "http://127.0.0.1:19840"


def call(method, path, data=None, headers=None):
    url = BASE + path
    if data is not None and isinstance(data, dict):
        data = json.dumps(data).encode("utf-8")
        headers = headers or {}
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read()
            # HTTP headers 大小写不敏感，统一转小写
            normalized = {k.lower(): v for k, v in r.headers.items()}
            return r.status, normalized, body
    except urllib.error.HTTPError as e:
        normalized = {k.lower(): v for k, v in e.headers.items()}
        return e.code, normalized, e.read()


def main():
    print("=== 1. GET / ===")
    s, h, b = call("GET", "/")
    print(f"  status={s}")
    print(f"  body={b.decode()}")
    assert s == 200

    print("\n=== 2. GET /health ===")
    s, h, b = call("GET", "/health")
    print(f"  status={s}, body={b.decode()}")
    assert s == 200
    data = json.loads(b)
    assert data["status"] == "ok"
    assert data["font_loaded"] is True

    print("\n=== 3. POST /oracle/render (auto_paste=False) ===")
    s, h, b = call("POST", "/oracle/render", {"text": "甲骨文", "auto_paste": False})
    print(f"  status={s}")
    print(f"  content-type={h.get('content-type')}")
    text_b64 = h.get("x-oracle-text-b64")
    import base64 as _b64
    if text_b64:
        print(f"  x-oracle-text-b64={text_b64} => {_b64.b64decode(text_b64).decode('utf-8')}")
    print(f"  x-oracle-pasted={h.get('x-oracle-pasted')}")
    print(f"  png bytes={len(b)}")
    assert s == 200
    assert h.get("content-type") == "image/png"
    assert len(b) > 1000

    # 保存
    out = r"e:\甲骨文输入法\oracle-bone-script-ime\server\test_output_api.png"
    with open(out, "wb") as f:
        f.write(b)
    print(f"  saved: {out}")

    print("\n=== 4. POST /oracle/render (empty text → 400) ===")
    s, h, b = call("POST", "/oracle/render", {"text": ""})
    print(f"  status={s}, body={b.decode()[:100]}")
    assert s == 400

    print("\n=== 5. POST /oracle/ocr (无权重 → 503) ===")
    boundary = b"----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        b"--" + boundary + b"\r\n"
        b'Content-Disposition: form-data; name="image"; filename="test.png"\r\n'
        b"Content-Type: image/png\r\n\r\n"
        b"\x89PNG\r\n\x1a\n" + b"\x00" * 100 + b"\r\n"
        b"--" + boundary + b"--\r\n"
    )
    req = urllib.request.Request(
        BASE + "/oracle/ocr",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary.decode()}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"  unexpected status={r.status}")
    except urllib.error.HTTPError as e:
        print(f"  status={e.code}, body={e.read().decode()[:200]}")
        assert e.code == 503

    print("\n=== ✅ 所有 smoke 测试通过 ===")


if __name__ == "__main__":
    main()