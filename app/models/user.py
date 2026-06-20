from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(20), default="customer")

    first_name = Column(String(100))
    last_name = Column(String(100))