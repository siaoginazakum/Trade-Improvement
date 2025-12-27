from fastapi import FastAPI, Request, HTTPException
import os, json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

@app.get("/")
def health():
    return {"ok": True}

@app.post("/webhook/tradingview")
async def tradingview_webhook(request: Request):
    raw = await request.body()
    text = raw.decode("utf-8", errors="replace").strip()

    payload = None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = {"message": text}

    if WEBHOOK_SECRET:
        if payload.get("secret") != WEBHOOK_SECRET:
            raise HTTPException(status_code=401, detail="bad secret")

    print("✅ TradingView alert received:", payload)

    return {"received": True}
