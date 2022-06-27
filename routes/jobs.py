from datetime import datetime
import time
import logging
from io import BytesIO

from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

import schedule
import xlsxwriter

from schemas.schema_scheduler import JobCreate, JobDelete
from models.table_job import JobConfig
from services.scheduler_job import create_job, read_job
from db.database import get_db
from models.table_posts import Post
from logger.log_info import logger

router = APIRouter(
    prefix='/job_tasks',
    tags=['Jobs']
)


@router.put('/update_job', status_code=status.HTTP_200_OK)
async def modify_job(job: JobCreate, db: Session = Depends(get_db)):
    try:
        create_job_interval = create_job(db=db, job=job)
        logger.info('message: successfully created an interval in the task')
        return create_job_interval
    except:
        logger.error('message: value is not a valid integer')


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
async def get_excel(db: Session = Depends(get_db)):
    """
    Выгрузка в excel файл из БД
    """

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)

    border = workbook.add_format({'border': 1, 'align': 'left'})
    color = workbook.add_format({'border': 1, 'align': 'left', 'bold': True, 'font_color': 'black'})

    worksheet = workbook.add_worksheet('record dataset')
    worksheet.set_column('A:A', 6)
    worksheet.set_column('B:B', 40)
    worksheet.set_column('C:C', 45)
    worksheet.set_column('D:D', 6)
    worksheet.set_column('E:E', 30)
    worksheet.set_column('F:F', 35)

    worksheet.set_row(0, 30)

    worksheet.write('A1', 'ID', color)
    worksheet.write('B1', 'Title', color)
    worksheet.write('C1', 'Description', color)
    worksheet.write('D1', 'Owner_id', color)
    worksheet.write('E1', 'Username', color)
    worksheet.write('F1', 'Email', color)

    posts = db.query(Post).all()
    for i, p in enumerate(posts):
        worksheet.write(i + 1, 0, p.id, border)
        worksheet.write(i + 1, 1, p.title, border)
        worksheet.write(i + 1, 2, p.description, border)
        worksheet.write(i + 1, 3, p.owner_id, border)
        worksheet.write(i + 1, 4, p.owner_name, border)
        worksheet.write(i + 1, 5, p.owner_email, border)
    workbook.close()
    output.seek(0)

    headers = {
        'Content-Disposition': 'attachment; filename="filename.xlsx"'
    }
    logger.info('successfully unloaded from the database to an excel file')
    return StreamingResponse(output, headers=headers)
