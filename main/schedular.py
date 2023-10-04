
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .process  import run_process
from .models import *

from django.shortcuts import render,redirect 
from django.contrib.auth.models import User

def start():
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_process,'interval', seconds=5)
    scheduler.start()
    scheduler.shutdown()
    # try:
    #   while True:
    #         pass
    # except (KeyboardInterrupt, SystemExit):
    # # Shut down the scheduler gracefully when exiting the program
    #   scheduler.shutdown()
