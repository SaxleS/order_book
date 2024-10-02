from fastapi import APIRouter
from app.api import orders, users, transactions  # Импортируйте transactions

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])