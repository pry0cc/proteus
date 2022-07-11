#!/bin/bash

sudo docker run -p 127.0.0.1:27017:27017 --name mongo -d mongo 
sudo docker run -p 127.0.0.1:6379:6379 --name redis -d redis
