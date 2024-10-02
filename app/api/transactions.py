from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.transactions import TransactionCRUD
from app.schemas.transaction import TransactionOut
from app.core.database import get_db

router = APIRouter()

class TransactionAPI:
    def __init__(self, db: Session):
        self.crud = TransactionCRUD(db)

    def get_transactions(self):
        return self.crud.get_transactions()

transaction_api = TransactionAPI

@router.get("/transactions", response_model=list[TransactionOut])
def get_transactions(db: Session = Depends(get_db)):
    return transaction_api(db).get_transactions()