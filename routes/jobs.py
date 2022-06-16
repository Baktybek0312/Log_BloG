from pytz import utc
from datetime import datetime
import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session

from schemas.schema_scheduler import JobCreate, JobDelete
from core.scheduler import my_scheduler
from core.settings import settings
from services.parse_data import get_data
from services.excel_data import get_data_report

router = APIRouter(
    prefix='/job_tasks',
    tags=['Jobs']
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post('/add_job')
async def add_scheduler_from_parse_data(job: JobCreate):
    """
    Добавление нового задания в расписание
    """
    try:
        schedule = my_scheduler.add_job(
            get_data, 'cron', id=job.job_id,
            hour=job.time_in_hours, minute=job.time_in_minute,
        )
        return {"scheduled": True, "job_id": schedule.id}
    except:
        raise HTTPException(status_code=400, detail=f'Job identifier {job.job_id} conflicts with an existing job')


@router.get('/get_scheduler_jobs')
async def get_scheduled_syncs():
    """
    Предоставит список текущих запланированных задач
    """
    schedules = []
    for job in my_scheduler.get_jobs():
        schedules.append({"job_id": str(job.id), "run_frequency": str(job.trigger), "next_run": str(job.next_run_time)})
    return {"jobs": schedules}


# @router.post('/update/{job_id}')
# def upgrade_job(job: JobCreate):
#     pass


@router.delete('/delete_job')
async def remove_jobs_from_scheduler(job: JobDelete):
    """
    Удаление задание из расписании
    """
    try:
        my_scheduler.remove_job(job_id=job.job_id)
        return {"message": f"Job {job.job_id} deleted!"}
    except:
        raise HTTPException(status_code=404, detail="Job id not exists!")


@router.get('/get_excel_file')
async def make_xls_file_response():
    return get_data_report()
