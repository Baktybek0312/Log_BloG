import schedule

from pytz import utc
from datetime import datetime
import time
import logging
from io import BytesIO

from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session

import xlsxwriter
import pandas as pd

from schemas.schema_scheduler import JobCreate, JobDelete
from models.table_job import JobConfig
from services.excel_data import get_data_report
from services.scheduler_job import create_job, read_job
from db.database import get_db

router = APIRouter(
    prefix='/job_tasks',
    tags=['Jobs']
)


@router.put('/update_job')
async def modify_job(job: JobCreate, db: Session = Depends(get_db)):
    return create_job(db=db, job=job)


@router.get('/get_scheduler_jobs')
async def get_job(db: Session = Depends(get_db)):
    return read_job(db=db)


@router.delete('/delete/{job_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_interval_job_id(id: int, db: Session = Depends(get_db)):
    job_id = db.query(JobConfig).filter(JobConfig.id == id)
    job = job_id.first()
    if job is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Job with id: {id} does not exist.")
    job_id.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/get_excel_file', response_description='xlsx')
async def make_xls_file_response():
    data = get_data_report()
    return data
    # output = BytesIO()
    # with xlsxwriter.Workbook(output) as workbook:
    #     worksheet = workbook.add_worksheet()
    #     worksheet.write(0, 0, 'id')
    #     worksheet.write(0, 1, 'title')
    #     worksheet.write(0, 2, 'description')
    #     worksheet.write(0, 3, 'owner_id')
    #     worksheet.write(0, 4, 'username')
    #     worksheet.write(0, 5, 'email')
    #     output.seek(0)
    # headers = {
    #     'Content-Disposition': 'attachment; filename="filename.xlsx"'
    # }
    # return StreamingResponse(output, headers=headers)
