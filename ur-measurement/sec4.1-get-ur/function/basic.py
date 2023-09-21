import datetime
import os
import time
import geoip2
import geoip2.database
import numpy as np

DEBUG = False

g_city = geoip2.database.Reader('./data/GeoLite2-City.mmdb')
g_asn = geoip2.database.Reader('./data/GeoLite2-ASN.mmdb')
def get_country(x):
    try:
        response = g_city.city(x)
        return \
                response.country.name
    except geoip2.errors.AddressNotFoundError:
        pass
    return np.nan


def get_city(x):
    try:
        response = g_city.city(x)
        return \
                response.city.name
    except geoip2.errors.AddressNotFoundError:
        pass
    return np.nan

def get_asn(x):
    try:
        response = g_asn.asn(x)
        return \
               response.autonomous_system_number
    except geoip2.errors.AddressNotFoundError:
        pass
    return np.nan


def get_now_time():
    return str(datetime.date.today()) + '_' + str(time.strftime("%H-%M-%S"))

def cmd(command):
    if DEBUG:
        print('[' + get_now_time() + '] CMD: ' + command)
        
    ans = os.popen(command).read()

    if DEBUG:        
        print('[' + get_now_time() + ']' + ans.strip())
    return ans

def load_line_file(source):
    res = []
    with open(source, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            res.append(line)
    return res

def to_line_file(arr, dest):
    with open(dest, 'w') as f:
        f.write('\n'.join(arr))


if __name__ == '__main__':
    pass