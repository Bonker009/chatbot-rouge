from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.api.auth.auth import get_current_user
from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserRead
from app.crud.users import get_users, get_user, update_user, delete_user
from typing import List
 
router = APIRouter()

@router.get("/users/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 10, current_user: UserRead = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_users(db, skip, limit)

@router.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, current_user: UserRead = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead(id=user.id, name=user.name, email=user.email)

@router.put("/users/{user_id}", response_model=UserRead)
def update_user_endpoint(user_id: int, user: UserCreate, current_user: UserRead = Depends(get_current_user), db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead(id=updated_user.id, name=updated_user.name, email=updated_user.email)

@router.delete("/users/{user_id}", response_model=UserRead)
def delete_user_endpoint(user_id: int, current_user: UserRead = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted_user = delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead(id=deleted_user.id, name=deleted_user.name, email=deleted_user.email)