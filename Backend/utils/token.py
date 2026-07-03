import os
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

from fastapi import Depends, HTTPException
from models import users
from sqlalchemy.orm import Session
from database import get_db

load_dotenv()   
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM="HS256"

def create_access_token(data: dict, expires_delta: timedelta
                         = timedelta(hours=2)):
    to_encode = data.copy()
    expire = datetime.now()+expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, db: Session = Depends(get_db)):
    if not token or token in ("undefined", "null"):
        raise HTTPException(status_code=401, detail="No token provided")
    try:
        to_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(to_decode["sub"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    current_user = db.query(users.User).filter(users.User.id == user_id).first()
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return current_user