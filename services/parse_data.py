import json
import time

from sqlalchemy.orm import Session

import requests

from models.table_posts import Post


def get_data(db: Session):
    time.sleep(2)
    URL = "http://127.0.0.1:8000/posts/list"
    response = requests.get(url=URL, headers={'Content-Type': 'application/json'})
    res = json.loads(response.text)

    for r in res['list']:
        c = db.query(Post).filter(Post.id == r['id']).first()
        if not c:
            data = Post()
            data.id = r['id']
            # if not r['title']:
            #     raise Exception("ошибка")
            data.title = r['title']
            data.description = r['description']
            data.owner_id = r['owner_id']
            db.add(data)
            db.commit()

    db.close()
    return {"status": 0}



