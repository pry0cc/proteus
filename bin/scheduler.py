#!/usr/bin/env python3

from datetime import datetime
import redis

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
r = redis.Redis(host='localhost', port=6379, db=0)

r.rpush('queue','bounty')    

scheduler = BlockingScheduler()
@scheduler.scheduled_job(IntervalTrigger(hours=5))
def queue_job():
    print('queuing!')
    r.rpush('queue','bounty')    

scheduler.start()
