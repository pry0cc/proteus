#!/usr/bin/env python3

from pymongo import MongoClient
import redis
from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0)
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.asm

@app.route("/subdomains")
def get_subdomains():
    req = request.args.get('target')
    query = {'target_id':req}
    res = db.subs.find(query)
    data = []

    for row in res:
        row.pop('_id')
        data.append(row)

    return jsonify(data)

@app.route("/http")
def get_http():
    req = request.args.get('target')
    query = {'target_id':req}
    res = db.http.find(query)
    data = []

    for row in res:
        row.pop('_id')
        data.append(row)

    return jsonify(data)


@app.route("/dns")
def get_dns():
    req = request.args.get('target')
    query = {'target_id':req}
    res = db.dnsx.find(query)
    data = []

    for row in res:
        row.pop('_id')
        data.append(row)

    return jsonify(data)


@app.route("/start_scan")
def start_scan():
    req = request.args.get('target')

    r.rpush('queue', req)

    data = {"message":"Scan launched!"}
    return jsonify(data)

