from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.orders import OrderCRUD
from app.crud.transactions import TransactionCRUD
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate
from app.core.database import get_db
from app.models.order import OrderType

router = APIRouter()

class OrderAPI:
    def __init__(self, db: Session):
        self.crud = OrderCRUD(db)
        self.transaction_crud = TransactionCRUD(db)

    def create_order(self, order: OrderCreate):
        new_order = self.crud.create_order(order)
        self.execute_matching_orders(new_order)
        return new_order

    def get_orders(self):
        return self.crud.get_orders()

    def get_order(self, order_id: int):
        order = self.crud.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    def delete_order(self, order_id: int):
        order = self.crud.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        self.crud.delete_order(order_id)
        return {"message": "Order deleted"}

    def update_order(self, order_id: int, order_update: OrderUpdate):
        order = self.crud.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return self.crud.update_order(order_id, order_update)
    

    
    def execute_matching_orders(self, new_order):
        if new_order.order_type == OrderType.BUY:
            matching_orders = self.crud.get_matching_sell_orders(new_order)
        else:
            matching_orders = self.crud.get_matching_buy_orders(new_order)
        updated_orders = []

        for matching_order in matching_orders:
            
            if matching_order.shares <= 0:
                continue

            # Определяе акций для исполнения
            shares_to_execute = min(new_order.shares, matching_order.shares)


            # Создаем транзакцию
            self.transaction_crud.create_transaction(
                stock_name=new_order.stock_name,
                shares=shares_to_execute,
                price_per_share=(
                    matching_order.price_per_share
                    if new_order.order_type == "BUY"
                    else new_order.price_per_share
                ),
                buyer_id=(
                    new_order.user_id
                    if new_order.order_type == "BUY"
                    else matching_order.user_id
                ),
                seller_id=(
                    new_order.user_id
                    if new_order.order_type == "SELL"
                    else matching_order.user_id
                ),
            )


            new_order.shares -= shares_to_execute
            matching_order.shares -= shares_to_execute


            self.crud.db.add(matching_order)
            self.crud.db.add(new_order)
            updated_orders.append(matching_order)

            if new_order.shares == 0:
                break


        self.crud.db.commit()
        self.crud.db.refresh(new_order)
        for order in updated_orders:
            self.crud.db.refresh(order)



order_api = OrderAPI

@router.post("/orders", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_api(db).create_order(order)

@router.get("/orders", response_model=list[OrderOut])
def get_orders(db: Session = Depends(get_db)):
    return order_api(db).get_orders()

@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return order_api(db).get_order(order_id)

@router.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return order_api(db).delete_order(order_id)

@router.put("/orders/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    return order_api(db).update_order(order_id, order_update)