from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from sqlalchemy.orm import Session
from .config import settings


oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credential_exception):

    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        id = payload.get("user_id")

        if id is None:
            raise credential_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credential_exception

    return token_data


def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                         detail=f'Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})

    token_data = verify_access_token(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    return user