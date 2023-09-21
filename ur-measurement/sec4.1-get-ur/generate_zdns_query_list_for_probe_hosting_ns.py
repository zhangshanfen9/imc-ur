import csv
import sys
from function.basic import *


DOMAIN_LIST_PATH = './data/tranco-1m.csv'
NS_LIST_PATH = './result/top_hosting_ns-1.csv'

DOMAIN_LIMIT = int(sys.argv[1])
NS_HOST_LIMIT = int(sys.argv[2])

domains = []
with open(DOMAIN_LIST_PATH, 'r')as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        if len(domains) < DOMAIN_LIMIT:
            domains.append(row[1])
        else:
            break

nses_oversea = []
with open(NS_LIST_PATH, 'r')as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        # print(row[1])
        # print(NS_HOST_LIMIT)
        if int(row[1]) >= NS_HOST_LIMIT:
            ip = row[0]
            nses_oversea.append(ip)
        else:
            continue

cmd('rm -r zdns_probe_list/oversea_top_list.txt')
for domain in domains:
    res = []
    for ns in nses_oversea:
        res.append([domain, ns])
    with open('zdns_probe_list/oversea_top_list.txt', 'a')as f:
        f_csv = csv.writer(f)
        f_csv.writerows(res)
