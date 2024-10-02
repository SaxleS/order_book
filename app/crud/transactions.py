from sqlalchemy.orm import Session
from app.models.transaction import Transaction

class TransactionCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_transaction(self, buyer_id: int, seller_id: int, stock_name: str, shares: int, price_per_share: float):
        transaction = Transaction(
            buyer_id=buyer_id,
            seller_id=seller_id,
            stock_name=stock_name,
            shares=shares,
            price_per_share=price_per_share
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)

        self.db.flush()
        return transaction

    def get_transactions(self):
        return self.db.query(Transaction).all()