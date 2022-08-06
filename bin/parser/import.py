#!/usr/bin/env python3

import sys
import json
from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017")
db = client.asm

filename = sys.argv[1]
scan_id = sys.argv[2]
collection_name = filename.split('.')[0].split("/")[-1]
collection = db[collection_name]
target_id = sys.argv[3]

scan_meta = {'scan_id':scan_id, 'target_id':target_id}

def jsonf_to_lines(filename):
    parsed_lines = []
    with open(filename, 'r') as reader:
        for line in reader.read().split('\n'):
            try:
                parsed = json.loads(line)
                parsed["scan_id"] = scan_id
                parsed["target_id"] = target_id
                parsed_lines.append(parsed)
            except Exception as err:
                print("Whoops %s", err)
    return parsed_lines

collection.insert_many(jsonf_to_lines(filename))
res = db.scans.find({'scan_id':scan_id})

i = 0
for row in res:
    i += 1

if i < 1:
    db.scans.insert_one(scan_meta)



