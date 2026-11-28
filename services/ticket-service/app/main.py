import io
import os
import uuid
from contextlib import asynccontextmanager

import qrcode
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .db import get_db, init_db
from .models import Ticket


@asynccontextmanager
async def lifespan(app):
    init_db()
    yield


app = FastAPI(title="Ticket Service", lifespan=lifespan)


class TicketIn(BaseModel):
    passenger_name: str = Field(min_length=1, max_length=100)
    origin: str = Field(min_length=1, max_length=100)
    destination: str = Field(min_length=1, max_length=100)


def to_dict(t: Ticket) -> dict:
    return {"code": t.code, "passenger_name": t.passenger_name, "origin": t.origin,
            "destination": t.destination, "status": t.status}


@app.get("/health")
def health():
    return {"status": "ok", "service": "ticket-service",
            "version": os.getenv("APP_VERSION", "dev")}


@app.post("/tickets", status_code=201)
def create_ticket(data: TicketIn, db: Session = Depends(get_db)):
    ticket = Ticket(code=str(uuid.uuid4()), **data.model_dump())
    db.add(ticket)
    db.commit()
    return to_dict(ticket)


@app.get("/tickets/{code}")
def get_ticket(code: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.code == code).first()
    if ticket is None:
        raise HTTPException(404, "ticket not found")
    return to_dict(ticket)


@app.get("/tickets/{code}/qr")
def ticket_qr(code: str, db: Session = Depends(get_db)):
    get_ticket(code, db)                      # 404 if the ticket does not exist
    png = io.BytesIO()
    qrcode.make(code).save(png)
    return Response(png.getvalue(), media_type="image/png")


@app.post("/tickets/{code}/use")
def use_ticket(code: str, db: Session = Depends(get_db)):
    ticket = get_ticket(code, db)             # 404 if the ticket does not exist
    if ticket["status"] == "USED":
        raise HTTPException(409, "ALREADY_USED")
    db.query(Ticket).filter(Ticket.code == code).update({"status": "USED"})
    db.commit()
    return {"result": "VALID"}
