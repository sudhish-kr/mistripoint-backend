from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False)
    full_name = Column(String(100))
    phone = Column(String(10))
    address = Column(Text)
    city = Column(String(100))
    pincode = Column(String(10))