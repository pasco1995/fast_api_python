from fastapi import Depends, status, HTTPException, APIRouter
from ..database import get_db
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/vote',
    tags=["Votes"],
)

#################################################
##########            CREATE           ##########
#################################################
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session  = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):

    found_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if found_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Post with id {vote.post_id} not found.')

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'User {current_user.id} has already voted on post {vote.post_id}.')
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote."}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Vote does not exist.')
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote."}