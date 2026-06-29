from sqlalchemy import Column, Integer
from app.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer)
    service_id = Column(Integer)
    quantity = Column(Integer, default=1)