import sys
from basic import *
import pandas as pd
import csv
import re
import json
import traceback
from concurrent.futures import ThreadPoolExecutor
import ssl
import hashlib
import eventlet
import queue

SSL_TIMEOUT = 5
SSL_THREAD_NUM = 100

eventlet.monkey_patch()

source = sys.argv[1]
limit = int(sys.argv[2])
is_alexa_style = int(sys.argv[3])
check_record_type = sys.argv[4]

# test = False
# if len(sys.argv) > 5 and sys.argv[5] == 'test':
#     test = True


def zipfile(path):
    cmd('zip -j ' + path + '.zip ' + path)
    cmd('rm -r ' + path)


def resolve_to_address():
    resolvers = load_line_file('middle/sampled_stable_ipv4_resolver.txt')
    domains = []
    if is_alexa_style == 1:
        with open(source, 'r') as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                if limit < 0 or len(domains) < limit:
                    domains.append(row[1])
                else:
                    break
    else:
        domains = load_line_file(source)
        if limit >= 0:
            domains = domains[:limit]

    zdns_probe_list_path = 'zdns_probe_list/get_standard_record-resolve_to_address.txt'

    cmd('rm -r ' + zdns_probe_list_path)
    for domain in domains:
        res = []
        for ns in resolvers:
            res.append([domain, ns])
        with open(zdns_probe_list_path, 'a') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(res)
    
    zdns_probe_result = 'middle/get_standard_record-resolve_to_address.json'
    cmd(r'cat %s | ./zdns %s --threads 300 --ipv4-lookup --result-verbosity trace | grep -vE "\"status\":\"(REFUSED|SERVFAIL|TIMEOUT)\"" > %s'% (zdns_probe_list_path, check_record_type + 'LOOKUP', zdns_probe_result))
    # zipfile(zdns_probe_list_path)

    probe_res_arr = []
    with open(zdns_probe_result, 'r') as f:
        for line in f:
            try:
                obj = json.loads(line)
                if obj['status'] != 'NOERROR': continue
                resolver = re.search(r'"name_server":"(.*?):53"', line).group(1)
                timestamp = obj['timestamp']
                domain = obj['name']
                ip_arr = []
                if 'ipv4_addresses' in obj['data']:
                    ip_arr += obj['data']['ipv4_addresses']
                if 'servers' in obj['data']:
                    for oitem in obj['data']['servers']:
                        if 'ipv4_addresses' in oitem:
                            ip_arr += oitem['ipv4_addresses']
                if 'exchanges' in obj['data']:
                    for oitem in obj['data']['exchanges']:
                        if 'ipv4_addresses' in oitem:
                            ip_arr += oitem['ipv4_addresses']
                
                for item in ip_arr:
                    probe_res_arr.append([domain, resolver, check_record_type, item, timestamp])
                    
            except:
                print(line)
                traceback.print_exc()
    
    zipfile(zdns_probe_result)

    ans = pd.DataFrame(probe_res_arr, columns=['domain', 'resolver', 'rtype', 'final_ip_address', 'timestamp'])
    name = 'middle/resolver_return_record' + '.csv'
    ans.to_csv(name, index=None)
    zipfile(name)
    return ans

"""
3. get annoation
    1. ASN，maxmind
    2. City，maxmind
    3. PTR, probe by ZDNS
    4. HTTPS cert
"""
def annotate_address(all_records):
    all_addresses = all_records['final_ip_address'].unique().tolist()
    # all_addresses = ['8.8.8.8', '13.107.160.205', '220.181.38.148']

    ans = pd.DataFrame(all_addresses, columns=['final_ip_address',])

    # asn and city
    ans['asn'] = ans['final_ip_address'].apply(get_asn)
    ans['city'] = ans['final_ip_address'].apply(get_city)

    # PTR
    print('[] get_standard_record: PTR')
    zdns_probe_list = './zdns_probe_list/ptr_probe.txt'
    to_line_file(all_addresses, zdns_probe_list)
    ptr_middle_result_list = './middle/ptr_probe.txt'
    cmd(r'cat %s  | ./zdns PTR --threads 150  --name-servers=8.8.8.8,1.1.1.1,8.8.4.4,1.0.0.1 --ipv4-lookup | grep -vE "\"status\":\"(NXDOMAIN)\"" > %s' % (zdns_probe_list, ptr_middle_result_list))

    tarr = []

    with open(ptr_middle_result_list, 'r') as f:
        for line in f:
            if "NOERROR" not in line:
                continue
            obj = json.loads(line)
            try:
                if obj['data']['answers'][0]['type'] == 'PTR':
                    tarr.append([obj['name'], obj['data']['answers'][0]['answer']])
            except KeyError:
                print(line)
    
    ptr_df = pd.DataFrame(tarr, columns=['final_ip_address', 'ptr'])

    zipfile(zdns_probe_list)
    zipfile(ptr_middle_result_list)

    # cert
    print('[] get_standard_record: cert')
    cert_que = queue.Queue()

    executor = ThreadPoolExecutor(max_workers=SSL_THREAD_NUM)
    thread_obj = []
    for item in all_addresses:
        thread_obj.append(executor.submit(get_certification_hash, item, cert_que))
    for tobj in thread_obj:
        tobj.result()

    tarr = []
    while not cert_que.empty():
        tarr.append(cert_que.get())
    cert_df = pd.DataFrame(tarr, columns=['final_ip_address', 'cert_hash'])
    cert_df.to_csv('./middle/cert_df.csv', index=None)
    zipfile('./middle/cert_df.csv')

    ans = pd.merge(ans, ptr_df, how='outer', on=['final_ip_address'])
    ans = pd.merge(ans, cert_df, how='outer', on=['final_ip_address'])

    name = 'result/annotated_record' + '.csv'
    ans.to_csv(name, index=None)
    zipfile(name)
    

def get_certification_hash(address, que):
    # print(get_certification_hash('47.103.24.173'))
    # print(get_certification_hash('8.134.50.24'))
    # print(get_certification_hash('31.13.96.194')) # timeout
    # print(get_certification_hash('127.0.0.1')) # refuse

    try:
        with eventlet.Timeout(SSL_TIMEOUT, False):
            hash = hashlib.md5(ssl.get_server_certificate((address, 443)).encode("utf-8")).hexdigest()
        que.put([address, hash])
    except:
        pass


if __name__ == '__main__':
    annotate_address(resolve_to_address())
    # que = queue.Queue()
    # get_certification_hash('220.181.38.251', que)
    # print(que.get())