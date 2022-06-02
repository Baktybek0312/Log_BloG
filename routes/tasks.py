import random
import time

from fastapi import FastAPI, BackgroundTasks
from fastapi import APIRouter, Depends, status, HTTPException

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from services import parse_data
from core.log_config import logger, divide
from db.database import get_db
from schemas.posts_schema import PostList

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)
# trigger = SetTrigger()
# scheduler = BackgroundScheduler()
URL = 'http://127.0.0.1:8000/posts/list'


@router.get("/")
async def read_root():
    a = 100
    b = random.randint(0, 1)
    return {"success": True, "result": divide(a, b)}


@router.post("/create_task")
async def create_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(background_tasks)
    return {'result': 'success'}


@router.get("/get_data")
def get_datas(db: Session = Depends(get_db)):
    return parse_data.get_data(db=db)

# scheduler.configure(timezone=str(tzlocal.get_localzone()))
# scheduler.add_job(trigger.UpdateSetRefresh, 'interval', seconds=2, id='1', name='refresh_hereoes_positions')
# scheduler.start()
#
# while True:
#     print(trigger.set_refresh)
#     time.sleep(2)
# @app.post("/upload")
# async def upload(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         with open(file.filename, 'wb') as f:
#             f.write(contents)
#     except Exception:
#         return {"message": "There was an error uploading the file"}
#     finally:
#         await file.close()
#     return {"message": f"Successfuly uploaded {file.filename}"}
