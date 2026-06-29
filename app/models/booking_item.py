from sqlalchemy import Column, Integer, Numeric
from app.database import Base

class BookingItem(Base):
    __tablename__ = "booking_items"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, nullable=False)
    service_id = Column(Integer, nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Numeric(10,2))