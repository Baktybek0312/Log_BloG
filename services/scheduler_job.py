from sqlalchemy.orm import Session

from models.table_job import JobConfig

from db.database import SessionLocal
from schemas.schema_scheduler import JobCreate, JobDelete
from models.table_job import JobConfig
from logger.log_info import logger


def create_job(db: Session, job: JobCreate):
    db_job = JobConfig(**job.dict())
    db.add(db_job)
    db.commit()
    return job


def read_job(db: Session):
    return db.query(JobConfig).all()
