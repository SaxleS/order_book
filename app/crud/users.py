from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users import UserCreate

class UserCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate):
        db_user = User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_users(self):
        return self.db.query(User).all()