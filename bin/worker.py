#!/usr/bin/env python3

import redis
import time
import subprocess
import threading

r = redis.Redis(host='localhost', port=6379, db=0)

def scan(target_id):
    print(target_id)
    subprocess.call(['sh', 'bin/scanner.sh', target_id])

while True:
    res = r.rpop('queue')
    if res != None:
        x = threading.Thread(target=scan, args=(res,))
        x.start()
        time.sleep(1)
