from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from utils.token import verify_token
from database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str= Depends(oauth2_scheme),db:Session=Depends(get_db)):
    current__user = verify_token(token, db)
    if current__user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return current__user

def role_required(roles:list):
    def role_decorator(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403,detail="Insufficient permissions")
        return current_user
    return role_decorator