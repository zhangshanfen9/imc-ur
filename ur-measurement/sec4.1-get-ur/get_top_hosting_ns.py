# %%
import pandas as pd
import numpy as np
import json
import traceback
import os
import re

# %%
TOP_LIMIT = -1
NS_RESULT_LIST = ['./middle/tranco_ns.json']

# %%
ip_hostnum_map = {}
def add_num_dict(x, num=1, d=ip_hostnum_map):
    if x not in d:
        d[x] = num
    else:
        d[x] += num

ip_domain_map = {}
def add_arr_dict(x, arr_item, d=ip_domain_map):
    if x not in d:
        # d[x] = arr_item
        d[x] = [arr_item, ]
    else:
        # d[x] += arr_item
        d[x].append(arr_item)

# %%
counted_domain = set()

for ns_res_path in NS_RESULT_LIST:
    with open(ns_res_path, 'r') as f:
        for line in f:
            try:
            # print(line)
                obj = json.loads(line)

                status = obj['status']
                if status != 'NOERROR':
                    continue
                
                domain = obj['name']
                if domain not in counted_domain:
                    counted_domain.add(domain)
                else:
                    continue
                
                for sitem in obj['data']['servers']:
                    try:
                        ns_addresses = sitem['ipv4_addresses']
                        ns_name = sitem['name']
                        for address in ns_addresses:
                            add_arr_dict(address, ns_name)
                            add_num_dict(address)
                    except KeyError:
                        pass
                        
                    # map(add_arr_dict, ns_addresses, [ns_name, ]*len(ns_addresses))
                    # map(add_num_dict, ns_addresses)

            except KeyError:
                pass

# %%
NS_HOST_LIMIT = -1

res = []
for ip in ip_domain_map:
    hn = ip_hostnum_map[ip]
    if NS_HOST_LIMIT > 0 and NS_HOST_LIMIT > hn:
        continue
    res.append([ip, hn, str(set(ip_domain_map[ip]))])

def takeSecond(elem):
    return elem[1]
res.sort(key=takeSecond, reverse=True)

import csv
headers = ['ns_ip_address', 'host_num', 'ns_domain']
with open('result/top_hosting_ns%d.csv'% NS_HOST_LIMIT,'w')as f:
    f_csv = csv.writer(f)
    f_csv.writerows(res)


