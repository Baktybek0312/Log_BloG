from pytz import utc
from datetime import datetime
from enum import Enum
from uuid import uuid4

import logging

from apscheduler.triggers.cron import CronTrigger
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session

from schemas.schema_scheduler import JobCreate, ActionEnum
from schemas.schema_scheduler import JobCreateDeleteResponse, JobListResponse
from core.scheduler import my_scheduler
from db.database import get_db, SessionLocal
from services import parse_data
from core.settings import settings
from services.parse_data import get_data

router = APIRouter(
    prefix='/job_tasks',
    tags=['Jobs']
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post('/add_job')
async def add_scheduler_from_parse_data(job: JobCreateDeleteResponse):
    """
    Добавление нового задания в расписание
    """
    schedule = my_scheduler.add_job(get_data, 'interval', id=job.job_id, seconds=job.time_in_seconds)
    return {"scheduled": True, "job_id": schedule.id}


@router.get('/get_scheduler_jobs')
async def get_scheduled_syncs():
    """
    Предоставит список текущих запланированных задач

    """
    schedules = []
    for job in my_scheduler.get_jobs():
        schedules.append({"job_id": str(job.id), "run_frequency": str(job.trigger), "next_run": str(job.next_run_time)})
    return {"jobs": schedules}


@router.put('/pause_job')
async def pause_scheduler_job(job_id: JobCreateDeleteResponse):
    my_scheduler.pause_job(job_id=job_id.job_id)
    return f"successfully stopped id {job_id.job_id}"


@router.delete('/delete_jobs')
async def remove_jobs_from_scheduler(job_id: JobCreateDeleteResponse):
    my_scheduler.remove_job(job_id=job_id.job_id)
    return f"deleted jobs{job_id}"
