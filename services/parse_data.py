import json

from sqlalchemy.orm import Session, joinedload

import requests
import pandas as pd

from models.table_posts import Post


def get_data(db: Session):
    """
    данная фукция парсит  URL = "http://127.0.0.1:8000/posts/list" и сохроняет в БД и excel файл
    """
    URL = "http://127.0.0.1:8000/posts/list"
    response = requests.get(url=URL, headers={'Content-Type': 'application/json'})
    res = json.loads(response.text)
    for r in res['list']:
        c = db.query(Post).filter(Post.id == r['id']).first()
        if not c:
            data = Post()
            data.id = r['id']
            data.title = r['title']
            data.description = r['description']
            data.owner_id = r['owner_id']
            db.add(data)
            db.commit()
    db.close()

    # excel_data = []
    # for record in res['list']:

    # json преобразует в excel
    df = pd.DataFrame.from_dict(res['list'])
    del df['owner']
    df.to_excel('output_get_data.xlsx', sheet_name='record dataset')

    return {"status": 0}
