# Proteus
Proteus - The axiom database and API https://github.com/pry0cc/axiom. <br>
Originally, written for [Hacking Together an ASM Platform Using ProjectDiscovery Tools](https://twitter.com/pdiscoveryio/status/1551558898879893506). 

# Setup

First, clone the repository
```
git clone https://github.com/pry0cc/proteus ~/.proteus
cd ~/.proteus
```

Next, modify config/notify.yaml to include your slack webhook.

Navigate to the bin directory and inspect the docker-compose.yml to make sure everything looks like your setup. You'll want to modify the volumes so that you can map to your local axiom setup.

```
services:
  redis:
    image: redis
  mongo:
    image: mongo
  worker:
    image: proteus/worker
    build:
      context: bin/worker/
    volumes:
      - /home/op/.axiom/accounts/personal.json:/root/.axiom/accounts/default.json # map your account here 
      - /home/op/.axiom/modules:/root/.axiom/modules # map modules
      - /home/op/.ssh:/root/.ssh # map SSH
      - /home/op/.proteus:/app # map proteus folder to the app (for persistence of data like rawdata & scans), not 100% necessary but nice to have.
```


```
cd bin/
sudo docker compose build
sudo docker compose up
```

Thats it!

# Usage
Store your target(s) in the local scope folder ( [~/.proteus/scope/](https://github.com/pry0cc/proteus/tree/main/scope) ) <br>
All fleets are unique to each target, so there is no crossover of data. You can either spin up instances and then launch scans, in which case, the instances will remain after, or you can just launch scans. If you launch a scan without any instances prensent, it will spin up 5 instances by default and then autoremove them when its done.

```
curl -s http://127.0.0.1:80/api/<target>/launch_scan
curl -s http://127.0.0.1:80/api/<target>/launch_scan?spinup=8
curl -s http://127.0.0.1:80/api/<target>/launch_scan?spinup=8&module=asm

curl -s http://127.0.0.1:80/api/<target>/spinup?instances=15 # spin up instances for a target

curl -s http://127.0.0.1:80/api/<target>/scans

curl -s http://127.0.0.1:80/api/<target>/<datatype>
curl -s http://127.0.0.1:80/api/<target>/dnsx
curl -s http://127.0.0.1:80/api/<target>/http
curl -s http://127.0.0.1:80/api/<target>/subs
curl -s http://127.0.0.1:80/api/<target>/nuclei

curl -s http://127.0.0.1:80/api/<target>/<datatype>?scan_id=<scan_id>
```

# Client Usage
The client will tabulate data, todo: added JSON or text output.

```
pip3 install -r bin/client/requirements.txt

bin/client/client.py --target <target> --type http
bin/client/client.py --target <target> --type dns
bin/client/client.py --target <target> --type host
bin/client/client.py --target <target> --type scans

bin/client/client.py --target <target> --type scans --scanid <scan_id>
```
