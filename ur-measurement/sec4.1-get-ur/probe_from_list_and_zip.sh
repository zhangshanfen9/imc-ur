#! /bin/sh
# $1 list, $2 type, $3 thread
# threads=300, 50

cat zdns_probe_list/$1 |./zdns $2 --threads $3 --ipv4-lookup --retries 3 --result-verbosity trace | grep -vE "\"status\":\"(REFUSED|SERVFAIL|TIMEOUT)\"" > middle/$1_$2-thd-$3.json
zip -j result/$1_$2-thd-$3.json.zip middle/$1_$2-thd-$3.json
rm -rf middle/$1_$2-thd-$3.json
