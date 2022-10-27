from fastapi import Depends, status, HTTPException, APIRouter
from ..database import get_db
from .. import models, schemas
from sqlalchemy.orm import Session
from typing import List

from ..utils import hash

router = APIRouter(
    prefix='/users',
    tags=["Users"],
)

#################################################
##########            CREATE           ##########
#################################################
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_users(user: schemas.UserCreate, db: Session  = Depends(get_db)):

    user.password = hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#################################################
##########            READ            ##########
#################################################
@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users


#################################################
##########          READ \w ID         ##########
#################################################
@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} does not exist.')

    return user