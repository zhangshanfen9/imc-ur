#! /bin/sh
threads=100
# start
if [ "$1"x != "test"x ];then
cat data/tranco-1m.csv | ./zdns nslookup --ipv4-lookup --threads $threads --name-servers=8.8.8.8,1.1.1.1,8.8.4.4,1.0.0.1 --retries 3 --alexa --output-file middle/tranco_ns.json
else
head -n 10 data/tranco-1m.csv | ./zdns nslookup --ipv4-lookup --threads $threads --name-servers=8.8.8.8,1.1.1.1,8.8.4.4,1.0.0.1 --retries 3 --alexa --output-file middle/tranco_ns.json
fi