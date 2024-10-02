from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from app.core.database import Base
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship

class OrderType(PyEnum):
    BUY = "BUY"
    SELL = "SELL"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    stock_name = Column(String, index=True)
    shares = Column(Integer, nullable=False)
    price_per_share = Column(Float, nullable=False)
    order_type = Column(Enum(OrderType), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # utcnow доступен

    user = relationship("User")