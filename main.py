from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware

from routes import jobs
from logger.log_info import logger

app = FastAPI()


@app.middleware('http')
async def log_request(request, call_next):
    logger.info(f'{request.method} {request.url}')
    response = await call_next(request)
    logger.info(f'Status code: {response.status_code}')
    body = b""
    async for chunk in response.body_iterator:
        body += chunk
    return Response(
        content=body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.include_router(jobs.router)
