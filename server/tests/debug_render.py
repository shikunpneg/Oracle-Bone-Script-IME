"""详细调试 render"""
import httpx
r = httpx.post(
    "http://127.0.0.1:19840/oracle/render",
    json={"text": "中", "auto_paste": False, "mode": "image"},
    timeout=10,
)
print(f"status={r.status_code}")
print(f"headers={dict(r.headers)}")
print(f"body={r.text[:500]}")