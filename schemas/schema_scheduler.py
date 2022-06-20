from datetime import datetime

from pydantic import BaseModel, Field
from typing import List


class JobCreate(BaseModel):
    # scheduled: bool = Field(title="Whether the job was scheduler or not",
    #                         description="Whether the job was scheduler or not")
    # job_id: str = Field(title="The Job ID in APScheduler", description="The Job ID in APScheduler")
    # time_in_hours: int = Field(title="The Job ID in APScheduler", description="To add time in hours", le=23)
    time: int = Field(title="The Job ID in APScheduler", description="To add time in minute")


class JobDelete(BaseModel):
    job_id: str = Field(title="The Job ID in APScheduler", description="The Job ID in APScheduler")

    class Config:
        schema_extra = {
            'example': {
                "job_id": "1",
            }
        }
