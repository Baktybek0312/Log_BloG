from sqlalchemy import (
    Column, String, Text, Integer
)

from db.database import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(Text)
    owner_id = Column(Integer)
    owner_name = Column(String)
    owner_email = Column(String)
