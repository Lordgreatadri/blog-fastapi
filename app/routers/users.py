from fastapi import FastAPI, Response, status, Depends, HTTPException, APIRouter
import psycopg2
from typing import List
from psycopg2.extras import RealDictCursor
import time 
from sqlalchemy.orm import Session 
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    tags=["Registration"],
    prefix="/api/v1/users"
)


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


#user signup
@router.post("/signup", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def singup(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    #hash the password here
    hashed_password = utils.hash( user.password)
    user.password = hashed_password

    # db_user = models.User(name=user.name,email=user.email, password=hashed_password)
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# #show user
@router.get("/{id}", response_model=schemas.UserResponse)
def show_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=404, detail=f"User with the id: {id} does not exist")
    
    return user

