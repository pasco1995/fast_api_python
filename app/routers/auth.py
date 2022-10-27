from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import models, schemas
from sqlalchemy.orm import Session

from ..utils import verify
from ..oauth2 import create_access_token

router = APIRouter(
    tags=["Auth"],
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials')

    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials')

    access_token = create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
