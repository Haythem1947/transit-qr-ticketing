import os

from fastapi import FastAPI

app = FastAPI(title="Ticket Service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "ticket-service",
            "version": os.getenv("APP_VERSION", "dev")}
