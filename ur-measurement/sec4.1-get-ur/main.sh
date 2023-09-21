#! /bin/sh

test='test' # run as test mode
# test=''   # run as normal mode

echo "[STEP 1]"
chmod +x *.sh
chmod +x ./zdns


echo "[STEP 2] get nameservers of top hosting providers"

echo "zdns_get_top_domain_ns.sh -> middle/tranco_ns.json"
./zdns_get_top_domain_ns.sh $test
echo "get_top_hosting_ns.py -> result/top_hosting_ns-1.csv"
python3 -u get_top_hosting_ns.py

zip -j middle/tranco_ns.json.zip middle/tranco_ns.json
rm -r middle/tranco_ns.json


echo "[STEP 3] generate the list of domains to be probed"

if [ "$test"x != "test"x ];then
top_limit=2000
ns_host_limit=50
else
top_limit=10
ns_host_limit=1
fi

echo "generate_zdns_query_list_for_probe_hosting_ns.py -> step5"
python3 -u generate_zdns_query_list_for_probe_hosting_ns.py ${top_limit} ${ns_host_limit}

echo "[STEP 4] collecting correct records"

echo "collecting active open resolvers"
sampled_resolver_num=3000
python3 -u function/get_active_resolver.py ${sampled_resolver_num} $test


echo "collecting responses from open resolvers with annotating information"
if [ "$test"x != "test"x ];then
sampled_domain_num=2000
else
sampled_domain_num=10
fi

python3 -u function/get_standard_record.py './data/tranco-1m.csv' ${sampled_domain_num} 1 A
./probe_from_list_and_zip.sh get_standard_record-resolve_to_address.txt TXT 300

# step5
echo "[STEP 5] collecting URs"
./probe_from_list_and_zip.sh oversea_top_list.txt alookup 300
./probe_from_list_and_zip.sh oversea_top_list.txt TXT 300
