from sqlalchemy import (
    Column, String, Text, Integer, ForeignKey
)
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)

    post = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner_name = Column(String)
    owner_email = Column(String)
    owner = relationship("User", back_populates="post")
