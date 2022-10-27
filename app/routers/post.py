from fastapi import Depends, Response, status, HTTPException, APIRouter
from ..database import get_db
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List


router = APIRouter(
    prefix='/posts',
    tags=['Posts'],
)

#################################################
##########             READ            ##########
#################################################
@router.get("/", response_model=List[schemas.PostAndVotesResponse])
def get_posts(db: Session  = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: str = ""):

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results


#################################################
##########            CREATE           ##########
#################################################
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session  = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#################################################
##########          READ \w ID         ##########
#################################################
@router.get("/{id}", response_model=schemas.PostAndVotesResponse)
def get_post(id: int, db: Session  = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found.')

    return post


#################################################
##########            DELETE           ##########
#################################################
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session  = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found.')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action.')

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#################################################
##########            UPDATE           ##########
#################################################
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(post: schemas.PostCreate, id : int, db: Session  = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    current_post = post_query.first()

    if current_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found.')

    if current_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action.')

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
