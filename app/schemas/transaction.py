from pydantic import BaseModel
import datetime

class TransactionBase(BaseModel):
    stock_name: str
    shares: int
    price_per_share: float

class TransactionOut(TransactionBase):
    buyer_id: int
    seller_id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True