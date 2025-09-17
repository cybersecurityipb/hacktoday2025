import secrets
import os
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated

from src.models import get_db, User


SECRET_KEY = secrets.token_hex(64)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(hours=1)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(user_id: int, is_admin: bool):
    data = {
        "user_id": user_id,
        "is_admin": is_admin,
        "exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRE
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You need to login to access this page.")
        return user

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You need to login to access this page.")
