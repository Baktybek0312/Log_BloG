from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes import jobs
# from routes import example_jobs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(jobs.router)
# app.include_router(example_jobs.router)
