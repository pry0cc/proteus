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

# kind of weird logic, but since we're using the asm module, we're basically looking for all the json files inside of the asm directory (and then merging them), finally deleting the asm dir because we merged the data

# this might become a huge bottleneck with huge data? idk? hope not.
find asm/ -type f -name "*.json*" | cut -d '.' -f 1-2 | cut -d '/' -f 2 |  sort -u  | while read src; do cat asm/$src* | sort -u > $src; done

rm -r asm

find "$scan_path" -type f -name "*.json" -exec "$ppath/bin/parser/import.py" {} "$scan_id" "$target_id" \;

cat host.json | jq -r '.host' | anew "$raw_path/host.txt" > "$raw_path/host.txt.new"
notify -bulk -i "$raw_path/host.txt.new"  -pc "$ppath/config/notify.yaml" -mf "New Hostnames Found! {{data}}"

cat http.json | jq -r '.url' | anew "$raw_path/url.txt" > "$raw_path/url.txt.new"
notify -bulk -i "$raw_path/url.txt.new"  -pc "$ppath/config/notify.yaml" -mf "New URLs found! {{data}}"

cat dns.json | jq -r '.host' | anew "$raw_path/resolved.txt"
cat dns.json | jq -r '.a?[]?' | anew "$raw_path/ips.txt"
