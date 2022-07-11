#!/usr/bin/env python3

from datetime import datetime
import redis

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
r = redis.Redis(host='localhost', port=6379, db=0)

r.rpush('queue','airbnb')    
scheduler = BlockingScheduler()
@scheduler.scheduled_job(IntervalTrigger(minutes=1))
def queue_job():
    print('queuing!')
    r.rpush('queue','att')    

scheduler.start()
