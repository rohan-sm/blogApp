# to create table or database structure

from sqlalchemy import Column, Integer,String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique = True)
    # This tells SQLAlchemy that a User can have many Posts
    posts = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"

    id =Column(Integer,primary_key=True,index=True)
    title =Column(String(50))
    content = Column(String(100))
    user_id=Column(Integer, ForeignKey("Users.id"))
    owner = relationship("User", back_populates="posts")
