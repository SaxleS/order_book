from sqlalchemy import create_engine
from app.models.users import User
from app.models.order import Order
from app.models.transaction import Transaction
from app.core.database import Base

# ручное создание таблиц
engine = create_engine("postgresql://order_book:rekwde4234rekNJrewfwef@13.49.223.194:5432/order_book")

Base.metadata.create_all(bind=engine)

print("Таблицы созданы успешно!")