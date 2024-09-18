from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.user_schema import UserCreate, UserRead 

def get_users(db: Session, skip: int = 0, limit: int = 10):
    query = text("SELECT id, username, email FROM users OFFSET :skip LIMIT :limit")
    result = db.execute(query, {"skip": skip, "limit": limit})
    return [UserRead(id=str(row.id), username=row.username, email=row.email) for row in result.fetchall()]

def get_user(db: Session, user_id: int):
    query = text("SELECT id, username, email FROM users WHERE id = :id")
    result = db.execute(query, {"id": user_id})
    return result.fetchone()

def update_user(db: Session, user_id: int, user: UserCreate):
    query = text("UPDATE users SET username = :username, email = :email WHERE id = :id RETURNING id, username, email")
    result = db.execute(query, {"username": user.name, "email": user.email, "id": user_id})
    db.commit()
    return result.fetchone()

def delete_user(db: Session, user_id: int):
    query = text("DELETE FROM users WHERE id = :id RETURNING id, username, email")
    result = db.execute(query, {"id": user_id})
    db.commit()
    return result.fetchone()