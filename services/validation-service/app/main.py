import os

from fastapi import FastAPI

app = FastAPI(title="Validation Service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "validation-service",
            "version": os.getenv("APP_VERSION", "dev")}
