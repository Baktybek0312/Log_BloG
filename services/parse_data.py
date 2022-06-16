import json

from sqlalchemy.orm import Session

import requests

from models.table_posts import Post
from db.database import SessionLocal

db: Session = SessionLocal()


def get_data():
    """
    данная фукция парсит  URL = "http://127.0.0.1:8000/posts/list" и сохроняет в БД
    """
    URL = "http://127.0.0.1:8000/posts/list"
    response = requests.get(url=URL, headers={'Content-Type': 'application/json'})
    res = json.loads(response.text)

    for r in res['list']:
        post = db.query(Post).filter(Post.id == r['id']).first()
        if not post:
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
    return {"status": 200}
