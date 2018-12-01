
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from django.apps import apps

class CustomRedisJobStore(RedisJobStore):
  def _reconstitute_jobs(self, job_states):
    if apps.ready:
      return super()._reconstitute_jobs(job_states)

    return []

scheduler = BackgroundScheduler(
  jobstores={
    'default': CustomRedisJobStore(
      host='localhost',
      port=6379,
    ),
  },
  executors={
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
  },
  job_defaults={
    'max_instances': 1,
  },
  timezone=utc,
)

scheduler.start()
scheduler.remove_all_jobs()
