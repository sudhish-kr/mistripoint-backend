from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False)
    address_id = Column(Integer, nullable=False)
    booking_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(30), default="Pending")