"""调试 headers"""
import urllib.request, json
req = urllib.request.Request(
    "http://127.0.0.1:19840/oracle/render",
    data=json.dumps({"text": "中", "auto_paste": False}).encode(),
    headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        print(f"status={r.status}")
        print("headers (raw):")
        for k, v in r.headers.items():
            print(f"  {k}: {v}")
except Exception as e:
    print(f"ERR: {e}")