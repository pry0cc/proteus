#!/usr/bin/env python3

import redis
import time
import subprocess
import threading

r = redis.Redis(host='redis', port=6379, db=0)
subprocess.call(['/root/.axiom/interact/axiom-account', 'default'])

def scan(data):
    print(str(data.decode("utf-8")).split(':'))
    if str(data.decode("utf-8")).split(':')[2] == "spinup":
        total = str(data.decode("utf-8")).split(':')[1]
        name = str(data.decode("utf-8")).split(':')[0]
        subprocess.call(['/root/.axiom/interact/axiom-fleet', name, "-i", total])
    else:
        subprocess.call(['sh', '/app/bin/worker/scanner.sh', data])

while True:
    res = r.rpop('queue')
    if res != None:
        x = threading.Thread(target=scan, args=(res,))
        x.start()
        time.sleep(1)
