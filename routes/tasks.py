import random
import time

from fastapi import BackgroundTasks, UploadFile, File
from fastapi import APIRouter, Depends, status, HTTPException

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from services import parse_data
from core.log_config import logger, divide
from db.database import get_db

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)


@router.get("/")
async def read_root():
    a = 100
    b = random.randint(0, 1)
    return {'success': True, 'result': divide(a, b)}


@router.on_event('startup')
async def create_task():
    time.sleep(5)
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_datas, 'cron', second='*/5')
    return {'result': 'success'}


@router.get('/get_data')
def get_datas(db: Session = Depends(get_db)):
    return parse_data.get_data(db=db)


# scheduler.configure(timezone=str(tzlocal.get_localzone()))
# scheduler.add_job(trigger.UpdateSetRefresh, 'interval', seconds=2, id='1', name='refresh_hereoes_positions')
# scheduler.start()
#
# while True:
#     print(trigger.set_refresh)
#     time.sleep(2)
