import time
import logging

from sqlalchemy.orm import Session
from sqlalchemy import desc
import schedule

from services.parse_data import get_data
from models.table_job import JobConfig
from db.database import SessionLocal
from logger.log_info import logger


schedule_logger = logger

db: Session = SessionLocal()


def record_data():
    """
    Утилитовая функция для запланированния задач
    """
    try:
        data = get_data()
        schedule_logger.info('success scheduler job')
        return data
    except:
        schedule_logger.error('sorry, but there is a problem with the server: bad status 500')


interval = db.query(JobConfig).order_by(desc(JobConfig.id)).first().interval

schedule.every(interval=interval).minutes.do(record_data)
print(schedule_logger)
print(schedule.get_jobs())

while True:
    schedule.run_pending()
    time.sleep(10)
