import os, time, requests
BASE = os.environ.get("GROK_API_URL", "https://api.x.ai/v1")
KEY  = os.environ.get("GROK_API_KEY")

t0 = time.time()
try:
    r = requests.get(
        BASE.rstrip("/") + "/models",
        headers={"Authorization": f"Bearer {KEY}"},
        timeout=3.0,
    )
    print("OK", r.status_code, "in", round(time.time()-t0,2), "s")
    print(r.text[:180])
except Exception as e:
    print("REQUEST FAILED:", repr(e))
