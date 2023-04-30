from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .import token_handeling 

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(token_handeling.update_token, 'interval', hours=24)
    scheduler.start()