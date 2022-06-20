import time
import logging

import schedule

from services.parse_data import get_data

logging.basicConfig()
schedule_logger = logging.getLogger('schedule')
schedule_logger.setLevel(level=logging.INFO)


def scheduler_job():
    """
    Функция для работы с
    """
    try:
        data = get_data()
        schedule_logger.info('success scheduler job')
        return data
    except:
        schedule_logger.info('sorry, but there is a problem with the server')


schedule.every(interval=5).seconds.do(scheduler_job)
print(schedule.get_jobs())
print(schedule_logger)

while True:
    schedule.run_pending()
    time.sleep(5)
