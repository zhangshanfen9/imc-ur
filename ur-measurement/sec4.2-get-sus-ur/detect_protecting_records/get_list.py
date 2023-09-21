import pandas as pd
import sys
top_hosting_ns = pd.read_csv('./output/result/top_hosting_ns-1.csv', names=['nameserver', 'hosting_sum', 'nameserver_domain'])


if len(sys.argv) >= 2 and sys.argv[1] == 'test':
    arr = top_hosting_ns['nameserver'].to_list()
else:
    arr = top_hosting_ns[top_hosting_ns['hosting_sum'] >= 50]['nameserver'].to_list()

with open('./detect_protecting_records/all_ns_set.txt', 'w') as f:
    f.write('\n'.join(arr))