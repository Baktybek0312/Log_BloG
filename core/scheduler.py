from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from core.settings import settings


jobstores = {
    'default': SQLAlchemyJobStore(url=settings.DATABASE_URL)
}
my_scheduler = AsyncIOScheduler(jobstores=jobstores)

my_scheduler.start()
