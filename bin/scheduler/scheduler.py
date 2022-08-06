#!/usr/bin/env python3

from datetime import datetime
import redis

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
r = redis.Redis(host='redis', port=6379, db=0)

scheduler = BlockingScheduler()
@scheduler.scheduled_job(IntervalTrigger(hours=5))
def queue_job():
    print('queuing!')
    r.rpush('queue','army')    

scheduler.start()
