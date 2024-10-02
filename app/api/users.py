from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.users import UserCRUD
from app.schemas.users import UserCreate, UserOut
from app.core.database import get_db

router = APIRouter()

class UserAPI:
    def __init__(self, db: Session):
        self.crud = UserCRUD(db)

    def create_user(self, user: UserCreate):
        return self.crud.create_user(user)

    def get_user(self, user_id: int):
        user = self.crud.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_users(self):
        return self.crud.get_users()

user_api = UserAPI

@router.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_api(db).create_user(user)

@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_api(db).get_user(user_id)

@router.get("/users", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return user_api(db).get_users()