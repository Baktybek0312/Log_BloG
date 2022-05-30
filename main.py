import uuid
import random

from fastapi import FastAPI
from fastapi.responses import JSONResponse

import requests

from core.log_config import logger, divide

app = FastAPI()


@app.middleware("http")
async def request_middleware(request, call_next):
    request_id = str(uuid.uuid4())
    with logger.contextualize(request_id=request_id):
        logger.info("Request started")

        try:
            return await call_next(request)

        except Exception as ex:
            logger.error(f"Request failed: {ex}")
            return JSONResponse(content={"success": False}, status_code=500)

        finally:
            logger.info("Request ended")


@app.get("/")
async def read_root():
    a = 100
    b = random.randint(0, 1)
    return {"success": True, "result": divide(a, b)}


URL = 'http://127.0.0.1:8000/posts/list'


@app.get("/get_data")
def get_data():
    data = requests.get(url=URL)

    with open('get_data_blog_posts.xls', 'wb') as file:
        file.write(data.content)
    return data.json()

# @app.post("/upload")
# async def upload(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         with open(file.filename, 'wb') as f:
#             f.write(contents)
#     except Exception:
#         return {"message": "There was an error uploading the file"}
#     finally:
#         await file.close()
#     return {"message": f"Successfuly uploaded {file.filename}"}
