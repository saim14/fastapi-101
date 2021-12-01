import models 
import schemas
import oauth2
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import  get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
) 

# Router decorator and functions parameters
# Body parameters - post: schemas.PostCreate
# Path parameters - url/{variable} - variable: data_type
# Database reference - db: Session = Depends(get_db)
# Return model from function - response_model=schemas.Post
# Query parameters - variable_name: data_type = optional_value
# Functions reference - current_user: dict =  Depends(oauth2.get_current_user)

######### CRUD operation for posts ############ 

# C: Create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: dict =  Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id = current_user.id, **post.dict()) # Efficient way to create new post
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # returning sql statement
    return new_post


# R: Read all posts 
@router.get("/", response_model=List[schemas.PostOut])
async def read_posts(
    db: Session = Depends(get_db), 
    current_user: dict =  Depends(oauth2.get_current_user), 
    limit: int=10, skip: int=0, search: Optional[str]=""
):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # If we want to only get currentuser posts
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    results = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("vote_counts")
        ).join(
            models.Vote, 
            models.Post.id == models.Vote.post_id, 
            isouter=True
            ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

# R: Read post by id
@router.get("/{post_id}", response_model=schemas.PostOut)
async def read_post(post_id: int, db: Session = Depends(get_db), current_user: dict =  Depends(oauth2.get_current_user)):
    post = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("vote_counts")
        ).join(
            models.Vote, 
            models.Post.id == models.Vote.post_id, 
            isouter=True
            ).group_by(models.Post.id).filter(models.Post.id == post_id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {post_id} not found")
    return post
       

# U: Update post by id
@router.put("/{post_id}", response_model=schemas.Post)
async def update_post(
    post_id: int, 
    post: schemas.PostUpdate, 
    db: Session = Depends(get_db), 
    current_user: dict =  Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {post_id} not found")
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"You are not authorized to update this post")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


# D: Delete post by id
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db), current_user: dict =  Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {post_id} not found")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"You are not authorized to delete this post")
    post.delete(synchronize_session=False)
    db.commit()