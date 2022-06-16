import tzlocal
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from core.settings import settings


my_scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))
jobstore = SQLAlchemyJobStore(url=settings.DATABASE_URL)
my_scheduler.add_jobstore(jobstore=jobstore)

my_scheduler.start()
