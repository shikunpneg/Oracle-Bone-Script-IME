"""FastAPI 客户端测试，捕获详细错误"""
import sys
sys.path.insert(0, '.')
import httpx
import json

print("Trying with auto_paste=False...")
try:
    r = httpx.post(
        "http://127.0.0.1:19840/oracle/render",
        json={"text": "中", "auto_paste": False},
        timeout=10,
    )
    print(f"  status={r.status_code}")
    print(f"  content-type={r.headers.get('content-type')}")
    print(f"  body bytes={len(r.content)}")
    if r.status_code == 200:
        with open("api_test_nopaste.png", "wb") as f:
            f.write(r.content)
        print("  saved: api_test_nopaste.png")
except Exception as e:
    print(f"  ERR: {e}")

print("\nTrying with auto_paste=True...")
try:
    r = httpx.post(
        "http://127.0.0.1:19840/oracle/render",
        json={"text": "中", "auto_paste": True},
        timeout=10,
    )
    print(f"  status={r.status_code}")
    print(f"  body={r.text[:200]}")
except Exception as e:
    print(f"  ERR: {e}")