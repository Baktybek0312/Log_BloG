from datetime import datetime

from pydantic import BaseModel, Field
from typing import List


class JobCreate(BaseModel):
    interval: int = Field(title="The Job ID in APScheduler", description="To add time in minute")


class JobDelete(BaseModel):
    id: int = Field(title="The Job ID in APScheduler", description="The Job ID in APScheduler")
