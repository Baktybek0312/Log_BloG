from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from db.database import Base


class JobConfig(Base):
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    interval = Column(Integer)
    create_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime)
