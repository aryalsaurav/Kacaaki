import os
from django.conf import settings

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kacaaki.settings")

app = Celery("kacaaki", broker="redis://localhost:6379/0")

app.config_from_object(settings, namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    pass
    # print(f'Request: {self.request!r}')

# app.conf.beat_schedule = {
#     "generate-invoices": {
#         "task": "system.tasks.generate_invoices",
#         "schedule": crontab(minute=20, hour=17),
#     },
# }