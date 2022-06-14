import json

from sqlalchemy.orm import Session
from fastapi import Depends

import requests
import pandas as pd

from models.table_posts import Post
from db.database import get_db, SessionLocal
# from schemas.schema_scheduler import CurrentScheduledJob, CurrentScheduledJobsResponse, JobCreateDeleteResponse

db: Session = SessionLocal()


def get_data():
    """
    данная фукция парсит  URL = "http://127.0.0.1:8000/posts/list" и сохроняет в БД и excel файл
    """
    URL = "http://127.0.0.1:8000/posts/list"
    response = requests.get(url=URL, headers={'Content-Type': 'application/json'})
    res = json.loads(response.text)

    for r in res['list']:
        check_data_id = db.query(Post).filter(Post.id == r['id']).first()
        if not check_data_id:
            data = Post()
            data.id = r['id']
            data.title = r['title']
            data.description = r['description']
            data.owner_id = r['owner_id']
            data.owner_name = r['owner']['username']
            data.owner_email = r['owner']['email']
            db.add(data)
            db.commit()
    db.close()

    # json преобразует в excel
    posts = db.query(Post).all()
    dt = []
    for p in posts:
        dict_dt = {
            'id': p.id, 'title': p.title,
            'description': p.description, 'owner_id': p.owner_id,
            'username': p.owner_name, 'email': p.owner_email
        }
        dt.append(dict_dt)
        df = pd.DataFrame(dt)
        df.to_excel('output_get_data.xlsx', sheet_name='record dataset')
    return {"status": 200}


# def create_scheduler_job(db: Session, schedule: schemas.schema_scheduler):
#     db_schedule = mo
