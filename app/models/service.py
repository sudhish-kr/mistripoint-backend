from sqlalchemy import Column, Integer, String, Text, Numeric
from app.database import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, nullable=False)
    name = Column(String(255))
    description = Column(Text)
    price = Column(Numeric(10,2))