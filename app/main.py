from fastapi import FastAPI
from threading import Thread
from app.monitor import start_monitoring

app = FastAPI()

@app.on_event("startup")
def start_monitor():
    Thread(target=start_monitoring, daemon=True).start()

@app.get("/")
def read_root():
    return {"status": "running"}

