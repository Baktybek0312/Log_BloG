from pytz import utc
import random
import time

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.schema_scheduler import JobCreate, ActionEnum, TypeEnum
from db.database import get_db
from utils.job_id_generate import generate_uuid
from services import parse_data

router = APIRouter(
    prefix='/job_tasks',
    tags=['Jobs']
)

# # @router.get('/get_data')
# def record_data(db: Session = Depends(get_db)):
#     data = parse_data.get_data(db=db)
#     return data

# @router.on_event('startup')
# async def run_scheduler():
#     # time.sleep(5)
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(func=record_data, trigger='cron', second='*/5', timezone=utc)
#     scheduler.start()
#     return {'result': 'success'}
