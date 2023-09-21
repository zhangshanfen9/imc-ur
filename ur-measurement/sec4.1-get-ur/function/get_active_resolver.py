from basic import *
import sys
import random


def check_resolver_list(source, sample_num, test):
    if not test:
        cmd('cat %s | ./zdns A --threads 150 --name-server-mode --override-name="www.iana.org" | grep "ianawww.vip.icann.org" | sed -r \'s/.+resolver":"([^:]+).*/\\1/\' > middle/alive_stable_ipv4_resolver.txt'% (source, ))
    else:
        cmd('head -n 50 %s | ./zdns A --threads 150 --name-server-mode --override-name="www.iana.org" | grep "ianawww.vip.icann.org" | sed -r \'s/.+resolver":"([^:]+).*/\\1/\' > middle/alive_stable_ipv4_resolver.txt'% (source, ))
    all_resolver = load_line_file('middle/alive_stable_ipv4_resolver.txt')
    random.shuffle(all_resolver)
    sampled_resolver = all_resolver[:sample_num]
    to_line_file(sampled_resolver, 'middle/sampled_stable_ipv4_resolver.txt')


if __name__ == '__main__':
    sample_num = int(sys.argv[1])
    test = False
    if len(sys.argv) > 2 and sys.argv[2] == 'test':
        test = True
    check_resolver_list(source='data/stable_ipv4.txt', sample_num=sample_num, test=test)