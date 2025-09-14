from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app=FastAPI()
models.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title:str
    content:str
    user_id:int

class UserBase(BaseModel):
    username:str


def get_db():#dependency
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/posts/",status_code=status.HTTP_201_CREATED)
async def create_post(post:PostBase,db: db_dependency):
    # FIX: First, check if the user actually exists.
    user = db.query(models.User).filter(models.User.id == post.user_id).first()
    if not user:
        # If not, raise a clean 404 error instead of crashing.
        raise HTTPException(status_code=404, detail=f"User with id {post.user_id} not found")

    # Now that we know the user exists, it's safe to create the post.
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post # Also fixed to return the object



@app.post("/users/",status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    # FIX: Check if the username is already taken.
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        # If it is, raise a 400 Bad Request error.
        raise HTTPException(status_code=400, detail="Username already registered")

    # Now it's safe to create the user.
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



@app.get("/users/{user_id}",status_code=status.HTTP_200_OK)
async def read_user(user_id:int,db:db_dependency):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="user not found")
    return user

@app.get("/posts/{post_id}",status_code=status.HTTP_200_OK)
async def read_post(post_id:int,db:db_dependency):
    post=db.query(models.Post).filter(models.Post.id==post_id).first()
    if post is None:
        raise HTTPException(status_code=404,detail="post not found")
    return post

@app.delete("/posts/{post_id}",status_code=status.HTTP_200_OK)
async def delete_post(post_id:int,db:db_dependency):
    post=db.query(models.Post).filter(models.Post.id==post_id).first()
    if post is None:
        raise HTTPException(status_code=404,detail="post not found")
    db.delete(post)
    db.commit()
    return {"detail":"post deleted successfully"}