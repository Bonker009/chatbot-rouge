from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import User
from app.api.auth.auth import ALGORITHM, SECRET_KEY, create_access_token, authenticate_user
from jwt.exceptions import InvalidTokenError
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user(db, username)
    except InvalidTokenError:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    return user