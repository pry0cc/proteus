#!/usr/bin/env python3

import json
import requests
import argparse
from tabulate import tabulate

class ProteusClient:
    def __init__(self, url):
        self.url = url

    def tabulate(self, json_resp):
        print(tabulate(json_resp, headers="keys", tablefmt="presto"))

    def gen_url(self, target, dtype, scan_id=""):
        url = self.url+"/"+target+"/"+dtype
        if scan_id != "":
            url += "?scan_id="+scan_id
        return url

    def get_data_raw(self, target, dtype, scan_id=""):
        url = self.gen_url(target, dtype, scan_id)

        r = requests.get(url)
        return r.json()

    def get_data(self, target, dtype, scan_id=""):
        self.tabulate(self.get_data_raw(target, dtype, scan_id))

    def dns(self, target, scan_id=""):
        d = self.get_data_raw(target, 'dns', scan_id)
        new_arr = [['Hostname', 'A',  'Timestamp']]

        for line in d:
            host = line['host']
            a = line['a']
            timestamp = line['timestamp']

            new_arr.append([host, a, timestamp])

        print(tabulate(new_arr, headers="firstrow", tablefmt="presto"))


    def http(self, target, scan_id=""):
        d = self.get_data_raw(target, 'http', scan_id)
        new_arr = [['URL', 'Title', 'Webserver']]

        for line in d:
            url = ""
            title = ""
            webserver = ""
            try:
                url = line['url']
                title = line['title']
                webserver = line['webserver']
            except:
                pass

            new_arr.append([url, title, webserver])

        print(tabulate(new_arr, headers="firstrow", tablefmt="presto"))

  
parser = argparse.ArgumentParser()
parser.add_argument('--target', help='Get target of choice')
parser.add_argument('--type', help='Get datatype of choice')
parser.add_argument('--scanid', default="", help='Limit results to a scan_id datatype of choice')

args = parser.parse_args()

client = ProteusClient("http://127.0.0.1:80/api")


if args.type == "http":
    client.http(args.target, args.scanid)
elif args.type == "dns":
    client.dns(args.target, args.scanid)
elif args.type != "":
    client.get_data(args.target, args.type, args.scanid)
