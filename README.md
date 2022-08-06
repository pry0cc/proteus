# Proteus
Proteus is an API and Database for Axiom

# Setup

First, clone the repository
```
git clone https://github.com/pry0cc/proteus
cd proteus
```

Next, modify config/notify.yaml to include your slack webhook.

Navigate to the bin directory and inspect the docker-compose.yml to make sure everything looks like your setup. You'll want to modify the volumes so that you can map to your local axiom setup.

```
cd bin/
sudo docker compose build
sudo docker compose up
```

Thats it!

# Usage
All fleets are unique to each target, so there is no crossover of data. You can either spin up instances and then launch scans, in which case, the instances will remain after, or you can just launch scans. If you launch a scan without any instances prensent, it will spin up 5 instances by default and then autoremove them when its done.

Somebody really should throw this into a python or go cli client huh?
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
```
pip3 install -r bin/client/requirements.txt

bin/client/client.py --target <target> --type http
bin/client/client.py --target <target> --type dns
bin/client/client.py --target <target> --type host
bin/client/client.py --target <target> --type scans

bin/client/client.py --target <target> --type scans --scanid <scan_id>
```
