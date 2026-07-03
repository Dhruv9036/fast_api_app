from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.oauth2 import get_current_user, role_required
from models.users import User
from schemas.user import UserCreate, UserResponse, Login_User
from schemas.token import Token
from database import get_db
from utils.security import hash_password, verify_password
from utils.token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    db_user = User(name=user.name, email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form_data.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token({
        "sub": str(existing_user.id),
        "role": existing_user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }