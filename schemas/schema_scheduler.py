from datetime import datetime
from enum import Enum
#
from pydantic import BaseModel, Field
from typing import List


class TypeEnum(str, Enum):
    cron = 'cron'
    single = 'single'


class ActionEnum(str, Enum):
    resume = 'resume'
    pause = 'pause'


class JobCreate(BaseModel):
    job_id: int
    name: str
    job_class: str
    args: dict
    job_type: TypeEnum
    crontab: str
    created_time: datetime = None


class CurrentScheduledJob(BaseModel):
    job_id: str = Field(title="The Job ID in APScheduler", description="The Job ID in APScheduler")
    run_frequency: str = Field(title="The Job Interval in APScheduler", description="The Job Interval in APScheduler")
    next_run: str = Field(title="Next Scheduled Run for the Job", description="Next Scheduled Run for the Job")

    class Config:
        schema_extra = {
            'example': {
                "job_id": "1",
                "run_frequency": "interval[0:05:00]",
                "next_run": "2020-11-10 22:12:09.397935+10:00"
            }
        }


class CurrentScheduledJobsResponse(BaseModel):
    jobs: List[CurrentScheduledJob]


class JobCreateDeleteResponse(BaseModel):
    scheduled: bool = Field(title="Whether the job was scheduler or not",
                            description="Whether the job was scheduler or not")
    job_id: str = Field(title="The Job ID in APScheduler", description="The Job ID in APScheduler")
    time_in_seconds: int = Field(title="The Job ID in APScheduler", description="To add time in seconds")

    class Config:
        schema_extra = {
            'example': {
                "scheduled": True,
                "job_id": "1",
                "time_in_seconds": "60"
            }
        }


class JobListResponse(BaseModel):
    jobs: List[JobCreateDeleteResponse]
