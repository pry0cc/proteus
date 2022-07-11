#!/usr/bin/env python3

import sys
import json
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.asm

filename = sys.argv[1]
scan_id = sys.argv[2]
#collection = db[sys.argv[3]]
collection = db[filename.split('.')[0].split("/")[-1]]
target_id = sys.argv[3]

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
