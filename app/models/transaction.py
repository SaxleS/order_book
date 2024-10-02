from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from app.core.database import Base
import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    stock_name = Column(String, index=True)
    shares = Column(Integer)
    price_per_share = Column(Float)
    buyer_id = Column(Integer, ForeignKey('users.id'))
    seller_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)