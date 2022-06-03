import json

from sqlalchemy.orm import Session, joinedload

import requests

from models.table_posts import Post


def get_data(db: Session):
    URL = "http://127.0.0.1:8000/posts/list"
    response = requests.get(url=URL, headers={'Content-Type': 'application/json'})
    res = json.loads(response.text)

    for r in res['list']:
        c = db.query(Post).options(joinedload(Post.owner).load_only(
            "username", "email")).filter(Post.id == r['id']).first()
        if not c:
            data = Post()
            data.id = r['id']
            data.title = r['title']
            data.description = r['description']
            data.owner_id = r['owner_id']
            data.owner = r['owner']
            db.add(data)
            with open('test.xlsx', 'w') as file:
                file.write(str(r))
            db.commit()
    db.close()

    return {"status": 0}
