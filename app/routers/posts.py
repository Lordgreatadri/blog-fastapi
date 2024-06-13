from fastapi import Response, status, Depends, HTTPException, APIRouter
import psycopg2
from typing import List, Optional
from psycopg2.extras import RealDictCursor
import time 
from sqlalchemy.orm import Session 
from sqlalchemy import func 

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/posts",
    tags=['Posts']
)


# #creating a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # post = post.dict()#convert data to json 
    # post = models.Post(title = post.title, content = post.content, published = post.published, owner_id=post.owner_id)
    # return current_user
    post = models.Post(owner_id=current_user.id, **post.model_dump())#this is the better way
    db.add(post)
    db.commit()
    db.refresh(post)

    return post


#get posts
@router.get('/', response_model=List[schemas.PostOut])
# @router.get('/')
def get_posts(db: Session = Depends(get_db), search:Optional[str] = "",limits:int = 15, skip:int=0):
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)
    # ).limit(limits).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(models.Post.title.contains(search)).group_by(models.Post.id).limit(limits).offset(skip).all()

    if posts is None:
        raise HTTPException(status_code=209, detail="No post content at the moment")
    
    return posts



#get owner posts
@router.get('/owner', response_model=List[schemas.PostOut])
def get_owner_posts(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user), limits:int = 20):
    # posts = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id
    # ).limit(limits).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.owner_id == current_user.id
    ).limit(limits).all()

    if posts is None:
        raise HTTPException(status_code=209, detail="No post content at the moment")
    
    return posts





# #show post
@router.get("/{id}", response_model=schemas.PostOut)
def show_post(id:int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=404, detail=f"No post content for the id: {id}")
    
    return post
          
                    





# #update post
@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_post(id:int, post: schemas.UpdatePost, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post_query.first() is None:
        raise HTTPException(status_code=404, detail=f"No post content for the id: {id}")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform the requested action")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return {
            "status" : status.HTTP_200_OK,
            "detail":"Post updated successfully",
            "data":post_query.first()
    } 
    








# #delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=404, detail=f"No post content for the id: {id}")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform the requested action")
    
    post.delete(synchronize_session = False)
    db.commit()

    return {
            "status" : status.HTTP_204_NO_CONTENT,
            "detail":"Post deleted successfully"
    } 