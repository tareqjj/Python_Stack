from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from rateUpdater import rateApi


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(rateApi.update_forecast, 'interval', minutes=45)
    scheduler.start()
