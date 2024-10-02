from fastapi import FastAPI
from app.api import orders, transactions, users 


app = FastAPI(
    title="Order Book API",
    description="API / AZATI - testTask [Anžhalika Hrytsevich]",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)



app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(orders.router, prefix="/api/v1", tags=["Orders"])
app.include_router(transactions.router, prefix="/api/v1", tags=["Transactions"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Order Book API"}