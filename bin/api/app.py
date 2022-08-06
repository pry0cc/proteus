#!/usr/bin/env python3

from pymongo import MongoClient
import redis
from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

r = redis.Redis(host='redis', port=6379, db=0)
client = MongoClient("mongodb://mongo:27017")
db = client.asm

@app.route("/api/<target>/<datatype>")
def get_subdomains(target, datatype):
    scan_id = request.args.get("scan_id")
    query = {'target_id':target}

    if scan_id != None:
        query['scan_id'] = scan_id

    collection = db[datatype]
    res = collection.find(query)
    data = []

    for row in res:
        row.pop('_id')
        data.append(row)

    return jsonify(data)


@app.route("/api/<target>/launch_scan")
def start_scan(target):
    instances = request.args.get("spinup")
    module = request.args.get("module")
    req = target

    if instances == None:
        instances = "0"

    if module == None:
        module="asm"

    r.rpush('queue', req+":"+str(instances)+":"+str(module))

    data = {"message":"Scan launched!"}
    return jsonify(data)


@app.route("/api/<target>/spinup")
def spinup(target):
    instances = request.args.get("instances")
    req = target

    if instances == None:
        instances = "3"
    
    module = "spinup"

    r.rpush('queue', req+":"+str(instances)+":"+module)

    data = {"message":"Fleet queued for initializing!"}
    return jsonify(data)

