#!/bin/bash

PATH="$PATH:/root/.axiom/interact:/root/go/bin"

echo "Scanning $1"

target_id="$(echo $1 | cut -d: -f 1)"
instances="$(echo $1 | cut -d: -f 2)"
module="$(echo $1 | cut -d: -f 3)"
ppath="/app"
scan_id="$target_id-$(date +%s)"
scan_path="$ppath/scans/$scan_id"
raw_path="$ppath/rawdata/$target_id/"
threads=13
notify="slack"

mkdir -p "$scan_path"
mkdir -p "$raw_path"

cd "$scan_path"
cp "$ppath/scope/$target_id" "$scan_path/scope.txt"

echo "$ppath"

if [ "$instances" -gt "0" ]; then
    axiom-scan scope.txt -m "$module" -o asm --fleet "$target_id" --spinup "$instances" --rm-when-done
else
    if [ "$(axiom-ls "$target_id*" | wc -l | awk '{ print $1 }')" -lt "2" ]; then
    	axiom-scan scope.txt -m "$module" -o asm --fleet "$target_id" --spinup 5 --rm-when-done
    fi 
    axiom-scan scope.txt -m "$module" -o asm --fleet "$target_id"
fi

#cat scope.txt | subfinder -json -o subs.json | jq --unbuffered -r '.host' | dnsx -json -o dnsx.json | jq --unbuffered -r '.host' | httpx -json -o http.json | jq --unbuffered -r '.url' | nuclei -o nuclei.json -json -severity low,medium,high,critical -t ~/nuclei-templates --stats | jq -c --unbuffered 'del(.timestamp) | del(."curl-command")' | anew "$raw_path/nuclei.json" | notify -pc "$ppath/config/notify.yaml" -mf "New vuln found! {{data}}"

#cat asm/dnsx.json | jq -r '.host' | tlsx -json -o asm/tls.json

find asm/ -type f -name "*.json*" | cut -d '.' -f 1-2 | cut -d '/' -f 2 |  sort -u  | while read src; do cat asm/$src* | sort -u > $src; done

rm -r asm

find "$scan_path" -type f -name "*.json" -exec "$ppath/bin/parser/import.py" {} "$scan_id" "$target_id" \;

cat subs.json | jq -r '.host' | anew "$raw_path/hosts.txt" > "$raw_path/hosts.txt.new"
notify -bulk -i "$raw_path/hosts.txt.new"  -pc "$ppath/config/notify.yaml" -mf "New Hostnames Found! {{data}}"

cat http.json | jq -r '.url' | anew "$raw_path/urls.txt" > "$raw_path/urls.txt.new"
notify -bulk -i "$raw_path/urls.txt.new"  -pc "$ppath/config/notify.yaml" -mf "New URLs found! {{data}}"

cat dnsx.json | jq -r '.host' | anew "$raw_path/resolved.txt"
cat dnsx.json | jq -r '.a?[]?' | anew "$raw_path/ips.txt"
