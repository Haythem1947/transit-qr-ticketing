from sqlalchemy import Column, DateTime, Integer, String, func

from .db import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    code = Column(String(36), unique=True, nullable=False)
    passenger_name = Column(String(100), nullable=False)
    origin = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default="ISSUED")
    created_at = Column(DateTime, server_default=func.now())
