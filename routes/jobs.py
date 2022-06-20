from pytz import utc
from datetime import datetime
import time
import threading
import logging
from io import BytesIO

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session
import xlsxwriter
import schedule

from schemas.schema_scheduler import JobCreate, JobDelete
from core.scheduler import my_scheduler
from core.settings import settings
from services.parse_data import get_data
from services.excel_data import get_data_report

router = APIRouter(
    prefix='/job_tasks',
    tags=['Jobs']
)


# async def add_scheduler_from_parse_data(job: JobCreate):
#     my_scheduler.add_job(get_data, trigger='interval', minutes=job.time)
#     print(my_scheduler)

# @router.post('/add_job')
# async def add_scheduler_from_parse_data(job: JobCreate):
#     """
#     Добавление нового задания в расписание
#     """
#     try:
#         schedule = my_scheduler.add_job(
#             get_data, 'cron', id=job.job_id,
#             hour=job.time_in_hours, minute=job.time_in_minute,
#         )
#         return {"scheduled": True, "job_id": schedule.id}
#     except:
#         raise HTTPException(status_code=400, detail=f'Job identifier {job.job_id} conflicts with an existing job')


# @router.get('/get_scheduler_jobs')
# async def get_scheduled_syncs():
#     """
#     Предоставит список текущих запланированных задач
#     """
#     schedules = []
#     for job in schedule.get_jobs():
#         print(job)
#         # schedules.append({"job_id": str(job.id), "run_frequency": str(job.trigger), "next_run": str(job.next_run_time)})
    # return {"jobs": schedules}


# @router.post('/update/{job_id}')
# def upgrade_job(job: JobCreate):
#     pass

#
# @router.delete('/delete_job')
# async def remove_jobs_from_scheduler(job: JobDelete):
#     """
#     Удаление задание из расписании
#     """
#     try:
#         my_scheduler.remove_job(job_id=job.job_id)
#         return {"message": f"Job {job.job_id} deleted!"}
#     except:
#         raise HTTPException(status_code=404, detail="Job id not exists!")


@router.get('/get_excel_file', response_description='xlsx')
async def make_xls_file_response():
    data = get_data_report()
    output = BytesIO()
    with xlsxwriter.Workbook(output) as workbook:
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, 'id')
        worksheet.write(0, 1, 'title')
        worksheet.write(0, 2, 'description')
        worksheet.write(0, 3, 'owner_id')
        worksheet.write(0, 4, 'username')
        worksheet.write(0, 5, 'email')
        output.seek(0)
    headers = {
        'Content-Disposition': 'attachment; filename="filename.xlsx"'
    }
    return StreamingResponse(output, headers=headers)
