from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate
from app.models.order import Order, OrderType
class OrderCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: OrderCreate):
        db_order = Order(**order.model_dump())
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def get_orders(self):
        return self.db.query(Order).order_by(Order.price_per_share, Order.created_at).all()

    def get_order(self, order_id: int):
        return self.db.query(Order).filter(Order.id == order_id).first()

    def delete_order(self, order_id: int):
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if order:
            self.db.delete(order)
            self.db.commit()

    def update_order(self, order_id: int, order_update: OrderUpdate):
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if order:
            for key, value in order_update.model_dump(exclude_unset=True).items():
                setattr(order, key, value)
            self.db.commit()
            self.db.refresh(order)
        return order

    def get_matching_sell_orders(self, order):
        return self.db.query(Order).filter(
            Order.stock_name == order.stock_name,
            Order.order_type == OrderType.SELL,
            Order.price_per_share <= order.price_per_share,
            Order.id != order.id
        ).order_by(Order.created_at).all()

    def get_matching_buy_orders(self, order):
        return self.db.query(Order).filter(
            Order.stock_name == order.stock_name,
            Order.order_type == OrderType.BUY,
            Order.price_per_share >= order.price_per_share,
            Order.id != order.id
        ).order_by(Order.created_at).all()