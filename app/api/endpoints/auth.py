from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserRead, Token
from app.api.auth.auth import create_user, authenticate_user, create_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the username already exists
    existing_user = authenticate_user(db, user.username, user.password)  # Reused for validation
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    new_user = create_user(db, user)
    return UserRead(id=str(new_user.id), username=new_user.username, email=new_user.email)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")