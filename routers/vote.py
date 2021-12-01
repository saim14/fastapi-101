import models 
import schemas
import oauth2
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import  get_db
from typing import List, Optional

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
) 

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already voted this post")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote created successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You haven't voted this post")
        db.delete(found_vote)
        db.commit()
        return {"message": "Vote deleted successfully"}
        
        
