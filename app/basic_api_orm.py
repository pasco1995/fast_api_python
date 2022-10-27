from fastapi import FastAPI, Depends, Response, status, HTTPException
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#################################################
##########             ROOT            ##########
#################################################
@app.get("/")
def root():
    return {"message": "Python API Development"}


#################################################
##########             READ            ##########
#################################################
@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session  = Depends(get_db)):

    posts = db.query(models.Post).all()

    return posts


#################################################
##########            CREATE           ##########
#################################################
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session  = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#################################################
##########          READ \w ID         ##########
#################################################
@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session  = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found.')

    return post


#################################################
##########            DELETE           ##########
#################################################
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session  = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found.')

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#################################################
##########            UPDATE           ##########
#################################################
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(post: schemas.PostCreate, id : int, db: Session  = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    current_post = post_query.first()

    if current_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found.')

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


