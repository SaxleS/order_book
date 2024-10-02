from pydantic import BaseModel
from enum import Enum
from typing import Optional
import datetime
from pydantic import Field

class OrderType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderBase(BaseModel):
    stock_name: str
    shares: int
    price_per_share: float
    order_type: OrderType

class OrderCreate(OrderBase):
    shares: int = Field(..., gt=0)
    user_id: int

class OrderUpdate(BaseModel):
    shares: Optional[int]
    price_per_share: Optional[float]

class OrderOut(OrderBase):
    id: int
    user_id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True